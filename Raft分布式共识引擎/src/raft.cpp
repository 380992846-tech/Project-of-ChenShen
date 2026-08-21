// ==================== raft_rpc.h ====================
#pragma once

#include "../include/raft.h"
#include <asio.hpp>
#include <thread>
#include <iostream>
#include <cstring>
#include <queue>
#include <unordered_map>
#include <functional>
#include <sstream>
#include <memory>
#include <atomic>
#include <condition_variable>
#include <algorithm>

using asio::ip::tcp;

// ==================== RPC消息类型枚举 ====================
enum class RpcType {
    REQUEST_VOTE_REQ,
    REQUEST_VOTE_RESP,
    APPEND_ENTRIES_REQ,
    APPEND_ENTRIES_RESP,
};

// ==================== 网络消息包装 ====================
struct RpcMessage {
    RpcType type;
    int srcId;
    int dstId;
    json payload;
    uint64_t reqId = 0;
    
    std::string serialize() const {
        json j = {
            {"type", static_cast<int>(type)},
            {"srcId", srcId},
            {"dstId", dstId},
            {"payload", payload},
            {"reqId", reqId}
        };
        std::string body = j.dump();
        uint32_t len = static_cast<uint32_t>(body.size());
        std::string result;
        result.resize(4 + body.size());
        std::memcpy(result.data(), &len, 4);
        std::memcpy(result.data() + 4, body.data(), body.size());
        return result;
    }
    
    static RpcMessage deserialize(const std::string& data) {
        if (data.size() < 4) throw std::runtime_error("Invalid message");
        json j = json::parse(data.substr(4));
        RpcMessage msg;
        msg.type = static_cast<RpcType>(j["type"].get<int>());
        msg.srcId = j["srcId"].get<int>();
        msg.dstId = j["dstId"].get<int>();
        msg.payload = j["payload"];
        msg.reqId = j.value("reqId", 0ULL);
        return msg;
    }
    
    static bool try_deserialize(const std::string& data, RpcMessage& msg) {
        if (data.size() < 4) return false;
        uint32_t len;
        std::memcpy(&len, data.data(), 4);
        if (data.size() < 4 + len) return false;
        try {
            msg = deserialize(data.substr(0, 4 + len));
            return true;
        } catch (...) {
            return false;
        }
    }
};

// ==================== 异步重连定时器 ====================
class ReconnectTimer {
public:
    using Callback = std::function<void()>;
    
    ReconnectTimer(asio::io_context& io, std::chrono::milliseconds interval)
        : timer_(io), interval_(interval), running_(false) {}
    
    ~ReconnectTimer() {
        stop();
    }
    
    void start(Callback cb) {
        callback_ = cb;
        running_ = true;
        do_wait();
    }
    
    void stop() {
        running_ = false;
        timer_.cancel();
    }
    
private:
    void do_wait() {
        if (!running_) return;
        timer_.expires_after(interval_);
        timer_.async_wait([this](asio::error_code ec) {
            if (ec == asio::error::operation_aborted) {
                return;
            }
            if (!ec && running_ && callback_) {
                callback_();
                do_wait();
            }
        });
    }
    
    asio::steady_timer timer_;
    std::chrono::milliseconds interval_;
    std::atomic<bool> running_;
    Callback callback_;
};

// ==================== RPC客户端连接 ====================
class RpcClient : public std::enable_shared_from_this<RpcClient> {
public:
    using Callback = std::function<void(const json&)>;
    using DisconnectCallback = std::function<void()>;
    
    RpcClient(asio::io_context& io, const std::string& host, int port)
        : socket_(io), resolver_(io), host_(host), port_(port), 
          connected_(false), reconnect_timer_(io, std::chrono::seconds(5)),
          reconnect_attempts_(0) {}
    
    ~RpcClient() { 
        close(); 
    }
    
    void set_disconnect_callback(DisconnectCallback cb) {
        disconnect_callback_ = cb;
    }
    
