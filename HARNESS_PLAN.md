# Harness 工程搭建方案

> **For Hermes:** 按此方案逐步执行，先 Phase 1-2（核心，即时见效），再 Phase 3-4（加固）。

**目标：** 将 AI Agent 裸跑成功率 20% 提升至 ~100%，覆盖 Claude Code + Codex + Hermes 三个 Agent

**架构：** Harness 五子系统（指令/工具/环境/状态/反馈）→ 写入 CLAUDE.md/AGENTS.md → Agent 启动自动加载 → 强制验证闭环

---

## 现状诊断

| 子系统 | 状态 | 问题 |
|--------|:--:|------|
| 指令 | ⚠️ 部分 | CLAUDE.md/AGENTS.md 有知识星图规则，缺 Harness 铁律 |
| 工具 | ⚠️ 过宽 | settings.json allow: Bash(*)/Write(*) 全部放行，冇 deny |
| 环境 | ❌ 未做 | 冇 setup.sh 锁版本，冇 frozen-lockfile |
| 状态 | ❌ 缺失 | 零个项目有 PROGRESS.md |
| 反馈 | ⚠️ 不足 | hermes-glass/webui 有部分；smart-agent/pro 冇 test/lint |

---

## Phase 1: 指令子系统 — CLAUDE.md + AGENTS.md 追加 Harness 铁律

### Task 1.1: 追加 Harness 铁律到 ~/.claude/CLAUDE.md

**文件：** `~/.claude/CLAUDE.md`（末尾追加）

**修改内容：**

```markdown
## Harness 工程铁律（成功率 20%→100%）

> 参考：Anthropic + OpenAI 双实验验证。模型决定上限，Harness 决定用到几成。

### ⛔ 完成定义（反馈子系统）

宣布"完成/Done"前，以下命令**必须全部跑通且退出码=0**：
1. 类型检查（tsc --noEmit / mypy / pyright）
2. 测试（pytest / vitest / jest）
3. Lint（eslint / ruff）
4. 构建（如项目有 build 脚本）

**退出码≠0 → 任务≠完成。** 不许说"应该可以了"、"理论上没问题"。

### 📋 会话启动

每新会话第一件事：
1. 读取项目根目录 `PROGRESS.md`（如存在）
2. 输出当前状态：✅已完成 / 🔄进行中 / 📋待办 / ⚠️已知问题

### 🔄 上下文焦虑管理

- Token 用量超 **70%**，主动停下
- 写完当前子任务断点 → 回写 PROGRESS.md → 写清楚"下一步做什么"
- 提示用户："上下文即将满载，建议开新会话继续。断点已写入 PROGRESS.md。"

### 💾 状态持久化

每完成一个子任务，**立即**回写 PROGRESS.md：
- 已完成：✅ 子任务名
- 进行中：→ 下一个子任务名
- 已知问题：如遇到未解决的坑，记录

### 🔐 权限边界

- `git push --force` → 先确认
- `rm -rf` → 先确认
- 修改 `.env` / 密钥文件 → 先确认
- 安装新依赖 → 先确认（锁定版本）
```

### Task 1.2: 追加 Harness 铁律到 ~/.hermes/AGENTS.md

**文件：** `~/.hermes/AGENTS.md`（末尾追加）

**修改内容：** 同上（将 `Claude` 改为 `Hermes`）。

---

## Phase 2: 状态子系统 — PROGRESS.md

### Task 2.1: 创建 PROGRESS.md 模板 + 写入规则

**文件：** 以下项目各创建一份 `PROGRESS.md`

| 项目 | 路径 | 优先级 |
|------|------|:--:|
| smart-agent | `~/workspace/smart-agent/PROGRESS.md` | 🔴 高 |
| smart-agent-pro | `~/workspace/smart-agent-pro/PROGRESS.md` | 🔴 高 |
| hermes-glass | `~/workspace/hermes-glass/PROGRESS.md` | 🟡 中 |
| hermes-webui | `~/workspace/hermes-webui/PROGRESS.md` | 🟡 中 |

**模板内容：**

```markdown
# [项目名] 进度追踪

> ⚠️ AI Agent 每新会话第一件事：读此文件
> 每完成子任务立即回写

## ✅ 已完成

<!-- 格式：YYYY-MM-DD 任务描述 -->

## 🔄 进行中

<!-- 当前正在做的任务 -->

## 📋 待办

<!-- 下一步要做的事 -->

## ⚠️ 已知问题

<!-- 遇到的坑、待解决的 bug、注意事项 -->
```

### Task 2.2: 在 AGENTS.md 中补充 PROGRESS.md 自动写入约定

在 AGENTS.md 的 Harness 铁律中已包含「每完成子任务立即回写 PROGRESS.md」，此步骤为确认生效。

---

## Phase 3: 权限子系统 — .claude/settings.json 加固

### Task 3.1: 追加 deny 规则

**文件：** `~/.claude/settings.json`

**当前问题：** `allow: Bash(*)` + `Write(*)` = 全部放行，冇防线

**修改：** 在 `permissions` 块追加 `deny` 数组：

```json
"permissions": {
  "allow": [...],
  "deny": [
    "Bash(rm -rf /*)",
    "Bash(rm -rf ~/*)",
    "Bash(rm -rf ./*)",
    "Bash(git push --force origin main)",
    "Bash(git push --force origin master)",
    "Bash(:(){ :|:& };:)",
    "Bash(chmod 777 *)",
    "Bash(sudo *)",
    "Edit(.env)",
    "Edit(.env.local)",
    "Edit(credentials*)",
    "Edit(*secret*)"
  ]
}
```

---

## Phase 4: 反馈子系统 — smart-agent 加 test/lint

### Task 4.1: smart-agent 加基础测试框架

**文件：** `~/workspace/smart-agent/`

**操作：**
1. 创建 `pyproject.toml` 或更新 `requirements-dev.txt`，加入 pytest + ruff
2. 创建 `tests/` 目录 + `tests/conftest.py`
3. 写一个 smoke test（验证项目可导入）
4. 确认 `pytest` 可运行

**验证：**
```bash
cd ~/workspace/smart-agent && python -m pytest tests/ -v
```
预期：至少 1 个 test pass

### Task 4.2: smart-agent-pro 同步加测试

同 Task 4.1，路径改为 `~/workspace/smart-agent-pro/`

---

## 执行顺序

```
Phase 1 (指令) → Phase 2 (状态) → Phase 3 (权限) → Phase 4 (反馈)
   ↓ 即时生效       ↓ 跨会话生效     ↓ 安全加固       ↓ 长期收益
```

Phase 1-2 做完，Agent 即时有 Harness 行为约束。
Phase 3 防越权操作。
Phase 4 补充验证能力。

---

## 预期效果

| 场景 | 修复前 | 修复后 |
|------|:--:|:--:|
| Agent 做完不验证就宣布 Done | ✅ 会发生 | ❌ 强制跑 test 否则不算完成 |
| 上下文满咗赶工跳测试 | ✅ 会发生 | ❌ 70% 主动停、写断点 |
| 新会话唔知上次进度 | ✅ 会发生 | ❌ 自动读 PROGRESS.md |
| Agent 误删文件 / force push | ✅ 可能 | ❌ deny 规则拦截 |
| 主力项目冇测试 | ✅ 现状 | ❌ 至少有 smoke test |
