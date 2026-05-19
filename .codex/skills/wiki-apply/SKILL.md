---
name: wiki-apply
description: Inspect bounded wiki self-directed execution suggestions without executing them.
---

Use the wiki apply runtime surface for the report wiki repository.

When triggered:

1. Confirm the current repository has `scripts/derive_self_directed_execution.py`.
2. Use the `decision_trace` contract in
   `wiki/ops/wiki-react-decision-trace-runtime.md` before suggesting repair,
   execution, taxonomy, parser, or promotion routes.
3. Run or reference `python3 scripts/build_runtime_context_injection.py` and
   `python3 scripts/derive_self_directed_execution.py`.
4. Read self-directed execution JSON when available.
5. Summarize `execute_now`, `defer_for_followup`, and `do_not_execute` as
   suggestions only.
6. For content enrichment, read the `content_enrichment_preview` or run
   `python3 scripts/build_wiki_content_enrichment.py`; this is preview only.
7. For content adjudication, read the `content_adjudication_review_package` or
   run `python3 scripts/build_wiki_content_adjudication.py`; this is review
   package only.
8. For Obsidian MOC projection, read the `moc_projection_preview` or run
   `python3 scripts/build_wiki_moc_projection.py` without `--apply`; this is
   preview only.
9. For explicit page frontmatter repairs, route to
   `python3 scripts/wiki_gate_precheck.py --mode frontmatter --target PATH`
   and use `target.repair_hints` before opening full taxonomy config.
10. Distinguish `page-frontmatter-fix`, `taxonomy-config-fix`,
   `runtime-parser-fix`, and `readable-graph-fix`; only page-frontmatter-fix
   can be bounded to an explicit page without a new runtime behavior change.

Boundaries:

- Do not create, modify, archive, or queue OpenSpec changes.
- Do not mark OpenSpec tasks complete.
- Do not execute queued work.
- Do not implement `execute_now` items unless the user gives a separate
  proceed signal and the repo gates pass.
- Do not write `wiki/moc` files from apply preview; explicit generator
  `--apply` is a separate write action.
- Do not write frontmatter from content enrichment preview.
- Do not write frontmatter or taxonomy from content adjudication review package.
