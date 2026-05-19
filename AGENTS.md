# LLM-WIKI Agent Entry

This repository is the runnable LLM-maintained wiki runtime. Global
instructions still own health checks, git truth-source checks, and general
execution discipline. This file owns repo-local runtime gates, intent routing,
wiki-governance boundaries, and behavior-asset constraints.

## Scope

- Read `PROJECT.md` first.
- Treat this repository as a runnable wiki runtime, not as a script dump or a
  thin repository note.
- Active OpenSpec change artifacts own current scope, task progress, and
  interruption checkpoints.
- `wiki/adr/` owns stable cross-change decisions.
- Keep business-specific rules from source repositories out of this repository
  unless a new OpenSpec change proves they are generic `LLM-WIKI` behavior.
- Do not treat `README.md` as runtime authority.

## Workflow Change Gate

- Treat changes to repo-default workflow, collaboration behavior, routing
  defaults, taxonomy gates, medical-loop authority, output routing, or
  behavior-asset evaluation as OpenSpec-level changes.
- For these changes, create or select an active OpenSpec change before editing
  `AGENTS.md`, `wiki/`, `scripts/`, `.codex/skills/`, or other repository
  guidance files.
- Large or semantic workflow changes require an active change under
  `openspec/changes/` with `proposal.md`, `design.md`, and `tasks.md`.
- Do not ship temporary wiki-only or skill-only fixes first and backfill
  OpenSpec later.
- Short approvals such as `可以`, `继续`, `加吧`, `确认`, `做吧`, and `go` only
  advance the current gate; they do not skip OpenSpec, verification, git
  checks, behavior replay, or commit boundaries.
- Do not copy another repository's full `AGENTS.md`. Extract only
  `LLM-WIKI`-owned runtime behavior with evidence.

## Workflow Routing

- For OpenSpec work, workflow repair, implementation, verification, archive, or
  ambiguous large tasks, use `.codex/skills/openspec-router/SKILL.md` before
  editing files or claiming completion.
- The router must emit one compact route line at the beginning of a routed task
  and after gate transitions.
- Use `.codex/skills/openspec-propose/SKILL.md` to create a new change,
  `.codex/skills/openspec-apply-change/SKILL.md` to implement an active
  change, and `.codex/skills/openspec-archive-change/SKILL.md` only after
  archive review passes.
- If `$openspec-explore` is active, stay read-only unless the user exits explore
  mode or asks for OpenSpec artifacts.
- OpenSpec gates do not replace wiki medical-loop gates, behavior-asset gates,
  or git truth-source checks.

## Hard Stops

| Situation | Required behavior |
|---|---|
| Active OpenSpec change reaches all checkboxes complete | Stop implementation. Default next action is archive review, not more implementation or immediate archive. |
| Current request changes repo workflow, routing, AGENTS, skills, taxonomy authority, output routing, or medical-loop authority | Require an active OpenSpec change before writing. |
| User challenges drift, missing skill routing, missing runtime, or skipped governance | Stop continuation, re-anchor to the latest user correction, and record behavior evidence before resuming edits. |
| Semantic `AGENTS.md`, `rules/*`, or `.codex/skills/*` change | Treat it as a behavior-asset change; run baseline and after-change replay. |
| Semantic `.codex/skills/*` edit, or an `AGENTS.md` edit that changes skill routing/authoring behavior | Load `writing-skills` and its `test-driven-development` prerequisite before writing. |
| Wiki medical-loop output is preview, proposed, blocked, or awaiting confirmation | Do not apply treatment, surgery, relation edits, taxonomy changes, ADR changes, AGENTS changes, skill changes, or OpenSpec lifecycle changes from that output. |
| `wiki-apply`, queue, graph, scorecard, context, or route surface suggests work | Treat it as bounded diagnostic evidence only until a separate proceed signal and repo gates pass. |
| External article, README, source repo, or example looks useful | Capture or reference as learning only; do not promote into hard rules, specs, skills, or archive-ready claims without evidence. |

## Behavior Replay Gate

- When a change, completion claim, or governance artifact says a runtime
  behavior will trigger, stop, route, reject, or persist differently in future
  sessions, include behavior replay evidence before treating the claim as
  complete or archive-ready.
- Minimum evidence: input or situation shape, trigger condition, expected route
  or stop behavior, repo-visible artifact a future agent should read, expected
  output or non-output, promotion or non-promotion boundary, and residual risk
  or proof boundary.
- Applies to semantic skill trigger changes, repo `AGENTS.md` runtime triggers,
  OpenSpec hard stops, archive / re-anchor / explore gates, learning-promotion
  gates, wiki runtime route changes, and claims such as "next time this will
  happen".
- Does not apply by default to one-off analysis, source summaries, or ordinary
  wiki capture that does not claim future runtime behavior.
- Fixture/manual walkthrough evidence is intermediate proof, not final rollout
  proof. Record the proof boundary explicitly.

## Behavior Asset Prior-Art Gate

