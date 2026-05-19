---
title: Li Xiang Interview Deep Reading Board Example
type: example
language: zh-CN
layer: examples
domain: public-report-output
audience: self
knowledge_level: working
period: evergreen
status: validated
updated_at: 2026-05-19
ai_generated: true
---

# 李想访谈全文窗口式精读板样例

## 样例定位

这是 `interview-deep-reading-board` 的 validated output-shape example。

它记录的是一种访谈精读 H5 形态：词云不是主输出，而是进入访谈窗口、
时间线、温度轴和证据面板的索引。

## 正例

- H5:
  [lixiang-luoyonghao-ai-agent-reading-board.html](interview-deep-reading-board-lixiang-luoyonghao/lixiang-luoyonghao-ai-agent-reading-board.html)
- 数据:
  [lixiang-luoyonghao-ai-agent-reading-board-data.js](interview-deep-reading-board-lixiang-luoyonghao/lixiang-luoyonghao-ai-agent-reading-board-data.js)
- 来源记录:
  [agentic-product-engineering-collaboration-lixiang-luoyonghao-ai-agent-reading-2026-05-18.md](../sources/agentic-product-engineering-collaboration-lixiang-luoyonghao-ai-agent-reading-2026-05-18.md)
- 过程记录:
  [lixiang-luoyonghao-reading-board-example-process.md](../ops/lixiang-luoyonghao-reading-board-example-process.md)
- 过程快照:
  [report gate review](interview-deep-reading-board-lixiang-luoyonghao/process/agentic-product-engineering-collaboration-our-operating-system-report-gate-review.md)
  and
  [brainstorming drift retro](interview-deep-reading-board-lixiang-luoyonghao/process/agentic-product-engineering-collaboration-workway-brainstorming-drift-2026-05-18.md)

## 反例

- 旧词云:
  [lixiang-luoyonghao-ai-agent-wordcloud.html](interview-deep-reading-board-lixiang-luoyonghao/lixiang-luoyonghao-ai-agent-wordcloud.html)

旧词云可以作为“压缩风险”的反例：视觉上像是覆盖了关键词，但它不能单独承载
访谈顺序、人物回合、相邻逻辑和用户点名段落。

## 可复用形态

- 以访谈顺序拆阅读窗口，窗口是主内容单位。
- 温度轴是横向阅读控制，不是装饰性筛选。
- 词云只做入口，必须能跳到窗口和证据。
- 证据面板跟随窗口、关键词或温度轴状态变化。
- 时间线保留访谈推进顺序。
- 修复漂移输出时，默认聚焦用户点名或此前缺失的段落。

## 本次关键修复点

用户明确指出旧输出压缩了“代码量不是问题、是否自建办公软件、飞书、
内部 Coworker、稳定 Agent、子 Agent、数据、MCP”这一段。正例 H5 将该段
作为显式窗口，而不是藏在泛化的 `Agent` 关键词下。

## 边界

- 这个样例记录输出形态，不保存完整访谈逐字稿。
- 版权材料只用短证据、转述、来源位置和本地 source 记录来保持覆盖。
- 过程快照只作为例子证据，不代表当前仓库的运行中 ops 状态。
- 这个样例不代表 H5 已经适合发布或同步到飞书；reader-facing gate 仍由
  `public-report-quality-gate` 管。

## 适用 Skill

- `interview-deep-reading-board`
- `public-report-quality-gate`
