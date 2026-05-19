# Learning Capture Routing

Use this reference when intent or source kind is not obvious.

## Intent Gate

| User Intent | Learning Capture? | Route |
|---|---|---|
| Deep-read, `精读`, learn capability, or learn what is useful | yes | classify source kind |
| Bare article, repo, README, or example link inside an active learning / governance / method-calibration thread | yes | classify source kind |
| Source provided immediately after the user asks how learning should work | yes | classify source kind |
| Write to wiki from source learning | yes | classify source kind |
| Score whether a source deserves deep reading | yes | classify source kind |
| Decide what to reuse, adapt, reject, or formalize | yes | classify source kind |
| Turn external-source learning into SOP, template, skill candidate, or workflow decision | yes | classify source kind |
| Latest news or fact lookup | no | answer normally, browsing if needed |
| Raw article / WeChat body fetch only | no | use source-specific reader |
| Bare link with no local reuse context and no learning thread | no | ask or handle as ordinary lookup/fetch |
| Short abstract with no local reuse intent | no | answer normally |
| Generic code review | no | use review workflow |

## Link Trigger Replay

Use this replay matrix when the user asks what should happen the next time they
drop a link, or when a bare link arrives in a recent learning / governance /
method-calibration thread.

| Input shape | Learning Capture? | Required route | Durable output |
|---|---|---|---|
| Bare article link inside an active learning / governance thread | yes | article module -> admission -> score | wiki notes only if the score and topic anchor justify them |
| `mp.weixin.qq.com` link inside an active learning / governance thread | yes | `weixin-reader` or equivalent source grounding -> article module -> admission -> score | wiki notes only if the score and topic anchor justify them |
| GitHub/GitLab repo or README link with learn/reuse/adapt intent | yes | repo/README module -> admission -> score | wiki notes only if the score and topic anchor justify them |
| Raw source body fetch, latest-news, fact lookup, or short abstract request | no | narrower source-specific or lookup path | no durable learning output by default |
| Bare link with no active learning context, local reuse context, wiki intent, or method-calibration context | no | clarify intent or handle as ordinary lookup/fetch | no durable learning output by default |

Replay output must state:

- selected route
- source kind
- score band or reason scoring did not run
- wiki target, weekly-review candidate status, or skip reason
- adoption boundary
- whether promotion is blocked pending evidence

## Source Kind Gate

| Source Kind | Signal | Module Route |
|---|---|---|
| Article-shaped | article, blog, paper, newsletter, WeChat post, article collection | `article.md` |
| Repo/README-shaped | GitHub/GitLab repo URL, README URL, repo docs, project structure | `repo-readme.md` |
| Example-shaped | output example, writing style, visual structure, workflow shape, method example | `example-reference.md` |
| Mixed | article discusses a repo, repo README supports an article, or example carries a method | start with the directly available source, then route to the second module only when the user asks for that evidence |

## Domain vs Reusable Capability Gate

Do not collapse the source's topic into the thing we learned to reuse.

| Field | Meaning | Example |
|---|---|---|
| Domain / topic | What the source is about | `agent harness`, `skill authoring`, `wiki governance`, `public report writing` |
| Reusable capability type | What future output can reuse from it | `content`, `structure`, `visual`, `evidence`, `boundary` |

Capability types:

| Type | Use when the source teaches... |
|---|---|
| `content` | concepts, arguments, facts, claims, vocabulary |
| `structure` | article order, section rhythm, split strategy, reading map |
| `visual` | diagram role, visual density, lifecycle map, comparison graphic |
| `evidence` | metrics, cases, observable scenes, proof style |
| `boundary` | adoption limits, future/current separation, non-claims |

Examples:

| Source | Domain | Reusable capability type |
|---|---|---|
| Skill authoring article | skill authoring / agent workflow | structure, visual, boundary |
| Account Harness reference group | agent harness / knowledge base | structure, visual |
| Agent SaaS WeChat article | agent-first software | structure, evidence, boundary |

## Topic Anchor Gate

| Topic Signal | Action |
|---|---|
| User explicitly names a topic, such as agent, harness, eval, README structure, or workflow governance | Check `wiki/ops/index.md`, matching filenames, and existing topic pages before creating durable notes |
| Source title or repo name strongly matches an existing wiki title, filename, or index entry | Prefer updating or linking the existing topic |
| Topic is weak, inferred only semantically, or not named by the user | Keep a candidate note for weekly review; do not force a link |
| Source is low-scoring or only generally interesting | Record skip reason or candidate status; do not create a durable topic page |

## Batch Triage

- When many sources arrive together, triage intent and score sources before
  deep reading.
- Only sources meeting the module's deep-read threshold should receive durable
  reading notes by default.
- Brief candidates and skip records are inputs for weekly review, not immediate
  compiled wiki pages.

## Mixed-Source Rules

- An article about a repo is article-shaped until the repo or README is read.
- A repo README used only for writing structure may be example-shaped.
- A WeChat article used only for raw body extraction should not trigger learning
  capture.
- A secondary interpretation can frame learning, but promotion needs primary
  source or local evidence.
- A topic anchor is a routing decision, not proof that the source is worth deep
  reading.

## Output Contract

Every learning result should say:

- source kind
- topic anchor or weekly-review candidate status
- source domain/topic when known
- reusable capability type when the point is expected to shape future output
- selected module
- what was learned
- local usefulness
- adoption boundary
- intended output use or skip reason when relevant
- next repository target, if any

For report, H5, Feishu, or public-material follow-up, hand off to
`references/output-use.md` and the public report quality gate.
