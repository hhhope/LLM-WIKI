---
name: wiki-status
description: Refresh and summarize the report wiki status surface from manifest and status artifacts.
---

Use the wiki status runtime surface for the report wiki repository.

When triggered:

1. Confirm the current repository has `scripts/build_wiki_status.py`.
2. Run or reference `python3 scripts/build_wiki_status.py`.
3. Read `wiki/status/manifest.json` and `wiki/status/wiki-status.md`.
4. Summarize page and source counts, inbox and OpenSpec counts, identity and
   relation coverage, graph parse health, strict frontmatter gate status,
   content enrichment health, content adjudication health, MOC projection
   health, scorecard score, blocking count, and top blockers when present.
5. Name next inspection routes such as `wiki-graph`, `wiki-scorecard`,
   `wiki-apply`, or `wiki-frontmatter-taxonomy` when the status shows drift.

Boundaries:

- Do not create, modify, archive, or queue OpenSpec changes.
- Do not mark OpenSpec tasks complete.
- Do not execute queued work.
- Do not implement a query engine, graph UI, scorecard, or change queue from
  this skill.
- Do not write `wiki/moc` files from status inspection.
- Do not write frontmatter from content enrichment health.
- Do not write frontmatter or taxonomy from content adjudication health.
