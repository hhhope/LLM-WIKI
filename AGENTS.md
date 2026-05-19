# LLM-WIKI Agent Entry

Use this repository as an LLM-maintained wiki seed. Global instructions still
own health checks, git truth-source checks, and general execution discipline.
This file owns repo-local wiki runtime gates and seed boundaries.

## Scope

- Read `PROJECT.md` first.
- Treat this repository as a runnable wiki seed, not as a dump of historical
  project material.
- Keep business-specific rules from source repositories out of this seed unless
  a new OpenSpec change proves they are generic wiki behavior.
- Do not treat `README.md` as runtime authority.

## Workflow Change Gate

- Treat changes to repo-default workflow, collaboration behavior, routing
  defaults, taxonomy gates, medical-loop authority, or output routing as
  OpenSpec-level changes.
- Large or semantic workflow changes require an active change under
  `openspec/changes/` with `proposal.md`, `design.md`, and `tasks.md`.
- Short approvals such as `可以`, `继续`, and `加吧` advance only the current
  gate; they do not skip OpenSpec, verification, or git checks.
- Do not copy another repository's full `AGENTS.md` into this seed. Extract only
  seed-level behavior with evidence.

## Intent Routing

- Use `.codex/skills/` for workflow routing.
- For self-running status, diagnosis, confirmation, treatment, surgery,
  recovery, or archive checks, route through `wiki-medical-agent`.
- For OpenSpec proposal, implementation, or archive work, use the matching
  `openspec-*` skill before editing lifecycle files.
- For wiki frontmatter, templates, or frontmatter-generating scripts, use
  `wiki-frontmatter-taxonomy`.
- For source learning, material processing, public report output, meeting-note
  output, and interview reading output, use the matching repo-local skill.

## Wiki Medical Loop

- The normal maintenance loop is: doctor -> review/confirm -> treatment or
  surgery -> recovery.
- The active medical case file is the authority for allowed actions.
- Proposed decisions are not executable. Confirmed decisions define what can be
  treated or planned.
- Do not write relations, taxonomy config, MOC pages, ADRs, AGENTS, skills, or
  OpenSpec lifecycle state from medical-loop previews unless a separate
  approved workflow scopes that write.

## Frontmatter Gate

- `wiki/config/frontmatter-taxonomy.yaml` is the source of truth for wiki
  frontmatter vocabulary and strict-gate rules.
- Do not duplicate the taxonomy vocabulary in `AGENTS.md`.
- Before claiming frontmatter compliance, run:
  `python3 scripts/check_wiki_frontmatter.py`.
- Generated wiki pages under strict-gated paths must emit compliant
  frontmatter.

## Output Routing

- Raw upstream material and evidence records belong in `wiki/sources/`.
- Workflow traces, operating learnings, medical cases, status investigations,
  and repo maintenance evidence belong in `wiki/ops/`.
- Stable cross-change decisions belong in `wiki/adr/`.
- Validated output-shape examples belong in `wiki/examples/`.
- Generated status surfaces belong in `wiki/status/`.

## Verification

- Before claiming the wiki can run, refresh or inspect:
  `python3 scripts/build_wiki_status.py`.
- For graph/runtime health, use the existing graph, scorecard, context, route,
  and self-directed execution scripts as bounded diagnostics only.
- For medical-loop readiness, run:
  `python3 scripts/build_wiki_medical_agent.py --intent-text "<request>"`.
- If a command reports blocked, awaiting confirmation, or preview-only output,
  report that state instead of calling the wiki autonomous.
