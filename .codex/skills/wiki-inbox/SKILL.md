---
name: wiki-inbox
description: Review pending report wiki inbox items that need intake or source routing.
---

Use the wiki inbox runtime surface for the report wiki repository.

When triggered:

1. Confirm the current repository has `inbox/` or `wiki/status/manifest.json`.
2. Run or reference `python3 scripts/build_wiki_status.py` when status needs
   refreshing.
3. Read `wiki/status/manifest.json`, `wiki/status/wiki-status.md`, and relevant
   `inbox/` filenames.
4. Summarize pending intake items and route them as candidate work only.

Boundaries:

- Do not create, modify, archive, or queue OpenSpec changes.
- Do not mark OpenSpec tasks complete.
- Do not execute queued work.
- Do not move or ingest inbox files unless the user explicitly asks.
