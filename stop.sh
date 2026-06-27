#!/bin/bash

# ============================================================
#  WalShield - Stop Script
# ============================================================

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PID_FILE=".walshield_pids"

echo -e "${YELLOW}[!] Stopping WalShield...${NC}"

if [ ! -f "$PID_FILE" ]; then
    echo -e "${RED}[!] No PID file found. WalShield may not be running.${NC}"
    echo -e "    Trying to kill by port anyway..."
    fuser -k 8000/tcp 2>/dev/null && echo -e "  ${GREEN}✔ Killed process on port 8000 (Backend)${NC}"
    fuser -k 5173/tcp 2>/dev/null && echo -e "  ${GREEN}✔ Killed process on port 5173 (Frontend)${NC}"
    exit 0
fi

while read -r PID; do
    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID"
        echo -e "  ${GREEN}✔ Stopped process PID $PID${NC}"
    else
        echo -e "  ${YELLOW}  PID $PID already stopped.${NC}"
    fi
done < "$PID_FILE"

rm -f "$PID_FILE"

# Kill any leftover uvicorn / vite processes
pkill -f "uvicorn main:app" 2>/dev/null
pkill -f "vite" 2>/dev/null

echo -e "${GREEN}[✔] WalShield stopped successfully.${NC}"
