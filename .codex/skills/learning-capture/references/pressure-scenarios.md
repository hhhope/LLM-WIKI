# Learning Capture Pressure Scenarios

Use these scenarios when validating `learning-capture`.

## Should Trigger

| Scenario | Expected | Result |
|---|---|---|
| User provides a technical article and says "精读，学到能力，落 wiki" | Trigger `learning-capture`, then article module | PASS |
| User drops article links inside an ongoing "学习这件事怎么做" thread without saying "学习一下" again | Trigger `learning-capture`, then classify each source kind | PASS |
| User provides multiple agent engineering articles and asks what is useful to the local system | Trigger `learning-capture`, then article module | PASS |
| User provides 30 article links in a learning thread | Trigger `learning-capture`, batch triage first, deep-read only sources meeting module threshold | PASS |
| User says "these are agent harness articles" | Trigger `learning-capture`, check existing agent/harness wiki topic before durable notes | PASS |
| User provides a GitHub repo and asks "这个方案能不能复用" | Trigger `learning-capture`, then repo-readme module | PASS |
| User provides a bare GitHub repo link after discussing reusable skill structure | Trigger `learning-capture`, then repo-readme module | PASS |
| User provides a GitHub README and asks to learn its structure for a local SOP | Trigger `learning-capture`, then repo-readme module | PASS |
| User provides a concrete output example and asks to reuse its structure | Trigger `learning-capture`, then example-reference module | PASS |

## Should Not Trigger

| Scenario | Expected | Result |
|---|---|---|
| User asks for latest news or fact lookup with no local reuse intent | Do not trigger learning capture | PASS |
| User asks only to fetch raw WeChat body text | Use `weixin-reader` | PASS |
| User sends a bare link with no learning thread, reuse intent, wiki intent, or method-calibration context | Do not trigger learning capture by default | PASS |
| User asks for a short abstract with no wiki or adaptation intent | Do not trigger learning capture | PASS |
| User provides a source with weak inferred topic only | Keep candidate for weekly review; do not force a wiki topic link | PASS |

## Cross-Route Cases

| Scenario | Expected | Result |
|---|---|---|
| Article describes a repo, but repo is not read | Article module; mark secondary interpretation where needed | PASS |
| Article describes a repo, and user asks whether repo structure can be reused | Article module first, then repo-readme module after reading repo/README | PASS |
| README is used only as an output-shape example | Example-reference module may be enough; do not force full repo learning | PASS |
| Article or repo takeaway is proposed for `AGENTS.md` | Require evidence-backed promotion gate or scoped OpenSpec change | PASS |

## Article Surface Retirement

| Scenario | Expected behavior |
|---|---|
| User provides a Chinese WeChat article and says "学一下，落 wiki" | Load `learning-capture`, route to article module, produce Chinese durable learning notes |
| User says "article learning 这套复用一下" | Load `learning-capture`, not a separate `article-learning-capture` skill |
| User provides a GitHub README for reuse | Load `learning-capture`, route to repo/README module |
| User provides an output-shape example | Load `learning-capture`, route to example/reference module |
| User asks for an English public README update | Keep the target artifact English-first |
