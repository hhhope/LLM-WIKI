---
name: public-report-quality-gate
description: Use when the user asks to write, polish, review, sync, or prepare reader-facing reports, Feishu review drafts, H5/share drafts, public materials, or reference-shaped outputs for an audience outside the current chat or worklog.
---

# Public Report Quality Gate

## Overview

Gate reader-facing output before it becomes a Feishu draft, report, H5, or
shareable material. Internal wiki notes are not public-ready by default.

## Outer Gate Role

For reader-facing output, this skill owns the outer gate. Subordinate skills may
handle source reading, learning capture, visual production, image generation,
Feishu writes, and verification, but they must not bypass the Article Intent
Contract, Reference Output Shape Gate, Visual Gate, Judgment Ownership Gate, or
Publish Gate.

Use this delegation map without replacing the child skills' own rules:

| Public output need | Delegate to |
|---|---|
| source or reference learning | `learning-capture` and narrower modules |
| interview deep reading, interview word cloud, interview timeline, temperature-axis evidence board, or draggable-evidence H5 | `interview-deep-reading-board` |
| article-level visual package | `knowledge-article-visual` |
| per-image poster or card script | `infographic-onepager` |
| generated bitmap assets | `imagegen` |
| Feishu document write | `lark-doc` |
| final verification | gate-review artifact, read-back, and visual QA |

## Repo-Public Lightweight Path

When Agent Intent Routing classifies a request as a repo-public artifact, this
gate owns a lightweight path.

Use the lightweight path for `README.md`, `docs/*`, `examples/*`, and published
templates when the output is meant for future contributors, users, agents, or
other readers outside the current chat or worklog.

Required checks:

- Identify the reader and job-to-be-done before drafting.
- Run an artifact-specific constraint scan before drafting. For README work,
  scan relevant `README SHALL`, `README`, and `readme` hits in `AGENTS.md`,
  `PROJECT.md`, `openspec/specs`, `.codex/skills`, `wiki/adr`, and `wiki/ops`.
- Avoid internal residue unless the artifact intentionally documents repo
  mechanics for its readers.
- Use fresh evidence before claiming the artifact is complete, review-ready,
  published, or synced.

The lightweight path does not require a `wiki/ops/*-report-gate-review.md`
artifact by default for small repo-public documentation edits. Create or update
a gate-review artifact when the output is review-ready, published, synced to
Feishu, complex, reference-shaped, or drift-corrected.

This path must not replace specialized gates for wiki frontmatter, semantic
skill edits, OpenSpec lifecycle, or external learning capture.

## When To Use

Use this skill when the request involves:

- public reports, executive summaries, share drafts, H5 pages, or Feishu review
  drafts
- rewriting internal wiki/ops material for readers
- repo-public artifacts such as `README.md`, `docs/*`, `examples/*`, or
  published templates when they are written, rewritten, polished, prepared, or
  updated for readers outside the current chat or worklog
- using an article, Feishu page, visual example, or prior report as an output
  reference
- claiming a draft is ready for review, sync, publish, or external reading

Do not use this skill for raw source capture, private scratch notes, or code
implementation reports unless the user asks for a reader-facing deliverable.

## Hard Rules

- Do not publish, sync to Feishu, or claim review-ready when any hard gate fails.
- Before Feishu sync or a review-ready claim, create or update a repo-visible
  `wiki/ops/*-report-gate-review.md` artifact.
- For complex, scored, reference-shaped, or drift-corrected drafts, record an
  Article Intent Contract before drafting or scoring: reader, reader decision or
  action, main line, non-goals, user-owned judgments, and agent-allowed work.
- If the output claims to use prior learning or external references, map the
  applicable learning artifacts before drafting: what was used, where it
  appears, and why relevant learning was skipped.
- For newspaper-style H5/share packages or public newspaper drafts, require a
  reader-visible citation surface before review-ready, publish, sync, or share
  claims. Internal source maps, learning use maps, or gate reviews do not
  substitute for reader-visible citations on load-bearing claims, figures,
  company examples, or visual panels.
- When a reference artifact is provided, write or state the reference structure
  map before drafting.
- For reference-shaped outputs, apply the Reference Output Shape Gate before
  review-ready claims: record the selected output shape, preserve it while
  drafting, and fail drafts that silently replace it with a different primary
  structure without explicit user approval. Reader-facing content must not
  include production instructions, image prompts, tool notes, or Hybrid routing
  text.
- If a reference page has child pages or a reading map with concrete links,
  read and map those linked pages before the Reference Structure Gate can pass.
- When content spans multiple reader jobs, choose a split strategy before
  writing a single long draft.
- If any hard gate is failed, partial, unknown, or not tested, do not assign a
  numeric score; mark the scorecard `INVALID`.