    void connect(std::function<void(bool)> callback = nullptr) {
        // 防止并发发起多次 async_connect（同一 socket 并发 connect 是未定义行为，
        // 会一直连不上——这正是节点间无法通信的元凶之一）
        if (connecting_.exchange(true)) {
            // 已经在连接中，暂存最新回调，等当前连接完成时再回调
            pending_connect_cb_ = callback;
            return;
        }
        
        auto self = shared_from_this();
        resolver_.async_resolve(host_, std::to_string(port_),
            [this, self, callback](asio::error_code ec, tcp::resolver::results_type endpoints) {
                if (ec) {
                    connecting_ = false;
                    auto cb = callback; if (!cb) cb = pending_connect_cb_;
                    pending_connect_cb_ = nullptr;
                    if (cb) cb(false);
                    schedule_reconnect();
                    return;
                }
                
                asio::async_connect(socket_, endpoints,
                    [this, self, callback](asio::error_code ec, tcp::endpoint) {
                        connecting_ = false;
                        auto cb = callback; if (!cb) cb = pending_connect_cb_;
                        pending_connect_cb_ = nullptr;
                        if (!ec) {
                            connected_ = true;
                            reconnect_attempts_ = 0;
                            reconnect_timer_.stop();
                            std::cout << "[Client] connected to " << host_ << ":" << port_ << std::endl;
                            do_read_header();
                            if (cb) cb(true);
                        } else {
                            std::cout << "[Client] connect " << host_ << ":" << port_
                                      << " FAILED: " << ec.message() << std::endl;
                            if (cb) cb(false);
                            schedule_reconnect();
                        }
                    });
            });
    }
    
    void send_request(RpcType type, const json& payload, Callback callback) {
        if (!connected_) {
            if (callback) callback(json{{"error", "not connected"}});
            schedule_reconnect();
            return;
        }
        
        uint64_t reqId = next_req_id_++;
        {
            std::lock_guard<std::mutex> lock(callbacks_mutex_);
            pending_callbacks_[reqId] = callback;
        }
        
        RpcMessage msg;
        msg.type = type;
        msg.srcId = 0;
        msg.dstId = 0;
        msg.payload = payload;
        msg.reqId = reqId;
        
        std::string data = msg.serialize();
        auto self = shared_from_this();
        asio::async_write(socket_, asio::buffer(data),
            [this, self, reqId](asio::error_code ec, size_t) {
                if (ec) {
                    std::lock_guard<std::mutex> lock(callbacks_mutex_);
                    auto it = pending_callbacks_.find(reqId);
                    if (it != pending_callbacks_.end()) {
                        it->second(json{{"error", ec.message()}});
                        pending_callbacks_.erase(it);
                    }
                    close();
                    schedule_reconnect();
                }
            });
    }
    
    void close() {
        connected_ = false;
        reconnect_timer_.stop();
        asio::error_code ec;
        socket_.close(ec);
        {
            std::lock_guard<std::mutex> lock(callbacks_mutex_);
            for (auto& [id, cb] : pending_callbacks_) {
                cb(json{{"error", "connection closed"}});
            }
            pending_callbacks_.clear();
        }
        if (disconnect_callback_) disconnect_callback_();
    }
    
    bool is_connected() const { return connected_; }
    const std::string& get_host() const { return host_; }
    int get_port() const { return port_; }
    
private:
    void schedule_reconnect() {
        if (reconnect_attempts_ >= 1000) return;
        reconnect_attempts_++;
        reconnect_timer_.start([this]() {
            if (!connected_ && !connecting_) {
                connect([](bool) {});
            }
        });
    }
    
    void do_read_header() {
        auto self = shared_from_this();
        asio::async_read(socket_, asio::buffer(header_buffer_, 4),
            [this, self](asio::error_code ec, size_t) {
                if (!ec) {
                    uint32_t body_len;
                    std::memcpy(&body_len, header_buffer_.data(), 4);
                    if (body_len > 1024 * 1024) {
                        close();
                        return;
                    }
                    body_buffer_.resize(body_len);
                    do_read_body(body_len);
                } else {
                    close();
                }
            });
    }
    
