# Hermes Native UI — 视觉设计系统

> **参考来源**: 白龙马 (Bailongma) 视觉语言
> **目标**: 创造一套「望落去就係高端嘢」嘅暗黑科技风 UI
> **核心手法**: 多层渐变底色 + 毛玻璃面板 + D3 活记忆图谱 + 6 套主题

---

## 一、设计原则

```
1. 氛围先于信息 — 底色 + 光晕营造沉浸感，唔係死黑
2. 层次靠透明度 — 面板用 rgba 半透明叠加，透视背景图谱
3. 状态靠动画 — 唔係静态图标，而係活的、呼吸的视觉
4. 主题靠变量 — 全部颜色 CSS 变量驱动，一套代码 6 种风格
5. 细节靠微交互 — 提示音、脉冲、抖动、过渡
```

---

## 二、色彩体系

### 默认主题：Hermes Midnight（借鉴白龙马 Midnight Steel）

```css
:root {
  /* 背景三层 */
  --bg0: #0a1118;           /* 最底层 */
  --bg1: #0f1822;           /* 中间层 */
  --bg-deep: #060a10;       /* 最深处 */
  
  /* 文字三层 */
  --ink: #d7e2ee;           /* 主文字 */
  --ink2: #9aabbe;          /* 辅文字 */
  --dim: #5d6d80;           /* 暗文字 */
  
  /* 线条 */
  --line: rgba(138, 168, 200, 0.10);
  --line-strong: rgba(138, 168, 200, 0.22);
  
  /* 面板 */
  --panel: rgba(11, 18, 26, 0.56);
  --console-bg: rgba(15, 24, 34, 0.42);
  
  /* 强调色 */
  --accent-cool: #8fb6d8;    /* 冷色强调 */
  --accent-warm: #d39872;    /* 暖色强调 */
  
  /* 图谱节点 */
  --node-low: #3a556e;
  --node-high: #cfe3f5;
  
  /* 光晕 */
  --glow-halo: rgba(143, 182, 216, 0.10);
  --glow-tint1: rgba(138, 158, 200, 0.08);
  --glow-tint2: rgba(211, 152, 114, 0.06);
  
  /* 连线 */
  --link-stroke: rgba(143, 182, 216, 0.18);
  
  /* 语义色 */
  --ok: #74d89f;
  --warn: #f0c866;
  --danger: #ff6b6b;
  --info: #6bb5ff;
  
  /* 品牌色 (Hermes 专属) */
  --brand-primary: #7c5ce7;    /* Hermes 紫 */
  --brand-secondary: #5b8def;  /* Hermes 蓝 */
}
```

### 3 套初始主题

| 主题 | 关键词 | 底色调 |
|------|--------|--------|
| **Midnight** | 暗黑科技 | 深蓝黑 `#0a1118` |
| **Aurora** | 极光紫 | 深紫 `#0d0a1a`（Hermes 品牌色） |
| **Forest** | 竹林绿 | 深绿 `#050806` |

### 后续加
| 主题 | 关键词 | 底色调 |
|------|--------|--------|
| **Crimson** | 暗红 | 深红 `#1a0a0c` |
| **Abyss** | 深海 | 深蓝 `#060d18` |

---

## 三、布局系统

### 3.1 三面板布局

```
┌──────────────────────────────────────────────────────┐
│  ┌──────────┬───────────────────┬──────────────────┐ │
│  │ Session  │                   │    Info Panel     │ │
│  │ Sidebar  │    Chat View      │  ┌──────────────┐ │ │
│  │          │                   │  │ Agent Status │ │ │
│  │ 会话1    │  ┌───────────────┐│  │ 节点: 42     │ │ │
│  │ 会话2    │  │ 消息列表      ││  │ tok/s: 28    │ │ │
│  │ 会话3    │  │               ││  ├──────────────┤ │ │
│  │          │  │ [User] Hello  ││  │ Memory List  │ │ │
│  │ [+新会话] │  │ [AI]  你好!  ││  │ · 记忆1      │ │ │
│  │          │  │ [AI]  工具... ││  │ · 记忆2      │ │ │
│  │ 底部:    │  │               ││  ├──────────────┤ │ │
│  │ ⚙ 设置   │  └───────────────┘│  │ Workspace    │ │ │
│  │ 🎨 主题   │  ┌───────────────┐│  │ · file.ts    │ │ │
│  │ 🔊 语音   │  │ Composer     ││  │ · readme.md  │ │ │
│  │           │  │ [上下文环 72%]││  └──────────────┘ │ │
│  │           │  │ ▸ [输入...]  ││                   │ │
│  └──────────┘  └───────────────┘│ ← 可折叠          │ │
│                └───────────────────────────────────┘ │
│                  背景: D3 记忆图谱                    │
└──────────────────────────────────────────────────────┘
```

### 3.2 毛玻璃参数

```css
.panel {
  background: var(--panel);              /* rgba 半透明 */
  backdrop-filter: blur(20px);           /* 毛玻璃核心 */
  -webkit-backdrop-filter: blur(20px);   /* Safari */
  border: 1px solid var(--line);         /* 微边框 */
  border-radius: 14px;                   /* 圆角 */
  box-shadow: 
    0 4px 24px rgba(0,0,0,0.3),         /* 外阴影 */
    inset 0 1px 0 rgba(255,255,255,0.03); /* 内高光 */
}
```

