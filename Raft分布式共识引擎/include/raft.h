#pragma once
#include <asio.hpp>
#include <vector>
#include <map>
#include <mutex>
#include <random>
#include <chrono>
#include <functional>
#include <fstream>
#include <nlohmann/json.hpp>  // 需要安装

using json = nlohmann::json;

// ==================== RPC消息定义 ====================
struct RequestVoteArgs {
    int term;
    int candidateId;
    int lastLogIndex;
    int lastLogTerm;
};
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(RequestVoteArgs, term, candidateId, lastLogIndex, lastLogTerm)

struct RequestVoteReply {
    int term;
    bool voteGranted;
};
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(RequestVoteReply, term, voteGranted)

struct AppendEntriesArgs {
    int term;
    int leaderId;
    int prevLogIndex;
    int prevLogTerm;
    std::vector<json> entries;  // 日志条目
    int leaderCommit;
};
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(AppendEntriesArgs, term, leaderId, prevLogIndex, prevLogTerm, entries, leaderCommit)

struct AppendEntriesReply {
    int term;
    bool success;
    int conflictIndex;  // 快速回退优化
    int conflictTerm;
};
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(AppendEntriesReply, term, success, conflictIndex, conflictTerm)

// ==================== 日志条目 ====================
struct LogEntry {
    int term;
    int index;
    json command;  // 状态机命令 {"op": "set", "key": "x", "value": 1}
};
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(LogEntry, term, index, command)

// ==================== 持久化元数据 ====================
struct PersistentState {
    int currentTerm = 0;
    int votedFor = -1;
    std::vector<LogEntry> logs;
};

// ==================== Raft节点类 ====================
class RaftNode {
public:
    enum Role { FOLLOWER, CANDIDATE, LEADER };
    
    RaftNode(int nodeId, const std::vector<std::string>& peerAddrs);
    ~RaftNode();
    
    // 启动和停止
    void start();
    void stop();
    
    // 状态机接口（KV store）
    void submitCommand(const json& cmd, std::function<void(bool, const json&)> callback);
    
private:
    // ---------- 核心状态 ----------
    int nodeId_;
    std::vector<std::string> peerAddrs_;
    Role role_ = FOLLOWER;
    std::mt19937 rng_;
    
    // 持久化状态（需要落盘）
    PersistentState persistentState_;
    std::mutex stateMutex_;

    // 选举计票（Candidate 期间累计票数）
    int voteCount_ = 0;
    
    // 易失性状态
    int commitIndex_ = 0;
    int lastApplied_ = 0;
    
    // Leader特有状态
    std::map<int, int> nextIndex_;   // 给每个Follower的下一条日志索引
    std::map<int, int> matchIndex_;  // 给每个Follower已复制的最高索引
    
    // 定时器
    asio::steady_timer electionTimer_;
    asio::steady_timer heartbeatTimer_;
    asio::io_context ioContext_;
    std::unique_ptr<std::thread> ioThread_;
    
    // RPC客户端
    std::map<int, std::unique_ptr<asio::ip::tcp::socket>> peerSockets_;
    
    // ---------- 核心方法 ----------
    void resetElectionTimer();
    void sendHeartbeat();
    void becomeFollower(int newTerm);
    void becomeCandidate();
    void becomeLeader();
    
    // RPC处理
    RequestVoteReply handleRequestVote(const RequestVoteArgs& args, int fromId);
    AppendEntriesReply handleAppendEntries(const AppendEntriesArgs& args, int fromId);
    
    // 日志复制
    void replicateLogs(int peerId);
    void advanceCommitIndex();
    void applyCommittedLogs();
    
    // 持久化
    void persist();
    bool loadPersist();
    
    // RPC发送
    void sendRequestVote(int peerId);
    void sendAppendEntries(int peerId);
};