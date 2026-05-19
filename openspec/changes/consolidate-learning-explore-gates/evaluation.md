# Evaluation

## RED Baseline

Initial command:

```bash
python3 -m pytest -q tests/test_learning_explore_gates.py
```

Observed result:

- Failed before executing tests because this seed repo does not ship pytest:
  `No module named pytest`.
- The test file was converted to standard-library `unittest` so the gate stays
  runnable in a fresh seed checkout.

RED command:

```bash
python3 -m unittest tests.test_learning_explore_gates
```

Observed RED result before implementation:

- `test_readme_learning_is_not_a_separate_active_skill` failed because
  `.codex/skills/readme-learning-capture/SKILL.md` existed.
- `test_repo_readme_module_is_self_contained_under_learning_capture` failed
  because `learning-capture/references/repo-readme.md` delegated to
  `.codex/skills/readme-learning-capture/SKILL.md`.
- `test_agents_do_not_route_active_learning_to_retired_readme_skill` failed
  because `AGENTS.md` still routed source-shape matches to
  `readme-learning-capture`.
- `test_agents_declares_missing_local_skill_stop_gate` failed because
  `AGENTS.md` lacked the missing-local-skill stop wording.
- `test_openspec_explore_defines_read_only_exit_boundary` failed because
  `openspec-explore` still used the generic upstream stance text.

Result: RED. The repo exposed duplicate repo/README learning entry surfaces
and did not clearly stop missing skill or explore-mode boundary drift.

## Prior-Art / Common-Rule Dedupe

Scanned:

- `AGENTS.md`
- `PROJECT.md`
- `.codex/skills/learning-capture/SKILL.md`
- `.codex/skills/learning-capture/references/repo-readme.md`
- `.codex/skills/readme-learning-capture/SKILL.md`
- `.codex/skills/openspec-explore/SKILL.md`
- `wiki/config/behavior-asset-evaluation.yaml`
- `openspec/changes/repair-wiki-runtime-governance-entry/*`
- `account-meeting-lore/.codex/skills/learning-capture/references/repo-readme.md`
- `account-meeting-lore/openspec/changes/consolidate-readme-learning-capture/evaluation.md`
- global `writing-skills` and `test-driven-development` guidance

Owns:

- This change owns retirement of the active
  `.codex/skills/readme-learning-capture/` runtime surface in `LLM-WIKI`.
- This change owns the missing-local-skill stop gate in `LLM-WIKI` `AGENTS.md`.
- This change owns LLM-WIKI-specific read-only and exit boundaries for
  `.codex/skills/openspec-explore/SKILL.md`.

References:

- `learning-capture` remains the parent gate for external-source learning.
- Repo/README behavior remains a module under
  `.codex/skills/learning-capture/references/`.
- `account-meeting-lore` is prior art only; it is not copied wholesale.
- Global git, health-check, and behavior-asset authoring discipline remains in
  global/common rules.

Rejects:

- Do not recreate `readme-learning-capture` as an active repo-local skill.
- Do not rewrite historical wiki or OpenSpec evidence only because it mentions
  the retired skill name.
- Do not import account-meeting-lore business rules, Feishu defaults, or
  explore trace requirements without a separate LLM-WIKI change.
- Do not treat `$openspec-explore` as implementation permission.

## Pressure Scenarios

Positive repo/README learning scenario:

- input or situation shape: user provides a GitHub repo or README and asks
  whether its approach should be reused in `LLM-WIKI`.
- trigger condition: external-source learning with repo/README evidence object.
- expected route: load `learning-capture`, then
  `references/repo-readme.md`.
- repo-visible artifact: `.codex/skills/learning-capture/SKILL.md` and
  `.codex/skills/learning-capture/references/repo-readme.md`.
- expected output: admission gate, score-first decision, reused / modified /
  rejected / adoption-boundary record.
- promotion or non-promotion boundary: no promotion into `AGENTS.md`, specs, or
  skills without OpenSpec and behavior replay.
- proof boundary: proves route and module availability, not future analysis
  quality.

Positive explore scenario:

- input or situation shape: user says `$openspec-explore` and asks to compare
  another repository's approach before changing LLM-WIKI.
