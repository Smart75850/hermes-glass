# ⚚ Hermes Glass

> AI 認知界面 — 為 Hermes Agent 打造的暗黑科技風 WebUI

Hermes Glass 係一個持續運行嘅 AI Agent **認知界面**。你可以透過佢同 Hermes Agent 對話、監控 AI 思考過程、探索記憶圖譜、搜尋歷史對話——全部都係即時嘅。

靈感來自白龍馬 (Bailongma) 嘅視覺設計語言，但完全為 Hermes 原生打造。

## 功能

| 功能 | 說明 |
|------|------|
| 💬 **即時聊天** | SSE 流式對話 + Markdown 渲染 + 斜杠命令 |
| 🧠 **記憶圖譜** | D3 力導向圖，56 個真實焦點節點 + 53 條關聯 |
| 🎨 **7 套主題** | Midnight · Aurora · Forest · Crimson · Abyss · Arctic · Sand |
| 🎤 **語音輸入** | 按住 Space 講嘢，放手出字（faster-whisper small） |
| 🔍 **記憶搜索** | FTS5 全文搜索 5239 條歷史消息 |
| 📊 **會話管理** | 建立/切換/刪除 Session · Token 用量統計 |
| ⚡ **AI 狀態球** | 神經節點網，思考/回覆/工具時變色變速 |
| 🃏 **ACUI 卡片** | Agent 推送嘅動態資訊卡片 |
| ⏰ **Cron 監控** | 定時任務狀態追蹤 |

## 架構

```
瀏覽器 (Hermes Glass UI)
    │
    ├── HTTP/SSE → Hermes WebUI (:8788) → Hermes Agent (:8642)
    ├── HTTP     → Memory Bridge (:8791) → SQLite (memory.db / state.db)
    └── WebSocket → STT Server (:8792)   → faster-whisper
```

## 快速開始

### 前提

- Hermes Agent 已安裝並運行
- Python 3.10+
- 瀏覽器（Chrome/Firefox/Edge）

### 啟動

```bash
# 1. 確保 Hermes WebUI 在運行
# http://127.0.0.1:8788

# 2. 啟動 Memory Bridge
cd hermes-webui
python memory_server.py &

# 3. 啟動語音服務（可選）
python stt_server_v3.py &

# 4. 打開 UI
# 訪問 http://127.0.0.1:8788/static/native/index.html
```

## 技術棧

| 層級 | 技術 |
|------|------|
| 框架 | 原生 JS (ES Modules) · 零依賴 |
| 可視化 | D3.js v7 — 力導向圖 |
| 樣式 | CSS 變數驅動 · 7 套主題 |
| 即時 | SSE + WebSocket |
| 語音 | faster-whisper (CTranslate2) |
| 記憶 | SQLite + FTS5 |

## 主題預覽

| Midnight | Aurora | Forest | Crimson | Abyss | Arctic | Sand |
|:--------:|:------:|:------:|:-------:|:-----:|:------:|:----:|
| 暗黑藍 | 極光紫 | 螢光綠 | 暗紅 | 深海藍 | 極地白 | 暖沙 |

## 鍵盤快捷鍵

| 快捷鍵 | 功能 |
|------|------|
| `Ctrl+S` | 打開設定 |
| `Ctrl+滾輪` | 縮放 UI |
| `按住 Space` | 語音輸入 |
| 輸入框 `/` | 斜杠命令選單 |
| `Enter` | 發送訊息 |

## 斜杠命令

| 命令 | 功能 |
|------|------|
| `/llm` | 設定 LLM 模型 |
| `/tts` | 設定語音合成 |
| `/theme` | 切換主題 |
| `/session` | 會話管理 |
| `/memory` | 記憶搜尋 |
| `/graph` | 切換記憶圖譜 |
| `/help` | 顯示全部命令 |

## 致謝

- [Bailongma](https://github.com/xiaoyuanda666-ship-it/BaiLongma) — 視覺設計靈感來源
- [Hermes Agent](https://hermes-agent.nousresearch.com/) — AI 後端
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — 語音識別
- [D3.js](https://d3js.org/) — 力導向圖

## License

MIT