### 3.3 面板尺寸

| 面板 | 宽度 | 行为 |
|------|------|------|
| Session Sidebar | 260px | 固定，可折叠 |
| Chat View | flex: 1 | 自适应 |
| Info Panel | 300px | 固定，可折叠 |
| Composer | 全宽 | 固定底部 |

---

## 四、氛围底色

### 多层渐变堆叠（最核心嘅视觉技巧）

```css
body {
  background:
    /* 第1层：左上角冷光晕 */
    radial-gradient(circle at 22% 18%, var(--glow-tint1), transparent 35%),
    /* 第2层：右下角暖光晕 */
    radial-gradient(circle at 80% 82%, var(--glow-tint2), transparent 38%),
    /* 第3层：整体深色渐变 */
    linear-gradient(160deg, var(--bg0), var(--bg1) 60%, var(--bg-deep) 100%);
  
  /* 固定背景，不跟滚动 */
  background-attachment: fixed;
}
```

**效果**：唔係死黑色，而係有光源方向、有深度嘅暗。

---

## 五、动画系统

### 5.1 全局过渡

```css
/* 主题切换：所有颜色平滑过渡 */
body {
  transition: background 0.6s ease, color 0.6s ease;
}
```

### 5.2 入场动画

| 动画名 | 用途 | 时长 | 缓动 |
|--------|------|------|------|
| `fade-up` | ACUI 卡片入场 | 0.35s | ease-out |
| `slide-from-right` | 通知卡片 | 0.4s | cubic-bezier(0.16,1,0.3,1) |
| `scale-up` | 居中弹窗 | 0.3s | cubic-bezier(0.34,1.56,0.64,1) |
| `scale-down` | 弹窗关闭 | 0.2s | ease-in |
| `slide-to-right` | 卡片滑出 | 0.35s | ease-in |

### 5.3 持续动画

| 动画名 | 用途 | 时长 | 行为 |
|--------|------|------|------|
| `neb-blink` | 思考指示器闪烁 | 1.2s | 无限循环 |
| `neb-cursor` | 打字光标 | 1s | 无限闪烁 |
| `neb-pulse` | 节点召回脉冲 | 10s | ease-out 一次 |
| `vinyl-spin` | 黑胶旋转 | 2s | 线性无限 |
| `ticker-scroll` | 跑马灯 | 30s | 线性无限 |

### 5.4 D3 物理动画

```
力导向图:
  - alpha 衰减: 0.028
  - 速度衰减: 0.3
  - 自然微抖: 每 6s，随机 30% 节点位移
  - 切线阻尼: 抑制剧烈旋转运动
```

### 5.5 SVG 滤镜

```xml
<filter id="neb-glow">
  <feGaussianBlur stdDeviation="3.2" result="blur"/>
  <feMerge>
    <feMergeNode in="blur"/>       <!-- 外发光 -->
    <feMergeNode in="SourceGraphic"/> <!-- 本体 -->
  </feMerge>
</filter>
```

---

## 六、D3 记忆图谱

### 6.1 视觉参数

```
节点:
  - 核心节点: r=9, 暖色
  - 普通节点: r=3.4+deg*0.9, 冷色
  - 节点色随时间衰减 (fade)
  - 召回高亮: brighter(2+useBoost*2)
  - 脉冲光环: neb-glow filter
  - 使用进度: 正弦脉冲 + 尺寸放大

连线:
  - 视觉父子线: 半透明, r=0.2
  - 随机补充线: 更淡, r=0.035
  - 颜色: link-stroke CSS 变量

力场:
  - 引力: 可调 0-5x (默认 1.0)
  - 斥力: 可调 0-5x (默认 1.35)
  - 节点大小: 可调 0-5x (默认 1.0)
```

### 6.2 交互

```
- 拖拽节点: 固定位置 (fx/fy)
- 滚轮缩放: 自定义实现，中心点缩放
- hover: 显示 tooltip
- 点击节点: 高亮该节点 900ms
- 双击空白: 重置视图
- 图谱调节: 滑块实时调节力场参数
```

---

## 七、响应式策略

```
桌面 (>1200px):   三面板全显示 + 背景图谱
平板 (768-1200px): 双面板（隐藏右侧）+ 背景图谱
手机 (<768px):     单面板（仅聊天）+ 隐藏图谱（省性能）
```

---

## 八、字体系统

```css
body {
  font-family: "Inter", "PingFang SC", "Microsoft YaHei", sans-serif;
  font-size: 14px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

code, pre, .mono {
  font-family: "JetBrains Mono", "Fira Code", "Consolas", monospace;
  font-size: 13px;
}
```

---

## 九、图标系统

**策略**: Emoji 先行，SVG 补充。同白龙马一样。

```
工具图标: emoji 映射
状态图标: ● 彩色圆点
操作图标: Unicode 符号 (▸ ☰ × ⚙ ▶ ♪ ⊞)
品牌图标: SVG (Hermes 翅膀 logo)
```

---

## 十、性能策略

| 策略 | 说明 |
|------|------|
| D3 限帧 | `requestAnimationFrame` 自然限帧 |
| 节点上限 | 最多显示 120 个节点 |
| 碰撞简化 | 节点 > 40 时碰撞迭代减为 1 |
| 移动端降级 | <768px 隐藏图谱 |
| CSS contain | 面板加 `contain: layout style` |
| 懒加载 | ACUI 组件动态 import |
