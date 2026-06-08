# Contributing to Hermes Glass

歡迎貢獻！Hermes Glass 係一個原生 JS WebUI 項目，冇前端框架依賴。

## 開發環境

```bash
git clone https://github.com/你的用戶名/hermes-glass.git
cd hermes-glass
# 部署到 Hermes WebUI 靜態目錄
cp -r ./* /你的/hermes-webui/static/native/
# 打開 http://127.0.0.1:8788/static/native/index.html
```

## 項目結構

```
src/
├── app.js          # 主應用
├── api.js          # Hermes API 客戶端
├── sse.js          # SSE 事件處理
├── voice.js        # 語音面板 + 神經球
├── i18n.js         # 中英雙語
└── acui/
    ├── renderer.js # ACUI 卡片系統
    └── animations.css
styles/
├── theme.css       # 7 套主題 CSS 變數
├── layout.css      # 佈局系統
└── animations.css  # 全局動畫
```

## 代碼風格

- 原生 JS (ES Modules)，唔加前端框架
- CSS 變數 (`var(--xxx)`) 做主題，唔 hardcode 顏色
- 新功能用 `t('key')` 做 i18n（zh + en 都要加）
- 保持單文件唔超過 ~60KB，太大就拆模組

## 加新主題

1. 喺 `styles/theme.css` 加 `[data-theme="xxx"]` 區塊
2. 喺 `index.html` 設定面板加 `.theme-dot`
3. 喺 `src/app.js` 嘅 `SLASH_COMMANDS` themes 列表加名

## 加新 API

1. `src/api.js` 加 endpoint method
2. `memory_server.py` 加 handler（如果需要新數據源）

## PR 檢查清單

- [ ] 中英文 i18n 都加咗
- [ ] 冇 hardcode 個人路徑
- [ ] 7 套主題都正常顯示
- [ ] 冇引入前端框架依賴