    void do_read_body(uint32_t body_len) {
        auto self = shared_from_this();
        asio::async_read(socket_, asio::buffer(body_buffer_.data(), body_len),
            [this, self, body_len](asio::error_code ec, size_t) {
                if (!ec) {
                    try {
                        std::string full_msg;
                        full_msg.resize(4 + body_len);
                        std::memcpy(full_msg.data(), header_buffer_.data(), 4);
                        std::memcpy(full_msg.data() + 4, body_buffer_.data(), body_len);
                        
                        RpcMessage msg = RpcMessage::deserialize(full_msg);
                        handle_response(msg);
                    } catch (...) {
                        // 解析失败
                    }
                    do_read_header();
                } else {
                    close();
                }
            });
    }
    
    void handle_response(const RpcMessage& msg) {
        if (msg.reqId != 0) {
            std::lock_guard<std::mutex> lock(callbacks_mutex_);
            auto it = pending_callbacks_.find(msg.reqId);
            if (it != pending_callbacks_.end()) {
                json response = msg.payload;
                it->second(response);
                pending_callbacks_.erase(it);
            }
        }
    }
    
    tcp::socket socket_;
    tcp::resolver resolver_;
    std::string host_;
    int port_;
    std::atomic<bool> connected_;
    std::atomic<bool> connecting_{false};
    std::function<void(bool)> pending_connect_cb_;
    std::array<char, 4> header_buffer_;
    std::string body_buffer_;
    uint64_t next_req_id_ = 1;
    std::mutex callbacks_mutex_;
    std::unordered_map<uint64_t, Callback> pending_callbacks_;
    ReconnectTimer reconnect_timer_;
    int reconnect_attempts_;
    DisconnectCallback disconnect_callback_;
};

// ==================== RPC服务端 ====================
class RpcServer {
public:
    using RequestHandler = std::function<RpcMessage(const RpcMessage&)>;
    
    RpcServer(asio::io_context& io, int port)
        : io_(io), acceptor_(io, tcp::endpoint(tcp::v4(), port)), port_(port),
          cleanup_timer_(io), running_(true) {}
    
    ~RpcServer() { 
        stop(); 
    }
    
    void start(RequestHandler handler) {
        handler_ = handler;
        do_accept();
        schedule_cleanup();
    }
    
    void stop() {
        running_ = false;
        
        asio::error_code ec;
        acceptor_.close(ec);
        
        cleanup_timer_.cancel();
        
        std::lock_guard<std::mutex> lock(sessions_mutex_);
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
            asio::error_code ec;
            socket_.close(ec);
        }
        
        bool is_open() const { 
            return socket_.is_open(); 
        }
        
    private:
        void do_read_header() {
            auto self = shared_from_this();
            asio::async_read(socket_, asio::buffer(header_buffer_, 4),
                [this, self](asio::error_code ec, size_t) {
                    if (!ec) {
                        uint32_t body_len;
                        std::memcpy(&body_len, header_buffer_.data(), 4);
                        if (body_len > 1024 * 1024) { close(); return; }
                        body_buffer_.resize(body_len);
                        do_read_body(body_len);
                    } else {
                        close();
                    }
                });
        }
        
        void do_read_body(uint32_t body_len) {
            auto self = shared_from_this();
            asio::async_read(socket_, asio::buffer(body_buffer_.data(), body_len),
                [this, self, body_len](asio::error_code ec, size_t) {
                    if (!ec) {
                        try {
                            std::string full_msg;
                            full_msg.resize(4 + body_len);
                            std::memcpy(full_msg.data(), header_buffer_.data(), 4);
                            std::memcpy(full_msg.data() + 4, body_buffer_.data(), body_len);
                            
                            RpcMessage req = RpcMessage::deserialize(full_msg);
                            RpcMessage resp = handler_(req);
                            resp.reqId = req.reqId;
                            
                            std::string data = resp.serialize();
                            asio::async_write(socket_, asio::buffer(data),
                                [this, self](asio::error_code ec, size_t) {
                                    if (ec) close();
                                });
                        } catch (const std::exception& e) {
                            json error_payload = {{"error", e.what()}};
                            RpcMessage error_msg;
                            error_msg.type = RpcType::APPEND_ENTRIES_RESP;
                            error_msg.payload = error_payload;
                            std::string data = error_msg.serialize();
                            asio::async_write(socket_, asio::buffer(data),
                                [this, self](asio::error_code, std::size_t) {});
                        }
                        do_read_header();
                    } else {
                        close();
                    }
                });
        }
        
