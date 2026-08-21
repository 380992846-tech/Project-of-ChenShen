#pragma once

#include <asio.hpp>
#include <vector>
#include <map>
#include <unordered_map>
#include <unordered_set>
#include <mutex>
#include <random>
#include <chrono>
#include <functional>
#include <fstream>
#include <memory>
#include <atomic>
#include <condition_variable>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

// ==================== JSON宏定义 ====================
#define JSON_DEFINE(...) \
    NLOHMANN_DEFINE_TYPE_INTRUSIVE(__VA_ARGS__)

// ==================== RPC消息定义 ====================
struct RequestVoteArgs {
    int term = 0;
    int candidateId = -1;
    int lastLogIndex = 0;
    int lastLogTerm = 0;
    
    json toJson() const {
        return {{"term", term}, {"candidateId", candidateId}, 
                {"lastLogIndex", lastLogIndex}, {"lastLogTerm", lastLogTerm}};
    }
    
    static RequestVoteArgs fromJson(const json& j) {
        RequestVoteArgs args;
        j.at("term").get_to(args.term);
        j.at("candidateId").get_to(args.candidateId);
        j.at("lastLogIndex").get_to(args.lastLogIndex);
        j.at("lastLogTerm").get_to(args.lastLogTerm);
        return args;
    }
};

struct RequestVoteReply {
    int term = 0;
    bool voteGranted = false;
    
    json toJson() const {
        return {{"term", term}, {"voteGranted", voteGranted}};
    }
    
    static RequestVoteReply fromJson(const json& j) {
        RequestVoteReply reply;
        j.at("term").get_to(reply.term);
        j.at("voteGranted").get_to(reply.voteGranted);
        return reply;
    }
};

struct AppendEntriesArgs {
    int term = 0;
    int leaderId = -1;
    int prevLogIndex = 0;
    int prevLogTerm = 0;
    std::vector<json> entries;
    int leaderCommit = 0;
    
    json toJson() const {
        json j;
        j["term"] = term;
        j["leaderId"] = leaderId;
        j["prevLogIndex"] = prevLogIndex;
        j["prevLogTerm"] = prevLogTerm;
        j["entries"] = entries;
        j["leaderCommit"] = leaderCommit;
        return j;
    }
    
    static AppendEntriesArgs fromJson(const json& j) {
        AppendEntriesArgs args;
        j.at("term").get_to(args.term);
        j.at("leaderId").get_to(args.leaderId);
        j.at("prevLogIndex").get_to(args.prevLogIndex);
        j.at("prevLogTerm").get_to(args.prevLogTerm);
        if (j.contains("entries")) {
            j.at("entries").get_to(args.entries);
        }
        j.at("leaderCommit").get_to(args.leaderCommit);
        return args;
    }
};

struct AppendEntriesReply {
    int term = 0;
    bool success = false;
    int conflictIndex = -1;
    int conflictTerm = -1;
    
    json toJson() const {
        return {{"term", term}, {"success", success}, 
                {"conflictIndex", conflictIndex}, {"conflictTerm", conflictTerm}};
    }
    
    static AppendEntriesReply fromJson(const json& j) {
        AppendEntriesReply reply;
        j.at("term").get_to(reply.term);
        j.at("success").get_to(reply.success);
        j.at("conflictIndex").get_to(reply.conflictIndex);
        j.at("conflictTerm").get_to(reply.conflictTerm);
        return reply;
    }
};

// ==================== 日志条目 ====================
struct LogEntry {
    int term = 0;
    int index = 0;
    json command;
    
    json toJson() const {
        return {{"term", term}, {"index", index}, {"command", command}};
    }
    
    static LogEntry fromJson(const json& j) {
        LogEntry entry;
        j.at("term").get_to(entry.term);
        j.at("index").get_to(entry.index);
        j.at("command").get_to(entry.command);
        return entry;
    }
};

// ==================== 持久化元数据 ====================
struct PersistentState {
    int currentTerm = 0;
    int votedFor = -1;
    std::vector<LogEntry> logs;
    
