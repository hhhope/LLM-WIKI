---
name: wiki-manifest
description: Inspect the generated report wiki source and routing manifest without changing runtime state.
---

Use the wiki manifest runtime surface for the report wiki repository.

When triggered:

1. Confirm the current repository has `scripts/build_wiki_status.py`.
2. Run or reference `python3 scripts/build_wiki_status.py`.
3. Read `wiki/status/manifest.json`.
4. Summarize manifest counts, source coverage, stale inputs, route pressure,
   missing generated artifacts, and proof boundaries.

Boundaries:

- Do not create, modify, archive, or queue OpenSpec changes.
- Do not mark OpenSpec tasks complete.
- Do not execute queued work.
- Do not infer hidden source meaning beyond the manifest fields.
