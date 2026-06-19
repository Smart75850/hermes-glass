#!/bin/bash
# Hermes Glass — 纯前端 Memory Bridge 启动脚本
# 已与 Hermes Agent 设割, 不再自动启动 Gateway
#
# ⚠️ 架构说明:
#   - 呢个脚本只启动 Memory Bridge (纯本地 SQLite 读取, 不烧 API)
#   - 官方 WebUI 请另外用: bash ~/workspace/hermes-webui/start.sh
#   - Gateway 请手动启动: hermes gateway run (会烧 API, 谨慎使用)
#
# 用法: bash ~/workspace/hermes-glass/start-all.sh

set -e

echo "🧠 Hermes Glass — Memory Bridge (纯本地, 不烧 API)"

# Memory Bridge (纯本地, 读 SQLite, 零 API 调用)
kill $(pgrep -f "memory_server.py") 2>/dev/null || true
sleep 1
nohup python3 "$HOME/workspace/hermes-glass/memory_server.py" > /tmp/memory-bridge.log 2>&1 &
echo "  ✅ Memory Bridge → http://127.0.0.1:8791"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🧠 Memory Bridge: http://127.0.0.1:8791"
echo ""
echo "  要启动官方 WebUI? → bash ~/workspace/hermes-webui/start.sh"
echo "  要用 Hermes Chat? → hermes chat"
echo "  要启动 Gateway?  → hermes gateway run  ⚠️ 会烧 API"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