        tcp::socket socket_;
        std::array<char, 4> header_buffer_;
        std::string body_buffer_;
        RequestHandler handler_;
    };
    
    void do_accept() {
        if (!running_) return;
        
        acceptor_.async_accept([this](asio::error_code ec, tcp::socket socket) {
            if (!ec && running_) {
                auto session = std::make_shared<Session>(std::move(socket), handler_);
                {
                    std::lock_guard<std::mutex> lock(sessions_mutex_);
                    sessions_.push_back(session);
                }
                std::cout << "[Server] accepted connection" << std::endl;
                session->start();
            }
            do_accept();
        });
    }
    
    void schedule_cleanup() {
        if (!running_) return;
        
        cleanup_timer_.expires_after(std::chrono::seconds(30));
        cleanup_timer_.async_wait([this](asio::error_code ec) {
            if (ec == asio::error::operation_aborted) {
                return;
            }
            if (!ec && running_) {
                cleanup_sessions();
                schedule_cleanup();
            }
        });
    }
    
    void cleanup_sessions() {
        std::lock_guard<std::mutex> lock(sessions_mutex_);
        sessions_.erase(std::remove_if(sessions_.begin(), sessions_.end(),
            [](const std::shared_ptr<Session>& s) {
                return !s || !s->is_open();
            }), sessions_.end());
    }
    
    asio::io_context& io_;
    tcp::acceptor acceptor_;
    int port_;
    RequestHandler handler_;
    std::mutex sessions_mutex_;
    std::vector<std::shared_ptr<Session>> sessions_;
    asio::steady_timer cleanup_timer_;
    std::atomic<bool> running_;
};

// ==================== Raft节点集成RPC ====================
class RaftNodeWithRPC : public RaftNode {
public:
    RaftNodeWithRPC(int nodeId, const std::vector<std::string>& peerAddrs)
        : RaftNode(nodeId, peerAddrs),
          rpc_server_(io_context_, get_own_port(peerAddrs, nodeId)),
          votes_(0),
          voted_peers_(),
          election_in_progress_(false) {
        
        // 设置服务端请求处理器
        // 说明：RPC 与选举定时器共用基类的 io_context_，由基类 start() 启动的 io 线程驱动，
        // 派生类这里不再另起线程，避免多 io_context / 重复线程带来的混乱与死锁
        rpc_server_.start([this](const RpcMessage& req) -> RpcMessage {
            return handle_rpc_request(req);
        });
        
        // 初始化客户端连接
        for (size_t i = 0; i < peerAddrs.size(); ++i) {
            if (static_cast<int>(i) == nodeId) continue;
            auto [host, port] = parse_addr(peerAddrs[i]);
            auto client = std::make_shared<RpcClient>(io_context_, host, port);
            clients_[static_cast<int>(i)] = client;
            
            client->set_disconnect_callback([this, peerId = static_cast<int>(i)]() {
                // 断线后由RpcClient内部自动重连
            });
            
            client->connect([this, peerId = static_cast<int>(i)](bool success) {
                if (success) {
                    std::cout << "[N" << node_id_ << "] connected to Peer " << peerId << std::endl;
                    std::lock_guard<std::mutex> lock(state_mutex_);
                    if (role_ == LEADER) {
                        replicate_logs(peerId);
                    }
                } else {
                    std::cerr << "[N" << node_id_ << "] connect Peer " << peerId 
                              << " FAILED, will retry in background" << std::endl;
                }
            });
        }
    }
    
    ~RaftNodeWithRPC() override {
        stop();
    }
    
    void stop() {
        // 先停 RPC 服务与 IO，避免新回调进入
        rpc_server_.stop();
        io_context_.stop();
        cv_.notify_all();
        
        for (auto& [peerId, client] : clients_) {
            client->close();
        }
        clients_.clear();
        
        // 关键修复：必须调用基类 stop() 来 join io_thread_。
        // 派生 stop() 若不 join，析构时基类 ~RaftNode 里的 stop() 会因 running_ 已 false 直接
        // return，留下可 join 的 std::thread 未被 join -> 析构 std::thread -> std::terminate。
        // 基类 stop() 会置 running_=false、reset work_guard、并 join io_thread_。
        RaftNode::stop();
    }
    
