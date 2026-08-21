@echo off
chcp 65001 >nul
echo ========================================
echo   启动 Raft 集群
echo ========================================

set EXE=build\raft_node.exe

if not exist %EXE% (
    echo [错误] 找不到 %EXE%!
    echo 请先编译: cmake --build build --config Release
    pause
    exit /b 1
)

set PEERS=127.0.0.1:9000,127.0.0.1:9001,127.0.0.1:9002

taskkill /F /IM raft_node.exe 2>nul

echo.
echo 启动节点 0 (命令端口 9100)...
start "Raft-Node-0" %EXE% --id=0 --peers=%PEERS% --cmd-port=9100

timeout /t 1 /nobreak >nul

echo 启动节点 1 (命令端口 9101)...
start "Raft-Node-1" %EXE% --id=1 --peers=%PEERS% --cmd-port=9101

timeout /t 1 /nobreak >nul

echo 启动节点 2 (命令端口 9102)...
start "Raft-Node-2" %EXE% --id=2 --peers=%PEERS% --cmd-port=9102

echo.
echo ========================================
echo 集群已启动!
echo ========================================
echo.
echo 测试命令:
echo   echo set test 42 ^| nc localhost 9100
echo   echo get test ^| nc localhost 9100
echo   echo status ^| nc localhost 9100
echo   echo dump ^| nc localhost 9100
echo.
pause