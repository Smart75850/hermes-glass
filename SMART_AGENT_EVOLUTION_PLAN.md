# Smart Agent 活体进化计划书

> 2026-06-11 | 基于项目全面审计 + 2026 最新 Agent 架构研究
> **目标**：将 Smart Agent 从「僵尸脚本」进化为「活体专项 Agent」

---

## 一、现有实力审计

### 🟢 已经领先行业嘅部分

| 能力 | Smart Agent 现有 | 行业 2026 标准 | 差距 |
|------|:--:|:--:|:--:|
| 多平台适配 | 7 平台（5 HTTP + 2 浏览器） | 多数 3-5 平台 | ✅ 领先 |
| Agent 编排 | LangGraph StateGraph DAG | LangGraph 系 2026 最主流框架 | ✅ 对齐 |
| 自修正 | CriticAgent review-retry loop | Reflexion 模式（Princeton 2023 基准） | ✅ 对齐 |
| 结构化输出 | Pydantic + JSON Schema 强制验证 | 行业标配 | ✅ 对齐 |
| 生产部署 | Go 二进制 6.7MB + Docker + WebUI | 多数组 Python only | ✅ 领先 |
| 测试覆盖 | 56/56 tests passing | 多数项目 <50% | ✅ 领先 |
| 会话管理 | CookieBridge + session_manager 三路fallback | 独特竞争力 | ✅ 领先 |
| 断点续跑 | checkpoint + --resume + SqliteSaver | Karpathy autoresearch 同类 | ✅ 对齐 |

### 🔴 甩漏（对比 2026 最新方案）

| 维度 | Smart Agent 缺咩 | 行业最新 |
|------|------|------|
| **长期记忆** | ❌ 冇跨 run 学习能力。每次 run 从零开始 | Reflexion 模式：持久化 verbal self-reflection |
| **自调节** | ⚠️ 有 Critic（自修正 prompt 输出），但唔识调策略 | Samsung SDS 自愈框架：失败检测→可靠性评估→自动恢复 |
| **持续运行** | ⚠️ 有 --schedule 但 CLI 模式，关机就停 | Daemon 模式 + health check + 自动重启 |
| **学习闭环** | ❌ 发布后唔 check 效果，唔识反馈优化 | Karpathy autoresearch：跑实验→评估→迭代 |
| **Agent 间通信** | ❌ 7 Agent 在 LangGraph 内协同，但对外冇统一 API 俾 Hermes 调度 | 行业：REST/WebSocket + 事件总线 |
| **失败自愈** | ⚠️ adapter 失败只 log error，唔识自动换策略 | 自愈框架：3 级恢复（重试→换参数→人工介入）|
| **效果追踪** | ❌ 发布后冇回查阅读量/互动数 | 闭环：发布→等待→采集数据→分析→优化下轮 |

---

## 二、2026 行业灵感对照

### 灵感 1: Reflexion（Princeton/MIT 2023，2026 主流落地）

**核心**：Agent 每次执行后自我反思 → 存入持久记忆 → 下次自动参考

```
你的 CriticAgent（现有）         → Reflexion 升级
─────────────────────────────────────────────
review-retry loop（单次修正）  →  跨 run 记忆：上次小红书 15:00 发流量好
只修正输出质量                →  修正发布策略
会话内有效                    →  持久化 SQLite，下个 run 继续学
```

**你可以抄嘅**：将现有 `trace_collector.py`（已记录高分输出）升级为 `reflection_store`（记录每次发布结果 + 自我反思 + 策略建议）。

### 灵感 2: Karpathy autoresearch（2026-03 开源，630 行 Python）

**核心**：Agent 修改代码 → 跑实验 → 看结果 → 决定下步

```
autoresearch 模式              →  Smart Agent 对应
─────────────────────────────────────────────
修改训练代码 → 跑实验          →  修改发布参数（时间/标签/平台）→ 跑一轮
评估 loss                     →  评估阅读量/互动/封号率
决定下步超参                  →  决定下轮策略
```

**你可抄嘅**：加 `ExperimentRunner` — 每天自动跑 3 轮不同策略的小红书发布，对比效果，选最优策略做主力。

### 灵感 3: Samsung SDS 自愈框架（2026-05 论文）

**核心**：三级自动恢复

```
Level 1: 重试（换 IP/换 session/加延迟）
Level 2: 降级（浏览器 mode → HTTP mode，或跳过该平台）
Level 3: 人工介入（连续 3 次失败 → 通知大老）
```

**你已有嘅**：三路 fallback（CDP → Persistent Profile → 账号轮换）。只需加自动触发逻辑。

---

## 三、甩漏分析（自测）

我 review 完你嘅 STATUS.md 同完整代码后，发现以下甩漏系我最初未提及嘅：

| # | 甩漏 | 严重度 | 说明 |
|---|------|:--:|------|
| 1 | **结果闭环缺失** | 🔴 | 7 Agent 生成内容 → 发布 → 然后呢？冇回查阅读量/评论/封号 |
| 2 | **配置散落** | 🟡 | `.env` / settings.py / account_manager.json 分三处，维护成本高 |
| 3 | **小红书 session 几小时过期** | 🟡 | 需每日 CDP，冇自动重登机制 |
| 4 | **抖音评论 HTTP 未攻破** | 🟡 | "API URL 已确认，cookie 层待攻坚" — STATUS.md P0 未完成项 |
| 5 | **跨平台内容策略不统一** | 🟢 | 同一篇内容发 7 平台，但平台特性（标题长度/标签格式/图片尺寸）靠 CopyWriter prompt，唔系结构化约束 |
| 6 | **MCP Server 接口不完整** | 🟢 | 有 smart_fetch MCP 工具，但冇 publish / schedule / status 等管理接口 |

