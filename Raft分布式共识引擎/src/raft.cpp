#include "raft.h"
#include <asio/read.hpp>
#include <asio/write.hpp>
#include <iostream>

using namespace std::chrono_literals;

// ==================== 构造函数 ====================
RaftNode::RaftNode(int nodeId, const std::vector<std::string>& peerAddrs)
    : nodeId_(nodeId), peerAddrs_(peerAddrs), rng_(std::random_device{}()),
      electionTimer_(ioContext_), heartbeatTimer_(ioContext_) {
    
    // 加载持久化状态
    if (!loadPersist()) {
        persistentState_.currentTerm = 0;
        persistentState_.votedFor = -1;
    }
    
    // 初始化Leader状态
    for (size_t i = 0; i < peerAddrs.size(); ++i) {
        if (i != nodeId) {
            nextIndex_[i] = persistentState_.logs.size() + 1;
            matchIndex_[i] = 0;
        }
    }
}

// ==================== 领导人选举 ====================
void RaftNode::becomeCandidate() {
    std::lock_guard<std::mutex> lock(stateMutex_);
    
    role_ = CANDIDATE;
    persistentState_.currentTerm++;
    persistentState_.votedFor = nodeId_;
    persist();
    
    voteCount_ = 1;  // 自己投自己
    std::cout << "[Node " << nodeId_ << "] 成为Candidate, Term=" << persistentState_.currentTerm << std::endl;
    
    // 并发发送RequestVote RPC
    for (auto& [peerId, addr] : peerAddrs_) {
        if (peerId == nodeId_) continue;
        
        // 异步发送投票请求
        sendRequestVote(peerId);
    }
    
    // 重置选举定时器（如果超时未当选，重新发起选举）
    resetElectionTimer();
}

void RaftNode::sendRequestVote(int peerId) {
    RequestVoteArgs args;
    args.term = persistentState_.currentTerm;
    args.candidateId = nodeId_;
    args.lastLogIndex = persistentState_.logs.size();
    args.lastLogTerm = persistentState_.logs.empty() ? 0 : persistentState_.logs.back().term;
    
    // 发送RPC并处理回复
    asio::post(ioContext_, [this, peerId, args]() {
        // 实际用TCP发送json序列化数据
        std::string msg = json(args).dump();
        
        // 异步接收回复
        // ... (网络IO代码)
        
        // 处理回复逻辑
        auto handleReply = [this, peerId](const RequestVoteReply& reply) {
            std::lock_guard<std::mutex> lock(stateMutex_);
            
            if (reply.term > persistentState_.currentTerm) {
                becomeFollower(reply.term);
                return;
            }
            
            if (role_ == CANDIDATE && reply.voteGranted) {
                voteCount_++;
                // 超过半数则成为Leader
                if (voteCount_ > (int)(peerAddrs_.size() / 2)) {
                    becomeLeader();
                }
            }
        };
    });
}

// ==================== 日志复制 ====================
void RaftNode::becomeLeader() {
    role_ = LEADER;
    std::cout << "[Node " << nodeId_ << "] 成为Leader, Term=" << persistentState_.currentTerm << std::endl;
    
    // 初始化nextIndex和matchIndex
    for (auto& [peerId, _] : peerAddrs_) {
        if (peerId == nodeId_) continue;
        nextIndex_[peerId] = persistentState_.logs.size() + 1;
        matchIndex_[peerId] = 0;
    }
    
    // 立即发送心跳
    sendHeartbeat();
}

void RaftNode::sendHeartbeat() {
    if (role_ != LEADER) return;
    
    for (auto& [peerId, _] : peerAddrs_) {
        if (peerId == nodeId_) continue;
        replicateLogs(peerId);
    }
    
    // 定时发送心跳 (50ms)
    heartbeatTimer_.expires_after(50ms);
    heartbeatTimer_.async_wait([this](asio::error_code ec) {
        if (!ec && role_ == LEADER) {
            sendHeartbeat();
        }
    });
}

