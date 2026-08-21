#include "raft.h"
#include <fstream>
#include <iostream>
#include <chrono>

// ==================== JSON序列化辅助 ====================
namespace {
    template<typename T>
    T from_json(const json& j) {
        return j.get<T>();
    }
}

// ==================== RaftNode 实现 ====================
RaftNode::RaftNode(int nodeId, const std::vector<std::string>& peerAddrs)
    : node_id_(nodeId),
      peer_addrs_(peerAddrs),
      rng_(std::random_device{}()),
      election_timer_(io_context_),
      heartbeat_timer_(io_context_),
      work_guard_(asio::make_work_guard(io_context_)) {
    
    // 加载持久化状态
    if (!load_persist()) {
        persistent_state_.currentTerm = 0;
        persistent_state_.votedFor = -1;
    }
    
    // 初始化Leader状态
    for (size_t i = 0; i < peer_addrs_.size(); ++i) {
        if (static_cast<int>(i) != node_id_) {
            next_index_[static_cast<int>(i)] = persistent_state_.logs.size() + 1;
            match_index_[static_cast<int>(i)] = 0;
        }
    }
}

RaftNode::~RaftNode() {
    stop();
}

void RaftNode::start() {
    if (running_) return;
    running_ = true;
    std::cout << "[N" << node_id_ << "] start() called" << std::endl;
    
    // 启动IO线程
    io_thread_ = std::make_unique<std::thread>([this]() {
        std::cout << "[N" << node_id_ << "] io_context.run() begin" << std::endl;
        io_context_.run();
        std::cout << "[N" << node_id_ << "] io_context.run() exited" << std::endl;
    });
    
    // 启动选举定时器
    reset_election_timer();
}

void RaftNode::stop() {
    if (!running_) return;
    running_ = false;
    
    work_guard_.reset();
    io_context_.stop();
    
    if (io_thread_ && io_thread_->joinable()) {
        io_thread_->join();
    }
}

void RaftNode::submitCommand(const json& cmd, std::function<void(bool, const json&)> callback) {
    std::lock_guard<std::mutex> lock(state_mutex_);
    
    if (role_ != LEADER) {
        if (callback) callback(false, {{"error", "not leader"}});
        return;
    }
    
    // 添加日志条目
    LogEntry entry;
    entry.term = persistent_state_.currentTerm;
    entry.index = persistent_state_.logs.size() + 1;
    entry.command = cmd;
    persistent_state_.logs.push_back(entry);
    
    // 持久化
    persist();
    
    // 立即复制到所有Follower
    for (auto& [peerId, _] : next_index_) {
        replicate_logs(peerId);
    }
    
    if (callback) callback(true, {{"index", entry.index}});
}

// ==================== 定时器管理 ====================
void RaftNode::reset_election_timer() {
    if (!running_) return;
    
    // 随机超时：500-1000ms
    // （足够容纳一轮 RequestVote 的往返；之前 150-300ms 太短，
    //   导致票还没回来就重新选举，term 狂涨、永远攒不够多数票）
    std::uniform_int_distribution<int> dist(500, 1000);
    int timeout_ms = dist(rng_);
    
    election_timer_.expires_after(std::chrono::milliseconds(timeout_ms));
    election_timer_.async_wait([this](asio::error_code ec) {
        on_election_timeout(ec);
    });
}

void RaftNode::on_election_timeout(asio::error_code ec) {
    if (ec || !running_) return;

    // 先判读角色（短暂持锁），释放后再发起选举——
    // 否则 become_candidate -> start_election 内部会再锁 state_mutex_，造成死锁
    {
        std::lock_guard<std::mutex> lock(state_mutex_);
        if (role_ == LEADER) {
            reset_election_timer();
            return;
        }
    }

    become_candidate();

    // 重置定时器（无论是否发起选举）
    reset_election_timer();
}

