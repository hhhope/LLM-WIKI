# Learning Output Use Handoff

Use this when a learning artifact is expected to shape a later report, H5,
Feishu draft, skill, OpenSpec proposal, or public material.

## Core Distinction

| Field | Question |
|---|---|
| Domain / topic | What is the source about? |
| Reusable capability type | What output capability did we learn from it? |
| Output use | Where will this learning change the output? |

Reusable capability type is not the source domain.

## Capability Types

| Type | Meaning |
|---|---|
| `content` | A concept, claim, argument, or vocabulary to consider |
| `structure` | Article order, split strategy, reading map, or section rhythm |
| `visual` | Diagram role, visual density, lifecycle map, or comparison graphic |
| `evidence` | Metrics, observable scenes, cases, or proof style |
| `boundary` | Future/current split, adoption boundary, or non-claim |

## Output Use Map Fields

Record these before claiming that a later output uses the learned reference:

| Field | Required Meaning |
|---|---|
| Learning artifact | Wiki path or source reference |
| Domain / topic | Source topic, if known |
| Capability type | `content`, `structure`, `visual`, `evidence`, or `boundary` |
| Learning point | The reusable lesson in one sentence |
| Output use | Section, visual, metric, evidence block, boundary statement, or skip |
| Skip reason | Required when the point is relevant but not used |

## Rules

- The final public draft does not need to expose internal wiki paths unless the
  user asks for citations.
- Newspaper-style H5/share packages and public newspaper drafts are stricter:
  the output-use map is internal process evidence and does not replace a
  reader-visible citation surface for load-bearing claims, figures, company
  examples, or visual panels.
- Do not force every learning point into the output.
- Do not silently discard relevant learning while claiming the output used it.
- Learning output use does not promote a point into a rule, spec, or skill.
