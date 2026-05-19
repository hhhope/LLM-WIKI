---
name: wiki-review-decisions
description: Use when confirming, triaging, or routing `wiki-doctor` findings into review decisions.
---

Use the wiki review-decision surface for the report wiki repository.
This is a legacy compatibility alias for `wiki-confirm`.
Prefer `wiki-confirm` for new user-facing prompts. This skill remains a
review-only routing entry for `wiki-doctor` diagnosis output.
default writes a complete confirmation record; stdout summary is only the live
chat/terminal surface.

Medical-loop sequence:

```text
wiki-doctor -> wiki-confirm -> wiki-treatment -> wiki-surgery -> wiki-recovery
诊断 -> 确诊 -> 治疗 -> 手术 -> 复查
```

When triggered:

1. Confirm the current repository has
   `scripts/build_wiki_review_decisions.py`.
2. Run `python3 scripts/build_wiki_review_decisions.py`; by default it writes
   a complete confirmation record under `wiki/ops/wiki-review-decisions/`.
3. Preserve these draft buckets exactly:
   `accepted_candidates`, `rejected_candidates`, `deferred_items`,
   `treatment_candidates`, `surgery_candidates`, and `openspec_required`.
4. Treat outputs as draft review routing, not approval.
5. Treat stdout as a summary and report the generated confirmation record path.
   Use `--stdout-json-only` only for explicit non-writing debug inspection.
   `--write-decision-record` remains a compatibility flag. Include
   `--decision-record-dir` only when the record must be written somewhere other
   than the default `wiki/ops/wiki-review-decisions/` directory.

Boundaries:

- Do not create, modify, archive, or queue OpenSpec changes.
- Do not mark OpenSpec tasks complete.
- Do not execute queued work.
- Do not write frontmatter.
- Do not mutate `wiki/config/frontmatter-taxonomy.yaml`.
- Do not write relation fields.
- Do not write `wiki/moc` files.
- Do not treat draft review decisions as human approval.