    json toJson() const {
        json j;
        j["currentTerm"] = currentTerm;
        j["votedFor"] = votedFor;
        j["logs"] = json::array();
        for (const auto& log : logs) {
            j["logs"].push_back(log.toJson());
        }
        return j;
    }
    
    static PersistentState fromJson(const json& j) {
        PersistentState state;
        j.at("currentTerm").get_to(state.currentTerm);
        j.at("votedFor").get_to(state.votedFor);
        if (j.contains("logs")) {
            for (const auto& item : j["logs"]) {
                state.logs.push_back(LogEntry::fromJson(item));
            }
        }
        return state;
    }
};

// ==================== Raft节点基类 ====================
class RaftNode {
public:
    enum Role { FOLLOWER, CANDIDATE, LEADER };
    
    RaftNode(int nodeId, const std::vector<std::string>& peerAddrs);
    virtual ~RaftNode();
    
    // 启动和停止
    virtual void start();
    virtual void stop();
    
    // 状态机接口
    void submitCommand(const json& cmd, std::function<void(bool, const json&)> callback);
    
    // 获取状态（用于调试）
    int getNodeId() const { return node_id_; }
    Role getRole() const { return role_; }
    int getCurrentTerm() const { return persistent_state_.currentTerm; }
    
protected:
    // ---------- 核心状态 ----------
    int node_id_;
    std::vector<std::string> peer_addrs_;
    Role role_ = FOLLOWER;
    std::mt19937 rng_;
    
    // 持久化状态
    PersistentState persistent_state_;
    
    // 易失性状态
    int commit_index_ = 0;
    int last_applied_ = 0;
    
    // Leader特有状态
    std::map<int, int> next_index_;
    std::map<int, int> match_index_;
    
    // 定时器
    asio::steady_timer election_timer_;
    asio::steady_timer heartbeat_timer_;
    asio::io_context io_context_;
    std::unique_ptr<std::thread> io_thread_;
    asio::executor_work_guard<asio::io_context::executor_type> work_guard_;
    
    // 运行控制
    std::atomic<bool> running_{false};
    std::mutex state_mutex_;
    std::condition_variable cv_;
    
    // ---------- 核心方法 ----------
    virtual void reset_election_timer();
    virtual void send_heartbeat();
    virtual void become_follower(int newTerm);
    virtual void become_candidate();
    virtual void become_leader();
    
    // RPC处理（子类可重写）
    virtual RequestVoteReply handle_request_vote(const RequestVoteArgs& args, int fromId);
    virtual AppendEntriesReply handle_append_entries(const AppendEntriesArgs& args, int fromId);
    
    // 日志复制
    virtual void replicate_logs(int peerId);
    virtual void advance_commit_index();
    virtual void apply_committed_logs();
    
    // 持久化
    virtual void persist();
    virtual bool load_persist();
    std::string get_persist_path() const;
    
    // RPC发送（子类必须实现）
    virtual void send_request_vote(int peerId) = 0;
    virtual void send_append_entries(int peerId) = 0;
    
    // 选举
    virtual void start_election();
    
    // 工具
    int get_peer_count() const { return static_cast<int>(peer_addrs_.size()); }
    bool is_quorum(int n) const { return n > get_peer_count() / 2; }
    
private:
    // 定时器回调
    void on_election_timeout(asio::error_code ec);
    void on_heartbeat_timeout(asio::error_code ec);
};

// ==================== JSON序列化支持 ====================
namespace nlohmann {
    template<>
    struct adl_serializer<LogEntry> {
        static void to_json(json& j, const LogEntry& entry) {
            j = entry.toJson();
        }
        static void from_json(const json& j, LogEntry& entry) {
            entry = LogEntry::fromJson(j);
        }
    };
    
    template<>
    struct adl_serializer<PersistentState> {
        static void to_json(json& j, const PersistentState& state) {
            j = state.toJson();
        }
        static void from_json(const json& j, PersistentState& state) {
            state = PersistentState::fromJson(j);
        }
    };
}