- Before semantically creating or modifying behavior assets such as
  `AGENTS.md`, `.codex/skills/*`, `rules/*`, or behavior-evaluation config,
  scan existing ownership first: this repo `AGENTS.md`, `PROJECT.md`, current
  OpenSpec change docs, relevant `wiki/ops`, `wiki/adr`, `wiki/config`,
  `.codex/skills`, global `~/.codex/AGENTS.md`, and relevant common rules.
- Classify proposed behavior before writing:
  `Owns` for `LLM-WIKI`-specific behavior, `References` for existing
  common/global behavior, and `Rejects` for source material that should not be
  promoted.
- Generic engineering constraints such as git discipline, testing, long-step
  reporting, and file-size thresholds stay in global/common rules unless this
  repo adds a stricter local boundary.
- Semantic behavior-asset changes must include `Prior-Art / Common-Rule
  Dedupe` evidence in the OpenSpec change evaluation before completion claims.

## High-Frequency Skills

Use these repo-local skills when the request or implementation scope matches.
They complement repo governance; they do not replace OpenSpec, medical-loop, or
behavior-asset gates. This is the single repo-local runtime routing table.
Before following a route, verify the named repo-local skill file exists. If a
route names a missing local skill, stop and report the missing local skill.
Do not continue as if the skill loaded, and do not treat a historical skill
name, global skill, or prior chat memory as the active repo-local route.
Historical skill name references are evidence only, not active routes.

| Situation | Load | Ownership |
|---|---|---|
| OpenSpec routing, workflow repair, implementation, verification, archive, or ambiguous large task | `.codex/skills/openspec-router/SKILL.md` plus the matching `openspec-*` skill | OpenSpec lifecycle router |
| Exploring ideas or clarifying requirements with `$openspec-explore` | `.codex/skills/openspec-explore/SKILL.md` | read-only explore stance unless writing OpenSpec artifacts |
| Wiki request needs explicit intent, route, boundary, or decision-trace replay | `.codex/skills/wiki-react/SKILL.md` | bounded decision-trace surface |
| Wiki status or "can it run" inspection | `.codex/skills/wiki-status/SKILL.md` | status surface only |
| Wiki query, source-integrated route, or context injection | `.codex/skills/wiki-query/SKILL.md`, `.codex/skills/wiki-route/SKILL.md`, or `.codex/skills/wiki-context/SKILL.md` | read-only context runtime |
| Manifest, graph, scorecard, utilization, or relation health | `.codex/skills/wiki-manifest/SKILL.md`, `.codex/skills/wiki-graph/SKILL.md`, or `.codex/skills/wiki-scorecard/SKILL.md` | diagnostic surface only |
| Inbox, queue, or self-directed execution suggestions | `.codex/skills/wiki-inbox/SKILL.md`, `.codex/skills/wiki-queue/SKILL.md`, or `.codex/skills/wiki-apply/SKILL.md` | preview and suggestion surface |
| Medical-loop status, diagnosis, confirmation, treatment, surgery, recovery, or archive checks | `.codex/skills/wiki-medical-agent/SKILL.md` | single normal user-facing medical-loop entry |
| Explicit legacy/debug medical stage evidence | `wiki-doctor`, `wiki-confirm`, `wiki-treatment`, `wiki-surgery`, or `wiki-recovery` stage skills | stage evidence only; ordinary use routes through `wiki-medical-agent` |
| Wiki frontmatter, templates, or scripts that generate wiki frontmatter | `.codex/skills/wiki-frontmatter-taxonomy/SKILL.md` | taxonomy gate |
| External articles, repos, READMEs, or examples used as learning/reference/adaptation material | `.codex/skills/learning-capture/SKILL.md`; use its repo/README, article, or example modules by source shape; use `weixin-reader` only as a source reader | learning and source routing |
| Materials, reports, attachments, public artifacts, meeting notes, interviews, or project-management reports | matching material/public/meeting/interview/project-management skill | delivery-sensitive output gates |
| Ambiguous request, speculative abstraction, narrow edit drift, or completion claim without fresh evidence | `clarify-before-acting`, `simplicity-first`, `surgical-changes`, or `verify-before-claiming` | guardrail skills |

## Agent Intent Routing

- Before acting, classify the user intent.
- Use `High-Frequency Skills` as the only repo-local route table.
- If the request writes, rewrites, polishes, prepares, or updates an artifact
  that will be read outside the current chat or worklog, route through the
  applicable parent gate before editing.
- Do not let a child skill or executor replace its parent gate. Examples:
  `imagegen`, browser/search, Python scripts, external CLIs, and shell commands
  are executors after the route owner is selected.
- Do not let public/material output gates replace specialized gates for
  frontmatter, semantic skill edits, OpenSpec lifecycle, wiki medical-loop
  authority, or external learning promotion.
- If multiple routes seem plausible, prefer the narrowest explicit route that
  preserves all parent gates. Ask only when the route ambiguity changes write
  authority or output destination.

## Wiki Runtime Stack

The wiki runtime chain is governed by repo-visible skills, ops records, and
scripts. Do not overclaim autonomy from script success.

