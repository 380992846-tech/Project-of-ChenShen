#include "raft.h"
#include <boost/asio/read.hpp>
#include <boost/asio/write.hpp>
#include <boost/asio/connect.hpp>
#include <boost/asio/ip/tcp.hpp>
#include <thread>
#include <queue>
#include <unordered_map>
#include <functional>
#include <sstream>
#include <iostream>
#include <cstring>

using asio::ip::tcp;

// ==================== RPC消息类型枚举 ====================
enum class RpcType {
    REQUEST_VOTE_REQ,
    REQUEST_VOTE_RESP,
    APPEND_ENTRIES_REQ,
    APPEND_ENTRIES_RESP,
    HEARTBEAT,  // 心跳是空AppendEntries
};

// ==================== 网络消息包装 ====================
struct RpcMessage {
    RpcType type;
    int srcId;
    int dstId;
    json payload;
    
    std::string serialize() const {
        json j = {
            {"type", static_cast<int>(type)},
            {"srcId", srcId},
            {"dstId", dstId},
            {"payload", payload}
        };
        std::string body = j.dump();
        // 4字节长度头 + body
        uint32_t len = body.size();
        std::string result;
        result.resize(4 + body.size());
        memcpy(result.data(), &len, 4);
        memcpy(result.data() + 4, body.data(), body.size());
        return result;
    }
    
    static RpcMessage deserialize(const std::string& data) {
        if (data.size() < 4) throw std::runtime_error("Invalid message");
        json j = json::parse(data.substr(4));
        RpcMessage msg;
        msg.type = static_cast<RpcType>(j["type"].get<int>());
        msg.srcId = j["srcId"];
        msg.dstId = j["dstId"];
        msg.payload = j["payload"];
        return msg;
    }
    
    static bool try_deserialize(const std::string& data, RpcMessage& msg) {
        if (data.size() < 4) return false;
        uint32_t len;
        memcpy(&len, data.data(), 4);
        if (data.size() < 4 + len) return false;
        try {
            msg = deserialize(data.substr(0, 4 + len));
            return true;
        } catch (...) {
            return false;
        }
    }
};

// ==================== RPC客户端连接 ====================
class RpcClient : public std::enable_shared_from_this<RpcClient> {
public:
    using Callback = std::function<void(const json&)>;
    
    RpcClient(asio::io_context& io, const std::string& host, int port)
        : socket_(io), resolver_(io), host_(host), port_(port), connected_(false) {}
    
    ~RpcClient() { close(); }
    
    // 异步连接
    void connect(std::function<void(bool)> callback = nullptr) {
        auto self = shared_from_this();
        resolver_.async_resolve(host_, std::to_string(port_),
            [this, self, callback](boost::system::error_code ec, tcp::resolver::results_type endpoints) {
                if (ec) {
                    if (callback) callback(false);
                    return;
                }
                
                asio::async_connect(socket_, endpoints,
                    [this, self, callback](boost::system::error_code ec, tcp::endpoint) {
                        if (!ec) {
                            connected_ = true;
                            do_read_header();
                            if (callback) callback(true);
                        } else {
                            if (callback) callback(false);
                        }
                    });
            });
    }
    
    // 发送请求（异步，带回调）
    void send_request(RpcType type, const json& payload, Callback callback) {
        if (!connected_) {
            callback(json{{"error", "not connected"}});
            return;
        }
        
        uint64_t reqId = next_req_id_++;
        pending_callbacks_[reqId] = callback;
        
        RpcMessage msg;
        msg.type = type;
        msg.srcId = 0;  // 由外层填充
        msg.dstId = 0;
        msg.payload = payload;
        msg.payload["_reqId"] = reqId;  // 嵌入请求ID用于匹配回复
        
        std::string data = msg.serialize();
        auto self = shared_from_this();
        asio::async_write(socket_, asio::buffer(data),
            [this, self, reqId](boost::system::error_code ec, size_t) {
                if (ec) {
                    auto it = pending_callbacks_.find(reqId);
                    if (it != pending_callbacks_.end()) {
                        it->second(json{{"error", ec.message()}});
                        pending_callbacks_.erase(it);
                    }
                    close();
                }
            });
    }
    
    void close() {
        connected_ = false;
        socket_.close();
        // 回调所有pending请求失败
        for (auto& [id, cb] : pending_callbacks_) {
            cb(json{{"error", "connection closed"}});
        }
        pending_callbacks_.clear();
    }
    
