---
name: wiki-queue
description: Preview ready, decision-needed, and blocked report wiki work without executing it.
---

Use the wiki queue runtime surface for the report wiki repository.

When triggered:

1. Confirm the current repository has `scripts/build_wiki_change_queue_preview.py`.
2. Run or reference `python3 scripts/build_wiki_change_queue_preview.py`.
3. Read queue preview JSON when available.
4. Summarize `ready`, `needs_user_decision`, and `blocked` work with source
   paths and caution notes.

Boundaries:

- Do not create, modify, archive, or queue OpenSpec changes.
- Do not mark OpenSpec tasks complete.
- Do not execute queued work.
- Do not turn preview items into tasks or commits by default.
