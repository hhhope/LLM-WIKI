---
name: openspec-apply-change
description: Implement tasks from an OpenSpec change. Use when the user wants to start implementing, continue implementation, or work through tasks.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.2.0"
---

Implement tasks from an OpenSpec change.

**Input**: Optionally specify a change name. If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

Use OpenSpec status and apply instructions to read context files, implement pending tasks, and keep `tasks.md` in sync.

## OpenSpec / Superpowers Execution Overlay

When a detailed Superpowers plan is useful during an OpenSpec change, treat it
as an execution overlay, not as a second task list.

Hard rules:

- `tasks.md` remains the only progress and completion ledger.
- Execution overlays must not define independent `Task 1`, `Task 2`, or similar
  task ids.
- Execution overlays must not use progress checkboxes.
- Execution overlays may document TDD strategy, module strategy, verification
  strategy, commit strategy, subagent strategy, and handoff notes.
- Commit slices are recovery evidence, not OpenSpec task completion.
- Update `tasks.md` when an OpenSpec task completion boundary is verified; do
  not defer completed OpenSpec task progress to a final sync step.

For the bad/good shape, read `references/execution-overlay.md`.
