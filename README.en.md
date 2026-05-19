English | [中文](README.md)

# LLM-WIKI

A runnable Markdown wiki seed maintained by agents.

This is not a packaged `llm-wiki` installer. It is a working seed repository:
repo-local skills, frontmatter taxonomy, status surfaces, runtime scripts, and
a medical-style maintenance loop live together so an agent can inspect,
diagnose, repair, and verify the wiki with bounded evidence.

This README follows the documentation shape of
[`sdyckjq-lab/llm-wiki-skill`](https://github.com/sdyckjq-lab/llm-wiki-skill):
positioning, quick start, highlights, structure, commands, and FAQ. The content
is specific to `LLM-WIKI`; it does not copy that project's installer, platform
matrix, graph demo, or optional source adapters.

## What This Is

LLM-WIKI is a seed repository for maintaining a Markdown wiki through an agent
workflow.

Core flow:

```text
preserve source evidence -> normalize wiki pages -> check taxonomy and graph
-> diagnose drift -> confirm safe changes -> treat or plan surgery -> recover
```

The current seed includes:

- a small wiki under `wiki/`;
- repo-local skills under `.codex/skills/`;
- strict frontmatter taxonomy configuration;
- status, graph, scorecard, context, routing, and medical-loop scripts;
- OpenSpec change records for governance changes;
- generated status artifacts that show what is healthy, drifting, blocked, or
  awaiting confirmation.

## 30-Second Start

From the repository root:

```bash
python3 scripts/build_wiki_status.py
python3 scripts/check_wiki_frontmatter.py
python3 scripts/extract_wiki_graph.py
python3 scripts/build_wiki_medical_agent.py --intent-text "status"
```

Start with these surfaces:

- `wiki/status/wiki-status.md`: current wiki health;
- `AGENTS.md`: repo-local agent routing and stop rules;
- `PROJECT.md`: project identity;
- `wiki/config/frontmatter-taxonomy.yaml`: wiki frontmatter rules;
- `.codex/skills/wiki-medical-agent/SKILL.md`: normal medical maintenance entry.

## Project Structure

```text
LLM-WIKI/
├── AGENTS.md                         # Repo-local agent rules and runtime gates
├── PROJECT.md                        # Project identity and source-of-truth note
├── README.md                         # Chinese entry
├── README.en.md                      # English entry
├── .codex/skills/                    # Repo-local workflow and wiki skills
├── openspec/changes/                 # Active/completed governance changes
├── scripts/                          # Runtime diagnostics and generators
└── wiki/
    ├── adr/                          # Stable decisions
    ├── config/                       # Taxonomy and behavior-asset config
    ├── domains/                      # Domain indexes
    ├── examples/                     # Validated output-shape examples
    ├── moc/                          # MOC projection target directory
    ├── ops/                          # Medical cases, traces, workflow evidence
    ├── reports/                      # Report index and report outputs
    ├── sources/                      # Source records and sanitized evidence
    ├── status/                       # Generated status artifacts
    ├── templates/                    # Wiki page templates
    └── timeline/                     # Timeline index and records
```

## Key Configuration

`wiki/config/frontmatter-taxonomy.yaml`

- Defines wiki layer, domain, and ops-area rules.
- Defines which wiki pages are covered by the strict gate.
- Drives `scripts/check_wiki_frontmatter.py`.

`wiki/config/behavior-asset-evaluation.yaml`

- Defines evaluation expectations for skills, rules, AGENTS, and other
  behavior assets.
- Keeps governance changes evidence-oriented rather than cosmetic.

`AGENTS.md`

- Explains how agents should route work inside this repository.
- Keeps README non-authoritative for runtime behavior.
- Points maintenance work to OpenSpec, the wiki medical loop, and verification
  commands.

`PROJECT.md`

- Provides project identity through frontmatter.
- Marks this repository as a runnable wiki seed.

## Highlight Skills

Repo-local skills are the main interface an agent should use before acting.

### Wiki Runtime

- `wiki-status`: refresh and summarize `wiki/status/`.
- `wiki-manifest`: inspect source and routing manifest outputs.
- `wiki-graph`: inspect graph extraction and relation health.
- `wiki-scorecard`: inspect semantic scoring and utilization diagnostics.
- `wiki-context`, `wiki-route`, `wiki-apply`: inspect bounded runtime context,
  routing, and self-directed execution suggestions.

### Medical Loop

- `wiki-medical-agent`: the normal entry point for diagnosis, confirmation,
  treatment, surgery, recovery, and archive checks.
- `wiki-doctor`, `wiki-confirm`, `wiki-treatment`, `wiki-surgery`,
  `wiki-recovery`: stage-specific evidence surfaces for explicit checks or
  bounded follow-up.
- `wiki-review-decisions`: builds confirmation records from adjudication output.

### Governance And Change Flow

- `openspec-router`: routes OpenSpec, Superpowers, and governance work before
  edits.
- `openspec-propose`: creates change artifacts.
- `openspec-apply-change`: implements an approved change.
- `openspec-archive-change`: archives only after archive review passes.
- `verify-before-claiming`: requires fresh evidence before completion claims.

### Source And Output Work

- `learning-capture` and `readme-learning-capture`: capture reusable learning
  from articles, repositories, README files, and examples.
- `material-collaboration-defaults`: route source materials into readable wiki
  records.
- `public-report-quality-gate`: control reader-facing outputs such as README,
  docs, examples, and public report drafts.
- `interview-deep-reading-board`, `meeting-note-output`,
  `project-management-weekly-skill`: specialized output workflows.

## Medical Maintenance Model

LLM-WIKI uses a medical metaphor to keep agents from applying speculative
repairs directly.

```text
doctor -> review/confirm -> treatment or surgery -> recovery
诊断   -> 确诊           -> 治疗 or 手术      -> 复查
```

Core rule: **the active case file is the authority for allowed action**. A
preview, diagnosis, or suggestion is not write permission.

The stages mean:

- **Doctor**: find candidate issues, drift, weak evidence, and structural risk.
- **Review / Confirm**: decide what is accepted, rejected, deferred, safe for
  treatment, surgery-required, or OpenSpec-required.
- **Treatment**: apply narrow, explicitly approved, low-risk fixes.
- **Surgery**: plan structural, governance, taxonomy, ADR, relation, or MOC
  changes.
- **Recovery**: rerun checks and record what changed, what remains blocked, and
  the next action.

Commands may return `awaiting_confirmation`, `preview_only`, or `blocked`.
Those are valid safety states, not failures to hide.

## Common Commands

### Status

```bash
python3 scripts/build_wiki_status.py
```

Writes:

- `wiki/status/manifest.json`
- `wiki/status/wiki-status.md`

### Frontmatter Check

```bash
python3 scripts/check_wiki_frontmatter.py
```

Run this before claiming taxonomy compliance.

### Graph Extraction

```bash
python3 scripts/extract_wiki_graph.py
python3 scripts/analyze_wiki_relations.py
```

Use these to inspect canonical objects, graph parse health, and relation drift.

### Scorecard And Runtime Context

```bash
python3 scripts/score_wiki_semantics.py
python3 scripts/summarize_wiki_scorecard.py
python3 scripts/build_wiki_runtime_context.py
python3 scripts/resolve_runtime_context_sources.py
python3 scripts/derive_runtime_auto_routing.py
python3 scripts/build_runtime_context_injection.py
python3 scripts/derive_self_directed_execution.py
```

These scripts are diagnostic. They do not prove full autonomy and should not be
treated as permission to execute queued work.

### Medical Agent

```bash
python3 scripts/build_wiki_medical_agent.py --intent-text "status"
```

Use this as the normal maintenance entry.

### Medical Stages

```bash
python3 scripts/build_wiki_medical_case.py
python3 scripts/build_wiki_review_decisions.py
python3 scripts/build_wiki_treatment.py
python3 scripts/build_wiki_surgery.py
python3 scripts/build_wiki_recovery.py
```

Stage commands are bounded by the case file and repo gates. Do not treat preview
output as approval to write unrelated wiki, taxonomy, ADR, MOC, OpenSpec, or
skill changes.

## Current Seed Health

Verified baseline at the time of this README update:

- frontmatter checker: `0` errors, with non-blocking producer warnings
  remaining;
- graph extraction: nodes are generated, relation coverage is still thin;
- medical agent: status reporting works, with the active case still
  `awaiting_confirmation`;
- OpenSpec: the self-running governance bootstrap is complete and ready for
  archive review, not automatically archived.

Run `python3 scripts/build_wiki_status.py` for the latest state instead of
trusting this snapshot.

## Boundaries

- This seed copies the system shape, not private history.
- `wiki/sources/` preserves source evidence; do not replace it with unsourced
  summaries.
- README explains the project for readers. Runtime authority lives in
  `AGENTS.md`, repo-local skills, OpenSpec changes, and generated status
  artifacts.
- Medical-loop previews are not permission to repair.
- MOC projection, content enrichment, content adjudication, and self-directed
  execution are diagnostic surfaces unless an approved workflow scopes a write.

## FAQ

### Is this the same as `sdyckjq-lab/llm-wiki-skill`?

No. That project is a multi-platform personal knowledge-base skill with
installers and source adapters. This repository is a runnable wiki seed focused
on repo-local governance, taxonomy checks, OpenSpec records, and medical-style
maintenance.

### Can I open it in Obsidian?

Yes. The wiki content is Markdown-first. Some generated diagnostics are aimed
at agents, but the pages can still be opened as ordinary Markdown.

### Does the wiki repair itself automatically?

No. It can diagnose, suggest, route, and verify. Actual writes require the right
gate: confirmed treatment for narrow fixes, surgery/OpenSpec for structural
changes, and recovery after writes.

### What should I run first?

```bash
python3 scripts/build_wiki_status.py
python3 scripts/build_wiki_medical_agent.py --intent-text "status"
```

Then inspect `wiki/status/wiki-status.md` and the case path returned by the
medical agent.

### Where should new content go?

- Source evidence: `wiki/sources/`
- Workflow evidence and medical traces: `wiki/ops/`
- Stable decisions: `wiki/adr/`
- Validated examples: `wiki/examples/`
- Generated health reports: `wiki/status/`

When creating or modifying wiki frontmatter, follow
`wiki/config/frontmatter-taxonomy.yaml` and rerun the checker.