| Layer | Use | Entry / Evidence |
|---|---|---|
| Core product contract | Preserve the runtime north star. | `wiki/ops/llm-wiki-core-product-contract.md` |
| Intent / decision trace | Classify route, boundary, forbidden actions, and replay shape. | `wiki-react`; report missing trace anchors instead of inventing them |
| Status / manifest | Inspect runnable status and generated status surfaces. | `wiki-status`, `wiki-manifest`, `scripts/build_wiki_status.py` |
| Graph / relation / scorecard | Inspect explicit structure and drift without semantic invention. | `wiki-graph`, `wiki-scorecard`, graph and scorecard scripts |
| Runtime context / source integration | Build bounded context from local runtime sources. | `wiki-route`, `wiki-context`, `wiki-query` |
| Self-directed execution | Summarize `execute_now`, `defer_for_followup`, and `do_not_execute` as suggestions. | `wiki-apply`; no automatic execution |
| Medical loop | Diagnose, confirm, treat, plan surgery, recover, and report archive checks through a case file. | `wiki-medical-agent` and active case records |
| Frontmatter taxonomy | Validate and repair strict-gated frontmatter. | `wiki-frontmatter-taxonomy`, `wiki/config/frontmatter-taxonomy.yaml` |
| Behavior asset evaluation | Validate behavior changes to AGENTS, rules, skills, and route tables. | `wiki/config/behavior-asset-evaluation.yaml`, OpenSpec evaluation |

## Wiki Medical Loop

- The normal maintenance loop is: doctor -> review/confirm -> treatment or
  surgery -> recovery.
- `wiki-medical-agent` is the single normal user-facing entry point for this
  loop.
- The active medical case file is the authority for allowed actions.
- `Confirmed Decisions` is the only executable decision surface.
- `Proposed Decisions` is not executable.
- Stage records are evidence attachments only.
- Treatment apply requires one active case file, executable confirmed treatment
  decisions, explicit human approval, recovery after apply, and evidence written
  back to the same case file.
- Relation, governance, ADR, MOC, taxonomy, AGENTS, skill, or OpenSpec-sensitive
  findings route to `surgery_required`, `awaiting_confirmation`, or `blocked`
  unless a separate approved workflow scopes the write.

## Frontmatter Taxonomy Gate

- `wiki/config/frontmatter-taxonomy.yaml` is the source of truth for wiki
  frontmatter vocabulary and strict-gate rules.
- Do not duplicate taxonomy vocabulary in `AGENTS.md`.
- Before creating or modifying wiki frontmatter, templates, or frontmatter
  generation scripts, load `.codex/skills/wiki-frontmatter-taxonomy/SKILL.md`.
- Before claiming frontmatter compliance, run
  `python3 scripts/check_wiki_frontmatter.py`.
- Generated wiki pages under strict-gated paths must emit compliant
  frontmatter.

## Skill Authoring Contract

- Repo-local `.codex/skills/*` files are English-first behavior assets unless
  a file explicitly preserves end-user-facing examples in another language.
- Keep repo-local `SKILL.md` files compact: trigger conditions, hard rules,
  concise anti-patterns, and short loading pointers. Move long examples,
  templates, and heavy reference material into linked `references/` files.
- Before creating or semantically editing a skill, classify its routing
  ownership as `high-level router/gate`, `module`, `tool wrapper`, or
  `reference helper`.
- If a skill is delivery-sensitive, name the applicable parent router/gate or
  explicitly state that no parent applies. The module must not weaken or bypass
  its parent gate.
- Semantic skill changes must follow `writing-skills` after reading its
  `test-driven-development` prerequisite. Include pressure scenarios, RED
  baseline, GREEN result, prior-art dedupe, parent-gate preservation, and
  residual risks.
- Semantic `AGENTS.md` changes that alter skill routing or authoring behavior
  must use the same behavior-evaluation standard; do not treat them as ordinary
  markdown edits.

## Output Routing

- Raw upstream material and evidence records belong in `wiki/sources/`.
- Workflow traces, operating learnings, medical cases, status investigations,
  behavior replays, and repo maintenance evidence belong in `wiki/ops/`.
- Stable cross-change decisions belong in `wiki/adr/`.
- Validated output-shape examples belong in `wiki/examples/`.
- Generated status surfaces belong in `wiki/status/`.
- Scoped repository-default behavior changes belong in an OpenSpec change.
- A link by itself does not require a wiki page. If reusable learning is
  extracted, record source reference, what was reused, what was modified, what
  was not formalized, target repo, and next step.

## Verification

- Before claiming the wiki can run, refresh or inspect
  `python3 scripts/build_wiki_status.py`.
- For graph/runtime health, use the existing graph, scorecard, context, route,
  manifest, queue, and self-directed execution scripts as bounded diagnostics
  only.
- For medical-loop readiness, run
  `python3 scripts/build_wiki_medical_agent.py --intent-text "<request>"`.
- For frontmatter compliance, run `python3 scripts/check_wiki_frontmatter.py`.
- For behavior-asset completion, preserve durable OpenSpec evaluation evidence:
  pressure scenarios, RED baseline, GREEN result, prior-art dedupe, verification
  commands, and residual risks.
- If a command reports blocked, awaiting confirmation, preview-only output, or
  missing runtime anchors, report that state instead of calling the wiki
  autonomous.
