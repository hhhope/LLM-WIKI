English | [中文](README.md)

# LLM-WIKI

LLM-WIKI is a project context-engineering repository for AI collaboration. It
organizes source evidence, project knowledge, Agent Skills, governance rules,
and maintenance records into a long-lived LLM-Wiki.

Its goal is not to create a Markdown folder or showcase scripts. Its goal is to
let humans and AI co-build on the same wiki structure: humans provide goals,
judgment, and authorization; AI reads, learns, generates, captures, and reviews;
the wiki stores evidence, context, decisions, and output shapes.

## Architecture

LLM-WIKI has four core layers.

```text
1. Source Layer
   wiki/sources
   Stores evidence from WeChat posts, articles, READMEs, meetings, interviews,
   and project materials.

2. Context Layer
   wiki/ops, wiki/examples, wiki/adr, wiki/status
   Stores workflow traces, output examples, stable decisions, and status
   surfaces.

3. Skill Layer
   .codex/skills
   Defines how agents read, learn, output, diagnose, govern, and verify.

4. Governance Layer
   AGENTS.md, OpenSpec, medical loop, frontmatter taxonomy
   Controls write boundaries, change lifecycle, classification rules, and
   recovery requirements.
```

These layers work together:

- the source layer answers “what evidence does AI rely on?”;
- the context layer lets the next conversation continue from prior work;
- the skill layer tells AI how to act;
- the governance layer controls what can change, who confirms it, and how it is reviewed.

## Governance Design

The governance principle is: **AI can do substantial reading, judgment, and
generation work, but key decisions need boundaries, evidence, and human review.**

Governance is not one-way approval. Inputs are gated, outputs are gated, and
boundary violations trigger review.

```text
External material / user intent
        |
        v
 [Input gates]
 Skill Gate + Learning Gate + Frontmatter Gate
        |
        v
 [AI defaults]
 Read context -> judge boundary -> choose Skill -> generate candidate artifact
        |
        v
 [Human protocol]
 Confirm goal -> make tradeoffs -> authorize writes -> accept release
        |
        v
 [Output gates]
 Public Output Gate + Medical Gate + OpenSpec Gate + Verification Gate
        |
        v
 Wiki / H5 / report / case file / status artifact

Boundary drift or dispute
        |
        v
 Review -> repair skill / taxonomy / OpenSpec / README / examples
```

LLM-WIKI uses three-layer collaboration governance:

```text
1. Human Review Layer
   Humans provide goals, tradeoffs, key confirmation, and acceptance.

2. Agent Skill Layer
   AI uses Skills to read context, judge boundaries, choose routes, generate
   artifacts, and propose repairs.

3. Runtime Evidence Layer
   Wiki pages, case files, status artifacts, and tool output record evidence
   and execute approved actions.
```

Tool scripts live in the third layer. They batch-process, generate status,
write structured records, and run checks. They do not replace AI judgment or
human review.

The human-side protocol is fixed: goals, judgments, authorization, and
acceptance stay with humans. The AI-side default is Skills: read context and
boundaries first, choose the route, then explain outputs with evidence. The
tool-side rule is narrower: tools record and check; preview, score, or script
output does not automatically become fact, rule, or approval.

### Gates

Primary gates are split between input and output:

- **Skill Gate**: agents match `.codex/skills/` before acting.
- **Learning Gate**: external material enters through `learning-capture` with
  source, reuse boundary, and target location.
- **Frontmatter Gate**: wiki pages follow `wiki/config/frontmatter-taxonomy.yaml`.
- **Public Output Gate**: README, H5, reports, and public examples go through
  `public-report-quality-gate`.
- **Medical Gate**: wiki self-maintenance goes through `wiki-medical-agent` and
  case files.
- **OpenSpec Gate**: governance, structure, and lifecycle changes go through
  OpenSpec.
- **Verification Gate**: completion claims go through `verify-before-claiming`
  with fresh evidence.

Input gates decide whether material enters, what identity it has, and where it
lands. Output gates decide whether artifacts can be published, rules can take
effect, and governance changes can be recorded. They prevent plausible-looking
AI output from becoming facts, rules, or structure without review.

## Featured Skills

Skills are not a command list. They are the agent's default operating
protocols. They connect user intent, external material, wiki context,
reader-facing artifacts, and governance changes into reviewable loops.

```text
Intent / material
   |
   v
Learning Intake -> Context Retrieval -> Output / Medical / Governance
   |                    |                         |
   v                    v                         v
sources / ops      status / graph            report / case / OpenSpec
   \____________________ evidence + review ____________________/
```

### 1. Learning Intake

Decides how external input enters long-lived context.

- `learning-capture` is the router: material identity, reuse boundary, and
  landing place come first.
- `readme-learning-capture` handles repo/README learning: transferable design
  choices are extracted, structures that should not be copied are rejected.
- `weixin-reader` is a reader: it fetches WeChat article bodies into Markdown;
  it does not own later judgment.
- `material-collaboration-defaults` handles meetings, attachments, report
  material, and preview drafts already dropped into the repo.

This group answers: what the material is, whether it is worth capturing, which
layer receives it, and how future agents should reuse it.

### 2. Context Retrieval

Lets agents retrieve evidence from the wiki instead of continuing from the
current chat alone.

