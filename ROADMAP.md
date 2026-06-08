# Hermes Native UI — 实施路线图

> **总原则**: 视觉先行，数据后接。每一期做完都要「睇得」。
> **总工期**: Phase 1-4 约 10-14 日（单人）
> **每期交付物**: 可打开嘅 HTML 页面，视觉效果可见

---

## Phase 0: 项目初始化（而家）

**目标**: 项目骨架就绪

```
✅ 目录结构
✅ DESIGN.md
✅ VISUAL.md
✅ ROADMAP.md（本文件）
⬜ package.json
⬜ index.html（入口）
⬜ README.md
```

**检查点**: `index.html` 可以喺浏览器打开，显示 "Hermes Native UI"

---

## Phase 1: 视觉骨架 ⭐ 最核心

**目标**: 做到白龙马级别嘅视觉效果（mock 数据）

**工期**: 2-3 日

### 1.1 CSS 主题系统
- [ ] `styles/theme.css` — CSS 变量体系
  - Midnight (暗黑蓝) — 默认
  - Aurora (极光紫) — Hermes 品牌色
  - Forest (竹林绿)
- [ ] 主题切换按钮 + localStorage 持久化
- [ ] 所有颜色过渡动画 0.6s

### 1.2 布局系统
- [ ] `styles/layout.css` — 三面板布局
  - Session Sidebar (260px, 可折叠)
  - Chat View (flex: 1)
  - Info Panel (300px, 可折叠)
- [ ] 面板毛玻璃效果（半透明 + backdrop-filter）
- [ ] 多层渐变底色（冷光晕 + 暖光晕 + 深色渐变）
- [ ] 网格叠加层 (`.grid-overlay`)

### 1.3 D3 记忆图谱背景
- [ ] `src/memory-graph.js`
  - D3 力导向图（mock 数据 20-50 节点）
  - 6 种力配置
  - 节点随"年龄"渐暗
  - 节点 glow 滤镜
  - 滚轮缩放（自定义，中心点缩放）
  - 拖拽节点
  - hover tooltip
  - 自然微抖 (每 6s)
  - 图谱调节面板（引力/斥力/节点大小滑块）
- [ ] 图谱显示/隐藏开关

### 1.4 思考流组件
- [ ] `src/thought-stream.js`
  - 时间戳行
  - 思考中动画
  - 工具调用行（emoji + 名称 + 参数 + 结果状态）
  - 自动滚动
  - Mock 数据展示效果

### 1.5 聊天界面
- [ ] `src/chat.js`
  - 消息气泡（User / AI）
  - Markdown 渲染
  - 输入框 + 发送按钮
  - 自动收起/展开
  - Mock 对话数据
- [ ] 斜杠命令菜单骨架

### 1.6 细节打磨
- [ ] 全局 tooltip
- [ ] AI 状态指示器（彩色圆点 + 文字）
- [ ] 连接状态指示
- [ ] 节点统计（节点数/连线数/tok/s）
- [ ] 图例（核心/记忆/知识/衰减）
- [ ] 重置视图按钮

**Phase 1 交付物**: 
打开 `index.html` → 睇到完整嘅暗黑科技风界面 → 背景 D3 图谱在动 → 面板有毛玻璃 → 可以切换主题 → 聊天有 mock 对话 → 思考流有 mock 工具调用

---

## Phase 2: 接入 Hermes 数据

**目标**: 替换 mock 数据，连接真实 Hermes 后端

**工期**: 2-3 日

### 2.1 API 客户端
- [ ] `src/api.js` — HTTP 客户端
  - 端口指向 Hermes API (8642)
  - 统一错误处理
  - 请求/响应拦截

### 2.2 SSE 事件流
- [ ] `src/sse.js`
  - 连接 Hermes SSE endpoint
  - 事件路由分发
  - 断线重连

### 2.3 聊天对接到 Hermes
- [ ] 发送消息 → `POST /api/message`
- [ ] 接收流式 → SSE `stream.chunk`
- [ ] 工具调用显示 → SSE `tool.call`
- [ ] 消息定稿 → SSE `message.complete`
- [ ] 会话历史 → `GET /api/sessions/:id/messages`

### 2.4 Session 列表
- [ ] `src/sessions.js`
  - 会话列表 → `GET /api/sessions`
  - 新建会话
  - 切换会话
  - 会话标题（自动生成）

### 2.5 记忆列表
- [ ] `src/memory-list.js`
  - 记忆列表 → `GET /api/memories`
  - 搜索记忆
  - 删除记忆

### 2.6 记忆图谱接真实数据
- [ ] D3 图谱用 `GET /api/memories` 数据
- [ ] 新记忆自动新增节点
- [ ] 记忆召回高亮节点

