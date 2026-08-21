cmake_minimum_required(VERSION 3.15)
project(Raft VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# 编译选项
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic -g -O2")
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4 /O2")
endif()

# 依赖管理：自动拉取独立版 ASIO 与 nlohmann/json（无需手动装 Boost）
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

# 源文件
file(GLOB_RECURSE RAFT_SOURCES "src/*.cpp")
list(REMOVE_ITEM RAFT_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/main.cpp")

add_executable(raft_node ${RAFT_SOURCES})

target_include_directories(raft_node PRIVATE include
    ${asio_SOURCE_DIR}/asio/include   # 独立版 ASIO 头文件
)

target_link_libraries(raft_node
    nlohmann_json::nlohmann_json
    Threads::Threads
    ws2_32   # Windows: ASIO 需要 Winsock
    mswsock  # Windows: AcceptEx
)

# 安装
install(TARGETS raft_node RUNTIME DESTINATION bin)

# 测试（如果存在 tests 目录）
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/tests)
    enable_testing()
    add_subdirectory(tests)
endif()
