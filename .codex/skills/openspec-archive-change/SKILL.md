---
name: openspec-archive-change
description: Archive a completed change in the experimental workflow. Use when the user wants to finalize and archive a change after implementation is complete.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.2.0"
---

Archive a completed change in the experimental workflow.

Before archiving:

- check artifact completion
- check `tasks.md`
- assess delta spec sync state

Archive by moving `openspec/changes/<name>` to `openspec/changes/archive/YYYY-MM-DD-<name>`.
