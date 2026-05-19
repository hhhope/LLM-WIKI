English | [中文](README.md)

# LLM-WIKI

LLM-WIKI is a project context-engineering repository for AI collaboration. It
organizes project knowledge, source evidence, Agent Skills, governance rules,
and maintenance records into a long-lived LLM-Wiki.

The goal is not to store Markdown files. The goal is human-AI co-building on a
shared knowledge structure:

- humans own goals, judgment, authorization, and acceptance;
- AI reads material, extracts structure, selects skills, generates artifacts,
  and proposes repairs;
- the wiki stores evidence, context, decisions, examples, and status;
- governance limits writes, confirms risk, and reviews results.

## Design Principles

### Context Engineering

LLM-WIKI follows Karpathy’s context engineering idea: instead of forcing all
context into a single chat window, organize project knowledge into a structure
agents can keep reading and updating.

### Skill First

Agent actions go through `.codex/skills/` first. Skills define reading,
writing, learning capture, output generation, diagnosis, recovery, and stop
conditions. Batch scripts are only tools; they do not own judgment.

### Evidence First

External material keeps source boundaries before entering the wiki. Claims,
methods, and output shapes must trace back to source evidence or operation
records.

### Human Review First

Diagnosis, previews, and suggestions are not write permission. Structural,
governance, rule, or high-risk output changes require human confirmation.

## Three-Layer Collaboration Governance

```text
1. Human Review Layer
   Humans provide goals, tradeoffs, key confirmation, and acceptance.

2. Agent Skill Layer
   AI uses skills to read context, judge boundaries, choose routes, generate
   artifacts, and propose repairs.

3. Runtime Evidence Layer
   Wiki pages, case files, status artifacts, and script output record evidence
   and execute approved actions.
```

All three layers are required before an operation can be treated as complete.

## Four-Layer Context Architecture

```text
1. Source Layer
   wiki/sources
   Stores evidence from articles, WeChat posts, READMEs, meetings, interviews,
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

## Core Loop 1: Learning Capture

`learning-capture` is the main entry for external information.

It does not simply summarize material. It decides how material should enter
long-lived context:

- should it be preserved as source evidence?
- does it contain a reusable method?
- should it become an output example?
- is it only a candidate observation?
- does it require OpenSpec, medical loop, or public report gate?

Typical path:

```text
article / WeChat post / README / meeting / interview / project material
-> learning-capture classifies source type and reuse boundary
-> wiki/sources stores evidence
-> wiki/ops stores methods, decisions, and collaboration traces
-> wiki/examples stores reusable output shapes
-> future agents reuse it through wiki-query / wiki-context / wiki-route
```

Related skills:

- `learning-capture`
- `readme-learning-capture`
- `weixin-reader`
- `material-collaboration-defaults`
- `interview-deep-reading-board`
- `meeting-note-output`
- `project-management-weekly-skill`
- `public-report-quality-gate`

## Core Loop 2: Agent Skills

`.codex/skills/` is the agent operating layer. It determines how agents act in
this repository.

Main skill groups:

- Context lookup: `wiki-query`, `wiki-context`, `wiki-route`
- Status diagnosis: `wiki-status`, `wiki-manifest`, `wiki-graph`, `wiki-scorecard`
- Bounded suggestions: `wiki-apply`
- Frontmatter: `wiki-frontmatter-taxonomy`
- Governance changes: `openspec-router`, `openspec-propose`,
  `openspec-apply-change`, `openspec-archive-change`
- Completion verification: `verify-before-claiming`
- Collaboration guardrails: `clarify-before-acting`, `simplicity-first`,
  `surgical-changes`

## Core Loop 3: Medical Agent

Medical Agent is the safe entry for wiki self-maintenance.

```text
doctor -> review/confirm -> treatment or surgery -> recovery
诊断   -> 确诊           -> 治疗 or 手术      -> 复查
```

Related skills:

- `wiki-medical-agent`
- `wiki-doctor`
- `wiki-confirm`
- `wiki-review-decisions`
- `wiki-treatment`
- `wiki-surgery`
- `wiki-recovery`

Medical Agent converges maintenance state into a case file. AI interprets the
case file, humans confirm key decisions, and tools execute only approved narrow
actions while leaving recovery evidence.

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
   Verify the artifact exists. Route structural or rule changes to medical loop
   or OpenSpec.
```

This is AI co-building: AI reads, extracts, judges, routes, generates, captures,
and reviews; humans own goals, judgment, authorization, and acceptance.

## Project Structure

```text
LLM-WIKI/
├── AGENTS.md                         # Agent rules for this repository
├── PROJECT.md                        # Project identity
├── README.md                         # Chinese entry
├── README.en.md                      # English entry
├── .codex/skills/                    # Agent Skills
├── openspec/changes/                 # Governance/change lifecycle
├── scripts/                          # Tool layer: batch processing and checks
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

## Key Entry Points

- `AGENTS.md`: agent rules and stop conditions;
- `.codex/skills/`: Agent Skills;
- `wiki/sources/`: source evidence;
- `wiki/ops/`: collaboration, medical, governance, and method records;
- `wiki/examples/`: reusable output shapes;
- `wiki/status/wiki-status.md`: current status surface;
- `wiki/config/frontmatter-taxonomy.yaml`: page classification rules.

## Boundaries

- README is a reader entry, not runtime authority.
- Runtime authority lives in `AGENTS.md`, skills, OpenSpec, case files, and
  status artifacts.
- Script output is tool-layer evidence, not judgment.
- External learning cannot become a rule directly; it must pass capture,
  evidence, and the proper gate.
- Medical previews are not repair permission.

## FAQ

### What does AI own here?

AI reads material, extracts structure, judges boundaries, selects skills,
generates artifacts, captures context, and triggers diagnosis or recovery.
Humans own goals, tradeoffs, authorization, and final acceptance.

### What do scripts own here?

Scripts handle batch processing, structured output, status generation,
frontmatter checks, and case refreshes. They do not replace AI judgment or
human review.

### Where should I start?

Start with `AGENTS.md`, `.codex/skills/`, `wiki/status/wiki-status.md`,
`wiki/sources/`, and `wiki/ops/`. Then let the agent choose the next route
through `wiki-query`, `wiki-context`, or `wiki-medical-agent`.
