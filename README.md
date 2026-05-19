[English](README.en.md) | 中文

# LLM-WIKI

一个基于 Karpathy「上下文工程」理念的 LLM-Wiki：把项目知识、运行规则、证据和
维护流程组织成 Agent 可读取、可诊断、可复查的上下文底座。

它不是一个打包好的 `llm-wiki` 安装器，而是一个已经能跑起来的
Wiki seed：仓库内置技能、frontmatter 分类规则、状态面、运行脚本和
“医疗式”维护闭环，让 Agent 可以基于证据诊断、确认、修复和复查。

## 这是什么

LLM-WIKI 是一套给 Agent 使用的项目知识底座。它把 Markdown Wiki 当作长期上下文，
把技能、taxonomy、状态检查、图谱诊断和医疗式维护流程放在同一个仓库里，让 Agent
不是只靠一次对话记忆工作，而是能持续读取、更新和验证项目知识。

核心流程：

```text
保留来源证据 -> 生成/整理 wiki 页面 -> 检查 taxonomy 和图谱
-> 诊断漂移 -> 确认安全改动 -> 治疗或手术 -> 复查
```

当前 seed 包含：

- `wiki/` 下的一组最小 Wiki 页面；
- `.codex/skills/` 下的仓库本地技能；
- 严格的 frontmatter taxonomy 配置；
- status、graph、scorecard、context、routing、medical-loop 脚本；
- 用于治理变更的 OpenSpec change 记录；
- 能显示健康、漂移、阻塞和待确认状态的生成状态面。

## 30 秒上手

在仓库根目录执行：

```bash
python3 scripts/build_wiki_status.py
python3 scripts/check_wiki_frontmatter.py
python3 scripts/extract_wiki_graph.py
python3 scripts/build_wiki_medical_agent.py --intent-text "status"
```

优先看的入口：

- `wiki/status/wiki-status.md`：当前 Wiki 健康状态；
- `AGENTS.md`：仓库本地 Agent 路由和停止规则；
- `PROJECT.md`：项目身份；
- `wiki/config/frontmatter-taxonomy.yaml`：Wiki frontmatter 规则；
- `.codex/skills/wiki-medical-agent/SKILL.md`：医疗式维护的正常入口。

## 项目结构

```text
LLM-WIKI/
├── AGENTS.md                         # 仓库本地 Agent 规则和运行门禁
├── PROJECT.md                        # 项目身份和 source-of-truth 说明
├── README.md                         # 中文入口
├── README.en.md                      # 英文入口
├── .codex/skills/                    # 仓库本地工作流和 wiki skills
├── openspec/changes/                 # 活跃/完成的治理变更
├── scripts/                          # 运行时诊断和生成脚本
└── wiki/
    ├── adr/                          # 稳定决策
    ├── config/                       # taxonomy 和行为资产配置
    ├── domains/                      # 领域索引
    ├── examples/                     # 已验证的输出形态示例
    ├── moc/                          # MOC 投影目标目录
    ├── ops/                          # 医疗病例、轨迹、工作流证据
    ├── reports/                      # 报告索引和报告输出
    ├── sources/                      # 来源记录和脱敏证据
    ├── status/                       # 生成状态面
    ├── templates/                    # Wiki 页面模板
    └── timeline/                     # 时间线索引和记录
```

## 关键配置

`wiki/config/frontmatter-taxonomy.yaml`

- 定义 Wiki layer、domain、ops_area 等分类规则。
- 定义 strict gate 覆盖哪些 Wiki 页面。
- 驱动 `scripts/check_wiki_frontmatter.py`。

`wiki/config/behavior-asset-evaluation.yaml`

- 定义 skills、rules、AGENTS 等行为资产的评估要求。
- 避免治理变更只停留在“文字好看”，要求留下证据。

`AGENTS.md`

- 说明 Agent 在本仓库里应该如何路由工作。
- 明确 README 不是运行时权威。
- 把维护工作指向 OpenSpec、Wiki 医疗闭环和验证命令。

`PROJECT.md`

- 通过 frontmatter 提供项目身份。
- 标记本仓库是一个可运行的 Wiki seed。

## 亮点技能

仓库本地技能是 Agent 行动前应该使用的主要接口。

### Wiki Runtime

- `wiki-status`：刷新并汇总 `wiki/status/`。
- `wiki-manifest`：检查 source 和 routing manifest。
- `wiki-graph`：检查图谱抽取和关系健康度。
- `wiki-scorecard`：检查语义评分和利用率诊断。
- `wiki-context`、`wiki-route`、`wiki-apply`：检查运行时上下文、路由和
  self-directed execution 建议。

### 医疗闭环

- `wiki-medical-agent`：诊断、确认、治疗、手术、复查和归档检查的正常入口。
- `wiki-doctor`、`wiki-confirm`、`wiki-treatment`、`wiki-surgery`、
  `wiki-recovery`：阶段性证据面，主要用于显式检查或受控跟进。
- `wiki-review-decisions`：从 adjudication 输出生成确认记录。

### 治理和变更流

- `openspec-router`：在 OpenSpec、Superpowers、治理工作开始前先路由。
- `openspec-propose`：创建 change artifacts。
- `openspec-apply-change`：执行已批准的变更。
- `openspec-archive-change`：只在 archive review 通过后归档。
- `verify-before-claiming`：声明完成前必须有新鲜证据。

### 来源和输出

