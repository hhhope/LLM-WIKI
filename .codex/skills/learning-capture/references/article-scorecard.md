# Article Learning Scorecard

Use this scorecard before deep reading. It has two stages: an admission gate and
a value score. Do not score a source until the admission gate is recorded.
If a score is created after deep reading or after conclusions were drafted, mark
it `retrospective`; it is useful for audit but does not count as score-first
admission evidence.

## Stage 1: Admission Gate

| Gate | Pass Condition | If It Fails |
|---|---|---|
| Source access | Original source, pasted text, screenshot, local PDF, or extracted body is available | Maximum score 40; ask for source material before deep reading |
| Source class | Classified as primary source, secondary interpretation, structure reference, or low-relevance/general-interest | Stop and classify before scoring |
| Source grounding | Extracted markdown, source map, bounded excerpts, or retrieval-failure note exists | Maximum score 50 until grounding exists |
| Local objective | User asks for learning, wiki capture, SOP, scoring, or local transfer | Do not use the article module |
| Copyright boundary | Useful notes can be written without full verbatim article text or full verbatim translation | Maximum score 59 |

## Source Classes

| Source Class | Use | Maximum Score |
|---|---|---:|
| Primary source | Authoritative source for the method, API, experiment, project, or official practice being studied | 100 |
| Secondary interpretation | Commentary, synthesis, translation, newsletter, or repost about another source | 80 unless it adds unique evidence; cannot be the only evidence for promotion |
| Structure reference | Example used for article structure, writing pattern, visual organization, or learning format | 80; use for format/method shape, not factual proof |
| Low-relevance/general-interest | Interesting but not tied to the current repo, agent workflow, output method, or behavior assets | 59 |

Apply the lowest relevant cap after scoring.

## Stage 2: Value Score

| Criterion | Points | Full Credit Anchor | Partial Credit Anchor | Zero Credit Anchor |
|---|---:|---|---|---|
| Source access and provenance | 20 | Stable URL plus author/publisher/date/access date and preserved source artifact | Metadata or source artifact is incomplete but recoverable | Source chain is unavailable or unverifiable |
| Evidence or method density | 25 | Contains concrete implementation detail, data, experiment, logs, architecture, or replayable method | Contains useful practice detail but limited evidence | Mostly generic opinion or slogan |
| Local capability gain | 25 | Changes how this repo should read, write, verify, route, or preserve work | Useful background but weak local action | No local workflow or asset implication |
| Transfer path | 15 | Can map to a wiki note, SOP, template, fixture, demo, comparison, or scoped change | Transfer path is plausible but not yet concrete | No clear artifact or behavior target |
| Verification path | 15 | Has an observable check: source citation, local demo, fixture, command, git comparison, or manual replay | Verification is possible but indirect | No way to verify the extracted learning |

## Decision Thresholds

- 75-100: deep-read and write durable wiki learning notes.
- 60-74: brief-read and keep a candidate note.
- Below 60: record source and skip reason.

Do not deep-read low-scoring material by default.

## Hard Caps

Apply the lowest relevant cap after scoring:

| Condition | Maximum Score |
|---|---:|
| Original source cannot be accessed and user did not provide content | 40 |
| Source grounding is missing | 50 |
| No credible author, publisher, or source chain | 55 |
| No evidence beyond opinion or generic advice | 65 |
| Secondary interpretation without unique evidence | 70 |
| Structure reference being used as factual proof instead of format/method shape | 59 |
| Low local relevance even if generally interesting | 59 |
| Duplicates existing repo learning with no new angle | 59 |
| Copyright boundary would require full verbatim reproduction to be useful | 59 |

## Required Score Record

Each scored article should record:

- admission gate result
- source class
- source artifact type
- score timing: score-first or retrospective
- total score
- score band
- per-criterion scores
- hard cap applied, if any
- decision: deep-read / brief-read / skip
- reason in one or two sentences

## Calibration Notes

- A famous source does not automatically score high.
- Primary-source status is not enough; local capability gain and verification
  path still matter.
- A secondary interpretation may be valuable for framing, but promotion needs
  primary-source or local evidence.
- A structure reference can teach output shape without proving technical claims.
- Do not use the score to hide uncertainty. If evidence is weak, mark the
  transfer point as candidate.
- Do not repair a missing score-first gate by adding a retrospective score and
  treating it as if it justified the original deep read.
