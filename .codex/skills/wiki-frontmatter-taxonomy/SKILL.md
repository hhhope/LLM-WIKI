---
name: wiki-frontmatter-taxonomy
description: Use when creating or modifying report wiki frontmatter, wiki templates, or repo-local scripts that generate wiki frontmatter.
---

Use the repo-local wiki frontmatter taxonomy gate.

Default routine check:

- Run `python3 scripts/wiki_gate_precheck.py --mode frontmatter` first.
- Add `--target PATH` when checking a specific page.
- Read the compact pass/fail, score, blocking count, top blockers, target
  repair hints, and full report paths from precheck output.

Load full sources only when needed:

- `wiki/config/frontmatter-taxonomy.yaml` when editing taxonomy config or when
  precheck output is insufficient to choose a field.
- `scripts/check_wiki_frontmatter.py` when changing or debugging checker logic.
- `docs/superpowers/specs/2026-05-13-wiki-frontmatter-taxonomy-design.md` when
  design context is needed.

Hard rules:

- Do not duplicate taxonomy vocabulary in this skill.
- Do not load the full taxonomy YAML or checker by default.
- Treat user language, AI drafts, folder names, and script guesses as hints until validated.
- Do not use local skill templates or ad hoc agent judgment as final taxonomy authority.
- Run the precheck before claiming taxonomy compliance or completion.
- If the precheck or checker reports errors, do not claim the taxonomy work is complete.

When creating or modifying frontmatter:

1. Run the precheck with `--target PATH`.
2. Determine the page layer by path and task.
3. Apply exact values and field options from `target.repair_hints`.
4. Use explicit uncertainty fields when classification is not known.
5. Load `wiki/config/frontmatter-taxonomy.yaml` only if repair hints do not identify the needed rule or option.
6. Run the precheck again and summarize remaining drift.

Boundaries:

- Do not batch-migrate legacy pages unless the active OpenSpec change lists them.
- Do not edit global agent instructions.
- Do not change scorecard scoring formulas from this skill.
- Do not treat checker warnings as proof that all legacy drift has been resolved.
