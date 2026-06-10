#!/bin/bash
# Hermes Mac — 一键启动所有服务
# 用法: bash start-all.sh

export DEEPSEEK_API_KEY="sk-REVOKED-2026-06-19"
export API_SERVER_KEY="hermes-mac-local-key-2026"
export GATEWAY_ALLOW_ALL_USERS="true"
export HERMES_WEBUI_PYTHON="$HOME/.local/pipx/venvs/hermes-agent/bin/python3"

echo "🚀 Hermes Mac 启动中..."

# 1. Gateway
kill $(pgrep -f "hermes gateway") 2>/dev/null
nohup hermes gateway run > /tmp/hermes-gateway.log 2>&1 &
echo "  ✅ Gateway (8642)"

# 2. Memory Bridge
kill $(pgrep -f "memory_server.py") 2>/dev/null
nohup python3 "$(dirname "$0")/memory_server.py" > /tmp/memory-bridge.log 2>&1 &
echo "  ✅ Memory Bridge (8791)"

# 3. WebUI
kill $(pgrep -f "hermes-webui/server.py\|bootstrap.py") 2>/dev/null
cd ~/workspace/hermes-webui && nohup bash start.sh 8788 > /tmp/hermes-webui.log 2>&1 &
echo "  ✅ WebUI + Hermes Glass (8788)"

sleep 5
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🌐 Hermes Glass: http://localhost:8788/static/native/index.html"
echo "  💬 Hermes CLI:   hermes chat"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
