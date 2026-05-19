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

After repairing `AGENTS.md`, the same text-gate replay finds the missing
runtime and governance layers.

GREEN command:

```text
rg -n "seed|Feishu|Go service|account-meeting-lore|Python commands as the primary runtime|## (Hard Stops|Behavior Replay Gate|Behavior Asset Prior-Art Gate|High-Frequency Skills|Agent Intent Routing|Wiki Runtime Stack|Skill Authoring Contract)|wiki-react|wiki-apply|wiki-route|wiki-context|wiki-medical-agent|writing-skills|test-driven-development|parent gate" AGENTS.md
```

Key GREEN hits:

```text
54:## Hard Stops
62:| Semantic `.codex/skills/*` edit, or an `AGENTS.md` edit that changes skill routing/authoring behavior | Load `writing-skills` and its `test-driven-development` prerequisite before writing. |
67:## Behavior Replay Gate
86:## Behavior Asset Prior-Art Gate
103:## High-Frequency Skills
113:| Wiki request needs explicit intent, route, boundary, or decision-trace replay | `.codex/skills/wiki-react/SKILL.md` | bounded decision-trace surface |
115:| Wiki query, source-integrated route, or context injection | `.codex/skills/wiki-query/SKILL.md`, `.codex/skills/wiki-route/SKILL.md`, or `.codex/skills/wiki-context/SKILL.md` | read-only context runtime |
117:| Inbox, queue, or self-directed execution suggestions | `.codex/skills/wiki-inbox/SKILL.md`, `.codex/skills/wiki-queue/SKILL.md`, or `.codex/skills/wiki-apply/SKILL.md` | preview and suggestion surface |
118:| Medical-loop status, diagnosis, confirmation, treatment, surgery, recovery, or archive checks | `.codex/skills/wiki-medical-agent/SKILL.md` | single normal user-facing medical-loop entry |
125:## Agent Intent Routing
142:## Wiki Runtime Stack
188:## Skill Authoring Contract
```

Behavior result:

- The prior thin runtime entry is replaced by hard stops, replay, prior-art,
  high-frequency skills, agent intent routing, wiki runtime stack, medical-loop
  authority, taxonomy gate, skill authoring contract, output routing, and
  verification.
- `High-Frequency Skills` owns the single repo-local runtime routing table.
  `Agent Intent Routing` classifies and preserves parent gates instead of
  creating a second table.
- `writing-skills` and `test-driven-development` are explicitly required for
  semantic skill edits and `AGENTS.md` edits that alter skill routing or
  authoring behavior.
- The source-reference business terms checked in the GREEN command do not
  appear in `AGENTS.md`.
- Runtime scripts are framed as executors/evidence, not as a substitute for
  agent route selection.

## Verification Evidence

Commands run from `/mnt/d/cloud/LLM-WIKI`:

```text
python3 scripts/check_wiki_frontmatter.py
python3 scripts/build_wiki_status.py
python3 scripts/build_wiki_medical_agent.py --intent-text "status: can this wiki runtime route governance correctly after AGENTS repair?"
rg -n "## (Hard Stops|Behavior Replay Gate|Behavior Asset Prior-Art Gate|High-Frequency Skills|Agent Intent Routing|Wiki Runtime Stack|Skill Authoring Contract)|wiki-react|wiki-apply|wiki-route|wiki-context|wiki-medical-agent|writing-skills|test-driven-development|parent gate|single repo-local runtime routing table" AGENTS.md
git diff --check
test -f scripts/check_behavior_assets.py && python3 scripts/check_behavior_assets.py || printf 'check_behavior_assets.py missing\n'
```

Results:

- `check_wiki_frontmatter.py` exited successfully with no terminal output.
- `build_wiki_status.py` refreshed `wiki/status/manifest.json` and
  `wiki/status/wiki-status.md`; the generated status now sees one active
  OpenSpec change.
- `build_wiki_medical_agent.py` returned `intent: status`, active case
  `wiki/ops/wiki-medical-cases/2026-05-19-081428-wiki-medical-case.md`,
  `state: awaiting_confirmation`, `allowed_action: report_status`, and
  `next_action: awaiting_confirmation`.
- Text gate found the repaired behavior layers in `AGENTS.md`: hard stops,
  behavior replay, prior-art, high-frequency skills, agent intent routing, wiki
  runtime stack, skill authoring, `wiki-react`, `wiki-route`, `wiki-context`,
  `wiki-apply`, `wiki-medical-agent`, `writing-skills`, and
  `test-driven-development`.
- `git diff --check` exited successfully with no output.
- `scripts/check_behavior_assets.py` is not present in this repository; this is
  a recorded verification limitation, not a pass.

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
- The repository has `wiki/config/behavior-asset-evaluation.yaml` but no
  `scripts/check_behavior_assets.py`, so behavior-asset checks remain
  documented by replay evidence rather than enforced by a local checker.
