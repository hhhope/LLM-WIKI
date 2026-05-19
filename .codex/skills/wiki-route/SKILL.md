---
name: wiki-route
description: Inspect source-integrated report wiki runtime routing suggestions.
---

Use the wiki route runtime surface for the report wiki repository.

When triggered:

1. Confirm the current repository has
   `scripts/resolve_runtime_context_sources.py`.
2. Run or reference `python3 scripts/resolve_runtime_context_sources.py` and
   `python3 scripts/derive_runtime_auto_routing.py`.
3. Read runtime source integration and auto-routing JSON when available.
4. Summarize `open_first`, `open_next`, and `do_not_open_first` with explicit
   source paths and caution notes.

Boundaries:

- Do not create, modify, archive, or queue OpenSpec changes.
- Do not mark OpenSpec tasks complete.
- Do not execute queued work.
- Do not open or promote blocked sources without user direction.