    bool is_connected() const { return connected_; }
    
private:
    void do_read_header() {
        auto self = shared_from_this();
        read_buffer_.resize(4);
        asio::async_read(socket_, asio::buffer(read_buffer_.data(), 4),
            [this, self](boost::system::error_code ec, size_t) {
                if (!ec) {
                    uint32_t body_len;
                    memcpy(&body_len, read_buffer_.data(), 4);
                    if (body_len > 1024 * 1024) {  // 1MB限制
                        close();
                        return;
                    }
                    read_buffer_.resize(4 + body_len);
                    do_read_body(body_len);
                } else {
                    close();
                }
            });
    }
    
    void do_read_body(uint32_t body_len) {
        auto self = shared_from_this();
        asio::async_read(socket_, asio::buffer(read_buffer_.data() + 4, body_len),
            [this, self](boost::system::error_code ec, size_t) {
                if (!ec) {
                    try {
                        RpcMessage msg = RpcMessage::deserialize(read_buffer_);
                        handle_response(msg);
                    } catch (...) {
                        // 解析失败
                    }
                    read_buffer_.resize(4);
                    do_read_header();
                } else {
                    close();
                }
            });
    }
    
    void handle_response(const RpcMessage& msg) {
        // 检查是否是回复（携带_reqId）
        if (msg.payload.contains("_reqId")) {
            uint64_t reqId = msg.payload["_reqId"];
            auto it = pending_callbacks_.find(reqId);
            if (it != pending_callbacks_.end()) {
                json response = msg.payload;
                response.erase("_reqId");
                it->second(response);
                pending_callbacks_.erase(it);
            }
        } else {
            // 这是主动推送（如心跳回复），交给上层处理
            if (on_response_) on_response_(msg);
        }
    }
    
    tcp::socket socket_;
    tcp::resolver resolver_;
    std::string host_;
    int port_;
    bool connected_;
    std::string read_buffer_;
    uint64_t next_req_id_ = 1;
    std::unordered_map<uint64_t, Callback> pending_callbacks_;
    
public:
    std::function<void(const RpcMessage&)> on_response_;
};

// ==================== RPC服务端 ====================
class RpcServer {
public:
    using RequestHandler = std::function<RpcMessage(const RpcMessage&)>;
    
    RpcServer(asio::io_context& io, int port)
        : io_(io), acceptor_(io, tcp::endpoint(tcp::v4(), port)), port_(port) {}
    
    void start(RequestHandler handler) {
        handler_ = handler;
        do_accept();
    }
    
    void stop() {
        acceptor_.close();
        for (auto& session : sessions_) {
            session->close();
        }
        sessions_.clear();
    }
    
private:
    class Session : public std::enable_shared_from_this<Session> {
    public:
        Session(tcp::socket socket, RequestHandler handler)
            : socket_(std::move(socket)), handler_(handler) {}
        
        void start() {
            do_read_header();
        }
        
        void close() {
            socket_.close();
        }
        
    private:
        void do_read_header() {
            auto self = shared_from_this();
            read_buffer_.resize(4);
            asio::async_read(socket_, asio::buffer(read_buffer_.data(), 4),
                [this, self](boost::system::error_code ec, size_t) {
                    if (!ec) {
                        uint32_t body_len;
                        memcpy(&body_len, read_buffer_.data(), 4);
                        if (body_len > 1024 * 1024) { close(); return; }
                        read_buffer_.resize(4 + body_len);
                        do_read_body(body_len);
                    } else {
                        close();
                    }
                });
        }
        
        void do_read_body(uint32_t body_len) {
            auto self = shared_from_this();
            asio::async_read(socket_, asio::buffer(read_buffer_.data() + 4, body_len),
                [this, self](boost::system::error_code ec, size_t) {
                    if (!ec) {
                        try {
                            RpcMessage req = RpcMessage::deserialize(read_buffer_);
                            RpcMessage resp = handler_(req);  // 业务处理
                            std::string data = resp.serialize();
                            asio::async_write(socket_, asio::buffer(data),
                                [this, self](boost::system::error_code ec, size_t) {
                                    if (ec) close();
                                });
                        } catch (...) {
                            // 解析失败，返回错误
                            json error_payload = {{"error", "parse error"}};
                            RpcMessage error_msg;
                            error_msg.type = RpcType::REQUEST_VOTE_RESP;  // 随便填
                            error_msg.payload = error_payload;
                            std::string data = error_msg.serialize();
                            asio::async_write(socket_, asio::buffer(data),
                                [this, self](boost::system::error_code, std::size_t) {});
                        }
                        read_buffer_.resize(4);
                        do_read_header();
                    } else {
                        close();
                    }
                });
        }
        
        tcp::socket socket_;
        std::string read_buffer_;
        RequestHandler handler_;
    };
    
