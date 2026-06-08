# ⚚ Hermes Glass

> AI 認知界面 — 為 Hermes Agent 打造的暗黑科技風 WebUI

Hermes Glass 係一個持續運行嘅 AI Agent **認知界面**，靈感來自白龍馬

## 📸 Preview

> Screenshots coming soon. Run locally to see the full interface.

| Chat View | Memory Graph | Thought Stream |
|-----------|-------------|----------------|
| *coming soon* | *coming soon* | *coming soon* |

### Quick Demo
```bash
git clone https://github.com/Smart75850/hermes-glass.git
cd hermes-glass
# Open index.html or deploy to Hermes WebUI static/native/
```
 (Bailongma) 嘅視覺設計語言，但完全為 Hermes Agent 原生打造。

你可以透過佢同 Hermes Agent 對話、監控 AI 思考過程、探索記憶圖譜、搜尋歷史對話——全部都係即時嘅。

## 截圖

> 📸 截圖區 — 請補充實際運行截圖或 GIF
> 
> 建議截圖內容：
> - 完整界面（7 套主題之一）
> - 同 Hermes 對話中（展示流式回覆）
> - 記憶圖譜（D3 力導向圖 + 節點互動）
> - 神經球 AI 狀態變化
> - 語音輸入中
> 
> 截圖可放 `docs/screenshots/` 目錄


## Architecture

```
Browser (Hermes Glass UI)
    |
    +-- HTTP/SSE -> Hermes WebUI (:8788) -> Hermes Agent
    +-- HTTP      -> Memory Bridge (:8791) -> SQLite (memory.db)
    +-- WebSocket -> STT Server (:8792)    -> faster-whisper
```

## Tech Stack

| Layer | Tech |
|-------|------|
| Framework | Native JS (ES Modules) · Zero dependencies |
| Visualization | D3.js v7 — Force-directed memory graph |
| Styling | CSS Variables · 7 themes · Glassmorphism panels |
| Real-time | SSE + WebSocket |
| Voice | faster-whisper (CTranslate2) |
| Memory | SQLite + FTS5 |

## 功能

| 功能 | 說明 |
|------|------|
| 💬 **即時聊天** | SSE 流式對話 + Markdown 渲染 + 7 個斜杠命令 |
| 🧠 **記憶圖譜** | D3 力導向圖，56 個真實焦點節點 + 53 條關聯，可拖拽/縮放 |
| 🎨 **7 套主題** | Midnight · Aurora · Forest · Crimson · Abyss · Arctic · Sand |
| ⚡ **AI 神經球** | 思考→橙黃旋轉、回覆→紫脈衝、錄音→紅閃、空閒→灰藍呼吸 |
| 🎤 **語音輸入** | 按住 Space Push-to-Talk，faster-whisper small 模型 |
| 🔍 **記憶搜索** | FTS5 全文搜索 5000+ 條歷史消息 |
| 📊 **會話管理** | 建立/切換/刪除 Session · Token 用量 · 上下文環 |
| 🃏 **ACUI 卡片** | Agent 動態推送資訊卡片（Cron 狀態 / Session 變化） |
| ⏰ **Cron 監控** | 4 個定時任務狀態顯示 |
| 📁 **工作區瀏覽** | 最近檔案列表 |
| 🌐 **中英雙語** | 設定面板一鍵切換 |
| 📱 **PWA** | 可安裝到桌面/手機 |

## 安裝

### 前提

- **Hermes Agent** 已安裝並運行（`hermes-agent`）
- **Hermes WebUI** 已安裝並運行（[nesquena/hermes-webui](https://github.com/nesquena/hermes-webui)）
- Python 3.10+
- 瀏覽器（Chrome / Firefox / Edge）

### 快速開始

```bash
# 1. Clone 項目
git clone https://github.com/你的用戶名/hermes-glass.git
cd hermes-glass

# 2. 複製到 Hermes WebUI 靜態目錄
cp -r ./* /你的/hermes-webui/static/native/

# 3. 安裝 Python 依賴（記憶橋接 + 語音）
pip install faster-whisper websockets numpy
# 語音可選：唔裝 faster-whisper 就冇語音輸入功能

# 4. 啟動記憶橋接服務（端口 8791）
cd /你的/hermes-webui/
python memory_server.py &

# 5. 啟動語音服務（端口 8792，可選）
python stt_server_v3.py &

# 6. 打開瀏覽器
# 訪問 http://127.0.0.1:8788/static/native/index.html
```

### 服務架構

```
瀏覽器 (Hermes Glass UI)
    │
    ├── HTTP/SSE → Hermes WebUI (:8788) → Hermes Agent (:8642)
    ├── HTTP     → Memory Bridge (:8791) → SQLite (memory.db / state.db)
    └── WebSocket → STT Server (:8792)   → faster-whisper
```

### 設定

Hermes Glass 唔需要額外設定檔。佢自動連接以下服務：

| 服務 | 端口 | 需要 |
|------|:--:|------|
| Hermes WebUI | 8788 | **必須** |
| Memory Bridge | 8791 | **必須**（記憶圖譜/搜索/Cron/檔案） |
| STT Server | 8792 | 可選（語音輸入） |

## 技術棧

| 層級 | 技術 |
|------|------|
| 框架 | 原生 JS (ES Modules) · **零前端依賴** |
| 可視化 | D3.js v7 (CDN) |
| 樣式 | CSS 變數 · 7 套主題 |
| 即時 | SSE + WebSocket |
| 語音 | faster-whisper (CTranslate2) |
| 記憶 | SQLite + FTS5 (via Python bridge) |

## 鍵盤快捷鍵

| 快捷鍵 | 功能 |
|------|------|
| `Ctrl+S` | 打開設定 |
| `Ctrl+滾輪` | 縮放 UI |
| `按住 Space` | 語音輸入 |
| `輸入 /` | 斜杠命令選單 |
| `Enter` | 發送訊息 |

## 斜杠命令

| 命令 | 功能 |
|------|------|
| `/llm` | 設定 LLM 模型 |
| `/tts` | 設定語音合成 |
| `/theme` | 切換主題 |
| `/session` | 會話管理 |
| `/memory` | 記憶搜尋 |
| `/graph` | 切換背景圖譜 |
| `/help` | 顯示全部命令 |

## 對比官方 WebUI

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

## 貢獻

歡迎 PR！請參考 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 致謝

- [Bailongma](https://github.com/xiaoyuanda666-ship-it/BaiLongma) — 視覺設計靈感
- [Hermes Agent](https://hermes-agent.nousresearch.com/) — AI 後端
- [Hermes WebUI](https://github.com/nesquena/hermes-webui) — 基礎設施
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — 語音識別
- [D3.js](https://d3js.org/) — 力導向圖

## License

MIT
