# ⚚ Hermes Glass

> AI 認知界面 — 為 Hermes Agent 打造的暗黑科技風 WebUI
> AI Cognitive Surface for Hermes Agent — Dark Tech WebUI

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="version">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
  <img src="https://img.shields.io/badge/tests-52%2F52-brightgreen" alt="tests">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey" alt="platform">
</p>

Hermes Glass 係一個持續運行嘅 AI Agent **認知界面**，靈感來自 [Bailongma](https://github.com/xiaoyuanda666-ship-it/BaiLongma) 嘅視覺設計語言，但完全為 **Hermes Agent** 原生打造。

你可以透過佢同 Hermes Agent 對話、監控 AI 思考過程、探索 D3 記憶圖譜、搜尋歷史對話、語音輸入 — 全部都係即時嘅。

---

## 📸 截圖

> 📸 請補充實際運行截圖或 GIF 放 `docs/screenshots/` 目錄
>
> 建議截圖內容：完整界面（7 套主題之一）、流式對話、記憶圖譜互動、神經球狀態變化、語音輸入中

---

## 🚀 快速開始

### 前提

| 需求 | 說明 |
|------|------|
| **Hermes Agent** | 已安裝並運行 → [安裝指南](https://hermes-agent.nousresearch.com/) |
| **Hermes WebUI** | [nesquena/hermes-webui](https://github.com/nesquena/hermes-webui) |
| Python | 3.10+ |
| 瀏覽器 | Chrome / Firefox / Edge |

### 一分鐘部署

```bash
# 1. Clone
git clone https://github.com/Smart75850/hermes-glass.git
cd hermes-glass

# 2. 部署到 Hermes WebUI 靜態目錄
cp -r index.html src/ styles/ manifest.json sw.js \
  /path/to/hermes-webui/static/native/

# 3. (可選) 記憶橋接 — 啟用記憶圖譜/搜索/Cron
pip install websockets
python memory_server.py &    # 端口 8791

# 4. (可選) 語音輸入 — 啟用 Push-to-Talk
pip install faster-whisper numpy
python stt_server_v3.py &    # 端口 8792

# 5. 打開瀏覽器
open http://127.0.0.1:8788/static/native/index.html
```

> 💡 **Mac 用戶**: 將路徑換成你嘅 hermes-webui 目錄，例如 `~/hermes-webui/static/native/`

---

## 🏗 架構

```
瀏覽器 (Hermes Glass UI)
    │
    ├── HTTP/SSE → Hermes WebUI (:8788) → Hermes Agent (:8642)
    ├── HTTP     → Memory Bridge (:8791) → SQLite (memory.db)
    └── WebSocket → STT Server (:8792)   → faster-whisper
```

| 服務 | 端口 | 必須？ | 用途 |
|------|:--:|:--:|------|
| Hermes WebUI | 8788 | ✅ 必須 | 聊天、Session、API 代理 |
| Memory Bridge | 8791 | ✅ 必須 | 記憶圖譜、FTS5 搜索、Cron、檔案 |
| STT Server | 8792 | 可選 | 語音輸入 (faster-whisper) |

---

## ✨ 功能

| 功能 | 說明 |
|------|------|
| 💬 **即時聊天** | SSE 流式對話 + Markdown 渲染 + 斜杠命令 |
| 🧠 **記憶圖譜** | D3 力導向圖，56 焦點節點 + 53 關聯，可拖拽/縮放 |
| 🎨 **7 套主題** | Midnight · Aurora · Forest · Crimson · Abyss · Arctic · Sand |
| ⚡ **AI 神經球** | 思考→橙黃旋轉、回覆→紫脈衝、錄音→紅閃、空閒→灰藍呼吸 |
| 🎤 **語音輸入** | 按住 Space Push-to-Talk，faster-whisper small 模型 |
| 🔍 **記憶搜索** | FTS5 全文搜索歷史消息 |
| 📊 **會話管理** | 建立/切換/刪除 Session · Token 用量 · 上下文環 |
| 🃏 **ACUI 卡片** | Agent 動態推送資訊卡片（Cron / Session 變化） |
| ⏰ **Cron 監控** | 定時任務狀態即時顯示 |
| 📁 **工作區瀏覽** | 最近檔案列表 |
| 🌐 **中英雙語** | 設定面板一鍵切換 |
| 📱 **PWA** | 可安裝到桌面/手機，離線可用 |

---

## ⌨️ 快捷鍵

| 快捷鍵 | 功能 |
|------|------|
| `Ctrl+S` | 打開設定 |
| `Ctrl+滾輪` | 縮放 UI |
| `按住 Space` | 語音輸入 |
| `輸入 /` | 斜杠命令選單 |
| `Enter` | 發送訊息 |

## 🔣 斜杠命令

| 命令 | 功能 |
|------|------|
| `/llm` | 設定 LLM 模型 |
| `/tts` | 設定語音合成 |
| `/theme` | 切換主題 |
| `/session` | 會話管理 |
| `/memory` | 記憶搜尋 |
| `/graph` | 切換背景圖譜 |
| `/help` | 顯示全部命令 |

---

## 🛠 技術棧

| 層級 | 技術 |
|------|------|
| 框架 | 原生 JS (ES Modules) · **零前端依賴** |
| 可視化 | D3.js v7 — 力導向記憶圖譜 |
| 樣式 | CSS Variables · 7 套主題 · Glassmorphism 面板 |
| 即時通訊 | SSE + WebSocket |
| 語音 | faster-whisper (CTranslate2) |
| 記憶 | SQLite + FTS5 (via Python bridge) |

---

## 🆚 對比官方 WebUI

Hermes Glass 唔係要取代官方 WebUI，而係補足佢冇嘅嘢：

| | 官方 WebUI | Hermes Glass |
|------|:--:|:--:|
| 聊天 + Session | ✅ | ✅ |
| 終端 + 檔案瀏覽 | ✅ | 部分 |
| Kanban + Goals | ✅ | API 就緒 |
| PWA + i18n | ✅ | ✅ |
| **D3 記憶圖譜** | ❌ | ✅ |
| **神經球 AI 狀態** | ❌ | ✅ |
| **7 套暗黑主題** | ❌ | ✅ |
| **語音輸入** | ❌ | ✅ |
| **FTS5 記憶搜索** | ❌ | ✅ |
| **ACUI 動態卡片** | ❌ | ✅ |

---

## 📂 項目結構

```
hermes-glass/
├── index.html          # 主頁面
├── src/                # JS 模組 (ES Modules)
├── styles/             # CSS 主題
├── docs/               # 文件 + 截圖
├── electron/           # Electron 桌面包裝 (計劃中)
├── manifest.json       # PWA manifest
├── sw.js               # Service Worker
├── DESIGN.md           # 設計文檔
├── VISUAL.md           # 視覺規範
├── ROADMAP.md          # 路線圖
├── CONTRIBUTING.md     # 貢獻指南
└── LICENSE             # MIT
```

---

## 🤝 貢獻

歡迎 PR！請參考 [CONTRIBUTING.md](CONTRIBUTING.md)。

**v1.0: 52/52 測試通過** ✅

## 🙏 致謝

- [Bailongma](https://github.com/xiaoyuanda666-ship-it/BaiLongma) — 視覺設計靈感
- [Hermes Agent](https://hermes-agent.nousresearch.com/) — AI 後端
- [Hermes WebUI](https://github.com/nesquena/hermes-webui) — 基礎設施
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — 語音識別
- [D3.js](https://d3js.org/) — 力導向圖

## 📄 License

MIT © 2026 輝 (Smart75850)
