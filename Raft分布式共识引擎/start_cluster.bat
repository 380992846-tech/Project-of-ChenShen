@echo off
rem ============================================
rem  Start 3-node Raft cluster
rem  (ASCII-only on purpose: cmd.exe parses .bat
rem   with GBK codepage, UTF-8 Chinese would garble
rem   the commands. Keep this file pure ASCII.)
rem ============================================

set EXE=build\raft_node.exe

if not exist %EXE% (
    echo [ERROR] %EXE% not found.
    echo Build first: cmake --build build
    pause
    exit /b 1
)

rem All 3 node addresses (INCLUDING self), indexed by node id.
rem NOTE: use a FRESH port range so leftover/zombie raft_node.exe
rem processes (still on 9000-9002 with huge terms) cannot interfere.
set PEERS=127.0.0.1:8100,127.0.0.1:8101,127.0.0.1:8102

rem Kill any leftover raft_node.exe
taskkill /F /IM raft_node.exe >nul 2>&1

echo.
echo Starting Node 0 ...
start "Raft-Node-0" %EXE% --id=0 --peers=%PEERS%

timeout /t 1 /nobreak >nul

echo Starting Node 1 ...
start "Raft-Node-1" %EXE% --id=1 --peers=%PEERS%

timeout /t 1 /nobreak >nul

echo Starting Node 2 ...
start "Raft-Node-2" %EXE% --id=2 --peers=%PEERS%

echo.
echo ============================================
echo  Cluster started (3 nodes on ports 8100-8102)
echo  Wait ~15s, then check each window for "Leader".
echo ============================================
echo.
pause
