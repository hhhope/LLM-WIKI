[English](README.en.md) | 中文

# LLM-WIKI

LLM-WIKI 是一个面向 AI 协作的项目上下文工程仓库。它将项目知识、来源证据、
Agent Skills、治理规则和维护记录组织为可长期演进的 LLM-Wiki。

项目目标不是保存 Markdown 文件，而是让人和 AI 在同一个知识结构上协作：

- 人负责目标、判断、授权和验收；
- AI 负责阅读材料、抽取结构、选择技能、生成产物、提出修复建议；
- Wiki 负责保存证据、上下文、决策、样例和状态；
- 治理体系负责限制写入、确认风险、复查结果。

## 设计原则

### 上下文工程

LLM-WIKI 采用 Karpathy 所说的 context engineering 思路：与其把上下文塞进一次对话，
不如把项目知识整理成 Agent 可以持续读取和更新的结构。

### Skill 优先

Agent 行动必须优先经过 `.codex/skills/`。Skills 定义了读取、写入、学习捕获、
输出生成、诊断、复查和停止条件。批处理脚本只作为工具层存在，不承担判断职责。

### 证据优先

外部材料进入 Wiki 前需要保留来源边界。结论、方法和输出形态必须能回到来源或操作记录。

### 人审优先

诊断、预览和建议不是写入许可。涉及结构、治理、规则或高风险输出时，需要人确认。

## 三层协作治理

```text
1. Human Review Layer
   人给目标、做取舍、确认关键判断、验收结果。

2. Agent Skill Layer
   AI 通过 skills 读取上下文、判断边界、选择路径、生成产物、提出修复。

3. Runtime Evidence Layer
   Wiki、case file、status artifact、脚本输出负责记录证据和执行已批准动作。
```

这三层共同决定一次操作是否可以继续。任何一层缺失，都不能声称完成。

## 四层上下文架构

```text
1. Source Layer
   wiki/sources
   保存文章、公众号、README、会议、访谈、项目材料等来源证据。

2. Context Layer
   wiki/ops、wiki/examples、wiki/adr、wiki/status
   保存工作流痕迹、输出样例、稳定决策和状态面。

3. Skill Layer
   .codex/skills
   定义 Agent 的读取、学习、输出、诊断、治理和验证行为。

4. Governance Layer
   AGENTS.md、OpenSpec、medical loop、frontmatter taxonomy
   控制写入边界、变更生命周期、分类规则和复查要求。
```

## 核心闭环一：Learning Capture

`learning-capture` 是外部信息进入 LLM-WIKI 的主入口。

它处理的问题不是“总结材料”，而是判断材料如何进入长期上下文：

- 是否需要保存为来源证据；
- 是否形成可复用方法；
- 是否成为输出样例；
- 是否只能作为候选观察；
- 是否需要进入 OpenSpec、medical loop 或 public report gate。

典型路径：

```text
文章 / 微信公众号 / README / 会议 / 访谈 / 项目材料
-> learning-capture 判断来源类型和复用边界
-> wiki/sources 保存证据
-> wiki/ops 保存方法、决策和协作痕迹
-> wiki/examples 保存可复用输出形态
-> 后续 Agent 通过 wiki-query / wiki-context / wiki-route 重新利用
```

相关 skills：

- `learning-capture`
- `readme-learning-capture`
- `weixin-reader`
- `material-collaboration-defaults`
- `interview-deep-reading-board`
- `meeting-note-output`
- `project-management-weekly-skill`
- `public-report-quality-gate`

## 核心闭环二：Agent Skills

`.codex/skills/` 是 Agent 的操作层。它决定 Agent 在本仓库里如何行动。

主要 skill 分组：

- 上下文检索：`wiki-query`、`wiki-context`、`wiki-route`
- 状态诊断：`wiki-status`、`wiki-manifest`、`wiki-graph`、`wiki-scorecard`
- 受控建议：`wiki-apply`
- Frontmatter：`wiki-frontmatter-taxonomy`
- 治理变更：`openspec-router`、`openspec-propose`、`openspec-apply-change`、`openspec-archive-change`
- 完成校验：`verify-before-claiming`
- 协作约束：`clarify-before-acting`、`simplicity-first`、`surgical-changes`

