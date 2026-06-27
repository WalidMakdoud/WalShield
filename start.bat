@echo off
:: ============================================================
::  WalShield - Auto Launcher (Windows)
::  Starts: Backend (FastAPI) + Frontend (React) + Agents loop
:: ============================================================

title WalShield Launcher
color 0A

echo.
echo   ██╗    ██╗ █████╗ ██╗     ███████╗██╗  ██╗██╗███████╗██╗     ██████╗
echo   ██║    ██║██╔══██╗██║     ██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗
echo   ██║ █╗ ██║███████║██║     ███████╗███████║██║█████╗  ██║     ██║  ██║
echo   ██║███╗██║██╔══██║██║     ╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║
echo   ╚███╔███╔╝██║  ██║███████╗███████║██║  ██║██║███████╗███████╗██████╔╝
echo    ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝
echo.
echo   Network Security Monitoring Toolkit
echo   ==================================================
echo.

:: Create logs directory
if not exist logs mkdir logs

:: ── Activate virtual environment ──────────────────────────
if exist myenv\Scripts\activate.bat (
    echo [+] Activating virtual environment...
    call myenv\Scripts\activate.bat
) else if exist venv\Scripts\activate.bat (
    echo [+] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [!] No virtual environment found. Using system Python.
)

:: ── Start FastAPI Backend ──────────────────────────────────
echo [+] Starting FastAPI Backend...
start "WalShield Backend" /min cmd /c "cd BackEnd && uvicorn main:app --host 0.0.0.0 --port 8000 --reload > ..\logs\backend.log 2>&1"
timeout /t 2 /nobreak >nul
echo     Backend started ^> http://localhost:8000
echo     API Docs: http://localhost:8000/docs

:: ── Start React Frontend ───────────────────────────────────
echo [+] Starting React Frontend...
start "WalShield Frontend" /min cmd /c "cd frontend && npm run dev > ..\logs\frontend.log 2>&1"
timeout /t 3 /nobreak >nul
echo     Frontend started ^> http://localhost:5173

echo.
echo [+] Starting Security Agents loop (every 5 minutes)...
echo     Press Ctrl+C in this window to stop the agent loop.
echo     Use Task Manager to close Backend and Frontend windows.
echo ==================================================
echo.

:: ── Agent Loop ────────────────────────────────────────────
set /a RUN=1

:AGENT_LOOP
    echo [Run #%RUN%] %DATE% %TIME%

    echo   --^> ARP Scanner...
    python Agent\arp_scn.py >> logs\arp_scanner.log 2>&1
    echo       done.

    echo   --^> Port Scanner Detection...
    python Agent\port_scaner_detection.py >> logs\port_scanner.log 2>&1
    echo       done.

    echo   --^> DoS Detection...
    python Agent\Dos_Scanner.py >> logs\dos_scanner.log 2>&1
    echo       done.

    echo   --^> Deauth Detection...
    python Agent\Deauth_Scanner.py >> logs\deauth_scanner.log 2>&1
    echo       done.

    set /a RUN=%RUN%+1
    echo   [OK] All agents done. Waiting 5 minutes...
    echo.
    timeout /t 300 /nobreak
goto AGENT_LOOP
