# Proposal: consolidate learning and explore gates

## Summary

Consolidate repo/README learning into `learning-capture`, tighten
`openspec-explore` as a read-only exploration stance, and add an explicit
missing-local-skill stop gate to `AGENTS.md`.

## Problem

`LLM-WIKI` currently exposes two active runtime surfaces for the same
repo/README learning intent:

- `.codex/skills/learning-capture/SKILL.md`
- `.codex/skills/readme-learning-capture/SKILL.md`

The `learning-capture` repo/README module still delegates back to the retired
surface shape, so future agents can keep loading the wrong entry.

`openspec-explore` is still the upstream generic text. It says exploration is a
stance, but it does not explain this repository's boundaries: read-only
exploration, no implementation, no behavior-asset edits during explore, and
OpenSpec artifacts only when explicitly requested.

`AGENTS.md` also lacks a clear missing-local-skill gate. If a historical skill
name remains in memory or in old wiki notes, an agent could continue as if the
skill loaded even when the repo-local file is absent.

## Scope

In scope:

- Retire the active `readme-learning-capture` skill surface.
- Move repo/README scorecard and pressure scenarios under
  `learning-capture/references/`.
- Make `learning-capture/references/repo-readme.md` self-contained.
- Update `AGENTS.md` so repo/README learning routes only through
  `learning-capture`, and missing local skill files stop the route.
- Update `.codex/skills/openspec-explore/SKILL.md` with LLM-WIKI-specific
  read-only and exit boundaries.
- Add behavior replay tests and evaluation evidence.

Out of scope:

- Rewriting historical wiki notes that mention `readme-learning-capture`.
- Importing account-meeting-lore business rules or trace requirements wholesale.
- Changing wiki medical-loop behavior.
- Archiving this or earlier OpenSpec changes.

## Success Criteria

- `find .codex/skills -maxdepth 2 -name SKILL.md` exposes
  `learning-capture` but not `readme-learning-capture`.
- Repo/README learning remains available through
  `learning-capture/references/repo-readme.md`.
- `AGENTS.md` no longer routes active work through `readme-learning-capture`.
- `AGENTS.md` has an explicit missing-local-skill stop gate.
- `openspec-explore` states read-only exploration, non-implementation, and exit
  boundaries clearly.
- Tests and OpenSpec evaluation record RED baseline, GREEN result, prior-art
  dedupe, and residual risk.