- Run a Section And Paragraph Drift Review for complex or drift-corrected
  drafts before review-ready claims. Compare section objectives and paragraph
  claims to the Article Intent Contract, then mark retain, compress, rewrite,
  delete, or ask the user.
- Apply the Judgment Ownership Gate: process can be delegated, but judgment cannot.
  Do not silently turn source material, reference examples, or polished prose
  into the user's main line, conclusion, priority, proof-strength claim, or
  public stance.
- When paragraph drift or judgment ownership fails, the overall score remains
  `INVALID`; diagnostic paragraph scores may still be recorded for repair.
- For complex reader-facing materials, decide reviewer routing before drafting.
  Route to `.codex/agents/public-report-reviewer.md` when at least two reviewer
  escalation signals are true.
- Treat voice quality as a hard gate, not a small style score.
- Preserve the core narrative. If the stated story changes, stop and re-anchor.
- State what each diagram or visual carries; do not add decorative diagrams. If
  the reference uses essential visuals, missing matching visuals are a hard
  Visual Gate failure for reference-shaped output.
- Ask the user at real output fork-points before acting, including image model
  vs H5/HTML, overwrite vs image-only update, draft-only vs Feishu sync, and
  publish title/status changes.
- When interview-like material is headed toward a reader-facing deep-reading
  H5, word cloud, timeline, temperature-axis, draggable-evidence board, or
  no-compression/full-text-coverage output, route interview structure through
  `interview-deep-reading-board` before ordinary report drafting or HTML
  production. This route does not replace this gate's reader intent, reference,
  visual, judgment, publish, or sync blockers.
- When a reader-facing `.html` report or H5 page needs standalone visual
  deliverables or section-level visual assets, do not satisfy the request by
  editing only in-page HTML sections. Stop direct HTML body edits first, route
  to visual package scripting and output-mode selection or inference, and
  produce or plan standalone visual assets before any optional HTML embedding.
- Generate required report visuals as local assets when requested, but do not
  insert images into Feishu by default. If the user will add images manually,
  keep Feishu sync text-only and preserve local asset paths.
- Treat Feishu image insertion as a separate external operation. It requires
  explicit user approval after stating the known client-freeze risk; image-token
  read-back is audit evidence, not proof of client usability.
- Feishu writes are handled by `lark-doc` after this gate passes and the user
  explicitly approves the write. After every Feishu write, use read-back
  verification before claiming success.
- Keep source reading, learning capture, visual generation, Feishu operations,
  and final verification under their own skills.
- Treat learning reuse as process evidence, not automatic promotion into
  `AGENTS.md`, specs, skills, or root instructions.

## Anti-pattern: Tool Executor Bypass

Tool Executor Bypass means routing delivery-sensitive work directly to a
low-level executor because the user mentioned a tool, while skipping the parent
workflow that owns intent, output shape, review, and evidence.

Example: reader-facing H5/report visuals must not jump straight to image
generation because the user mentioned an image model. First follow
`public-report-quality-gate -> knowledge-article-visual ->
infographic-onepager -> imagegen`.

The same principle applies to search/browser, Feishu writing, code execution,
and image generation: they are executors, not workflow owners.

## Load

- Scorecard and hard gates: `references/scorecard.md`
- Gate review artifact contract: `references/gate-review-artifact.md`
- Reviewer routing: `references/reviewer-routing.md`
- Learning use map: `references/learning-use-map.md`
- Report group templates and split routing: `references/report-group-templates.md`
- Validation scenarios: `references/pressure-scenarios.md`

## Common Mistakes

- Turning a wiki ops note into a Feishu draft without rewriting for readers
- Copying a reference page's section labels without mapping its structure
- Keeping the right facts but silently replacing the selected output shape with
  a different primary structure
- Treating linked reading-map articles as placeholders instead of sources
- Silently choosing one output template when reviewer routing is required
- Treating interview word clouds or timelines as ordinary HTML/report work
  instead of routing the interview structure through
  `interview-deep-reading-board`
- Packing overview, runtime, migration, validation, and roadmap into one page
- Using slogans such as "X = manages Y" instead of explaining the evolution
- Letting repo paths, OpenSpec details, or agent workflow leak into public text
- Saying a draft "learned from" a source without showing the section, visual,
  metric, evidence block, boundary statement, or skip reason it affected
- Treating an internal source map as enough for a newspaper/H5 reader when the
  shareable output lacks visible citation routes
- Scoring a whole article while skipping paragraph-level drift diagnostics
- Letting the agent choose the article's public judgment because the prose reads
  smoothly
- Treating broad Feishu sync approval as approval to insert images
- Claiming image delivery quality from image tokens or read-back alone
- Treating a named `.html` target as permission to replace requested one-page
  infographics or knowledge cards with H5 sections only
