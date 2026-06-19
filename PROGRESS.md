# Hermes Glass 进度追踪

> ⚠️ AI Agent 每新会话第一件事：读此文件

## ✅ 已完成

- 2026-06-10 Harness 工程方案制定
- **2026-06-14 🔒 安全审计 & 后台烧钱修复**
  - 根因: auto_decompose + cron job + auxiliary 后台持续调用 DeepSeek API，余额烧至 ¥9.78
  - 源码: api.js 默认模型 pro→flash, 硬编码路径→localStorage
  - 源码: app.js polling 5min→15min + Page Visibility API
  - 脚本: start-all.sh 移除硬编码 key, 从 .env 读取
  - 配置: config.yaml 安全锁全部到位
  - 环境: aiohttp/pyyaml/cryptography 已安装, 官方 WebUI 正常运行

- **2026-06-14 🔗 与 Hermes Agent 设割**
  - Hermes Glass 改为纯前端 Memory Bridge 项目，不再自动启动 Gateway
  - 官方 WebUI (`~/workspace/hermes-webui/`) 独立启动: `bash start.sh`
  - Gateway 手动启动: `hermes gateway run` (安全锁已生效)

## 🔄 进行中

<!-- 当前正在做的任务 -->

## 📋 待办

<!-- 下一步 -->

## ⚠️ 已知问题

- 原生 JS (ES Modules) + D3.js + faster-whisper + SQLite
- 官方 WebUI Chat 功能需要 Gateway 运行 (手动启动, 安全模式)

## 🔒 安全守则 (2026-06-14)

- ❌ 不可启用 kanban.auto_decompose
- ❌ 不可添加 cron job 而 cron_mode=deny
- ❌ 不可在 auxiliary 中设 provider=auto
- ❌ 不可硬编码 API key
- ✅ 启动前确认 config.yaml 安全锁已到位
