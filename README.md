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

治理不是单向审批，而是“进入有门禁、产出有门禁、越界有复盘”。

```text
外部材料 / 用户意图
        |
        v
 [入口门禁]
 Skill Gate + Learning Gate + Frontmatter Gate
        |
        v
 [AI 默认规范]
 读取上下文 -> 判断边界 -> 选择 Skill -> 生成候选产物
        |
        v
 [人固定规范]
 目标确认 -> 关键取舍 -> 授权写入 -> 验收发布
        |
        v
 [出口门禁]
 Public Output Gate + Medical Gate + OpenSpec Gate + Verification Gate
        |
        v
 Wiki / H5 / 报告 / case file / status artifact

越界或争议
        |
        v
 复盘 -> 修正 skill / taxonomy / OpenSpec / README / 示例
```

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

人侧规范相对固定：目标、判断、授权和验收必须由人确认。  
AI 侧规范默认收敛到 Skills：先读上下文和边界，再选择路径，最后用证据说明产出。  
工具侧规范只记录和检查，不把 preview、score 或脚本输出自动升级为事实、规则或批准。

### 门禁

LLM-WIKI 的主要门禁分为入口和出口：

- **Skill Gate**：Agent 行动前先匹配 `.codex/skills/`，不能绕过技能直接写。
- **Learning Gate**：外部材料先经过 `learning-capture`，明确来源、复用边界和沉淀位置。
- **Frontmatter Gate**：Wiki 页面遵循 `wiki/config/frontmatter-taxonomy.yaml`。
- **Public Output Gate**：README、H5、报告、公开样例等读者面产物走 `public-report-quality-gate`。
- **Medical Gate**：Wiki 自维护走 `wiki-medical-agent`，由 case file 管理状态。
- **OpenSpec Gate**：治理、结构或生命周期变更走 OpenSpec。
- **Verification Gate**：声明完成前走 `verify-before-claiming`，用新鲜证据复查。

入口门禁决定材料能不能进、以什么身份进、沉淀到哪里。出口门禁决定产物能不能发布、规则能不能生效、治理变更能不能落库。它们的目的不是增加流程，而是防止 AI 把“看起来合理的输出”直接升级为规则、结构或事实。

## 特色 Skills

Skills 不是命令清单，而是 Agent 的默认操作协议。它们把“用户意图、外部材料、Wiki 上下文、读者产物、治理变更”接成可复查的闭环。

```text
意图 / 材料
   |
   v
Learning Intake -> Context Retrieval -> Output / Medical / Governance
   |                    |                         |
   v                    v                         v
sources / ops      status / graph            report / case / OpenSpec
   \____________________ evidence + review ____________________/
```

### 1. Learning Intake

负责判断外部输入如何进入长期上下文。

- `learning-capture` 是总路由：先判断材料身份、复用边界和沉淀位置。
- `readme-learning-capture` 处理 Repo/README 学习：提取可迁移设计，拒绝不应照搬的结构。
- `weixin-reader` 是读取器：只把微信公众号正文取回为 Markdown，不拥有后续判断。
- `material-collaboration-defaults` 处理已进入仓库的会议、附件、报告素材和预览稿。

这一组解决“材料是什么、值不值得沉淀、进入 sources / ops / examples 哪一层、后续 Agent 如何复用”。

### 2. Context Retrieval

负责让 Agent 从 Wiki 取证据，而不是只靠当前对话继续写。

- `wiki-query` 组合路由、上下文和文本检索。
- `wiki-context` 读取运行时上下文包。
- `wiki-route` 给出来源整合后的路由建议。
- `wiki-status`、`wiki-manifest` 查看当前状态面和来源清单。
- `wiki-graph`、`wiki-scorecard` 检查关系、覆盖度和语义健康度。

这一组只提供诊断和上下文，不自动授权写入。

### 3. Medical Maintenance

负责 Wiki 自维护的闭环，不是自动修复器。

```text
wiki-medical-agent
        |
        v
doctor -> review/confirm -> treatment or surgery -> recovery
诊断   -> 确诊           -> 治疗 or 手术      -> 复查
```

`wiki-medical-agent` 是正常入口；`wiki-doctor`、`wiki-review-decisions`、`wiki-treatment`、`wiki-surgery`、`wiki-recovery` 是阶段能力。AI 负责诊断和方案，人确认关键判断，工具只执行已批准动作，最后用 recovery 留痕。

### 4. Reader-Facing Output

负责把材料变成读者面产物，而不是把内部草稿直接发布。

- `public-report-quality-gate` 管 README、H5、报告、公开样例的读者意图、结构、引用和判断归属。
- `interview-deep-reading-board` 管访谈深读、证据板、时间线、温度轴等结构化深读产物。
- `meeting-note-output` 管会议纪要输出。
- `project-management-weekly-skill` 管项目周报、里程碑和风险沟通。

这一组解决“给谁看、让读者做什么判断、用什么结构承载证据、什么时候可以发布”。

### 5. Governance Promotion

负责把候选判断升级为规则、结构或生命周期变更。

- `openspec-router`
- `openspec-propose`
- `openspec-apply-change`
- `openspec-archive-change`
- `wiki-frontmatter-taxonomy`
- `verify-before-claiming`
- `clarify-before-acting`
- `simplicity-first`
- `surgical-changes`

这一组控制升级路径：先澄清边界，再最小化变更，再用 OpenSpec、taxonomy、验证证据记录结构性变更。没有通过这组门禁的内容，只能是草稿、候选观察或局部产物。

## 案例：微信公众号文章到 H5 / 报告

输入不是单独的一篇文章，而是“材料 + 意图”：

- 一篇微信公众号文章；
- 目标产物，例如 H5 深度阅读、报告草稿、卡片、时间线、温度轴或证据板；
- 读者、使用场景和是否需要沉淀到 Wiki。

推荐路径：

```text
1. 用户意图 -> learning-capture
   Agent 先判断这是来源证据、方法参考、案例素材、输出任务，还是候选观察。

2. 按材料形态选择读取器
   如果是 mp.weixin.qq.com，再调用 weixin-reader 取正文；如果材料已经在仓库中，
   走 material-collaboration-defaults；如果是 README/Repo，走 readme-learning-capture。

3. 按目标选择产物链路
   H5、报告、卡片、证据板、时间线、温度轴等不是固定产物，由用户意图和读者目标决定。

4. wiki/sources + wiki/ops
   保存来源证据、摘要、可复用方法、争议点、输出用途和后续动作。

5. public-report-quality-gate / interview-deep-reading-board
   如果进入读者可见的 H5、报告或深度阅读产物，先过读者意图、结构、引用和判断归属门禁。

6. verify-before-claiming / medical loop
   验证目标产物和 Wiki 沉淀都真实存在；如涉及结构、规则或 Wiki 治理变更，进入
   medical loop 或 OpenSpec。
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
