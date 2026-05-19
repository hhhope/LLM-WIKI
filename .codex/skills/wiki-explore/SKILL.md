---
name: wiki-explore
description: Use when the user explicitly invokes wiki:explore, or when an ongoing wiki-backed exploration is rejected as shallow, incomplete, off-target, or not enough.
---

# Wiki Explore

Use this as the repo's evidence-depth exploration surface. It is not a
replacement for `wiki-query`; use `wiki-query` for bounded retrieval and
`wiki-explore` when the user needs a depth judgment.

For ambiguous, rejected, or high-risk exploration, emit a compact
`decision_trace` using `wiki/ops/wiki-react-decision-trace-runtime.md` before
choosing whether the route is static precheck, exploratory scoring,
OpenSpec/proposal, or stop.

## When To Use

Use this skill when:

- The user explicitly invokes `wiki:explore`.
- An ongoing wiki-backed exploration, source review, report repair, or
  governance replay is rejected as shallow, incomplete, off-target, or not
  enough.
- The user asks what remains in an explored wiki topic and the answer depends
  on existing `wiki/ops`, `wiki/sources`, `wiki/reports`, specs, or skills.

Do not use this skill for ordinary one-off file lookup. Use `wiki-query` for
bounded retrieval only.

## Required Output

Every answer under this skill must include:

- Current object: exact topic/thread/report/source set being explored.
- Opened evidence: concrete repo-visible files or source groups opened.
- Evidence surface: which source map, timeline, public pool, evidence matrix,
  gate review, output draft, and residual-risk artifacts exist or are missing.
- Enoughness judgment: what the current evidence is enough for and not enough
  for.
- Next boundary: continue exploring, harden sources, propose OpenSpec, repair a
  report, or stop.

## Gates

Load `references/behavior-gate.md` for the detailed replay gates.

## Boundaries

- Do not create, modify, archive, or queue OpenSpec changes from this skill.
- Do not mark OpenSpec tasks complete.
- Do not execute queued work.
- Do not claim semantic search, embeddings, or hidden ranking.
- Recommend a new OpenSpec change only when behavior or default workflow should
  change.
