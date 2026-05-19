# Reviewer Routing

Use this reference to decide whether a public/report/H5/Feishu draft needs the
manual reviewer role before drafting, scoring, syncing, or claiming
review-ready.

## Escalation Signals

Reviewer routing is required when at least two signals are true:

| Signal | Meaning |
|---|---|
| Multi-page or series output | The material contains overview, runtime, migration, validation, roadmap, or similar page groups |
| External reference structure | A Feishu wiki, article, visual example, prior report, or repo example shapes the output |
| Public target | The output is a Feishu review draft, H5, executive report, or shareable material |
| Evidence decision | A scorecard, gate-review artifact, sync-readiness decision, or read-back evidence is required |
| Drift history | The user reported drift, failed quality, missing template choice, or rejected draft |
| Template / visual / learning choice | The task needs template selection, visual style selection, or learning-use mapping |

## Required Behavior

When reviewer routing is required:

- record `reviewer routing: required` in the gate-review artifact
- load `.codex/agents/public-report-reviewer.md`
- do not silently choose the final template
- do not assign a quality score until hard gates pass
- keep rubric-schema checks separate from draft-quality scores
- do not spawn a sub-agent unless the user explicitly asks for delegation

When reviewer routing is not required:

- record `reviewer routing: not required` or `not applicable`
- state which signals were checked
- continue with the ordinary public report hard gates

## Invalid States

- A complex report has at least two escalation signals, but the gate-review
  artifact omits reviewer routing.
- The agent picks one template without listing alternatives when reviewer
  routing is required.
- A score of 100 from rubric schema arithmetic is treated as draft-quality
  proof.
- Reviewer routing is used as permission to auto-spawn a sub-agent.
