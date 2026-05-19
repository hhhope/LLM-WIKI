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

### Gates

Primary gates:

- **Skill Gate**: agents match `.codex/skills/` before acting.
- **Learning Gate**: external material enters through `learning-capture` with
  source, reuse boundary, and target location.
- **Public Output Gate**: README, H5, reports, and public examples go through
  `public-report-quality-gate`.
- **Frontmatter Gate**: wiki pages follow `wiki/config/frontmatter-taxonomy.yaml`.
- **Medical Gate**: wiki self-maintenance goes through `wiki-medical-agent` and
  case files.
- **OpenSpec Gate**: governance, structure, and lifecycle changes go through
  OpenSpec.
- **Verification Gate**: completion claims go through `verify-before-claiming`
  with fresh evidence.

The gates prevent plausible-looking AI output from becoming facts, rules, or
structure without review.

## Featured Skills

### 1. Input To Long-Lived Context

These are not four duplicate entry points. They are different roles in one
input chain.

- `learning-capture`: the router. It decides whether an external input should
  become learning, what the reuse boundary is, and where it should land.
- `readme-learning-capture`: the repo/README module. It handles GitHub/GitLab
  projects, README structure, reusable design choices, and what should not be
  copied.
- `weixin-reader`: the WeChat reader. It only fetches `mp.weixin.qq.com`
  article bodies into Markdown; later analysis belongs to learning or output
  skills.
- `material-collaboration-defaults`: the material collaboration route. It
  handles meeting notes, attachments, preview drafts, report material, and
  other source files already dropped into the repo.

This chain decides:

- whether material should be captured;
- whether it belongs in `wiki/sources`, `wiki/ops`, or `wiki/examples`;
- what remains a candidate observation;
- how future agents should reuse it.

### 2. Agent Context

Lets agents retrieve wiki context instead of relying only on the current chat.

- `wiki-query`
- `wiki-context`
- `wiki-route`
- `wiki-status`
- `wiki-manifest`
- `wiki-graph`
- `wiki-scorecard`

### 3. Medical Loop

Supports safe wiki self-maintenance.

- `wiki-medical-agent`
- `wiki-doctor`
- `wiki-confirm`
- `wiki-review-decisions`
- `wiki-treatment`
- `wiki-surgery`
- `wiki-recovery`

Medical loop:

```text
doctor -> review/confirm -> treatment or surgery -> recovery
诊断   -> 确诊           -> 治疗 or 手术      -> 复查
```

Medical Agent does not auto-repair. It converges maintenance state into a case
file: AI interprets, humans confirm, tools execute approved actions, and
recovery records evidence.

### 4. Public Output

Turns material into reader-facing artifacts.

- `public-report-quality-gate`
- `interview-deep-reading-board`
- `meeting-note-output`
- `project-management-weekly-skill`

These skills control README, H5, reports, interview deep reads, meeting notes,
and project weekly outputs so internal drafts are not treated as publishable
artifacts.

### 5. Governance

Controls structural changes and completion claims.

- `openspec-router`
- `openspec-propose`
- `openspec-apply-change`
- `openspec-archive-change`
- `wiki-frontmatter-taxonomy`
- `verify-before-claiming`
- `clarify-before-acting`
- `simplicity-first`
- `surgical-changes`

## Example: WeChat Article To H5 / Report

Input: a WeChat article.  
Goal: generate an H5 deep-reading page, report draft, card, or evidence board.

Recommended path:

```text
1. weixin-reader
   Fetch or structure the WeChat material and preserve source boundaries.

2. learning-capture
   Decide whether the material is evidence, method reference, case material, or
   candidate observation.

3. wiki/sources + wiki/ops
   Store source evidence, summaries, reusable methods, disputes, and next
   actions.

4. public-report-quality-gate / interview-deep-reading-board
   Choose the output gate and structure from the reader goal.

5. Output artifact
   H5, report, card, timeline, temperature axis, or evidence board is written to
   the target artifact path or wiki/examples.

6. verify-before-claiming / medical loop
   Verify the artifact exists. Route structural, rule, or wiki governance
   changes to the medical loop or OpenSpec.
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