### 2.7 设置面板
- [ ] `src/settings.js`
  - 对接 `GET /api/config`
  - LLM 模型配置
  - Provider 配置
  - 保存回 Hermes

**Phase 2 交付物**: 
全部数据来自真实 Hermes → 可以聊天 → Session 可切换 → 记忆图谱用真实记忆 → 设置可保存

---

## Phase 3: ACUI 卡片 + 多媒体

**目标**: 高级交互功能

**工期**: 3-4 日

### 3.1 ACUI 卡片系统
- [ ] `src/acui/client.js` — WebSocket 连接
- [ ] `src/acui/renderer.js` — 组件生命周期
- [ ] `src/acui/registry.js` — 组件注册
- [ ] `src/acui/animations.css` — 入场/退场动画

### 3.2 Hermes 专用卡片
- [ ] `status-card.js` — Agent 运行状态
- [ ] `goal-card.js` — Goals 目标进度
- [ ] `kanban-card.js` — Kanban 任务卡片
- [ ] `confirm-card.js` — 安全确认弹窗

### 3.3 语音面板
- [ ] `src/voice.js`
  - 3D 声波点云球（Canvas 2D）
  - 麦克风开关
  - 状态指示（idle/listening/recognizing）
  - 对接 Hermes STT/TTS

### 3.4 TTS 音效
- [ ] `src/tts-fx.js`
  - Web Audio API 音效处理
  - Jarvis 风格提示音
  - 播放/打断管理

### 3.5 工作区面板
- [ ] `src/workspace.js`
  - 文件列表 → `GET /api/workspace`
  - 文件预览

**Phase 3 交付物**: 
ACUI 卡片可推送 → 语音面板可用 → TTS 音效 → 工作区浏览

---

## Phase 4: Electron 打包 + 打磨

**目标**: 桌面端独立应用

**工期**: 2 日

### 4.1 Electron 打包
- [ ] `electron/main.cjs`
  - 窗口管理
  - 系统托盘
  - 开机启动
- [ ] `electron/preload.cjs`
- [ ] `package.json` build 配置
- [ ] 自动更新

### 4.2 最终打磨
- [ ] 性能优化（节点上限、碰撞简化）
- [ ] 响应式适配
- [ ] 中英双语 i18n
- [ ] 错误边界处理

**Phase 4 交付物**: 
`Hermes Native UI Setup.exe` 安装包 → 双击启动 → 自动连接 Hermes → 全部功能可用

---

## 里程碑总览

```
Phase 0  ██ 而家       项目初始化
Phase 1  ████████      ⭐ 视觉骨架（最重要）
         ↑ 做完呢步已经好靓
Phase 2  ████████      接入真实 Hermes 数据
         ↑ 可以有真实对话
Phase 3  ████████      ACUI 卡片 + 多媒体
         ↑ 完整功能
Phase 4  ████          Electron 桌面打包
         ↑ 发布安装包
```

---

## 依赖关系

```
Phase 0 ──→ Phase 1 ──→ Phase 2 ──→ Phase 3 ──→ Phase 4
               │            │            │
               │            │            └── ACUI 需要 WebSocket
               │            └── 需要 Hermes 运行中
               └── 无依赖，独立可做
```

---

## 关键技术风险

| 风险 | 影响 | 应对 |
|------|------|------|
| Hermes SSE 格式同预期不同 | Phase 2 延迟 | Phase 1 先用 mock，Phase 2 再适配真格式 |
| D3 力导向图性能 | 低配机卡顿 | 节点上限 120，碰撞降级，移动端隐藏 |
| WebSocket ACUI 后端唔支持 | Phase 3 做唔到 | 先用 HTTP polling 替代，后续加 WS |
| Electron 打包兼容性 | Phase 4 延迟 | 先用浏览器版，Electron 是锦上添花 |

---

## 每日进度追踪

| 日 | Phase | 任务 | 状态 |
|----|-------|------|:----:|
| 1 | 0-1 | 项目初始化 + CSS 主题 + 布局 | ⬜ |
| 2 | 1 | D3 记忆图谱 | ⬜ |
| 3 | 1 | 思考流 + 聊天界面 | ⬜ |
| 4 | 1 | 细节打磨 + Phase 1 验收 | ⬜ |
| 5 | 2 | API 客户端 + SSE 对接 | ⬜ |
| 6 | 2 | 聊天/Session 接入 | ⬜ |
| 7 | 2 | 记忆图谱 + 设置面板接入 | ⬜ |
| 8 | 3 | ACUI 卡片系统 | ⬜ |
| 9 | 3 | 语音面板 + TTS | ⬜ |
| 10 | 3 | 工作区面板 | ⬜ |
| 11 | 4 | Electron 打包 | ⬜ |
| 12 | 4 | 最终打磨 + 发布 | ⬜ |

---

> **下一步**: 开始 Phase 1，创建视觉骨架代码。
