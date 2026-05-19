---
name: openspec-explore
description: Enter explore mode - a thinking partner for exploring ideas, investigating problems, and clarifying requirements. Use when the user wants to think through something before or during a change.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.0"
  generatedBy: "1.2.0"
---

Enter explore mode. Think deeply. Visualize freely. Follow the conversation wherever it goes.

**IMPORTANT: Explore mode is for thinking, not implementing.** You may read files, search code, and investigate the codebase, but you must NEVER write code or implement features. If the user asks you to implement something, remind them to exit explore mode first and create a change proposal. You MAY create OpenSpec artifacts (proposals, designs, specs) if the user asks—that's capturing thinking, not implementing.

**This is a stance, not a workflow.** There are no fixed steps, no required sequence, no mandatory outputs. You're a thinking partner helping the user explore.

## LLM-WIKI Boundaries

When the user gives an explicit `$openspec-explore` trigger, enter a read-only
exploration stance first. Do not turn the request into implementation, archive,
medical-loop apply, AGENTS edits, skill edits, wiki rewrites, or script changes.
This is a read-only exploration stance.

`$openspec-explore` is not implementation permission. It allows reading,
comparison, hypothesis shaping, and requirement clarification. It may create or
update OpenSpec artifacts only when the user explicitly asks for OpenSpec
artifacts; ordinary repository edits still require the user to exit explore and
pass the normal proposal/apply gates.

Hard rules:

- Must not edit `AGENTS.md`, `.codex/skills/*`, `wiki/*`, `scripts/*`, or
  implementation files during explore unless the user explicitly exits explore
  or asks for OpenSpec artifacts.
- Must not treat an explore conclusion as approval to write behavior assets.
- Must not use a missing local skill, historical skill name, or global skill as
  a substitute for a repo-local route.
- If the user asks to implement while explore is active, state the boundary and
  ask for an exit from explore or a proposal/apply gate.
