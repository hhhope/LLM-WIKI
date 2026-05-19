# Evaluation: bootstrap self-running wiki governance

## Behavior Expected To Change

Before this change, a future agent entering `LLM-WIKI` saw only a short seed
entry. After this change, the same agent should identify the repo-local gates
for OpenSpec, wiki medical-loop status, frontmatter taxonomy, output routing,
and verification before editing or claiming completion.

## Baseline Scenario

Input:

```text
看下我们wiki可以自己跑起来了吗？我看和account-meeting-lore的 agent.md的差距还是很大
```

Old route from `AGENTS.md` absence:

- read `PROJECT.md`;
- use `.codex/skills/`;
- preserve sources and use medical loop;
- no repo-visible instruction for OpenSpec-gated workflow changes;
- no repo-visible hard stop for medical-loop case authority;
- no explicit behavior-asset evaluation gate;
- no compact output routing or verification checklist.

Observed baseline result:

- status, graph, and medical-agent scripts could run;
- frontmatter strict gate failed on a generated review-decision record;
- self-directed execution returned zero `execute_now` actions;
- the repo did not yet explain how a future agent should safely repair those
  findings.

## After-Change Scenario

Expected route after `AGENTS.md` update:

- classify the request as a self-running governance inspection or repair;
- for semantic workflow changes, create/select an active OpenSpec change;
- route status/diagnosis through `wiki-medical-agent`;
- route wiki frontmatter edits through the taxonomy gate;
- keep source material in `wiki/sources`, workflow evidence in `wiki/ops`, and
  stable decisions in `wiki/adr`;
- verify with current commands before claiming completion.

## Verification Evidence

Commands run from `/mnt/d/cloud/LLM-WIKI`:

```text
python3 scripts/check_wiki_frontmatter.py --json-output /tmp/llm-wiki-frontmatter.json --markdown-output /tmp/llm-wiki-frontmatter.md
python3 -m py_compile scripts/wiki_review_decisions.py scripts/build_wiki_review_decisions.py
python3 scripts/build_wiki_review_decisions.py --decision-record-dir /tmp/llm-wiki-review-test --limit 1
python3 scripts/build_wiki_status.py
python3 scripts/extract_wiki_graph.py
python3 scripts/build_wiki_medical_agent.py --intent-text "status: can this wiki run itself after governance bootstrap?"
```

Results:

- Frontmatter checker exited successfully with `error: 0`, `warn: 6`,
  `blocking_entry_count: 0`, and score `75 / 100`.
- Remaining frontmatter findings are `possible_unregistered_producer` warnings
  for scripts containing frontmatter-looking text.
- Generated review-decision Markdown in `/tmp/llm-wiki-review-test/` starts
  with `layer: ops`, `domain: wiki`, `ops_area: wiki-runtime`,
  `canonical_object: wiki-review-decision-record`, and
  `artifact_type: review-decision-record`.
- `build_wiki_status.py` refreshed `wiki/status/manifest.json` and
  `wiki/status/wiki-status.md`.
- Graph extraction reported `node_count: 5`, `edge_count: 0`, and
  `warning_count: 1`.
- Medical agent reported `intent: status`, `state: awaiting_confirmation`,
  `allowed_action: report_status`, and `next_action: awaiting_confirmation`.

Completion boundary:

- The strict frontmatter blocker is cleared; the full scorecard still reports
  drift because producer registration warnings remain.
- The wiki can run its status and medical-loop diagnostics, but the medical case
  remains `awaiting_confirmation`; this is not autonomous repair.

## Residual Risks

- This Phase 0 governance bootstrap does not create a product CLI or archive
  workflow.
- Relation coverage can remain thin even after strict frontmatter passes.
- The medical case may remain `awaiting_confirmation`; that is a valid bounded
  state, not proof of autonomous repair.
