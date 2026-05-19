---
name: wiki-medical-agent
description: Use as the single normal user-facing entry point for wiki medical-loop status, diagnosis, confirmation, treatment, surgery, recovery, and archive checks.
---

Use this skill as the single normal user-facing entry point for the LLM-WIKI
medical loop.

The agent must classify user intent before execution, resolve the active case
file, validate state, then route to the bounded worker.

Normal command:

```bash
python3 scripts/build_wiki_medical_agent.py --intent-text "<user request>"
```

Every response must show:

- Intent
- Case
- State
- Allowed action
- Blocked action, when blocked
- Next Action

Authority model:

- The case file is the only authority.
- `Confirmed Decisions` is the only executable decision surface.
- `Proposed Decisions` is not executable.
- Stage records are evidence attachments only.

Status / Blocked Response:

- If the user only asks for status, report the fixed fields above.
- If the user is trying to continue, modify, apply, repair, or decide next
  steps, and the medical-agent result is `report_status`, `blocked`,
  `awaiting_confirmation`, or `archive_ready`, do not stop at the fixed fields.
- Before asking the user for missing details, provide a read-only prediagnosis
  based on already available state or at most one local read-only check.
- Include: script result, interpreted live user intent, read-only
  prediagnosis, recommended next action, and the specific point that still
  requires user confirmation, if any.
- This rule does not expand write authority or bypass the case-file authority
  model.

Treatment apply:

- Requires one active case file.
- Requires executable confirmed treatment decisions.
- Requires explicit human approval via `--approved-domain` or
  `--approved-detail`.
- Must run recovery after apply.
- Must update the same case file with treatment and recovery evidence.

Boundaries:

- Do not auto-execute newly discovered candidates.
- Do not write relation fields.
- Do not mutate taxonomy config, MOC pages, ADRs, AGENTS, skills, or OpenSpec
  lifecycle state unless a separate approved workflow explicitly scopes it.
- Relation, governance, ADR, MOC, and OpenSpec-sensitive findings route to
  `surgery_required`, `awaiting_confirmation`, or `blocked`.
