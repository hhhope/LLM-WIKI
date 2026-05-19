# Repo/README Learning Pressure Scenarios

Use these scenarios when validating repo/README learning through
`learning-capture`.

## Should Trigger

| Scenario | Expected | Result |
|---|---|---|
| User provides a GitHub repo and asks "这个方案能不能复用" | Trigger `learning-capture`, route to repo/README module, run admission and score first | PASS |
| User provides a README and asks to learn its structure for a local SOP | Score first; deep-read only if 75+ | PASS |
| User provides a repo after discussing reusable skill structure | Treat as learning context and score before deep reading | PASS |
| User asks what to reuse, adapt, reject, or formalize from a repo | Preserve reused / modified / rejected / adoption boundary / status | PASS |

## Should Not Trigger

| Scenario | Expected | Result |
|---|---|---|
| User asks for generic code review of a repository | Use review workflow, not README learning | PASS |
| User provides a bare repo link with no learning, reuse, wiki, or method context | Do not assume durable learning by default | PASS |
| User asks for latest repo stars or facts only | Answer fact lookup; do not create learning notes | PASS |

## Gate Scenarios

| Scenario | Expected | Result |
|---|---|---|
| Repo scores 75+ after admission | Deep-read and write durable wiki notes | PASS |
| Repo scores 60-74 | Keep brief candidate for review | PASS |
| Repo scores below 60 | Record source and skip reason | PASS |
| Repo conclusion is used to modify `AGENTS.md` | Require evidence-backed promotion gate or OpenSpec change | PASS |
