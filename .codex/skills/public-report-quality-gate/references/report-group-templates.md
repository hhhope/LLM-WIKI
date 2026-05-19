# Report Group Templates

Use these as structure patterns, not fixed headings. Replace labels with the
reader's language.

## Reference Structure Map

Before drafting from a reference artifact, record:

| Field | Question |
|---|---|
| Source | Which page/article/report is the shape reference? |
| Reader job | What problem does the reference help readers solve? |
| Page group | Is it one page, a multi-page group, or a roadmap series? |
| Reading path | What should readers read first, next, and only if needed? If the reference path links to concrete articles, list each title, URL/token, and confirmed page job. |
| Visual logic | What do diagrams carry: layers, lifecycle, contrast, maturity, or decisions? |
| Writing standard | What tone, density, section opening style, and evidence style does it use? |
| Reuse boundary | What shape is reused, what content is local, and what must not be copied? |

Reference map completeness rule:

- A parent wiki page with `has_child: true` is incomplete until its linked or
  child pages are read.
- A reading map with concrete links is incomplete until each linked page's title
  and job are recorded.
- A reference with essential visuals is incomplete until the local visual plan
  says what matching visual relationship, sequence, contrast, or decision will
  carry.
- Incomplete reference maps force Reference Structure Gate `FAIL` and scorecard
  `INVALID`.

## Learning Use Map

Before drafting from prior learning, record:

| Field | Question |
|---|---|
| Learning artifact | Which wiki note, source record, example, or prior gate review is being reused? |
| Domain / topic | What is the source about? |
| Reusable capability type | Is the reusable lesson content, structure, visual, evidence, or boundary? |
| Learning point | What exact lesson is expected to shape the output? |
| Output use | Which section, visual, metric, evidence block, boundary statement, or named output element will use it? |
| Skip reason | If the lesson is relevant but not used, why? |

The learning use map proves the output process used or rejected learning
deliberately. It does not make internal wiki paths part of the public article
unless citations are requested.

## Split Routing

Split the material when at least two of these are true:

- one page explains the whole system and another explains runtime behavior
- adoption/migration steps need a separate checklist
- validation/evidence deserves its own page
- roadmap/maturity stages are useful but distract from the overview
- the overview exceeds a focused reader journey
- the user asks for reference parity with a multi-page source
- the reference reading map points to concrete linked articles

## Four-Page Group Pattern

| Page | Owns | Must Not Own |
|---|---|---|
| Overview | positioning, composition, audience, reading path, main evolution story | detailed implementation, exhaustive evidence |
| Runtime | default operating sequence, roles, handoffs, expected behavior | installation history or roadmap promises |
| Install / Migration | adoption sequence, prerequisites, done criteria | daily runtime details |
| Validation / Cases | evidence, examples, proof boundaries, non-overclaim notes | new policy or unresolved design |

Optional fifth page:

| Page | Owns | Must Not Own |
|---|---|---|
| Roadmap | maturity levels, next-stage priorities, constraints | claiming future automation is already present |

## Public Draft Skeleton

```markdown
# <Reader-facing title>

> <One sentence positioning: what this helps the reader understand or decide.>

## Why This Exists

<Problem and stakes in reader language.>

## The Evolution Path

<Main story. For example: scattered work memory -> reusable team knowledge ->
structured knowledge base.>

## How To Read This Group

| If you want to know... | Read... | Outcome |
|---|---|---|

## Current Stage

<One table or diagram that gives the reader orientation.>

## What This Does Not Claim

<Boundaries, proof limits, and next review needs.>
```