void RaftNode::send_heartbeat() {
    if (!running_) return;
    
    std::lock_guard<std::mutex> lock(state_mutex_);
    
    if (role_ == LEADER) {
        // 向所有Follower发送心跳
        for (auto& [peerId, _] : next_index_) {
            // 只发送空AppendEntries
            send_append_entries(peerId);
        }
    }
    
    // 调度下一次心跳
    if (running_) {
        heartbeat_timer_.expires_after(std::chrono::milliseconds(50));
        heartbeat_timer_.async_wait([this](asio::error_code ec) {
            if (!ec && running_) {
                send_heartbeat();
            }
        });
    }
}

// ==================== 角色切换 ====================
void RaftNode::become_follower(int newTerm) {
    if (newTerm > persistent_state_.currentTerm) {
        persistent_state_.currentTerm = newTerm;
        persistent_state_.votedFor = -1;
        persist();
    }
    
    role_ = FOLLOWER;
    std::cout << "[N" << node_id_ << "] became FOLLOWER, Term=" 
              << persistent_state_.currentTerm << std::endl;
    
    // 重置定时器
    reset_election_timer();
}

void RaftNode::become_candidate() {
    role_ = CANDIDATE;
    leader_id_ = -1;   // 进入选举，暂时没有 Leader
    persistent_state_.currentTerm++;
    persistent_state_.votedFor = node_id_;
    persist();
    
    std::cout << "[N" << node_id_ << "] became CANDIDATE, Term=" 
              << persistent_state_.currentTerm << std::endl;
    
    // 发起选举
    start_election();
}

void RaftNode::become_leader() {
    role_ = LEADER;
    leader_id_ = node_id_;   // 自己成为 Leader
    
    // 初始化Leader状态
    for (size_t i = 0; i < peer_addrs_.size(); ++i) {
        int peerId = static_cast<int>(i);
        if (peerId != node_id_) {
            next_index_[peerId] = persistent_state_.logs.size() + 1;
            match_index_[peerId] = 0;
        }
    }
    
    std::cout << "[N" << node_id_ << "] became LEADER, Term=" 
              << persistent_state_.currentTerm << std::endl;
    
    // 启动心跳
    heartbeat_timer_.expires_after(std::chrono::milliseconds(0));
    heartbeat_timer_.async_wait([this](asio::error_code ec) {
        if (!ec && running_) {
            send_heartbeat();
        }
    });
}

void RaftNode::start_election() {
    for (auto& [peerId, _] : next_index_) {
        send_request_vote(peerId);
    }
}

// ==================== RPC处理 ====================
RequestVoteReply RaftNode::handle_request_vote(const RequestVoteArgs& args, int fromId) {
    RequestVoteReply reply;
    reply.term = persistent_state_.currentTerm;
    reply.voteGranted = false;
    
    if (args.term < persistent_state_.currentTerm) {
        return reply;
    }
    
    if (args.term > persistent_state_.currentTerm) {
        become_follower(args.term);
        reply.term = persistent_state_.currentTerm;
    }
    
    // 检查是否已经投票给其他人
    if (persistent_state_.votedFor != -1 && persistent_state_.votedFor != args.candidateId) {
        return reply;
    }
    
    // 检查日志是否至少和本节点一样新
    int lastLogIndex = persistent_state_.logs.size();
    int lastLogTerm = lastLogIndex > 0 ? persistent_state_.logs.back().term : 0;
    
    if (args.lastLogTerm < lastLogTerm ||
        (args.lastLogTerm == lastLogTerm && args.lastLogIndex < lastLogIndex)) {
        return reply;
    }
    
    // 投票给该候选人
    reply.voteGranted = true;
    persistent_state_.votedFor = args.candidateId;
    persist();
    
    // 重置选举定时器（收到合法投票请求，说明集群有活跃Leader）
    reset_election_timer();
    
    return reply;
}

