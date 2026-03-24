#!/usr/bin/env bash
# run.sh — Run every time to start the app
set -e

CYAN='\033[0;36m'; GREEN='\033[0;32m'; NC='\033[0m'
info() { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()   { echo -e "${GREEN}[OK]${NC}    $*"; }

# Read PORT from .env
PORT=8501
[ -f .env ] && PORT=$(grep '^PORT' .env | cut -d'=' -f2 | tr -d ' ')

# Start Ollama if not running
if pgrep -x "ollama" &>/dev/null; then
    ok "Ollama already running."
else
    info "Starting Ollama daemon..."
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
    ok "Ollama started."
fi

echo -e "\n${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}   🦙  App running at: http://localhost:${PORT}       ${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

streamlit run app.py \
    --server.port "$PORT" \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false
