---
name: wiki-react
description: Use when a wiki request needs explicit intent, route, boundary, or decision-trace replay before action.
---

Use the bounded wiki ReAct decision-trace surface for the report wiki repository.

When triggered:

1. Confirm the current repository has
   `wiki/ops/wiki-react-decision-trace-runtime.md`.
2. Read `wiki/ops/wiki-react-decision-trace-runtime.md`.
3. Classify the wiki request intent, evidence object, and risk level.
4. Produce a compact `decision_trace` with action, observation, decision,
   boundary, and forbidden actions checked.
5. For replay or evaluation, use `wiki/evals/wiki-react-trace-cases.json` and
   `python3 scripts/eval_wiki_decision_trace.py --traces TRACE_JSON`.
6. Route onward to the appropriate wiki skill, such as `wiki-status`,
   `wiki-query`, `wiki-apply`, `wiki-explore`, or `wiki-scorecard`.
7. For `obsidian_graph_projection`, require `read_graph_context`,
   `read_status_manifest`, and `preview_moc_projection`, with boundary
   `explicit_moc_generator_required`.
8. For `wiki_content_enrichment`, require `preview_content_enrichment` and
   static precheck evidence, with boundary
   `frontmatter_enrichment_preview_only`.
9. For `wiki_content_adjudication`, require `preview_content_enrichment`,
   `build_adjudication_review_package`, and `run_adjudication_eval`, with
   boundary `adjudication_review_only`.

Boundaries:

- Do not create, modify, archive, or queue OpenSpec changes.
- Do not mark OpenSpec tasks complete.
- Do not execute queued work.
- Do not treat article weight, temperature, source confidence, relation
  strength, or scorecard bands as hard gates.
- Do not use Python to classify natural-language intent; Python only validates
  agent-produced traces.
- Do not write `wiki/moc` files from react or eval.
- Do not write frontmatter from react or eval.
- Do not write taxonomy from react or eval.