AppendEntriesReply RaftNode::handle_append_entries(const AppendEntriesArgs& args, int fromId) {
    AppendEntriesReply reply;
    reply.term = persistent_state_.currentTerm;
    reply.success = false;
    reply.conflictIndex = -1;
    reply.conflictTerm = -1;
    
    if (args.term < persistent_state_.currentTerm) {
        return reply;
    }
    
    if (args.term > persistent_state_.currentTerm) {
        become_follower(args.term);
        reply.term = persistent_state_.currentTerm;
    }
    
    // 重置选举定时器（收到Leader的心跳，说明集群有Leader）
    leader_id_ = args.leaderId;
    reset_election_timer();
    
    // 检查prevLogIndex和prevLogTerm是否匹配
    if (args.prevLogIndex > static_cast<int>(persistent_state_.logs.size())) {
        // Follower日志太短
        reply.conflictIndex = persistent_state_.logs.size() + 1;
        reply.conflictTerm = -1;
        return reply;
    }
    
    int prevTerm = args.prevLogIndex > 0 ? persistent_state_.logs[args.prevLogIndex - 1].term : 0;
    if (args.prevLogIndex > 0 && prevTerm != args.prevLogTerm) {
        // 冲突：找出该term的第一个日志
        reply.conflictTerm = prevTerm;
        int firstIndex = 1;
        for (int i = 1; i <= args.prevLogIndex; ++i) {
            if (persistent_state_.logs[i - 1].term == prevTerm) {
                firstIndex = i;
                break;
            }
        }
        reply.conflictIndex = firstIndex;
        return reply;
    }
    
    // 追加日志
    int startIdx = args.prevLogIndex;
    for (size_t i = 0; i < args.entries.size(); ++i) {
        int idx = startIdx + i + 1;
        if (idx <= static_cast<int>(persistent_state_.logs.size())) {
            // 如果已存在且term不同，删除后续日志
            if (persistent_state_.logs[idx - 1].term != args.entries[i]["term"].get<int>()) {
                persistent_state_.logs.resize(idx - 1);
                persistent_state_.logs.push_back(LogEntry::fromJson(args.entries[i]));
            }
        } else {
            persistent_state_.logs.push_back(LogEntry::fromJson(args.entries[i]));
        }
    }
    
    // 更新commitIndex
    if (args.leaderCommit > commit_index_) {
        commit_index_ = std::min(args.leaderCommit, static_cast<int>(persistent_state_.logs.size()));
        apply_committed_logs();
    }
    
    persist();
    reply.success = true;
    return reply;
}

// ==================== 日志复制 ====================
void RaftNode::replicate_logs(int peerId) {
    // 由子类实现
}

void RaftNode::advance_commit_index() {
    if (role_ != LEADER) return;
    
    int n = get_peer_count();
    for (int i = commit_index_ + 1; i <= static_cast<int>(persistent_state_.logs.size()); ++i) {
        int count = 1;  // 自己
        for (const auto& [peerId, matchIdx] : match_index_) {
            if (matchIdx >= i) count++;
        }
        
        if (count > n / 2 && persistent_state_.logs[i - 1].term == persistent_state_.currentTerm) {
            commit_index_ = i;
            apply_committed_logs();
        }
    }
}

void RaftNode::apply_committed_logs() {
    while (last_applied_ < commit_index_) {
        last_applied_++;
        const auto& entry = persistent_state_.logs[last_applied_ - 1];
        apply_command(entry.command);
    }
}

void RaftNode::apply_command(const json& cmd) {
    // 默认：只打印；子类（如 KV 存储）可重写为真正的状态机应用
    std::cout << "[N" << node_id_ << "] apply log: " << cmd.dump() << std::endl;
}

// ==================== 持久化 ====================
std::string RaftNode::get_persist_path() const {
    return "raft_" + std::to_string(node_id_) + ".json";
}

void RaftNode::persist() {
    json j = persistent_state_.toJson();
    std::ofstream file(get_persist_path());
    if (file.is_open()) {
        file << j.dump(4);
    }
}

bool RaftNode::load_persist() {
    std::ifstream file(get_persist_path());
    if (!file.is_open()) return false;
    
    try {
        json j;
        file >> j;
        persistent_state_ = PersistentState::fromJson(j);
        return true;
    } catch (const std::exception& e) {
        std::cerr << "加载持久化数据失败: " << e.what() << std::endl;
        return false;
    }
}