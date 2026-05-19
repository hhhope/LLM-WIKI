---
name: wiki-recovery
description: Use only for explicit legacy/debug recovery evidence; ordinary wiki medical-loop recovery requests route through wiki-medical-agent.
---

Use this skill for the recovery / 复查 stage of the LLM-WIKI medical loop.
Recovery proves current state by running bounded non-mutating checks and
preserving failures as findings.

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

1. Confirm the current repository has `scripts/build_wiki_recovery.py`.
2. Run or reference `python3 scripts/build_wiki_recovery.py`.
3. Preserve check summaries, command exit codes, and failure findings.
4. Treat `blocked_by_recovery_findings` as not fixed yet.
5. Treat `archive-ready` as a recovery result only, not automatic archive.
6. If the user asks for a recovery record, run
   `python3 scripts/build_wiki_recovery.py --write-recovery-record`.

Boundaries:

- Do not create, modify, archive, or queue OpenSpec changes.
- Do not mark OpenSpec tasks complete.
- Do not execute queued work.
- Recovery does not apply treatment or surgery.
- Do not write frontmatter.
- Do not write relation fields.
- Do not mutate `wiki/config/frontmatter-taxonomy.yaml`.
- Do not write `wiki/moc` files.
- Do not mutate ADR decisions, AGENTS, skills, status files, or OpenSpec state.
