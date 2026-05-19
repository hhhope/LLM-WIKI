---
title: agentic-product-engineering-collaboration / lixiang-luoyonghao ai-agent reading
canonical_object: agentic-product-engineering-collaboration
artifact_type: source-reading-note
layer: sources
domain: product-engineering-collaboration
source_type: external-wechat-article
created: 2026-05-18
source_url: https://mp.weixin.qq.com/s/Cz3fyYoqNdsSUFFtJdij7A
source_title: 李想罗永浩26年5月对话视频版/文字版
source_date: 2026-05-13
status: text-used-for-draft
target:
  - wiki/reports/agentic-product-engineering-collaboration-our-operating-system.html
---

# Agentic Product Engineering Collaboration / Li Xiang And Luo Yonghao AI-Agent Reading

## Source Reference

- Source: `李想罗永浩26年5月对话视频版/文字版`
- URL: https://mp.weixin.qq.com/s/Cz3fyYoqNdsSUFFtJdij7A
- Published: 2026-05-13
- Accessed: 2026-05-18
- Source class: secondary interview transcript / operator method reference
- Source artifact: extracted Markdown from `weixin-reader`
- Copyright boundary: this note preserves paraphrased learning only, not the full transcript.

## Admission And Score

Score timing: retrospective. The user explicitly asked to use this article for
the current H5, so the source was fetched before the formal score record.

| Field | Result |
|---|---|
| Admission gate | Pass: original WeChat body was fetched and metadata preserved. |
| Source class | Secondary interview transcript / method reference. |
| Total score | 82 / 100, capped by secondary-source status. |
| Score band | Deep-read and write durable notes. |
| Decision | Use for H5 text calibration and keep as candidate learning, not as a hard rule. |

Score breakdown:

| Criterion | Score |
|---|---:|
| Source access and provenance | 18 / 20 |
| Evidence or method density | 22 / 25 |
| Local capability gain | 23 / 25 |
| Transfer path | 11 / 15 |
| Verification path | 8 / 15 |

## Case Notes For Current H5

### Case 1: Research Team Built A Cowork Demo First

The transcript's strongest collaboration case is the research / strategy group:
a research lead brought several new graduates, studied Anthropic's workflow, and
built a Cowork-like Demo instead of producing a traditional PRD. The Demo
covered work collaboration, data connection, cloud/local model routing, and
work-value measurement. They then validated collaboration with HR and data
connection with the data warehouse team.

Local transfer: use this as a case for "professional people move earlier into
verifiable artifacts." Research/product can make the problem runnable first;
engineering, data, security, and operations owners then turn it into a stable
production system.

### Case 2: Agent Workflow For Making Plans

Li Xiang describes his own Agent workflow as:

1. ask Agent to analyze;
2. ask it to produce multiple competing plans;
3. let the plans score or challenge each other;
4. optimize the plan;
5. human chooses;
6. execute based on the chosen plan.

Local transfer: this is the source for adding `多方案验证` before Spec / ADR.
It makes the discussion visible and verifiable instead of relying on a leader's
implicit intent or a single preselected plan.

### Case 3: Chassis AI And 200ms / 400ms Reaction Gap

The chassis case is a strong "vertical system" example. The useful claim for
this H5 is not that our topic is automotive hardware; it is that vertical AI
value comes from perception-to-execution optimization. Human reaction from
seeing an object to braking and execution is described as roughly 350-400ms;
older autonomous-driving reaction is described as around 400ms; the new system
is described as a little over 200ms. A separate brake-by-wire detail contrasts
older mechanical braking at roughly 60-70ms with electronic brake-by-wire at
13ms.

Local transfer: use this as analogy, not technical proof. In product-engineering
collaboration, the equivalent is not one smarter model, but shortening the whole
chain from intent -> plan -> spec -> execution -> evidence -> decision ->
writeback.

### Case 4: In-Car Agent Architecture Splits Generic And Deterministic Work