    void do_accept() {
        auto self = this;
        acceptor_.async_accept([this, self](boost::system::error_code ec, tcp::socket socket) {
            if (!ec) {
                auto session = std::make_shared<Session>(std::move(socket), handler_);
                sessions_.push_back(session);
                session->start();
            }
            do_accept();
        });
    }
    
    asio::io_context& io_;
    tcp::acceptor acceptor_;
    int port_;
    RequestHandler handler_;
    std::vector<std::shared_ptr<Session>> sessions_;
};

// ==================== Raft节点集成RPC ====================
// 将RPC集成到RaftNode类中
class RaftNodeWithRPC : public RaftNode {
public:
    RaftNodeWithRPC(int nodeId, const std::vector<std::string>& peerAddrs)
        : RaftNode(nodeId, peerAddrs),
          rpc_server_(ioContext_, get_port_from_addr(peerAddrs[nodeId])) {
        
        // 设置服务端请求处理器
        rpc_server_.start([this](const RpcMessage& req) -> RpcMessage {
            return handle_rpc_request(req);
        });
        
        // 初始化客户端连接
        for (size_t i = 0; i < peerAddrs.size(); ++i) {
            if (i == nodeId) continue;
            auto [host, port] = parse_addr(peerAddrs[i]);
            auto client = std::make_shared<RpcClient>(ioContext_, host, port);
            clients_[i] = client;
            
            // 异步连接
            client->connect([this, i](bool success) {
                if (success) {
                    std::cout << "[Node " << nodeId_ << "] 连接到 Peer " << i << std::endl;
                    if (role_ == LEADER) {
                        // 如果已经是Leader，立即同步日志
                        replicateLogs(i);
                    }
                } else {
                    std::cerr << "[Node " << nodeId_ << "] 连接 Peer " << i << " 失败，将重试" << std::endl;
                    // 重连逻辑由心跳触发
                }
            });
        }
    }
    
private:
    // ==================== RPC请求处理 ====================
    RpcMessage handle_rpc_request(const RpcMessage& req) {
        RpcMessage resp;
        resp.srcId = nodeId_;
        resp.dstId = req.srcId;
        
        try {
            switch (req.type) {
                case RpcType::REQUEST_VOTE_REQ: {
                    RequestVoteArgs args = req.payload.get<RequestVoteArgs>();
                    RequestVoteReply reply = handleRequestVote(args, req.srcId);
                    resp.type = RpcType::REQUEST_VOTE_RESP;
                    resp.payload = json(reply);
                    break;
                }
                case RpcType::APPEND_ENTRIES_REQ: {
                    AppendEntriesArgs args = req.payload.get<AppendEntriesArgs>();
                    AppendEntriesReply reply = handleAppendEntries(args, req.srcId);
                    resp.type = RpcType::APPEND_ENTRIES_RESP;
                    resp.payload = json(reply);
                    break;
                }
                default:
                    resp.payload = json{{"error", "unknown rpc type"}};
            }
        } catch (const std::exception& e) {
            resp.payload = json{{"error", e.what()}};
        }
        return resp;
    }
    
    // ==================== 发送RPC到对端 ====================
    void send_rpc(int peerId, RpcType type, const json& payload,
                  std::function<void(const json&)> callback = nullptr) {
        auto it = clients_.find(peerId);
        if (it == clients_.end() || !it->second->is_connected()) {
            if (callback) callback(json{{"error", "peer not connected"}});
            return;
        }
        
        // 在payload中嵌入请求ID用于匹配回复
        json send_payload = payload;
        
        if (callback) {
            it->second->send_request(type, send_payload, callback);
        } else {
            // 无回调的RPC（如心跳）
            it->second->send_request(type, send_payload, [](const json&) {});
        }
    }
    
    // ==================== 重写RPC发送方法 ====================
    void sendRequestVote(int peerId) override {
        RequestVoteArgs args;
        args.term = persistentState_.currentTerm;
        args.candidateId = nodeId_;
        args.lastLogIndex = persistentState_.logs.size();
        args.lastLogTerm = persistentState_.logs.empty() ? 0 : persistentState_.logs.back().term;
        
        std::cout << "[Node " << nodeId_ << "] 发送RequestVote到 " << peerId
                  << ", Term=" << args.term << std::endl;
        
        send_rpc(peerId, RpcType::REQUEST_VOTE_REQ, json(args),
            [this, peerId](const json& resp_json) {
                if (resp_json.contains("error")) {
                    std::cerr << "[Node " << nodeId_ << "] RequestVote到 " << peerId
                              << " 失败: " << resp_json["error"] << std::endl;
                    return;
                }
                
                try {
                    RequestVoteReply reply = resp_json.get<RequestVoteReply>();
                    std::lock_guard<std::mutex> lock(stateMutex_);
                    
                    if (reply.term > persistentState_.currentTerm) {
                        becomeFollower(reply.term);
                        return;
                    }
                    
                    if (role_ == CANDIDATE && reply.voteGranted) {
                        voteCount_++;
                        if (voteCount_ > (peerAddrs_.size() / 2)) {
                            becomeLeader();
                        }
                    }
                } catch (const std::exception& e) {
                    std::cerr << "解析RequestVote回复失败: " << e.what() << std::endl;
                }
            });
    }
    
