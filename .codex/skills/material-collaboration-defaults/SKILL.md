---
name: material-collaboration-defaults
description: Use when the user drops meeting notes, weekly materials, reports, attachments, preview html, or other source files and expects Codex to process them without repeated workflow confirmation.
---

# Material Collaboration Defaults

## Overview

Turn newly dropped materials into readable repo outputs without stalling at placeholder intake pages or re-asking the whole workflow.

## When to Use

- The user drops meeting notes, transcripts, weekly materials, attachments, Feishu exports, screenshots, or `html/preview` files into the repo.
- The user says “你去处理”, “整理一下”, “归档一下”, or otherwise expects end-to-end material processing.
- The user did not spell out steps but clearly expects proactive organization.

Do not use this skill for pure coding tasks or when the user explicitly limits the work to a single placeholder step.

## Rules

- Start with `source`. Do not stop at placeholder text if readable conclusions can be written.
- Add `ops` outputs when the material already contains actions, owners, blockers, or dates.
- Process incrementally. Update existing linked pages instead of re-running the whole inbox.
- Ask only at real output forks, especially whether editable `html/h5/preview` assets should be updated in addition to wiki pages.
- Follow repo workflow boundaries from [AGENTS.md](../../../AGENTS.md); do not restate the full repo policy here.

## Common Mistakes

- Finishing with a “待补充” placeholder page
- Treating intake creation as the end of processing
- Re-scanning the whole repository for every new drop
- Re-confirming the entire workflow when only one output fork needs a decision
- Extracting no conclusions, risks, or follow-up items from rich source material