    void start_loop() {
        std::unique_lock<std::mutex> lock(state_mutex_);
        while (running_) {
            cv_.wait_for(lock, std::chrono::seconds(1));
        }
    }
    
    // ==================== 对外命令接口 ====================
    // 读取本地已应用 KV 值（不经过 Raft，直接读本节点状态机）
    json get_kv(const std::string& key) {
        std::lock_guard<std::mutex> lock(kv_mutex_);
        auto it = kv_store_.find(key);
        if (it == kv_store_.end()) return {{"found", false}};
        return {{"found", true}, {"value", it->second}};
    }
    
    // 返回节点当前状态（角色/任期/Leader/日志长度/已应用位置）
    json status() {
        // 分别加锁：kv_store_ 由 kv_mutex_ 保护，其余由 state_mutex_ 保护。
        // 分开加锁（而非持 state_mutex_ 时读 kv_store_）避免不同互斥锁保护的并发读（数据竞争）。
        int kv_size = 0;
        {
            std::lock_guard<std::mutex> lk(kv_mutex_);
            kv_size = static_cast<int>(kv_store_.size());
        }
        std::lock_guard<std::mutex> lock(state_mutex_);
        const char* roleStr = (role_ == LEADER) ? "LEADER" : (role_ == CANDIDATE) ? "CANDIDATE" : "FOLLOWER";
        return {
            {"node", node_id_},
            {"role", roleStr},
            {"term", persistent_state_.currentTerm},
            {"leader", leader_id_},
            {"logLen", static_cast<int>(persistent_state_.logs.size())},
            {"commitIndex", commit_index_},
            {"lastApplied", last_applied_},
            {"kvSize", kv_size}
        };
    }
    
protected:
    // ==================== 覆盖基类虚函数 ====================
    void start_election() override {
        std::lock_guard<std::mutex> lock(state_mutex_);
        
        // 先重置本地投票状态（关键：必须在发送RPC之前）
        votes_ = 1;  // 自己投自己
        voted_peers_.clear();
        voted_peers_.insert(node_id_);
        election_in_progress_ = true;
        current_election_term_ = persistent_state_.currentTerm;
        
        // 再调用基类（基类内部会发送RPC，回调会使用上面重置后的状态）
        RaftNode::start_election();
    }
    
    void become_follower(int term) override {
        // 注意：不要在入口 lock(state_mutex_)——它可能被 handle_request_vote /
        // 回复回调（已持锁）调用，重复加非递归锁会死锁（io 线程卡死，不回票，选不出 Leader）
        RaftNode::become_follower(term);
        votes_ = 0;
        voted_peers_.clear();
        election_in_progress_ = false;
    }
    
    void become_leader() override {
        // 同 become_follower：可能被已持锁的回复回调调用，不能在入口重复加锁
        RaftNode::become_leader();
        votes_ = 0;
        voted_peers_.clear();
        election_in_progress_ = false;
    }
    
    RequestVoteReply handle_request_vote(const RequestVoteArgs& args, int srcId) override {
        // 不能在入口 lock(state_mutex_)：基类可能调 become_follower（派生版会再锁）→ 死锁
        return RaftNode::handle_request_vote(args, srcId);
    }
    
    AppendEntriesReply handle_append_entries(const AppendEntriesArgs& args, int srcId) override {
        // 同上，避免重复加锁死锁
        return RaftNode::handle_append_entries(args, srcId);
    }
    
