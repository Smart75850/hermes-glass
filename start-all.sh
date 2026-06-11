#!/bin/bash
# Hermes Mac — 一键启动所有服务
# 用法: bash ~/workspace/hermes-glass/start-all.sh
# 开机自动运行: 已配置 launchd → ~/Library/LaunchAgents/com.hermes.mac.plist

export DEEPSEEK_API_KEY="sk-REVOKED-2026-06-19"
export API_SERVER_KEY="hermes-mac-local-key-2026"
export GATEWAY_ALLOW_ALL_USERS="true"
export HERMES_WEBUI_PYTHON="$HOME/.local/pipx/venvs/hermes-agent/bin/python3"
export HTTP_PROXY="http://127.0.0.1:7897"
export HTTPS_PROXY="http://127.0.0.1:7897"

echo "🚀 Hermes Mac 启动中..."

# 1. Gateway
kill $(pgrep -f "hermes gateway") 2>/dev/null
sleep 1
nohup hermes gateway run > /tmp/hermes-gateway.log 2>&1 &
echo "  ✅ Gateway (:8642)"

# 2. Memory Bridge
kill $(pgrep -f "memory_server.py") 2>/dev/null
sleep 1
nohup python3 "$HOME/workspace/hermes-glass/memory_server.py" > /tmp/memory-bridge.log 2>&1 &
echo "  ✅ Memory Bridge (:8791)"

# 3. WebUI + Hermes Glass
kill $(pgrep -f "hermes-webui/server.py\|bootstrap.py") 2>/dev/null
sleep 1
cd "$HOME/workspace/hermes-webui" && nohup bash start.sh 8793 > /tmp/hermes-webui.log 2>&1 &
echo "  ✅ WebUI + Hermes Glass (:8793)"

sleep 5
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🌐 Hermes Glass: http://127.0.0.1:8793/static/hg/index.html"
echo "  💬 Hermes CLI:   hermes chat"
echo "  🧠 Ollama:       http://127.0.0.1:11434"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
