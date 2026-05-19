# Evaluation: repair wiki runtime governance entry

## Pressure Scenarios

Positive scenario 1:

- input or situation shape: user asks why the prior `AGENTS.md` reference work
  lost the wiki runtime, governance runtime, intent routing, skill table, and
  behavior constraints.
- trigger condition: semantic repair to repo `AGENTS.md`, a behavior asset.
- expected route: `openspec-router` -> new OpenSpec repair change ->
  `writing-skills` / TDD-style behavior evaluation -> `openspec-apply-change`.
- repo-visible artifact: this change directory and repaired `AGENTS.md`.
- expected output: route line, RED/GREEN evidence, prior-art dedupe, and a
  repaired runtime entry.
- promotion or non-promotion boundary: source-reference structure may be
  adapted; source business rules are rejected.
- proof boundary: local text replay and command verification prove repo-visible
  behavior gates, not multi-session autonomous compliance.

Positive scenario 2:

- input or situation shape: user asks "wiki 自己跑起来了吗" or asks for status,
  diagnosis, treatment, surgery, recovery, queue, graph, context, or apply.
- trigger condition: wiki runtime or medical-loop intent.
- expected route: classify through `Agent Intent Routing`; load the matching
  `High-Frequency Skills` row, normally `wiki-medical-agent` for medical-loop
  work or the specific bounded wiki runtime surface for read-only inspection.
- repo-visible artifact: `AGENTS.md`, `.codex/skills/wiki-*/SKILL.md`, and
  `wiki/ops/wiki-medical-cases/*` when a case exists.
- expected output: intent, case/state or bounded runtime summary, allowed
  action, blocked action when relevant, and next action.
- promotion or non-promotion boundary: previews and suggestions do not mutate
  ADRs, taxonomy, MOC, AGENTS, skills, or OpenSpec lifecycle state.
- proof boundary: script output is executor evidence; route correctness is
  recorded in this evaluation.

Negative scenario:

- input or situation shape: user says "参考
  `D:\cloud\account-meeting-lore\AGENTS.md`" while repairing this repo entry.
- trigger condition: external repo used as prior-art for governance structure.
- expected route: scan source reference, adapt only generic runtime governance
  shape, reject Go, Feishu, meeting-lore, report-portfolio, and historical
  source-repo decisions unless a separate `LLM-WIKI` change proves ownership.
- repo-visible artifact: `AGENTS.md` non-promotion boundaries and this
  evaluation.
- expected output: no copied business workflow and no Python-led story that
  substitutes for agent runtime routing.
- promotion or non-promotion boundary: source-reference business defaults stay
  rejected.
- proof boundary: this is a local governance repair, not proof that every
  downstream skill has complete behavior replay coverage.

## RED Baseline

Baseline command:

```text
rg -n "Hard Stops|Behavior Replay Gate|Behavior Asset Prior-Art Gate|High-Frequency Skills|Agent Intent Routing|Wiki Runtime Stack|Skill Authoring Contract|writing-skills|test-driven-development|wiki-react|wiki-apply|wiki-route|wiki-context|wiki-medical-agent|parent gate|Pressure Scenarios|RED Baseline|GREEN Result|Prior-Art / Common-Rule Dedupe" AGENTS.md openspec/changes/bootstrap-self-running-wiki-governance/evaluation.md openspec/changes/repair-wiki-runtime-governance-entry/evaluation.md
```

Observed baseline before repairing `AGENTS.md`:

```text
AGENTS.md:32:  recovery, or archive checks, route through `wiki-medical-agent`.
openspec/changes/bootstrap-self-running-wiki-governance/evaluation.md:42:- route status/diagnosis through `wiki-medical-agent`;
openspec/changes/repair-wiki-runtime-governance-entry/evaluation.md:3:## Pressure Scenarios
openspec/changes/repair-wiki-runtime-governance-entry/evaluation.md:7:## RED Baseline
openspec/changes/repair-wiki-runtime-governance-entry/evaluation.md:11:## GREEN Result
openspec/changes/repair-wiki-runtime-governance-entry/evaluation.md:15:## Prior-Art / Common-Rule Dedupe
```

Baseline failure:

- `AGENTS.md` has no `Hard Stops`, `Behavior Replay Gate`, `Behavior Asset
  Prior-Art Gate`, `High-Frequency Skills`, `Agent Intent Routing`, `Wiki
  Runtime Stack`, or `Skill Authoring Contract`.
- Existing evaluation for the bootstrap change does not show
  `writing-skills`, TDD-style RED/GREEN replay, parent-gate preservation, or
  prior-art dedupe.
- The only runtime skill surfaced by `AGENTS.md` is `wiki-medical-agent`; the
  read-only wiki runtime surfaces such as `wiki-react`, `wiki-route`,
  `wiki-context`, and `wiki-apply` are not organized as an entry path.

## GREEN Result

Pending implementation.

## Prior-Art / Common-Rule Dedupe

Scanned:

- `PROJECT.md`
- current repo `AGENTS.md`
- `wiki/index.md`
- `wiki/ops/index.md`
- `wiki/ops/llm-wiki-core-product-contract.md`
- `wiki/ops/llm-wiki-self-evolution-medical-loop.md`
- `wiki/config/behavior-asset-evaluation.yaml`
- `.codex/skills/*/SKILL.md`
- `openspec/changes/bootstrap-self-running-wiki-governance/*`
- `/mnt/d/cloud/account-meeting-lore/AGENTS.md`
- `/home/yan/.codex/rules/common/development-workflow.md`
- `/home/yan/.codex/rules/common/git-workflow.md`
- `/home/yan/.codex/rules/common/testing.md`
- `/home/yan/.codex/skills/writing-skills/SKILL.md`
- `/home/yan/.codex/skills/test-driven-development/SKILL.md`

Owns:

- `LLM-WIKI` runtime entry routing in repo `AGENTS.md`.
- The mapping from this repo's `.codex/skills/wiki-*` surfaces to startup
  intent routing.
- Non-promotion boundaries for source-reference business rules.
- Change-local behavior replay evidence for this repair.

References:

- Global health, git, and long-step discipline from root instructions and
  common rules.
- `writing-skills` and `test-driven-development` for semantic behavior-asset
  evaluation.
- `wiki/config/behavior-asset-evaluation.yaml` for required replay fields and
  route-table ownership constraints.
- Source-reference `account-meeting-lore/AGENTS.md` only for governance
  structure.

Rejects:

- Copying source-repo Go engineering defaults.
- Copying Feishu, meeting-lore, report-portfolio, or historical
  source-repository decisions into this repo entry.
- Treating Python commands as the primary runtime governance story.
- Treating script success as proof that future agents will route correctly.

## Residual Risks

- This change repairs the repo-visible entry path; it does not add stable
  `openspec/specs/` for every runtime behavior.
- Text replay is local proof. It does not replace future multi-session pressure
  testing if the runtime grows.
- Existing wiki ops pages for the core product contract and medical loop remain
  brief; they are cited as runtime anchors, not full specifications.
