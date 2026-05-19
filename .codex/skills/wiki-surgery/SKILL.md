---
name: wiki-surgery
description: Use only for explicit legacy/debug surgery evidence; ordinary wiki medical-loop surgery requests route through wiki-medical-agent.
---

Use this skill for the surgery / 手术 stage of the LLM-WIKI medical loop.
Surgery is plan-only in this repository until a later explicit apply workflow
or OpenSpec change exists.

Ordinary use routes through `wiki-medical-agent`.

Use this stage skill directly only for explicit legacy/debug evidence. Direct
stage output is legacy/debug evidence only; it is not authoritative and does
not update case state unless routed through the medical agent and written back
to the active case file.

Medical-loop sequence:

```text
wiki-doctor -> wiki-confirm -> wiki-treatment -> wiki-surgery -> wiki-recovery
诊断 -> 确诊 -> 治疗 -> 手术 -> 复查
```

When triggered:

1. Confirm the current repository has `scripts/build_wiki_surgery.py`.
2. Make the intent judgment before running surgery:
   if `wiki/ops/wiki-medical-cases/` contains a current case file, use that
   file as the authority and run
   `python3 scripts/build_wiki_surgery.py --case-file <case-file>`.
3. If the user asks for a surgery record for that case, run
   `python3 scripts/build_wiki_surgery.py --case-file <case-file> --write-surgery-record --update-case-file`.
   This writes a surgery evidence attachment and updates the same case file.
4. If no case file exists, stop and route to `wiki-confirm` or
   `scripts/build_wiki_medical_case.py`; do not silently fall back to raw
   adjudication for normal surgery intent.
5. Use surgery planning for `relation_weak_evidence`, `drift_risk`,
   `adr_risk`, `openspec_required`, taxonomy candidates, MOC projection
   changes, governance pages, and broad batch repair.
6. Explain the output as a plan-only surgery package, not surgery approval.
   Human review targets the case file's `Confirmed Decisions`; the surgery
   record is only a fidelity/evidence attachment.

Boundaries:

- Do not create, modify, archive, or queue OpenSpec changes.
- Do not mark OpenSpec tasks complete.
- Do not execute queued work.
- Do not write frontmatter.
- Do not write relation fields.
- Do not mutate `wiki/config/frontmatter-taxonomy.yaml`.
- Do not write `wiki/moc` files.
- Do not mutate ADR decisions, AGENTS, skills, or OpenSpec state.
- Do not treat a surgery plan as approval to apply surgery.
- Route post-operation checks to `wiki-recovery`.
