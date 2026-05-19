---
name: wiki-treatment
description: Use only for explicit legacy/debug treatment evidence; ordinary wiki medical-loop treatment requests route through wiki-medical-agent.
---

Use this skill for the treatment / 治疗 stage of the LLM-WIKI medical loop.
Treatment handles bounded low-risk frontmatter repair after explicit human
approval.

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

1. Confirm the current repository has `scripts/build_wiki_treatment.py`.
2. Make the intent judgment before running treatment:
   if `wiki/ops/wiki-medical-cases/` contains a current case file, use that
   file as the authority and run
   `python3 scripts/build_wiki_treatment.py --case-file <case-file>`.
3. Default to dry-run: treatment defaults to dry-run and must not write files
   unless `--apply` is present.
4. Require explicit human approval through `--approved-domain` or
   `--approved-detail`.
5. To actually apply the case-confirmed treatment candidates, keep
   `--case-file <case-file>`, add `--apply`, and add either
   `--approved-domain` or `--approved-detail`.
6. When writing a treatment record for a case, also use `--update-case-file`
   so the same case file records the treatment evidence attachment.
7. Treat `--write-treatment-record` as a reviewable treatment record under
   `wiki/ops/wiki-treatment-runs/`, not as surgery approval.
8. The human review surface is the case file's `Confirmed Decisions`; do not
   rebuild treatment intent from raw adjudication for normal case treatment.

Boundaries:

- Do not create, modify, archive, or queue OpenSpec changes.
- Do not mark OpenSpec tasks complete.
- Do not execute queued work.
- Do not apply treatment without `--apply`.
- Do not apply treatment without `--approved-domain` or `--approved-detail`.
- Do not write relation fields.
- Do not mutate `wiki/config/frontmatter-taxonomy.yaml`.
- Do not write `wiki/moc` files.
- Do not mutate ADR decisions, AGENTS, skills, or OpenSpec state.
- Route broad, structural, governance, relation, MOC, ADR, taxonomy, or
  OpenSpec-sensitive work to `wiki-surgery`.