The transcript splits user needs into generic tasks, generic information
retrieval, precise control, necessary records, and personalization. It also
contrasts an Agent-heavy weather query that wastes minutes and tokens with a
local car interface that returns quickly and cheaply.

Local transfer: generic Agent capability and deterministic vertical capability
should coexist. Use general models for exploration and plans; use stable local
interfaces, rules, tests, and governed data access where the job is known and
must be reliable.

## Reusable Learning

### 1. Agent Needs A Real Production Environment

The transcript separates broad consumer AI use from agentic work. General AI can
act like an upgraded search or answer surface, but Agent work needs a real
task environment, production context, and feedback chain. Without that
environment, users quickly lose meaningful feedback.

Use in H5: strengthen the distinction between generic AI adoption and vertical
production workflows. Our target is not "everyone uses AI", but "our real
product-engineering chain becomes agent-readable, executable, and reviewable".

### 2. Professional People Still Matter More, Not Less

The transcript pushes back on the claim that professional work is simply
replaced. AI raises the ceiling for people who already understand the domain,
taste, constraints, and production consequences. Non-specialists can create a
demo, but production deployment still needs professional engineering,
architecture, testing, security, and operations judgment.

Use in H5: keep the role-change section away from "all roles become coders".
The sharper message is: professional people move closer to executable artifacts,
and each role owns a harder, more valuable part of the chain.

### 3. Build Verifiable Demos Before Formal Production

The useful product/strategy pattern is not writing longer PRDs. A specialist can
turn a question into a verifiable demo or competing方案, then engineers take the
validated path into scalable production.

Use in H5: add a step before formal engineering execution: ask Agent to analyze,
generate multiple方案, score tradeoffs, optimize the selected方案, and let the
human owner choose what becomes production work.

### 4. From Certainty Control To Capability Growth

The interview describes a management shift: when AI and Agent workflows become
normal, leaders should stop demanding premature certainty and instead set better
questions, ask for competing verifiable方案, and select from visible tradeoffs.

Use in H5: strengthen the "Boss / owner" role. Management should not measure AI
usage rate; it should ask whether the question is right, whether the方案 are
verifiable, and whether professional owners can turn them into production.

### 5. Hard And Correct Work Is Collaboration Infrastructure

The transcript names work-collaboration, data access, and value measurement as
hard problems after personal productivity improves. The local adaptation should
be conservative: do not let Agent read production data freely; instead create
governed data access, evidence matrices, and review packets.

Use in H5: keep the article's "do hard and correct things" direction, but adapt
it to our repo boundary: intent packets, specs, governed evidence, real DB/API
checks, review packets, and failure writeback.

## Adaptation Boundary

- Do not claim the transcript proves our workflow is correct.
- Do not import the car-company strategy, hardware, embodied-intelligence, or
overseas-business sections into this H5.
- Do not turn "direct database reading" into an unsafe local rule. Our use is
  governed real-data verification and access-controlled evidence.
- Do not use this as proof for layoffs, org design, or headcount decisions.

## Output Use

| Capability type | Learning point | H5 use |
|---|---|---|
| content | Agent needs real production feedback, not generic chat usage. | Added text calibration around generic vs vertical AI work. |
| structure | Analyze, produce competing方案, score, optimize, human choose, execute. | Added into the nine-step workflow and 30-day pilot. |
| boundary | Specialist value increases when AI turns expertise into executable artifacts. | Strengthened role-change and final-judgment sections. |
| evidence | Hard problems are collaboration, data access, and value measurement. | Used as a boundary for governed evidence and review packets. |
| evidence | Cowork Demo, chassis 200ms/400ms contrast, and in-car Agent architecture show that vertical systems beat isolated generic tool use. | Rewrote section `05A · 新材料校准` as case-led reasoning from point to system-level conclusion. |

## Next Step

Use this note as a source-learning record for the current text draft only. Image
scripts and share-package updates are explicitly deferred until the user confirms
the text direction.