void RaftNode::replicateLogs(int peerId) {
    AppendEntriesArgs args;
    args.term = persistentState_.currentTerm;
    args.leaderId = nodeId_;
    args.leaderCommit = commitIndex_;
    
    // 计算prevLogIndex和prevLogTerm
    int prevIndex = nextIndex_[peerId] - 1;
    args.prevLogIndex = prevIndex;
    args.prevLogTerm = (prevIndex <= 0) ? 0 : persistentState_.logs[prevIndex - 1].term;
    
    // 准备待复制的日志条目
    if (nextIndex_[peerId] <= (int)persistentState_.logs.size()) {
        for (int i = nextIndex_[peerId] - 1; i < (int)persistentState_.logs.size(); ++i) {
            args.entries.push_back(json(persistentState_.logs[i]));
        }
    }
    
    // 发送AppendEntries RPC
    // ... (实际发送代码)
    
    // 处理回复
    auto handleReply = [this, peerId](const AppendEntriesReply& reply) {
        std::lock_guard<std::mutex> lock(stateMutex_);
        
        if (reply.term > persistentState_.currentTerm) {
            becomeFollower(reply.term);
            return;
        }
        
        if (role_ == LEADER) {
            if (reply.success) {
                // 成功复制，更新matchIndex和nextIndex
                int newMatchIndex = args.prevLogIndex + args.entries.size();
                matchIndex_[peerId] = std::max(matchIndex_[peerId], newMatchIndex);
                nextIndex_[peerId] = matchIndex_[peerId] + 1;
                
                // 尝试推进commitIndex
                advanceCommitIndex();
            } else {
                // 失败回退（快速回退优化）
                if (reply.conflictTerm == -1) {
                    nextIndex_[peerId] = reply.conflictIndex;
                } else {
                    // 查找conflictTerm的最后出现位置
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
                replicateLogs(peerId);  // 重试
            }
        }
    };
}

// ==================== 推进commitIndex ====================
void RaftNode::advanceCommitIndex() {
    if (role_ != LEADER) return;
    
    // 找到N使得多数派matchIndex >= N
    std::vector<int> matchList;
    for (auto& [id, idx] : matchIndex_) {
        matchList.push_back(idx);
    }
    matchList.push_back(persistentState_.logs.size());  // 自己
    std::sort(matchList.begin(), matchList.end(), std::greater<int>());
    
    int majority = matchList[peerAddrs_.size() / 2];
    if (majority > commitIndex_) {
        // 确保该条目是当前Term的（保证安全性）
        if (persistentState_.logs[majority - 1].term == persistentState_.currentTerm) {
            commitIndex_ = majority;
            applyCommittedLogs();
        }
    }
}

// ==================== 网络分区恢复处理（关键） ====================
void RaftNode::becomeFollower(int newTerm) {
    role_ = FOLLOWER;
    persistentState_.currentTerm = newTerm;
    persistentState_.votedFor = -1;
    persist();
    
    std::cout << "[Node " << nodeId_ << "] 转为Follower, Term=" << newTerm << std::endl;
    resetElectionTimer();
}

// ==================== 持久化 ====================
void RaftNode::persist() {
    std::ofstream file("raft_" + std::to_string(nodeId_) + ".bin", std::ios::binary);
    json j = {
        {"term", persistentState_.currentTerm},
        {"votedFor", persistentState_.votedFor},
        {"logs", persistentState_.logs}
    };
    std::string data = j.dump();
    file.write(data.c_str(), data.size());
}

bool RaftNode::loadPersist() {
    std::ifstream file("raft_" + std::to_string(nodeId_) + ".bin", std::ios::binary);
    if (!file) return false;
    
    std::string data((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
    json j = json::parse(data);
    persistentState_.currentTerm = j["term"];
    persistentState_.votedFor = j["votedFor"];
    persistentState_.logs = j["logs"].get<std::vector<LogEntry>>();
    return true;
}

// ==================== 启动 ====================
void RaftNode::start() {
    ioThread_ = std::make_unique<std::thread>([this]() {
        ioContext_.run();
    });
    
    resetElectionTimer();
}

void RaftNode::resetElectionTimer() {
    // 随机150-300ms
    std::uniform_int_distribution<int> dist(150, 300);
    int timeoutMs = dist(rng_);
    
    electionTimer_.expires_after(std::chrono::milliseconds(timeoutMs));
    electionTimer_.async_wait([this](asio::error_code ec) {
        if (!ec) {
            std::lock_guard<std::mutex> lock(stateMutex_);
            if (role_ != LEADER) {
                becomeCandidate();
            }
        }
    });
}