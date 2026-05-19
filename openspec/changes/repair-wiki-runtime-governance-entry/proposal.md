# Proposal: repair wiki runtime governance entry

## Summary

Repair the `LLM-WIKI` repository entry so future agents see the wiki runtime,
governance runtime, intent routing, high-frequency skill table, and behavior
asset constraints before acting.

## Problem

The previous bootstrap change compressed `AGENTS.md` into a thin entry. It
preserved a few OpenSpec, medical-loop, frontmatter, output, and verification
notes, but it lost the runtime governance layer that made the source reference
useful.

The failure mode is behavioral, not cosmetic:

- wiki runtime surfaces such as `wiki-react`, `wiki-route`, `wiki-context`,
  `wiki-apply`, and `wiki-medical-agent` are present but not organized as the
  repo entry path;
- hard stops, behavior replay, prior-art dedupe, high-frequency skills, agent
  intent routing, and skill authoring constraints are missing from `AGENTS.md`;
- the evaluation evidence proves command execution, not future-agent route
  behavior;
- `writing-skills` / TDD-style behavior evaluation was not applied even though
  the change modified a behavior asset.

## Scope

In scope:

- Add an OpenSpec repair change for this behavior-asset fix.
- Rewrite `AGENTS.md` as the runnable wiki runtime and governance entry.
- Preserve source-repo business boundaries while adapting its governance
  structure to `LLM-WIKI`.
- Record RED baseline, GREEN result, prior-art dedupe, and replay evidence.
- Run repository verification for frontmatter, status, medical-agent routing,
  and text-level behavior gates.

Out of scope:

- Copying `account-meeting-lore` business workflows wholesale.
- Adding Go, Feishu, report-portfolio, or meeting-lore defaults that are not
  already generic or present in `LLM-WIKI`.
- Implementing new runtime scripts or product UI.
- Archiving previous or current OpenSpec changes.
- Pushing without explicit user approval.

## Success Criteria

- `AGENTS.md` names the wiki runtime stack, governance runtime, intent routing,
  high-frequency skills, hard stops, and behavior-asset gates.
- The change-local evaluation includes pressure scenarios, RED baseline, GREEN
  result, prior-art / common-rule dedupe, and residual risks.
- Verification evidence distinguishes agent behavior gates from script
  executors.
- The old failure shape no longer routes to a thin "seed" summary or
  Python-led verification story.
