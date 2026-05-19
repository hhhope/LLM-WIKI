[English](README.en.md) | 中文

# LLM-WIKI

LLM-WIKI 是一个面向 AI 协作的项目上下文工程仓库。它把来源证据、项目知识、
Agent Skills、治理规则和维护记录组织成一个可长期演进的 LLM-Wiki。

它的目标不是搭一个 Markdown 文件夹，也不是展示一组脚本，而是让人和 AI 可以围绕同一套
Wiki 结构持续共建：人提供目标、判断和授权；AI 通过 Skills 读取、学习、生成、沉淀和复查；
Wiki 保存证据、上下文、决策和输出形态。

## 架构

LLM-WIKI 的核心架构分四层。

```text
1. Source Layer / 来源层
   wiki/sources
   保存公众号、文章、README、会议、访谈、项目材料等来源证据。

2. Context Layer / 上下文层
   wiki/ops、wiki/examples、wiki/adr、wiki/status
   保存工作流痕迹、输出样例、稳定决策和状态面。

3. Skill Layer / 技能层
   .codex/skills
   定义 Agent 如何读取、学习、输出、诊断、治理和验证。

4. Governance Layer / 治理层
   AGENTS.md、OpenSpec、medical loop、frontmatter taxonomy
   控制写入边界、变更生命周期、分类规则和复查要求。
```

这四层共同构成 LLM-WIKI：

- 来源层解决“AI 依据什么说”；
- 上下文层解决“下一轮对话如何接上”；
- 技能层解决“AI 应该怎么行动”；
- 治理层解决“什么能改、谁确认、怎么复查”。

## 治理设计

LLM-WIKI 的治理理念是：**AI 可以执行大量阅读、判断和生成工作，但关键判断必须有边界、有证据、有人审。**

因此仓库采用三层协作治理：

```text
1. Human Review Layer
   人给目标、做取舍、确认关键判断、验收结果。

2. Agent Skill Layer
   AI 通过 Skills 读取上下文、判断边界、选择路径、生成产物、提出修复。

3. Runtime Evidence Layer
   Wiki、case file、status artifact、工具输出负责记录证据和执行已批准动作。
```

工具脚本属于第三层，只负责批量处理、状态生成、结构化记录和检查；它们不替代 AI 判断，也不替代人审。

### 门禁

LLM-WIKI 的主要门禁包括：

- **Skill Gate**：Agent 行动前先匹配 `.codex/skills/`，不能绕过技能直接写。
- **Learning Gate**：外部材料先经过 `learning-capture`，明确来源、复用边界和沉淀位置。
- **Public Output Gate**：README、H5、报告、公开样例等读者面产物走 `public-report-quality-gate`。
- **Frontmatter Gate**：Wiki 页面遵循 `wiki/config/frontmatter-taxonomy.yaml`。
- **Medical Gate**：Wiki 自维护走 `wiki-medical-agent`，由 case file 管理状态。
- **OpenSpec Gate**：治理、结构或生命周期变更走 OpenSpec。
- **Verification Gate**：声明完成前走 `verify-before-claiming`，用新鲜证据复查。

这些门禁的目的不是增加流程，而是防止 AI 把“看起来合理的输出”直接升级为规则、结构或事实。

## 特色 Skills

### 1. 输入到长期上下文

这不是四个重复入口，而是一条输入链上的不同职责。

- `learning-capture`：总路由。先判断外部输入是不是值得学习、复用边界是什么、应该沉淀到哪里。
- `readme-learning-capture`：Repo/README 专用学习模块。处理 GitHub/GitLab 项目、README 结构、可复用设计和不应照搬的边界。
- `weixin-reader`：微信公众号读取器。只负责把 `mp.weixin.qq.com` 正文可靠取回为 Markdown，后续分析仍交给学习或输出类 skill。
- `material-collaboration-defaults`：材料协作默认路由。处理会议纪要、附件、预览稿、报告素材等已经进入仓库的材料，避免停在占位 intake。

这条链路关注的是：

- 这份材料是否值得沉淀；
- 应进入 `wiki/sources`、`wiki/ops` 还是 `wiki/examples`；
- 哪些只是候选观察，不能升级成规则；
- 后续 Agent 如何重新利用。

### 2. Agent Context 系列

负责让 Agent 从 Wiki 中取上下文，而不是只靠当前对话。

- `wiki-query`
- `wiki-context`
- `wiki-route`
- `wiki-status`
- `wiki-manifest`
- `wiki-graph`
- `wiki-scorecard`

它们让 Agent 可以先看已有状态、关系、上下文和路由建议，再决定下一步。

### 3. Medical Loop 系列

负责 Wiki 自维护。

- `wiki-medical-agent`
- `wiki-doctor`
- `wiki-confirm`
- `wiki-review-decisions`
- `wiki-treatment`
- `wiki-surgery`
- `wiki-recovery`

医疗闭环：

```text
doctor -> review/confirm -> treatment or surgery -> recovery
诊断   -> 确诊           -> 治疗 or 手术      -> 复查
```

Medical Agent 的重点不是自动修复，而是把维护状态收敛到 case file：AI 判断，人确认，工具执行已批准动作，最后 recovery 留痕。

### 4. Public Output 系列

负责把材料加工成读者面产物。

- `public-report-quality-gate`
- `interview-deep-reading-board`
- `meeting-note-output`
- `project-management-weekly-skill`

它们控制 README、H5、报告、访谈深读、会议纪要、项目周报等输出，避免把内部草稿直接当成可发布内容。

### 5. Governance 系列

负责结构性变更和完成声明。

- `openspec-router`
- `openspec-propose`
- `openspec-apply-change`
- `openspec-archive-change`
- `wiki-frontmatter-taxonomy`
- `verify-before-claiming`
- `clarify-before-acting`
- `simplicity-first`
- `surgical-changes`

这些 Skills 让治理变更有边界、有生命周期、有验证。

## 案例：微信公众号文章到 H5 / 报告

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
   验证产物存在；如涉及结构、规则或 Wiki 治理变更，进入 medical loop 或 OpenSpec。
```

这个例子体现的是 AI 共建：AI 负责读材料、抽结构、判断边界、选择 Skill、生成产物、沉淀上下文和触发复查；人负责目标、取舍、授权和验收。

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

## 入口

- `AGENTS.md`：Agent 运行规则和停止条件；
- `.codex/skills/`：Agent Skills；
- `wiki/sources/`：来源证据；
- `wiki/ops/`：协作、医疗、治理和方法记录；
- `wiki/examples/`：可复用输出形态；
- `wiki/status/wiki-status.md`：当前状态面；
- `wiki/config/frontmatter-taxonomy.yaml`：页面分类规则。

## 边界

- README 是读者入口，不是运行时权威。
- 运行时权威在 `AGENTS.md`、Skills、OpenSpec、case file 和 status artifacts。
- 工具输出是证据，不是判断本身。
- 外部学习不能直接升级成规则，必须经过 capture、证据和 gate。
- Medical preview 不是修复许可。
