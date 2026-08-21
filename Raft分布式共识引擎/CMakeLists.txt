cmake_minimum_required(VERSION 3.15)
project(Raft VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# 编译选项
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Release")
endif()

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic")
    set(CMAKE_CXX_FLAGS_RELEASE "-O2 -DNDEBUG")
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4")
    set(CMAKE_CXX_FLAGS_RELEASE "/O2")
endif()

# 依赖：自动拉取独立版 ASIO + nlohmann/json
include(FetchContent)

FetchContent_Declare(
    asio
    GIT_REPOSITORY https://github.com/chriskohlhoff/asio.git
    GIT_TAG        asio-1-30-2
)
FetchContent_MakeAvailable(asio)

FetchContent_Declare(
    json
    URL https://github.com/nlohmann/json/releases/download/v3.11.3/json.tar.xz
)
FetchContent_MakeAvailable(json)

find_package(Threads REQUIRED)

# 源文件：raft.cpp(V4.0: RPC + RaftNodeWithRPC + main) + raft_node.cpp(基类实现)
set(RAFT_SOURCES
    src/raft.cpp
    src/raft_node.cpp
)

add_executable(raft_node ${RAFT_SOURCES})

target_include_directories(raft_node PRIVATE
    include
    ${asio_SOURCE_DIR}/asio/include
    ${json_SOURCE_DIR}/include
)

target_compile_definitions(raft_node PRIVATE
    ASIO_STANDALONE
    ASIO_NO_DEPRECATED
    _WIN32_WINNT=0x0A00
)

target_link_libraries(raft_node
    nlohmann_json::nlohmann_json
    Threads::Threads
)

if(WIN32)
    target_link_libraries(raft_node ws2_32 mswsock)
else()
    find_library(RT_LIB rt)
    if(RT_LIB)
        target_link_libraries(raft_node ${RT_LIB})
    endif()
    target_link_libraries(raft_node pthread)
endif()

install(TARGETS raft_node RUNTIME DESTINATION bin)

message(STATUS "Raft V4.0 配置完成: ${RAFT_SOURCES}")
