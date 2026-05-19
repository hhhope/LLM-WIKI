---
name: surgical-changes
description: Use when the task is narrow but the edit is drifting into adjacent cleanup, style normalization, comment churn, or unrelated refactors.
---

# Surgical Changes

## Overview

Edit only what the current goal requires. Clean up your own side effects, not unrelated territory.

## Use When

- The diff is spreading into adjacent files or unrelated blocks
- A narrow fix is turning into opportunistic cleanup
- The existing code is imperfect, but that is not today's problem

## Rules

- Every edit should trace directly to the current task.
- Clean only the orphaned pieces your change creates.
- Call out older problems if useful, but do not smuggle them into the diff.
- Keep the local style unless the task explicitly changes style.

## Anti-Patterns

- Reordering a whole file while fixing one bug
- Washing comments, naming, and formatting during a narrow change
- Sneaking in a small refactor under unrelated task cover

## Self-Check

`If I delete this line, does the task still hold? If yes, it probably does not belong in this diff.`