- `learning-capture`、`readme-learning-capture`：从文章、仓库、README、示例中捕获可复用学习。
- `material-collaboration-defaults`：把来源材料路由为可读 Wiki 记录。
- `public-report-quality-gate`：控制 README、docs、examples 和公开报告草稿等读者面输出。
- `interview-deep-reading-board`、`meeting-note-output`、
  `project-management-weekly-skill`：专门的输出工作流。

## 医疗式维护体系

LLM-WIKI 用医疗隐喻限制 Agent 直接套用推测性修复。

```text
doctor -> review/confirm -> treatment or surgery -> recovery
诊断   -> 确诊           -> 治疗 or 手术      -> 复查
```

核心原则：**active case file 才是允许行动的权威**。预览、诊断、建议都不是写入许可。

各阶段含义：

- **Doctor / 诊断**：发现候选问题、漂移、弱证据和结构风险。
- **Review / Confirm / 确诊**：判断哪些接受、拒绝、延期、可治疗、需手术或需 OpenSpec。
- **Treatment / 治疗**：执行窄范围、明确批准、低风险的修复。
- **Surgery / 手术**：规划结构、治理、taxonomy、ADR、relation、MOC 等更大改动。
- **Recovery / 复查**：重跑检查，记录改了什么、还阻塞什么、下一步是什么。

命令返回 `awaiting_confirmation`、`preview_only` 或 `blocked` 是正常安全状态，
不是应该隐藏的失败。

## 常用命令

### 状态面

```bash
python3 scripts/build_wiki_status.py
```

写入：

- `wiki/status/manifest.json`
- `wiki/status/wiki-status.md`

### Frontmatter 检查

```bash
python3 scripts/check_wiki_frontmatter.py
```

声明 taxonomy 合规前必须跑。

### 图谱抽取

```bash
python3 scripts/extract_wiki_graph.py
python3 scripts/analyze_wiki_relations.py
```

用于检查 canonical objects、图谱解析健康度和 relation 漂移。

### Scorecard 和运行时上下文

```bash
python3 scripts/score_wiki_semantics.py
python3 scripts/summarize_wiki_scorecard.py
python3 scripts/build_wiki_runtime_context.py
python3 scripts/resolve_runtime_context_sources.py
python3 scripts/derive_runtime_auto_routing.py
python3 scripts/build_runtime_context_injection.py
python3 scripts/derive_self_directed_execution.py
```

这些脚本是诊断面，不证明完全自治，也不是执行 queued work 的许可。

### Medical Agent

```bash
python3 scripts/build_wiki_medical_agent.py --intent-text "status"
```

这是正常维护入口。

### 医疗阶段命令

```bash
python3 scripts/build_wiki_medical_case.py
python3 scripts/build_wiki_review_decisions.py
python3 scripts/build_wiki_treatment.py
python3 scripts/build_wiki_surgery.py
python3 scripts/build_wiki_recovery.py
```

阶段命令受 case file 和仓库 gate 约束。不要把 preview 输出当作批准去写
Wiki、taxonomy、ADR、MOC、OpenSpec 或 skill。

## 当前 Seed 健康度

这份 README 更新时的已验证基线：

- frontmatter checker：`0` error，仍有非阻塞 producer warning；
- graph extraction：能生成节点，但 relation coverage 还很薄；
- medical agent：status reporting 可用，active case 仍是 `awaiting_confirmation`；
- OpenSpec：自运行治理 bootstrap 已完成，下一步是 archive review，不是自动归档。

最新状态请运行 `python3 scripts/build_wiki_status.py`，不要只信这份快照。

## 边界

- 这个 seed 复制的是系统形态，不是私有历史。
- `wiki/sources/` 保存来源证据，不要用无来源总结替代。
- README 面向读者解释项目；运行时权威在 `AGENTS.md`、repo-local skills、OpenSpec
  changes 和生成状态面。
- 医疗闭环 preview 不是修复许可。
- MOC projection、content enrichment、content adjudication、self-directed execution
  都是诊断面；除非有批准的 workflow 明确授权，否则不写入。

## FAQ

### 这和 `sdyckjq-lab/llm-wiki-skill` 是同一个项目吗？

不是。那个项目是多平台个人知识库 skill，带安装器和素材适配器。本仓库是一个可运行的
Wiki seed，重点是 repo-local governance、taxonomy 检查、OpenSpec 记录和医疗式维护。

### 可以用 Obsidian 打开吗？

可以。Wiki 内容是 Markdown-first。部分生成诊断面主要给 Agent 读，但页面仍可作为普通
Markdown 打开。

### 它会自动修复自己吗？

不会直接自动修。它可以诊断、建议、路由和验证。真正写入需要走正确 gate：窄修走已确认
treatment，结构改动走 surgery/OpenSpec，写完再 recovery。

### 第一次应该跑什么？

```bash
python3 scripts/build_wiki_status.py
python3 scripts/build_wiki_medical_agent.py --intent-text "status"
```

然后看 `wiki/status/wiki-status.md` 和 medical agent 返回的 case path。

### 新内容应该放哪里？

- 来源证据：`wiki/sources/`
- 工作流证据和医疗轨迹：`wiki/ops/`
- 稳定决策：`wiki/adr/`
- 已验证示例：`wiki/examples/`
- 生成健康报告：`wiki/status/`

创建或修改 Wiki frontmatter 时，遵循 `wiki/config/frontmatter-taxonomy.yaml`，
并重新运行 checker。