- `wiki-query` combines routing, context, and text search.
- `wiki-context` reads the runtime context bundle.
- `wiki-route` returns source-integrated routing suggestions.
- `wiki-status` and `wiki-manifest` inspect current status and source lists.
- `wiki-graph` and `wiki-scorecard` inspect relations, coverage, and semantic
  health.

This group provides diagnostics and context. It does not authorize writes by
itself.

### 3. Medical Maintenance

Supports wiki self-maintenance without becoming an auto-repair bot.

```text
wiki-medical-agent
        |
        v
doctor -> review/confirm -> treatment or surgery -> recovery
诊断   -> 确诊           -> 治疗 or 手术      -> 复查
```

`wiki-medical-agent` is the normal entry. `wiki-doctor`,
`wiki-review-decisions`, `wiki-treatment`, `wiki-surgery`, and `wiki-recovery`
are stage capabilities. AI diagnoses and proposes; humans confirm key
decisions; tools execute approved actions; recovery records evidence.

### 4. Reader-Facing Output

Turns material into reader-facing artifacts without publishing internal drafts.

- `public-report-quality-gate` owns reader intent, structure, citation, and
  judgment ownership for README, H5, reports, and public examples.
- `interview-deep-reading-board` owns interview deep reads, evidence boards,
  timelines, and temperature-axis outputs.
- `meeting-note-output` owns meeting-note outputs.
- `project-management-weekly-skill` owns project weekly reports, milestones,
  and risk communication.

This group answers: who reads it, what judgment the reader needs to make, what
structure carries the evidence, and when the artifact can be published.

### 5. Governance Promotion

Promotes candidate judgments into rules, structures, or lifecycle changes.

- `openspec-router`
- `openspec-propose`
- `openspec-apply-change`
- `openspec-archive-change`
- `wiki-frontmatter-taxonomy`
- `verify-before-claiming`
- `clarify-before-acting`
- `simplicity-first`
- `surgical-changes`

This group controls the upgrade path: clarify the boundary, minimize the
change, then record structural changes through OpenSpec, taxonomy, and fresh
verification evidence. Anything that has not passed this path remains a draft,
candidate observation, or local artifact.

## Example: WeChat Article To H5 / Report

The input is not just an article. It is material plus intent:

- a WeChat article;
- the target artifact, such as an H5 deep read, report draft, card, timeline,
  temperature axis, or evidence board;
- reader, usage scenario, and whether the result should be captured into the
  wiki.

Recommended path:

```text
1. User intent -> learning-capture
   The agent first decides whether the material is evidence, method reference,
   case material, output work, or candidate observation.

2. Choose the reader by material shape
   If the source is mp.weixin.qq.com, call weixin-reader to fetch the body. If
   the material already lives in the repo, use material-collaboration-defaults.
   If it is a README or repo, use readme-learning-capture.

3. Choose the artifact path by intent
   H5, report, card, evidence board, timeline, and temperature axis are not
   fixed outputs. The user's intent and reader goal decide the shape.

4. wiki/sources + wiki/ops
   Store source evidence, summaries, reusable methods, disputes, output-use
   hints, and next actions.

5. public-report-quality-gate / interview-deep-reading-board
   For reader-visible H5, reports, or deep-reading artifacts, pass reader
   intent, structure, citation, and judgment-ownership gates first.

6. verify-before-claiming / medical loop
   Verify that the target artifact and wiki capture both exist. Route
   structural, rule, or wiki governance changes to the medical loop or OpenSpec.
```

This is AI co-building: AI reads, extracts structure, judges boundaries,
selects Skills, generates artifacts, captures context, and triggers review;
humans own goals, judgment, authorization, and acceptance.

## Project Structure

```text
LLM-WIKI/
├── AGENTS.md                         # Agent rules for this repository
├── PROJECT.md                        # Project identity
├── README.md                         # Chinese entry
├── README.en.md                      # English entry
├── .codex/skills/                    # Agent Skills
├── openspec/changes/                 # Governance/change lifecycle
├── scripts/                          # Tool layer: batch processing, status, checks
└── wiki/
    ├── sources/                      # Source evidence
    ├── ops/                          # Workflow traces, medical cases, governance evidence
    ├── examples/                     # Reusable output shapes
    ├── adr/                          # Stable decisions
    ├── config/                       # Taxonomy and behavior-asset config
    ├── status/                       # Generated status surfaces
    ├── moc/                          # MOC projection target directory
    ├── domains/                      # Domain indexes
    ├── reports/                      # Report outputs
    ├── templates/                    # Page templates
    └── timeline/                     # Timeline records
```

## Entry Points

- `AGENTS.md`: agent rules and stop conditions;
- `.codex/skills/`: Agent Skills;
- `wiki/sources/`: source evidence;
- `wiki/ops/`: collaboration, medical, governance, and method records;
- `wiki/examples/`: reusable output shapes;
- `wiki/status/wiki-status.md`: current status surface;
- `wiki/config/frontmatter-taxonomy.yaml`: page classification rules.

## Boundaries

- README is a reader entry, not runtime authority.
- Runtime authority lives in `AGENTS.md`, Skills, OpenSpec, case files, and
  status artifacts.
- Tool output is evidence, not judgment.
- External learning cannot become a rule directly; it must pass capture,
  evidence, and the proper gate.
- Medical previews are not repair permission.
