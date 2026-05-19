---
name: wiki-query
description: Build bounded wiki context from route, context, and explicit text-search evidence.
---

Use the wiki query runtime surface for the report wiki repository.

When triggered:

1. Confirm the current repository has wiki runtime scripts and `wiki/`.
2. For high-risk or ambiguous requests, use the `decision_trace` contract in
   `wiki/ops/wiki-react-decision-trace-runtime.md` before choosing a route.
3. Run or reference `python3 scripts/build_wiki_status.py`,
   `python3 scripts/derive_runtime_auto_routing.py`, and
   `python3 scripts/build_runtime_context_injection.py` as needed.
4. Use explicit `rg -n` text search for the user's query terms.
5. Read `wiki/status/manifest.json`, `wiki/status/wiki-status.md`,
   `/tmp/wiki-runtime-auto-routing.json`, `/tmp/wiki-context-injection.json`,
   and explicit text matches when available.
6. Summarize bounded context using `open_first`, `open_next`, `do_not_anchor`,
   explicit matches, caution notes, and proof boundaries.

Boundaries:

- Do not create, modify, archive, or queue OpenSpec changes.
- Do not mark OpenSpec tasks complete.
- Do not execute queued work.
- This is not semantic search: no embeddings, hidden semantic ranking, or
  unstated source inference.
