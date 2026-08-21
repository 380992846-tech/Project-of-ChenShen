cmake_minimum_required(VERSION 3.14)
project(Raft)

set(CMAKE_CXX_STANDARD 17)

find_package(Boost REQUIRED COMPONENTS asio)
find_package(nlohmann_json REQUIRED)

add_executable(raft_node
    src/raft.cpp
    src/rpc.cpp
    src/persistence.cpp
)

target_link_libraries(raft_node
    Boost::asio
    nlohmann_json::nlohmann_json
    pthread
)