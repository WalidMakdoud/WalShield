#!/bin/bash

# ============================================================
#  WalShield - Auto Launcher
#  Starts: Backend (FastAPI) + Frontend (React) + Agents loop
# ============================================================

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# PID file to track processes
PID_FILE=".walshield_pids"
LOG_DIR="logs"
AGENT_INTERVAL=300  # 5 minutes in seconds

# Create logs directory
mkdir -p "$LOG_DIR"

echo -e "${CYAN}"
echo "  ██╗    ██╗ █████╗ ██╗     ███████╗██╗  ██╗██╗███████╗██╗     ██████╗ "
echo "  ██║    ██║██╔══██╗██║     ██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗"
echo "  ██║ █╗ ██║███████║██║     ███████╗███████║██║█████╗  ██║     ██║  ██║"
echo "  ██║███╗██║██╔══██║██║     ╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║"
echo "  ╚███╔███╔╝██║  ██║███████╗███████║██║  ██║██║███████╗███████╗██████╔╝"
echo "   ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝ "
echo -e "${NC}"
echo -e "${CYAN}   By Walid Makdoud"
echo -e "${GREEN}  Network Security Monitoring Toolkit${NC}"
echo "  =================================================="
echo ""

# ── Check if already running ──────────────────────────────
if [ -f "$PID_FILE" ]; then
    echo -e "${YELLOW}[!] WalShield appears to be already running.${NC}"
    echo -e "    Run ${RED}./stop.sh${NC} first, then try again."
    exit 1
fi

# ── Activate virtual environment if it exists ─────────────
if [ -d "myenv" ]; then
    echo -e "${GREEN}[+] Activating virtual environment...${NC}"
    source myenv/bin/activate
elif [ -d "venv" ]; then
    echo -e "${GREEN}[+] Activating virtual environment...${NC}"
    source venv/bin/activate
else
    echo -e "${YELLOW}[!] No virtual environment found. Using system Python.${NC}"
fi

# ── Start FastAPI Backend ─────────────────────────────────
echo -e "${GREEN}[+] Starting FastAPI Backend...${NC}"
cd BackEnd
uvicorn main:app --host 0.0.0.0 --port 8000 --reload > "../$LOG_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
cd ..

sleep 2

if kill -0 "$BACKEND_PID" 2>/dev/null; then
    echo -e "    ${GREEN}✔ Backend running${NC} (PID: $BACKEND_PID) → http://localhost:8000"
    echo -e "    ${CYAN}  API Docs: http://localhost:8000/docs${NC}"
else
    echo -e "    ${RED}✘ Backend failed to start. Check logs/$LOG_DIR/backend.log${NC}"
    exit 1
fi

# ── Start React Frontend ──────────────────────────────────
echo -e "${GREEN}[+] Starting React Frontend...${NC}"
cd frontend
npm run dev > "../$LOG_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
cd ..

sleep 3

if kill -0 "$FRONTEND_PID" 2>/dev/null; then
    echo -e "    ${GREEN}✔ Frontend running${NC} (PID: $FRONTEND_PID) → http://localhost:5173"
else
    echo -e "    ${RED}✘ Frontend failed to start. Check $LOG_DIR/frontend.log${NC}"
    kill "$BACKEND_PID" 2>/dev/null
    exit 1
fi

# ── Save PIDs ─────────────────────────────────────────────
echo "$BACKEND_PID" > "$PID_FILE"
echo "$FRONTEND_PID" >> "$PID_FILE"

echo ""
echo -e "${GREEN}[+] Starting Security Agents (every 5 minutes)...${NC}"
echo -e "    Agents: ARP Scanner | Port Scanner | DoS Detector | Deauth Detector"
echo ""
echo -e "${YELLOW}  Press Ctrl+C to stop all services.${NC}"
echo "  =================================================="
echo ""

# ── Trap Ctrl+C to clean up ───────────────────────────────
cleanup() {
    echo ""
    echo -e "${YELLOW}[!] Stopping WalShield...${NC}"
    kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null
    rm -f "$PID_FILE"
    echo -e "${GREEN}[✔] All services stopped. Goodbye!${NC}"
    exit 0
}
trap cleanup SIGINT SIGTERM

# ── Agent Loop (every 5 minutes) ─────────────────────────
RUN=1
while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${CYAN}[⚡] Run #$RUN — $TIMESTAMP${NC}"

    echo -e "  ${GREEN}→ ARP Scanner...${NC}"
    timeout 60 python Agent/arp_scn.py >> "$LOG_DIR/arp_scanner.log" 2>&1
    echo -e "    done."

    echo -e "  ${GREEN}→ Port Scanner Detection...${NC}"
    timeout 60 python Agent/port_scaner_detection.py >> "$LOG_DIR/port_scanner.log" 2>&1
    echo -e "    done."

    echo -e "  ${GREEN}→ DoS Detection...${NC}"
    timeout 60 python Agent/Dos_Scanner.py >> "$LOG_DIR/dos_scanner.log" 2>&1
    echo -e "    done."

    echo -e "  ${GREEN}→ Deauth Detection...${NC}"
    timeout 60 python Agent/Deauth_Scanner.py >> "$LOG_DIR/deauth_scanner.log" 2>&1
    echo -e "    done."

    echo -e "  ${CYAN}✔ All agents done. Next run in 5 minutes...${NC}"
    echo ""

    RUN=$((RUN + 1))
    sleep "$AGENT_INTERVAL"
done
