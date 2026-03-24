#!/usr/bin/env bash
# setup.sh — Run ONCE on first use
set -e

CYAN='\033[0;36m'; GREEN='\033[0;32m'; NC='\033[0m'
info() { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()   { echo -e "${GREEN}[OK]${NC}    $*"; }

echo -e "\n${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}   🦙  LLaMA 3 Local AI — One-Shot Setup           ${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# Read model name from .env
MODEL_NAME="llama3"
[ -f .env ] && MODEL_NAME=$(grep '^MODEL_NAME' .env | cut -d'=' -f2 | tr -d ' ')

# 1. Install Ollama
if command -v ollama &>/dev/null; then
    ok "Ollama already installed."
else
    info "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    ok "Ollama installed."
fi

# 2. Start Ollama daemon
if pgrep -x "ollama" &>/dev/null; then
    ok "Ollama already running."
else
    info "Starting Ollama daemon..."
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
    ok "Ollama started."
fi

# 3. Pull model
if ollama list 2>/dev/null | grep -q "$MODEL_NAME"; then
    ok "${MODEL_NAME} already pulled."
else
    info "Pulling ${MODEL_NAME} (~4.7 GB)..."
    ollama pull "$MODEL_NAME"
    ok "${MODEL_NAME} ready."
fi

# 4. Python deps
info "Installing Python packages..."
pip install -r requirements.txt -q
ok "Packages installed."

echo -e "\n${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}   ✅  Done! Now run:  bash run.sh                 ${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