    void send_request_vote(int peerId) override {
        RequestVoteArgs args;
        args.term = persistent_state_.currentTerm;
        args.candidateId = node_id_;
        args.lastLogIndex = persistent_state_.logs.size();
        args.lastLogTerm = persistent_state_.logs.empty() ? 0 : persistent_state_.logs.back().term;
        
        // 记录发送时的任期，用于回调中校验
        uint64_t send_term = args.term;send_rpc(peerId, RpcType::REQUEST_VOTE_REQ, args.toJson(),
            [this, peerId, send_term](const json& resp_json) {
                if (resp_json.contains("error")) {
                    std::cerr << "[N" << node_id_ << "] RequestVote to " << peerId
                              << " failed: " << resp_json["error"] << std::endl;
                    return;
                }
                
                try {
                    RequestVoteReply reply = RequestVoteReply::fromJson(resp_json);
                    
                    std::lock_guard<std::mutex> lock(state_mutex_);

                    // 若对端任期更高：无论本节点是 Candidate/Leader，都必须立刻降级为 Follower
                    // 并更新 term（Raft Figure 2: "If RPC response contains term T > currentTerm: set currentTerm=T, convert to follower"）。
                    // 此检查必须先于下面的任期判等，否则更高 term 的响应会被 return 拦掉，旧节点永不退位（分区中旧 Leader 持续 ack 的根因）。
                    if (reply.term > persistent_state_.currentTerm) {
                        become_follower(reply.term);
                        return;
                    }

                    // 校验：选举已结束，或任期不匹配（对端回复了过期/不同的 term），忽略此回复
                    if (!election_in_progress_ || reply.term != send_term) {
                        return;
                    }
                    
                    if (role_ == CANDIDATE && reply.voteGranted) {
                        // 检查是否已经投过票
                        if (voted_peers_.find(peerId) == voted_peers_.end()) {
                            voted_peers_.insert(peerId);
                            votes_++;
                            std::cout << "[N" << node_id_ << "] got vote from Peer " << peerId
                                      << " (votes=" << votes_ << ")" << std::endl;
                            
                            if (votes_ > static_cast<int>(peer_addrs_.size() / 2)) {
                                become_leader();
                            }
                        }
                    }
                } catch (const std::exception& e) {
                    std::cerr << "[N" << node_id_ << "] parse RequestVote reply failed: " << e.what() << std::endl;
                }
            });
    }
    
    void send_append_entries(int peerId) override {
        AppendEntriesArgs args;
        args.term = persistent_state_.currentTerm;
        args.leaderId = node_id_;
        args.leaderCommit = commit_index_;
        
        int prevIndex = next_index_[peerId] - 1;
        
        if (prevIndex < 0) {
            prevIndex = 0;
        }
        
        args.prevLogIndex = prevIndex;
        args.prevLogTerm = (prevIndex == 0 || prevIndex > static_cast<int>(persistent_state_.logs.size())) 
                           ? 0 
                           : persistent_state_.logs[prevIndex - 1].term;
        
        int startIdx = next_index_[peerId] - 1;
        if (startIdx < 0) startIdx = 0;
        
        if (startIdx < static_cast<int>(persistent_state_.logs.size())) {
            for (int i = startIdx; i < static_cast<int>(persistent_state_.logs.size()); ++i) {
                args.entries.push_back(persistent_state_.logs[i].toJson());
            }
        }
        
        // 保存发送时的任期，用于回调校验
        uint64_t send_term = args.term;
        
        send_rpc(peerId, RpcType::APPEND_ENTRIES_REQ, args.toJson(),
            [this, peerId, args, send_term](const json& resp_json) {
                if (resp_json.contains("error")) {
                    return;
                }
                
                try {
                    AppendEntriesReply reply = AppendEntriesReply::fromJson(resp_json);
                    
                    std::lock_guard<std::mutex> lock(state_mutex_);

                    // 对端任期更高 -> 立即降级为 Follower（先于任期判等，见 RequestVote 回调同款修复）
                    if (reply.term > persistent_state_.currentTerm) {
                        become_follower(reply.term);
                        return;
                    }

                    // 校验任期是否匹配（对端回复了过期/不同的 term，忽略）
                    if (reply.term != send_term) {
                        return;
                    }
                    
                    if (role_ == LEADER) {
                        if (reply.success) {
                            int newMatchIndex = args.prevLogIndex + static_cast<int>(args.entries.size());
                            match_index_[peerId] = std::max(match_index_[peerId], newMatchIndex);
                            next_index_[peerId] = match_index_[peerId] + 1;
                            advance_commit_index();
                        } else {
                            if (reply.conflictTerm == -1) {
                                next_index_[peerId] = std::max(1, reply.conflictIndex);
                            } else {
                                int lastIndex = -1;
                                for (int i = static_cast<int>(persistent_state_.logs.size()) - 1; i >= 0; --i) {
                                    if (persistent_state_.logs[i].term == reply.conflictTerm) {
                                        lastIndex = i + 1;
                                        break;
                                    }
                                }
                                if (lastIndex > 0) {
                                    next_index_[peerId] = lastIndex;
                                } else {
                                    next_index_[peerId] = std::max(1, reply.conflictIndex);
                                }
                            }
                            if (role_ == LEADER) {
                                send_append_entries(peerId);
                            }
                        }
                    }
                } catch (const std::exception& e) {
                    std::cerr << "[N" << node_id_ << "] parse AppendEntries reply failed: " << e.what() << std::endl;
                }
            });
    }
    
