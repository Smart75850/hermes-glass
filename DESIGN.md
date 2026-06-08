# Hermes Native UI — 架构设计文档

> **目标**: 为 Hermes Agent 打造一个**视觉震撼、技术可控**的原生 WebUI
> **参考**: 白龙马 (Bailongma) 的视觉设计语言，但数据结构对 Hermes 原生
> **原则**: 视觉先行，数据后接。无框架，纯原生 JS + Web Components。

---

## 一、项目定位

```
白龙马 UI = 教材（学佢嘅设计思路，唔抄佢嘅代码）
Hermes Native UI = 作品（为 Hermes 量身打造，技术完全可控）

关系：
  白龙马 → 启发 → Hermes Native UI
  唔係 fork、唔係移植、唔係适配
  而係「同一个视觉层次，完全唔同嘅实现」
```

---

## 二、整体架构

```
┌──────────────────────────────────────────────────────────┐
│                    浏览器 / Electron                      │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │                  Hermes Native UI                   │  │
│  │                                                    │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────────────┐    │  │
│  │  │ Session  │  │  Chat   │  │  Memory Graph   │    │  │
│  │  │  List    │  │  View   │  │  (D3 Force)     │    │  │
│  │  │          │  │         │  │                 │    │  │
│  │  │ 会话列表  │  │ 聊天+   │  │  背景记忆图谱    │    │  │
│  │  │          │  │ 思考流   │  │                 │    │  │
│  │  └─────────┘  └─────────┘  └─────────────────┘    │  │
│  │                                                    │  │
│  │  ┌──────────────────────────────────────────────┐  │  │
│  │  │              Composer Bar                     │  │  │
│  │  │  [上下文环] [消息输入........................] [发送] │  │  │
│  │  │  [模型] [Profile] [设置] [工作区]              │  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  │                                                    │  │
│  │  ┌──────────────────────┐  ┌──────────────────┐   │  │
│  │  │  ACUI Host           │  │  Modal Overlay    │   │  │
│  │  │  (Agent 推送卡片)    │  │  (设置/面板/确认)  │   │  │
│  │  └──────────────────────┘  └──────────────────┘   │  │
│  └────────────────────────────────────────────────────┘  │
│                          │                               │
│          SSE /events     │  REST /api/*                  │
│          WebSocket /ws   │                               │
│                          ▼                               │
│  ┌────────────────────────────────────────────────────┐  │
│  │                Hermes Agent Backend                 │  │
│  │  Gateway :8642  │  API Server :8642                 │  │
│  │  memory.db  │  state.db  │  streaming.py            │  │
│  │  toolsets  │  sessions  │  platforms                │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

---

## 三、组件树

```
<App>
├── <MemoryGraph />           # D3 力导向图背景 (z-index: 1)
├── <MainLayout>              # 主布局 (z-index: 2)
│   ├── <SessionSidebar />    # 左栏：会话列表
│   ├── <ChatView>            # 中栏：聊天 + 思考流
│   │   ├── <ChatMessages />  #   消息列表（自动收起/展开）
│   │   ├── <ThoughtStream /> #   思考流时间线（L1:用户触发）
│   │   └── <Composer />      #   输入栏 + 上下文环
│   └── <InfoPanel />         # 右栏：状态/记忆/文件
│       ├── <AgentStatus />   #   运行状态
│       ├── <MemoryList />    #   记忆列表
│       └── <WorkspaceQuick />#   工作区快速浏览
├── <ACUIHost />              # ACUI 卡片宿主
├── <SettingsModal />         # 设置弹窗
├── <VoicePanel />            # 语音面板
├── <ThemeSwitcher />         # 主题切换
└── <Tooltip />               # 全局 tooltip
```

---

## 四、数据流

### 4.1 SSE 事件流（单向：后端 → 前端）

```
Hermes streaming.py → SSE /events → 前端 handle(e)
                                       │
    ┌──────────────┬──────────────┬────┴────┬──────────────┐
    ▼              ▼              ▼         ▼              ▼
ChatView      ThoughtStream   AgentStatus  MemoryGraph   ACUIHost
(消息气泡)     (工具时间线)    (状态更新)   (节点更新)    (卡片)
```

**SSE 事件设计（兼容 Hermes streaming 格式）**：

| 事件类型 | 来源 | 触发 |
|----------|------|------|
| `session.start` | gateway | 新会话开始 |
| `stream.chunk` | LLM | 逐 token 流式输出 |
| `stream.end` | LLM | 流式段落结束 |
| `tool.call` | executor | 工具调用（名称+参数+结果） |
| `tool.error` | executor | 工具执行失败 |
| `message.complete` | gateway | 完整回复定稿 |
| `memory.written` | memory | 新记忆写入 |
| `memory.recalled` | memory | 记忆召回 |
| `focus.change` | context | 上下文焦点变化 |
| `agent.status` | gateway | Agent 运行状态 |
| `session.title` | gateway | 会话标题更新 |

### 4.2 REST API（双向）

| 端点 | 方法 | 用途 |
|------|------|------|
| `/api/sessions` | GET | 会话列表 |
| `/api/sessions/:id` | GET | 单个会话详情 |
| `/api/sessions/:id/messages` | GET | 会话消息历史 |
| `/api/message` | POST | 发送消息 |
| `/api/memories` | GET | 记忆列表/搜索 |
| `/api/memories/:id` | PATCH/DELETE | 修改/删除记忆 |
| `/api/config` | GET | 当前配置摘要 |
| `/api/status` | GET | Agent 运行状态 |
| `/api/workspace` | GET | 工作区文件列表 |

### 4.3 WebSocket（双向：ACUI 卡片）

```
Agent → WebSocket → ACUI Client → Renderer → Web Component → DOM
                                              ↓
                                        signal (用户交互)