---

## 四、进化路线图

### Phase 1：记忆层 — 1 周（🟢 低风险，高回报）

```
目标：Agent 有跨 run 记忆，唔再次次从零开始
```

| # | 模块 | 做法 | 文件 |
|:--|------|------|------|
| 1.1 | 发布日志 | 每次 publish 记录：平台/时间/内容类型/标签/结果 | 新：`src/memory/publish_log.py` |
| 1.2 | 策略记忆 | SQLite 存 "小红书下午3点用#AI绘画标签流量好 → 下次优先" | 新：`src/memory/strategy_memory.py` |
| 1.3 | 反思注入 | run 启动时自动读取上次反思，注入 Agent prompt | 改：`src/orchestrator/pipeline.py` |
| 1.4 | 效果回查 | publish 后等 2h → 自动搜索自己发嘅内容 → 采集阅读量 | 复用：现有 search adapter |

### Phase 2：API 层加固 — 3 天（🟢 低风险）

```
目标：Hermes 可以 HTTP call Smart Agent，唔使人手 CLI
```

| # | 模块 | 做法 |
|:--|------|------|
| 2.1 | REST API 完善 | 已有 `sidecar_server.py:18500`，加 `POST /api/publish` `GET /api/status` `POST /api/schedule` |
| 2.2 | Go API 同步 | `go/internal/api/` 加相同接口，Go 二进制自带 API |
| 2.3 | Hermes 集成 | 写 Hermes skill `smart-agent`，封装 curl 调用 |

### Phase 3：自愈层 — 1 周（🟡 中风险）

```
目标：平台封咗自动执生，唔使大老人手介入
```

| # | 模块 | 做法 |
|:--|------|------|
| 3.1 | 三级恢复 | Level1 重试(换IP) → Level2 降级(换adapter mode) → Level3 通知 |
| 3.2 | 小红书 session 自动重登 | 检测 session 过期 → 自动触发 CDP 收割 |
| 3.3 | 失败模式识别 | 记录失败 pattern → "小红书连续3次signature error → 可能算法更新 → 通知大老" |

### Phase 4：自调节层 — 2 周（🔴 高风险，需先完成 Phase 1）

```
目标：Agent 自己学边种策略好，自动调整
```

| # | 模块 | 做法 |
|:--|------|------|
| 4.1 | ExperimentRunner | 每天自动跑 3 轮 A/B test（不同时间/标签/内容类型） |
| 4.2 | 策略优化 | 收集数据 → 统计 → 自动切换最优策略 |
| 4.3 | 跨平台协同 | "B站流量好 → 自动加频；小红书限流 → 自动降频" |

---

## 五、做完 vs 唔做：量化对比

| 指标 | 而家（僵尸） | Phase 1-2 后 | Phase 1-4 后 |
|------|:--:|:--:|:--:|
| 人手操作 | 每次 CLI 命令 | Hermes 一句 curl | Hermes 一句 natural language |
| 平台封号 | 全死，人手动救 | 自动跳过 + 通知 | 自动降级 + 自愈 |
| 策略优化 | 人手分析数据 | 每日自动报告 | Agent 自行 A/B test + 切换 |
| 跨 run 学习 | 次次从零开始 | 参考上次反思 | 持续进化 |
| 单次 run 成功率 | ~70% | ~85% | ~95% |
| 人力投入 | 每日 1h+ 运维 | 每周 10min 睇报告 | 每周 2min 审核决策 |

---

## 六、诚实风险评估

| 风险 | 概率 | 应对 |
|------|:--:|------|
| 自调节过度优化导致封号 | 中 | Phase 4 加安全边界（每日最多 N 次/平台） |
| 逆向签名算法突然更新 | 高 | Phase 3 自愈层自动降级到浏览器 mode |
| 记忆数据膨胀 | 低 | SQLite 定期清理，只保留最近 30 天 |
| Hermes 调度延迟 | 低 | REST API 同步调用，timeout 设 5 分钟 |

---

## 七、建议执行顺序

```
本周: Phase 1.1-1.2 (发布日志 + 策略记忆)  ← 最快见效果
下周: Phase 2 (API 加固 + Hermes 集成)     ← 打通调度
下下周: Phase 3 (自愈层)                    ← 稳定性飞跃
下月: Phase 4 (自调节)                      ← 真正「活」
```

---

## 八、同行业对标

| 产品 | 定位 | Smart Agent 进化后 |
|------|------|------|
| Omniwork | 通用创作 Agent OS | Smart Agent = **内容发布专项 Agent OS** |
| JVS Claw | 云手机 + Agent | Smart Agent = **本地 + Web 双模 Agent** |
| MediaCrawler(阿江) | HTTP 逆向爬虫 | Smart Agent = **爬虫 + AI 分析 + 自我进化** |
| 蝉妈妈/飞瓜 | 数据 Dashboard | Smart Agent = **数据采集 + Agent 分析 + 自动执行** |
