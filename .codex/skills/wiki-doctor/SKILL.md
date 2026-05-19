---
name: wiki-doctor
description: Use only for explicit legacy/debug doctor evidence; ordinary wiki medical-loop diagnosis requests route through wiki-medical-agent.
---

Use the wiki doctor review-package surface for the report wiki repository.
This is a review-only diagnostic entry.
default writes a complete diagnosis record; stdout summary is only the live
chat/terminal surface.

Ordinary use routes through `wiki-medical-agent`.

Use this stage skill directly only for explicit legacy/debug evidence. Direct
stage output is legacy/debug evidence only; it is not authoritative and does
not update case state unless routed through the medical agent and written back
to the active case file.

Medical-loop sequence:

```text
wiki-doctor -> wiki-confirm -> wiki-treatment -> wiki-surgery -> wiki-recovery
诊断 -> 确诊 -> 治疗 -> 手术 -> 复查
```

When triggered:

1. Confirm the current repository has
   `scripts/build_wiki_content_adjudication.py`.
2. Run `python3 scripts/build_wiki_content_adjudication.py`; by default it
   writes a complete diagnosis record under `wiki/ops/wiki-doctor-runs/`.
3. Summarize the review package sections:
   `full_detail_set`, `review_focus_set`, `taxonomy_candidate_set`,
   `drift_trace_set`, and `eval_result`.
4. Default to `review_focus_set` for the user-facing diagnosis, but preserve
   that each focus item points back to `full_detail_set`.
5. Surface taxonomy candidates as candidates only; do not treat them as
   approved YAML changes.
6. Surface drift traces as evidence for where agent judgment or governance risk
   may have entered the flow.
7. Route any actual frontmatter write, taxonomy update, or MOC write to a
   separate explicitly approved change path.
8. Treat stdout as a summary and report the generated diagnosis record path.
   Use `--stdout-json-only` only for explicit non-writing debug inspection.
   `--write-review-record` remains a compatibility flag.
   Include `--review-record-dir` when the record must be written somewhere
   other than the default `wiki/ops/wiki-doctor-runs/` directory.
9. Treat generated files under `wiki/ops/wiki-doctor-runs/` as diagnosis
   records only. They are review evidence, not approval to apply repairs.
10. When the user asks what to do next, answer in medical-loop terms:
    Use `wiki-confirm` to 确诊 doctor findings; Use `wiki-treatment` for
    explicitly approved low-risk 治疗; Use `wiki-surgery` for broad structural
    or governance-sensitive 手术 planning; Use `wiki-recovery` to 复查 after
    treatment or surgery planning.

Boundaries:

- Do not create, modify, archive, or queue OpenSpec changes.
- Do not mark OpenSpec tasks complete.
- Do not execute queued work.
- Do not write frontmatter from doctor output.
- Do not mutate `wiki/config/frontmatter-taxonomy.yaml`.
- Do not write `wiki/moc` files.
- Do not treat `eval_result.passed` as approval to apply structure.
- Do not treat a review record as approval to apply frontmatter, taxonomy, MOC,
  OpenSpec, or queued-work changes.
