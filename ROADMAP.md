# Hermes Glass — 實施路線圖

> 更新日期: 2026-06-08

## Phase 0: 項目初始化 ✅
- [x] 項目結構 + DESIGN.md + VISUAL.md + ROADMAP.md
- [x] package.json + AGENTS.md + .gitignore

## Phase 1: 視覺骨架 ✅
- [x] 7 套 CSS 變數主題
- [x] 毛玻璃三面板佈局
- [x] D3 記憶圖譜（力導向圖 + glow + 自然微抖）
- [x] 聊天界面 + Markdown + 斜杠命令
- [x] 思考流時間線

## Phase 2: Hermes 真實數據 ✅
- [x] SSE 流式對話（POST /api/chat/start + EventSource）
- [x] Session 列表/切換/新建/刪除
- [x] Token 用量面板
- [x] 上下文環

## Phase 3: 記憶系統 + 面板 ✅
- [x] SQLite 記憶圖譜（56 nodes / 53 links）
- [x] FTS5 記憶搜索（5239 條消息）
- [x] 焦點列表 + Token 用量
- [x] Cron 任務監控面板
- [x] 工作區檔案瀏覽
- [x] ACUI 動態卡片系統
- [x] 神經球 AI 狀態可視化
- [x] 語音輸入（Push-to-Talk + faster-whisper）
- [x] 中英雙語 i18n
- [x] PWA 支援
- [x] Kanban API

## Phase 4: 打磨 + 開源 ✅
- [x] 52/52 測試通過
- [x] README + LICENSE
- [x] Git repo 初始化
- [x] 記憶文件更新（Hermes MEMORY.md + Claude Code memory）
- [x] 文字可選取複製
- [x] 金色騎士馬頭 logo

## 可選後續
- [ ] Kanban 任務板 *(planned v0.2.0)*前端 UI
- [ ] Goals 目標追蹤 *(planned v0.2.0)*面板
- [ ] 手機端適配 *(planned v0.2.0)*優化
- [ ] Electron 桌面 *(planned v0.2.0)*打包
- [ ] 更多 ACUI 卡片類型
- [ ] 語音識別雲端 API 支援（OpenAI Whisper API）
