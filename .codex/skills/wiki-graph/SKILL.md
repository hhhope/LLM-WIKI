---
name: wiki-graph
description: Inspect the report wiki structural graph and relation-analysis runtime layers.
---

Use the wiki graph runtime surface for the report wiki repository.

When triggered:

1. Confirm the current repository has `scripts/extract_wiki_graph.py`.
2. Run or reference `python3 scripts/extract_wiki_graph.py`,
   `python3 scripts/analyze_wiki_relations.py`, and
   `python3 scripts/summarize_wiki_graph.py`.
3. Read generated graph, relation-analysis, and summary JSON when available.
4. Summarize canonical objects, source layers, relation counts, warnings, and
   representative pages as structural evidence only.
5. When present, summarize MOC candidates as projection candidates only.

Boundaries:

- Do not create, modify, archive, or queue OpenSpec changes.
- Do not mark OpenSpec tasks complete.
- Do not execute queued work.
- Do not claim semantic understanding from graph structure alone.
- Do not write `wiki/moc` files from graph inspection.
