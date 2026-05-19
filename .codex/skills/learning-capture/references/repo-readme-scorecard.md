# Repo/README Learning Scorecard

Use this scorecard before deep reading a GitHub/GitLab repository or README.
Do not score until the admission gate is recorded.

## Admission Gate

| Gate | Pass Condition | If It Fails |
|---|---|---|
| Source access | Repository, README, repo docs, or pasted equivalent is available | Maximum score 40; ask for source material before deep reading |
| Source class | Classified as official repo, example repo, implementation reference, structure reference, or low-relevance/general-interest | Stop and classify before scoring |
| Source grounding | README, key files, directory map, or retrieval-failure note exists | Maximum score 50 until grounding exists |
| Local objective | User asks for reuse, adaptation, template, skill, workflow, wiki, or local transfer | Do not use this module |
| Adaptation boundary | Local reuse can be separated from copying external structure wholesale | Maximum score 59 |

## Source Classes

| Source Class | Use | Maximum Score |
|---|---|---:|
| Official repo | Source repository for the project, tool, framework, or workflow being studied | 100 |
| Implementation reference | Repo demonstrates concrete structure, tests, commands, skills, agents, or docs useful locally | 90 |
| Example repo | Repo is useful as a pattern example but is not authoritative for the domain | 80 |
| Structure reference | Repo is used for information architecture, writing shape, or workflow organization | 80; not factual proof |
| Low-relevance/general-interest | Interesting but weak local transfer path | 59 |

Apply the lowest relevant cap after scoring.

## Value Score

| Criterion | Points | Full Credit Anchor |
|---|---:|---|
| Source access and provenance | 20 | Stable repo/README URL plus key path list and access date |
| Evidence or method density | 25 | Concrete docs, skills, commands, tests, examples, or operating workflow |
| Local capability gain | 25 | Changes how this repo should route, write, verify, store, or review work |
| Transfer path | 15 | Maps to wiki note, SOP, template, skill candidate, comparison, or OpenSpec change |
| Verification path | 15 | Can be checked by repo paths, commands, structure comparison, or manual replay |

## Score Bands

| Score | Action |
|---|---|
| 75-100 | Deep-read and write durable wiki notes |
| 60-74 | Brief-read and keep a candidate note |
| 0-59 | Record source and skip reason |

Do not deep-read low-scoring repos by default.

## Required Score Record

- admission gate result
- source class
- source artifact type
- score timing: score-first or retrospective
- total score
- score band
- per-criterion scores
- hard cap applied, if any
- decision: deep-read / brief-read / skip
- reused / modified / rejected / adoption boundary / status