## 核心闭环三：Medical Agent

Medical Agent 是 Wiki 自维护的安全入口。

```text
doctor -> review/confirm -> treatment or surgery -> recovery
诊断   -> 确诊           -> 治疗 or 手术      -> 复查
```

相关 skills：

- `wiki-medical-agent`
- `wiki-doctor`
- `wiki-confirm`
- `wiki-review-decisions`
- `wiki-treatment`
- `wiki-surgery`
- `wiki-recovery`

Medical Agent 的职责是把维护状态收敛到 case file。AI 根据 case file 判断当前状态，
人确认关键决策，工具只执行已批准的窄操作并留下复查证据。

## 示例：微信公众号文章到 H5/报告

输入：一篇微信公众号文章。  
目标：生成 H5 深度阅读、报告草稿、卡片或证据板。

推荐路径：

```text
1. weixin-reader
   获取或整理公众号材料，保留来源边界。

2. learning-capture
   判断材料是来源证据、方法参考、案例素材，还是候选观察。

3. wiki/sources + wiki/ops
   保存原始证据、摘要、可复用方法、争议点和后续动作。

4. public-report-quality-gate / interview-deep-reading-board
   根据读者目标选择输出门禁和结构。

5. 输出产物
   H5、报告、卡片、时间线、温度轴、证据板等进入目标产物路径或 wiki/examples。

6. verify-before-claiming / medical loop
   验证产物存在；如涉及结构或规则变更，进入 medical loop 或 OpenSpec。
```

这个流程体现的是 AI 共建：AI 不只是生成文字，而是负责阅读、抽取、判断、路由、生成、
沉淀和复查；人负责目标、判断、授权和验收。

## 项目结构

```text
LLM-WIKI/
├── AGENTS.md                         # Agent 在本仓库的运行规则
├── PROJECT.md                        # 项目身份
├── README.md                         # 中文入口
├── README.en.md                      # 英文入口
├── .codex/skills/                    # Agent Skills
├── openspec/changes/                 # 治理/结构变更生命周期
├── scripts/                          # 工具层：批处理、状态生成、检查
└── wiki/
    ├── sources/                      # 来源证据
    ├── ops/                          # 工作流痕迹、医疗病例、治理证据
    ├── examples/                     # 可复用输出形态
    ├── adr/                          # 稳定决策
    ├── config/                       # taxonomy 和行为资产配置
    ├── status/                       # 生成状态面
    ├── moc/                          # MOC 投影目标目录
    ├── domains/                      # 领域索引
    ├── reports/                      # 报告输出
    ├── templates/                    # 页面模板
    └── timeline/                     # 时间线
```

## 关键入口

- `AGENTS.md`：Agent 运行规则和停止条件；
- `.codex/skills/`：Agent Skills；
- `wiki/sources/`：来源证据；
- `wiki/ops/`：协作、医疗、治理和方法记录；
- `wiki/examples/`：可复用输出形态；
- `wiki/status/wiki-status.md`：当前状态面；
- `wiki/config/frontmatter-taxonomy.yaml`：页面分类规则。

## 边界

- README 是读者入口，不是运行时权威。
- 运行时权威在 `AGENTS.md`、skills、OpenSpec、case file 和 status artifacts。
- 脚本输出是工具层证据，不是判断本身。
- 外部学习不能直接升级成规则，必须经过 capture、证据和 gate。
- 医疗闭环 preview 不是修复许可。

## FAQ

### AI 在这里承担什么职责？

AI 负责阅读材料、提取结构、判断边界、选择 skills、生成产物、沉淀上下文、触发诊断和复查。
人负责目标、取舍、授权和最终验收。

### 工具脚本承担什么职责？

工具脚本负责批量处理、结构化输出、状态生成、frontmatter 检查和 case file 刷新。它们不替代
AI 判断，也不替代人审。

### 第一次应该看哪里？

先看 `AGENTS.md`、`.codex/skills/`、`wiki/status/wiki-status.md`、`wiki/sources/`、
`wiki/ops/`，再让 Agent 通过 `wiki-query`、`wiki-context` 或 `wiki-medical-agent`
判断下一步。