    void replicate_logs(int peerId) override {
        send_append_entries(peerId);
    }
    
    void advance_commit_index() override {
        RaftNode::advance_commit_index();
    }
    
    // 把一条已提交的日志条目应用到 KV 状态机
    void apply_command(const json& cmd) override {
        std::lock_guard<std::mutex> lock(kv_mutex_);
        std::string op = cmd.value("op", "");
        if (op == "set") {
            std::string key = cmd.value("key", "");
            std::string val = cmd.value("value", "");
            kv_store_[key] = val;
            std::cout << "[N" << node_id_ << "] APPLY set " << key << " = " << val << std::endl;
        } else if (op == "del") {
            std::string key = cmd.value("key", "");
            kv_store_.erase(key);
            std::cout << "[N" << node_id_ << "] APPLY del " << key << std::endl;
        } else {
            std::cout << "[N" << node_id_ << "] APPLY unknown cmd: " << cmd.dump() << std::endl;
        }
    }
    
private:
    // ==================== RPC请求处理 ====================
    RpcMessage handle_rpc_request(const RpcMessage& req) {
        RpcMessage resp;
        resp.srcId = node_id_;
        resp.dstId = req.srcId;
        resp.type = RpcType::APPEND_ENTRIES_RESP;
        
        try {
            switch (req.type) {
                case RpcType::REQUEST_VOTE_REQ: {
                    RequestVoteArgs args = RequestVoteArgs::fromJson(req.payload);
                    std::cout << "[N" << node_id_ << "] RPC: RequestVote from src=" << req.srcId
                              << " term=" << args.term << std::endl;
                    RequestVoteReply reply = handle_request_vote(args, req.srcId);
                    resp.type = RpcType::REQUEST_VOTE_RESP;
                    resp.payload = reply.toJson();
                    std::cout << "[N" << node_id_ << "] RPC: RequestVote reply voteGranted="
                              << reply.voteGranted << " term=" << reply.term << std::endl;
                    break;
                }
                case RpcType::APPEND_ENTRIES_REQ: {
                    AppendEntriesArgs args = AppendEntriesArgs::fromJson(req.payload);
                    AppendEntriesReply reply = handle_append_entries(args, req.srcId);
                    resp.type = RpcType::APPEND_ENTRIES_RESP;
                    resp.payload = reply.toJson();
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
        if (it == clients_.end()) {
            if (callback) callback(json{{"error", "peer not found"}});
            return;
        }
        
        if (!it->second->is_connected()) {
            it->second->connect([this, peerId, type, payload, callback](bool success) {
                if (success) {
                    send_rpc(peerId, type, payload, callback);
                } else if (callback) {
                    callback(json{{"error", "connection failed"}});
                }
            });
            return;
        }
        
        if (callback) {
            it->second->send_request(type, payload, callback);
        } else {
            it->second->send_request(type, payload, [](const json&) {});
        }
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
    
    // 取得本节点的监听端口，并做越界检查：
    // --peers 必须传入【全部】节点地址（含自己），按节点ID排列，即 addrs[nodeId] 就是本节点自己的地址
    static int get_own_port(const std::vector<std::string>& addrs, int nodeId) {
        if (nodeId < 0 || static_cast<size_t>(nodeId) >= addrs.size()) {
            throw std::runtime_error(
                "nodeId=" + std::to_string(nodeId) + " out of range (addr list size=" +
                std::to_string(addrs.size()) + "). --peers must contain ALL node addresses "
                "(including self), indexed by node id; e.g. each of 3 nodes: "
                "--peers=127.0.0.1:9000,127.0.0.1:9001,127.0.0.1:9002");
        }
        return get_port_from_addr(addrs[nodeId]);
    }
    
    // ==================== 成员变量 ====================
    // 注意：这里不要重复声明 io_context_ / io_thread_ / running_ / state_mutex_ / cv_，
    // 它们会遮蔽基类成员，导致“两把互斥锁保护同一份状态”和“两个 io 上下文”的混乱，
    // 全部复用基类的（raft.h 已保证 io_context_ 先于定时器构造）。
    RpcServer rpc_server_;
    std::unordered_map<int, std::shared_ptr<RpcClient>> clients_;
    
    // KV 状态机（由 apply_command 在日志提交后写入；kv_mutex_ 与 state_mutex_ 相互独立，
    // 避免在 io 线程已持 state_mutex_ 时又被 apply_command 重复加锁导致死锁）
    std::map<std::string, std::string> kv_store_;
    std::mutex kv_mutex_;
    
    // 选举相关
    int votes_ = 0;
    std::unordered_set<int> voted_peers_;
    std::atomic<bool> election_in_progress_;
    uint64_t current_election_term_ = 0;
};

// ==================== main函数 ====================
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
    
    std::cout << "Raft node " << nodeId << " starting, cluster size=" << peerAddrs.size() << std::endl;

    try {
        auto node = std::make_shared<RaftNodeWithRPC>(nodeId, peerAddrs);
        node->start();

        // 交互式命令线程（读 stdin）
        std::thread cmd_thread([node]() {
            std::cout << "Commands: set <k> <v> | del <k> | get <k> | status | quit" << std::endl;
            std::string line;
            while (std::getline(std::cin, line)) {
                std::istringstream iss(line);
                std::string op;
                iss >> op;
                if (op == "quit" || op == "exit") {
                    break;
                } else if (op == "set") {
                    std::string k, v;
                    if (!(iss >> k >> v)) { std::cout << "usage: set <key> <value>" << std::endl; continue; }
                    node->submitCommand({{"op", "set"}, {"key", k}, {"value", v}},
                        [k, v](bool ok, const json& r) {
                            if (ok) std::cout << "OK set " << k << " = " << v
                                              << " (index " << r.value("index", -1) << ")" << std::endl;
                            else std::cout << "ERROR: " << r.value("error", "?") << std::endl;
                        });
                } else if (op == "del") {
                    std::string k;
                    if (!(iss >> k)) { std::cout << "usage: del <key>" << std::endl; continue; }
                    node->submitCommand({{"op", "del"}, {"key", k}},
                        [k](bool ok, const json& r) {
                            if (ok) std::cout << "OK del " << k
                                              << " (index " << r.value("index", -1) << ")" << std::endl;
                            else std::cout << "ERROR: " << r.value("error", "?") << std::endl;
                        });
                } else if (op == "get") {
                    std::string k;
                    if (!(iss >> k)) { std::cout << "usage: get <key>" << std::endl; continue; }
                    json r = node->get_kv(k);
                    if (r.value("found", false)) std::cout << k << " = " << r["value"] << std::endl;
                    else std::cout << k << " = (not found)" << std::endl;
                } else if (op == "status") {
                    json s = node->status();
                    // 用 get<std::string>() 取出纯字符串，避免输出带 JSON 引号（role="LEADER"）
                    std::cout << "node=" << s["node"].get<int>()
                              << " role=" << s["role"].get<std::string>()
                              << " term=" << s["term"].get<int>()
                              << " leader=" << s["leader"].get<int>()
                              << " logLen=" << s["logLen"].get<int>()
                              << " kvSize=" << s["kvSize"].get<int>() << std::endl;
                } else {
                    std::cout << "Commands: set <k> <v> | del <k> | get <k> | status | quit" << std::endl;
                }
            }
        });
        cmd_thread.detach();

        node->start_loop();
    } catch (const std::exception& e) {
        std::cerr << "[main] exception: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}