```

---

## 五、技术选型

| 层级 | 技术 | 原因 |
|------|------|------|
| 框架 | **原生 JS (ES Modules)** | 零依赖，技术可控，同 Hermes CLI 一致 |
| 可视化 | **D3.js v7** | 力导向图是核心视觉，D3 最成熟 |
| 样式 | **CSS 变量 + CSS Animations** | 多主题驱动，无预处理器 |
| 组件 | **Web Components (Custom Elements)** | ACUI 卡片系统需要 |
| 实时 | **SSE (EventSource)** + **WebSocket** | 双通道，各司其职 |
| 打包 | **Electron 33** (可选) | 桌面端独立窗口 |
| 字体 | **Inter + JetBrains Mono** | 同白龙马，科技感强 |

---

## 六、文件结构

```
hermes-native-ui/
├── index.html                  # 入口
├── package.json                # 项目配置 (Electron 可选)
├── README.md                   # 项目说明
├── DESIGN.md                   # 本文件：架构设计
├── VISUAL.md                   # 视觉设计系统
├── ROADMAP.md                  # 实施路线图
│
├── src/
│   ├── app.js                  # 🎯 主应用入口（init + bootstrap）
│   ├── api.js                  # Hermes API 客户端
│   ├── sse.js                  # SSE 事件处理器
│   ├── chat.js                 # 聊天系统（消息+流式+斜杠命令）
│   ├── thought-stream.js       # 思考流时间线组件
│   ├── memory-graph.js         # D3 记忆图谱背景
│   ├── memory-list.js          # 记忆列表面板
│   ├── sessions.js             # Session 侧栏
│   ├── composer.js             # 输入栏 + 上下文环
│   ├── settings.js             # 设置面板
│   ├── workspace.js            # 工作区文件浏览
│   ├── markdown.js             # Markdown 渲染
│   ├── voice.js                # 语音面板（点云球）
│   ├── tts-fx.js              # TTS 音效（Web Audio）
│   ├── theme.js                # 主题管理器
│   │
│   └── acui/                   # ACUI 动态卡片系统
│       ├── client.js           # WebSocket 连接
│       ├── renderer.js         # 组件生命周期管理
│       ├── registry.js         # 组件注册表
│       ├── animations.css      # 入场/退场动画
│       └── components/         # Hermes 专用卡片
│           ├── status-card.js      # Agent 状态卡片
│           ├── goal-card.js        # 目标进度卡片
│           ├── kanban-card.js      # Kanban 任务卡片
│           └── confirm-card.js     # 安全确认弹窗
│
├── styles/
│   ├── theme.css               # CSS 变量体系（3-5 套主题）
│   ├── layout.css              # 布局系统
│   ├── components.css          # 组件样式
│   ├── chat.css                # 聊天样式
│   ├── graph.css               # 图谱样式
│   └── animations.css          # 全局动画
│
├── electron/
│   ├── main.cjs                # Electron 主进程
│   └── preload.cjs             # 预加载脚本
│
└── docs/
    ├── screenshots/            # 截图
    └── comparison.md           # 同白龙马对比分析
```

---

## 七、同白龙马嘅关键差异

| 维度 | 白龙马 | Hermes Native UI |
|------|--------|-----------------|
| **后端** | 自建 Express 3721 | 直连 Hermes API 8642 |
| **运行模型** | TICK 心跳循环 | Gateway Session 模型 |
| **会话管理** | 简单对话列表 | 完整 Session CRUD + 标题自动生成 |
| **记忆系统** | 自建 mem_id + FTS5 | 对接 Hermes memory.db |
| **工具系统** | 50+ 自定义工具 | Hermes toolsets (20+) |
| **平台** | 5 个社交平台 | Hermes 10+ 平台 |
| **语言** | 中文 only | 中英双语 |
| **认证** | 无 | Hermes auth.json |
| **文件浏览** | 无 | Hermes 工作区 |
| **上下文环** | 无 | Token 用量可视化 |
| **目标追踪** | 无 | Hermes Goals 系统 |
| **Kanban** | 无 | Hermes Kanban 面板 |
| **视觉风格** | 暗黑科技 + 毛玻璃 | 继承白龙马视觉语言，Hermes 品牌色 |
