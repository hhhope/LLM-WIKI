# Proposal: bootstrap self-running wiki governance

## Summary

Add the minimum repo-visible governance needed for `LLM-WIKI` to operate as a
self-maintaining wiki seed instead of a loose copy of scripts, skills, and
pages.

## Problem

The seed repository can already run status, graph, and medical-loop commands,
but its repo `AGENTS.md` does not explain the runtime gates that future agents
must follow. Compared with `account-meeting-lore`, the missing layer is not
business-specific detail; it is the compact workflow boundary that tells an
agent when to route through OpenSpec, wiki medical-loop status, frontmatter
taxonomy checks, and verification.

The current seed also exposes one immediate strict frontmatter blocker in a
generated wiki review-decision record. If generated medical-loop records can
violate the strict gate, the seed is not yet self-running.

## Scope

In scope:

- Add a minimal OpenSpec change to make the governance work explicit.
- Update repo `AGENTS.md` with compact self-running wiki gates.
- Keep `account-meeting-lore` business rules out of the seed.
- Make wiki review-decision records emit strict-gate-compatible frontmatter.
- Fix the existing generated review-decision record.
- Refresh status artifacts and record verification evidence.

Out of scope:

- Copying the full `account-meeting-lore` `AGENTS.md`.
- Adding business-specific meeting-lore, Go service, Feishu, or report rules.
- Building a new query engine, UI, or product CLI.
- Archiving this change.
- Pushing the branch without explicit user approval.

## Success Criteria

- Future agents can identify this repo's OpenSpec, wiki medical-loop,
  frontmatter, output-routing, and verification gates from `AGENTS.md`.
- The active OpenSpec change has `proposal.md`, `design.md`, `tasks.md`, and
  `evaluation.md`.
- `python3 scripts/check_wiki_frontmatter.py` passes or any remaining findings
  are warnings only.
- `python3 scripts/build_wiki_status.py` runs successfully.
- `python3 scripts/build_wiki_medical_agent.py --intent-text "...status..."`
  reports the current case state without applying repairs.