    void sendAppendEntries(int peerId) override {
        AppendEntriesArgs args;
        args.term = persistentState_.currentTerm;
        args.leaderId = nodeId_;
        args.leaderCommit = commitIndex_;
        
        int prevIndex = nextIndex_[peerId] - 1;
        args.prevLogIndex = prevIndex;
        args.prevLogTerm = (prevIndex <= 0) ? 0 : persistentState_.logs[prevIndex - 1].term;
        
        if (nextIndex_[peerId] <= (int)persistentState_.logs.size()) {
            for (int i = nextIndex_[peerId] - 1; i < (int)persistentState_.logs.size(); ++i) {
                args.entries.push_back(json(persistentState_.logs[i]));
            }
        }

        send_rpc(peerId, RpcType::APPEND_ENTRIES_REQ, json(args),
            [this, peerId, args](const json& resp_json) {
                if (resp_json.contains("error")) {
                    // 网络错误，标记节点不可达，后续重试
                    return;
                }
                
                try {
                    AppendEntriesReply reply = resp_json.get<AppendEntriesReply>();
                    std::lock_guard<std::mutex> lock(stateMutex_);
                    
                    if (reply.term > persistentState_.currentTerm) {
                        becomeFollower(reply.term);
                        return;
                    }
                    
                    if (role_ == LEADER) {
                        if (reply.success) {
                            // 成功复制
                            int newMatchIndex = args.prevLogIndex + args.entries.size();
                            matchIndex_[peerId] = std::max(matchIndex_[peerId], newMatchIndex);
                            nextIndex_[peerId] = matchIndex_[peerId] + 1;
                            advanceCommitIndex();
                        } else {
                            // 快速回退
                            if (reply.conflictTerm == -1) {
                                nextIndex_[peerId] = reply.conflictIndex;
                            } else {
                                int lastIndex = -1;
                                for (int i = persistentState_.logs.size() - 1; i >= 0; --i) {
                                    if (persistentState_.logs[i].term == reply.conflictTerm) {
                                        lastIndex = i + 1;
                                        break;
                                    }
                                }
                                if (lastIndex > 0) {
                                    nextIndex_[peerId] = lastIndex;
                                } else {
                                    nextIndex_[peerId] = reply.conflictIndex;
                                }
                            }
                            // 立即重试
                            if (role_ == LEADER) {
                                replicateLogs(peerId);
                            }
                        }
                    }
                } catch (const std::exception& e) {
                    std::cerr << "解析AppendEntries回复失败: " << e.what() << std::endl;
                }
            });
    }
    
    // ==================== 工具函数 ====================
    static std::pair<std::string, int> parse_addr(const std::string& addr) {
        size_t colon = addr.find(':');
        if (colon == std::string::npos) {
            return {addr, 9000};
        }
        return {addr.substr(0, colon), std::stoi(addr.substr(colon + 1))};
    }
    
    static int get_port_from_addr(const std::string& addr) {
        return parse_addr(addr).second;
    }
    
    // ==================== 成员变量 ====================
    RpcServer rpc_server_;
    std::unordered_map<int, std::shared_ptr<RpcClient>> clients_;
};

// ==================== main函数示例 ====================
int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << " --id=<nodeId> --peers=<addr1,addr2,...>" << std::endl;
        return 1;
    }
    
    int nodeId = -1;
    std::vector<std::string> peerAddrs;
    
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg.find("--id=") == 0) {
            nodeId = std::stoi(arg.substr(5));
        } else if (arg.find("--peers=") == 0) {
            std::string peers = arg.substr(8);
            std::stringstream ss(peers);
            std::string addr;
            while (std::getline(ss, addr, ',')) {
                peerAddrs.push_back(addr);
            }
        }
    }
    
    if (nodeId < 0 || peerAddrs.empty()) {
        std::cerr << "Invalid arguments" << std::endl;
        return 1;
    }
    
    std::cout << "启动Raft节点 " << nodeId << ", 集群大小=" << peerAddrs.size() << std::endl;
    
    RaftNodeWithRPC node(nodeId, peerAddrs);
    node.start();
    
    // 保持运行
    std::this_thread::sleep_for(std::chrono::hours(24));
    
    return 0;
}