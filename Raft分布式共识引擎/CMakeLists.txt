cmake_minimum_required(VERSION 3.14)
project(Raft)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 依赖库
find_package(Boost REQUIRED COMPONENTS system)
find_package(nlohmann_json REQUIRED)
find_package(Threads REQUIRED)

# 可执行文件（raft.cpp = RaftNode 核心；raft_v2.cpp = RPC 网络层 + main）
add_executable(raft_node
    src/raft.cpp
    src/raft_v2.cpp
)

target_link_libraries(raft_node
    Boost::system
    nlohmann_json::nlohmann_json
    Threads::Threads
    pthread
    ws2_32   # Windows: Boost.Asio 需要 Winsock
    mswsock  # Windows: AcceptEx
)

target_include_directories(raft_node PRIVATE include)