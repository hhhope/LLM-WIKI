# Evaluation: interview-deep-reading-board skill

## Pressure Scenarios

### Scenario 1: Long interview plus word cloud request

- Input shape: user asks for a word cloud from a long multi-speaker interview.
- Expected route: load this skill, ask whether to make a full-window interview
  reading board, and treat the word cloud as an index.
- Expected non-route: do not create a decorative word cloud as the main output.

### Scenario 2: User reports compression and a missing passage

- Input shape: user says the output compressed the full interview and names a
  missing passage, such as code volume, Feishu, Coworker, stable employee Agent,
  subagents, data, and MCP.
- Expected route: preserve that passage as an explicit window or window group.
- Expected non-route: do not hide the passage under generic `Agent` keywords.

### Scenario 3: Reader-facing interview H5

- Input shape: user asks for an H5, share page, or reader-facing report from an
  interview.
- Expected route: `public-report-quality-gate` remains the parent gate and
  delegates interview structure to this skill.
- Expected non-route: this skill does not publish, sync to Feishu, or claim
  review-ready status by itself.

### Scenario 4: Ordinary non-dialogue article summary

- Input shape: user asks for a short summary of a non-dialogue article with no
  timeline, temperature axis, or full-coverage concern.
- Expected route: existing material, learning, or public-report workflows.
- Expected non-route: do not ask the full-window interview-board fork question.

## RED Baseline

Baseline checks before creating this skill:

```text
test -e .codex/skills/interview-deep-reading-board/SKILL.md
skill_exists=1

rg -n 'interview-deep-reading-board|全文窗口式精读板|temperature-axis evidence board|interview deep reading' AGENTS.md .codex/skills/public-report-quality-gate/SKILL.md wiki/examples
<no matches>

test -e wiki/examples/interview-deep-reading-board-lixiang-luoyonghao.md
example_exists=1
```

The runtime surface did not have a dedicated interview skill, public gate
delegation, AGENTS route, or H5 example. The original Li Xiang word-cloud output
also demonstrated compression by hiding the Coworker / Feishu / stable Agent /
subagent / MCP section until the user pasted it back.

## GREEN Result

Verified implementation evidence:

- `SKILL.md` defines interview-like triggers and the required Chinese fork
  question.
- `references/h5-output-shape.md` defines the H5 shape and marks the old
  word-cloud artifact as a counterexample.
- `public-report-quality-gate` delegates interview H5/word-cloud/timeline/
  temperature-axis evidence boards to this skill while preserving parent gates.
- `AGENTS.md` includes a lightweight route to this skill.
- `wiki/examples/interview-deep-reading-board-lixiang-luoyonghao.md` links the
  validated H5, data file, source note, and old word-cloud counterexample.

Verification snippets:

```text
skill_exists_after=0
example_exists_after=0

AGENTS.md: route to `.codex/skills/interview-deep-reading-board/SKILL.md`
public-report-quality-gate/SKILL.md: delegation row and hard route check
SKILL.md: required Chinese fork question
wiki/examples/interview-deep-reading-board-lixiang-luoyonghao.md: validated output-shape example
```

## Prior-Art / Common-Rule Dedupe

Scanned:

- repo `AGENTS.md`
- `PROJECT.md`
- `.codex/skills/material-collaboration-defaults/SKILL.md`
- `.codex/skills/public-report-quality-gate/SKILL.md`
- `.codex/skills/learning-capture/SKILL.md`
- `.codex/skills/weixin-reader/SKILL.md`
- `openspec/specs/public-report-quality-gate/spec.md`
- `openspec/specs/skill-authoring-contract/spec.md`
- `openspec/specs/skill-evaluation-evidence/spec.md`
- `openspec/specs/local-skill-pressure-tests/spec.md`
- `docs/superpowers/specs/2026-05-19-interview-deep-reading-board-design.md`

Owns:

- interview-specific full-window reading-board routing;
- interview H5 output-shape reference;
- user-highlighted interview passage protection;
- word-cloud-as-index boundary for interview boards.

References:

- `public-report-quality-gate` for reader-facing readiness, review, publish,
  Feishu sync, and citation boundaries;
- `material-collaboration-defaults` for source-first material handling;
- `weixin-reader` for WeChat retrieval;
- `learning-capture` for reusable learning capture;
- repo `AGENTS.md` and OpenSpec specs for behavior-asset evaluation.

Rejects:

- copying the full interview workflow into `AGENTS.md`;
- replacing the public output gate;
- creating a generic long-form article reading skill;
- storing full copyrighted interview transcripts verbatim;
- treating the old word-cloud-only artifact as the recommended output.

## Residual Risks

- Markdown pressure scenarios do not guarantee every future client will
  auto-load this skill.
- "Full coverage" is structured window coverage, not permission to store a full
  copyrighted transcript.
- Window counts remain proportional to source length.
- A visually polished H5 can still fail if the source-order window map is weak.
