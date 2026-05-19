---
name: openspec-router
description: Use when work in this OpenSpec-governed repository mentions Superpowers, OpenSpec, workflow gates, implementation, verification, archive, or process repair.
---

# OpenSpec Router

Route the next action before editing files, implementing code, committing,
pushing, archiving, or claiming a workflow repair is complete.

## Purpose

This skill is a small router. It does not replace Superpowers, OpenSpec, or
AGENTS.md.

- Superpowers owns method discipline: brainstorming, planning, TDD, execution,
  and review practices.
- OpenSpec owns authoritative lifecycle state: proposal, design, specs, tasks,
  verification, completion, and archive.
- AGENTS.md owns repo discipline: health checks, git truth, validation, commit
  behavior, and hard stops.

## When To Use

Use this skill when any of these are true:

- The user mentions `$superpowers:*`.
- The user mentions OpenSpec, change, proposal, tasks, verification, archive,
  or workflow gates.
- `PROJECT.md` declares `source_of_truth: openspec` and the task is large.
- The user asks why a workflow was skipped or asks to fix workflow integration.
- A task could plausibly be explore, brainstorm, propose, implement, verify, or
  archive.

## Router Steps

Before action, answer:

1. Intent: what is the user asking for now?
2. Gate: what class of action is allowed next?
3. Route line: what one-line route should be visible to the user?

Intent values:

- `explore`
- `brainstorm`
- `propose`
- `implement`
- `verify`
- `archive`
- `repair-workflow`

Gate values:

- `read-only`
- `ask-or-present`
- `write-superpowers-spec`
- `write-openspec-change`
- `implement`
- `verify`
- `complete`

## Required Route Line

At the start of a routed task, and after any gate transition, say one compact
route line.

Examples:

```text
Route: brainstorm -> superpowers spec; OpenSpec read-only until spec review.
Route: propose -> OpenSpec change; Superpowers brainstorming not active.
Route: implement -> OpenSpec apply; Superpowers execution skills may assist.
Route: verify -> evidence check; no mock evidence accepted for live acceptance.
```

Keep the route line short. Do not turn normal collaboration into a matrix or
long state-machine report.

## Hard Rules

1. If `$superpowers:brainstorming` is active, OpenSpec is read-only until the
   Superpowers written design/spec review gate passes.
2. Short approvals such as `可以`, `继续`, `确认`, `做吧`, and `go` only advance
   the current gate. They do not imply permission to skip into OpenSpec edits,
   implementation, commit, push, or archive.
3. Writing a Superpowers artifact does not create authoritative lifecycle
   state. Accepted lifecycle changes must be copied into OpenSpec before
   implementation or archive claims.
4. OpenSpec remains the source of truth for large changes.
5. Implementation requires an active OpenSpec change with clear tasks unless
   the task is explicitly small and outside OpenSpec scope.
6. Completion and archive claims require OpenSpec evidence. Superpowers
   checkboxes alone are not completion evidence.
7. Mock data cannot satisfy a live acceptance route when the user asks for real
   integration or real verification.

## Anti-Patterns

- Do not let OpenSpec execution bypass Superpowers brainstorming gates.
- Do not treat `source_of_truth: openspec` as permission to skip interactive
  design when the user invoked Superpowers.
- Do not create a heavy state-machine framework for ordinary work.
- Do not let `docs/superpowers/*` conflict with OpenSpec. If they disagree,
  OpenSpec wins and the Superpowers file is a draft or execution aid.
- Do not treat `补进去`, `可以`, or `继续` as permission to edit OpenSpec if the
  current gate is still brainstorming or Superpowers spec review.

## Scenario Replay Checklist

After editing this skill, replay the cases from
`docs/superpowers/specs/2026-05-15-openspec-router-design.md`:

1. Brainstorming request.
2. Short approval during design.
3. Continue after design approval.
4. Implementation request.
5. Verification request.
6. Archive request.
7. Original incident.

Record the result in
`docs/superpowers/specs/2026-05-15-openspec-router-replay.md`.