- trigger condition: explicit `$openspec-explore` trigger.
- expected route: read-only exploration stance first.
- repo-visible artifact: `.codex/skills/openspec-explore/SKILL.md` and
  `AGENTS.md`.
- expected output: analysis, hypotheses, and possible proposal direction; no
  AGENTS, skill, wiki, script, or implementation edits unless the user exits
  explore or asks for OpenSpec artifacts.
- promotion or non-promotion boundary: explore conclusions are not write
  approval.
- proof boundary: static replay verifies the boundary text and route, not a
  live future conversation.

Negative should-not-trigger scenario:

- input or situation shape: user asks for latest repo facts, stars, or generic
  code review.
- trigger condition: no local learning, reuse, wiki, or method-calibration
  intent.
- expected route: do not use durable repo/README learning capture.
- repo-visible artifact: no new learning page required.
- expected output: answer the narrow lookup or route to review workflow.
- promotion or non-promotion boundary: no behavior-asset promotion from raw
  lookup.
- proof boundary: validates non-trigger shape, not external fact freshness.

Missing skill scenario:

- input or situation shape: `AGENTS.md` or a historical note names a skill path
  that does not exist locally.
- trigger condition: route target is a missing local skill.
- expected route: stop and report the missing local skill.
- repo-visible artifact: `AGENTS.md`.
- expected output: no continuation as if the skill loaded.
- promotion or non-promotion boundary: historical skill names are evidence
  only, not active routes.
- proof boundary: static test verifies route-table paths and stop wording.

Parent gate preservation:

- `learning-capture` remains the parent gate for external source learning.
- `weixin-reader` remains only a source reader.
- `openspec-explore` remains a read-only stance unless the user exits explore
  or asks for OpenSpec artifacts.
- OpenSpec, medical-loop, frontmatter, public-output, and behavior-asset gates
  remain unchanged.

## GREEN Result

Command:

```bash
python3 -m unittest tests.test_learning_explore_gates
```

Observed GREEN result:

```text
......
----------------------------------------------------------------------
Ran 6 tests in 0.299s

OK
```

The GREEN run proves:

- active `readme-learning-capture` skill surface is absent;
- repo/README references live under `learning-capture`;
- `AGENTS.md` no longer routes active learning through the retired skill;
- `AGENTS.md` has a missing-local-skill stop gate;
- `AGENTS.md` route table references existing local skill paths;
- `openspec-explore` states read-only and exit boundaries.

## Validation Evidence

Commands:

```bash
python3 -m unittest tests.test_learning_explore_gates
find .codex/skills -maxdepth 2 -name SKILL.md | sort | rg 'readme-learning-capture|learning-capture|openspec-explore'
rg -n "readme-learning-capture" AGENTS.md .codex/skills tests scripts openspec/changes/consolidate-learning-explore-gates
python3 scripts/check_wiki_frontmatter.py --json-output /tmp/llm-wiki-learning-explore-frontmatter.json --markdown-output /tmp/llm-wiki-learning-explore-frontmatter.md
openspec validate consolidate-learning-explore-gates --strict
```

Observed results:

- `unittest`: `Ran 6 tests ... OK`.
- Active skill scan: only `learning-capture` and `openspec-explore` matched;
  no active `readme-learning-capture` skill remained.
- Active reference scan: `readme-learning-capture` remains only in the new test
  and this OpenSpec change evidence, not in `AGENTS.md`, active skills,
  scripts, or old active route surfaces.
- Frontmatter checker: `0 error`, `6 warn`, `blocking_entry_count: 0`; warnings
  are existing non-blocking producer warnings.
- OpenSpec validate: `Change 'consolidate-learning-explore-gates' is valid`.
  PostHog telemetry flush printed network warnings after the valid result; the
  command exited 0.

## Residual Risks

- Historical OpenSpec changes, wiki notes, or prior chat summaries may still
  mention `readme-learning-capture`; those remain evidence only.
- The current live session's injected skill list may still include the retired
  skill until a new session reloads repo-local skills. The repo file surface is
  corrected for future loads.
- This change does not add a full behavior-asset checker script; it adds a
  focused standard-library replay test for this boundary.
- This change does not prove future source-analysis quality or future model
  compliance in every conversation.
