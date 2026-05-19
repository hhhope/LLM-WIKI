# OpenSpec / Superpowers Execution Overlay

## Bad Shape: Parallel Task Ledger

This shape caused drift during `add-product-status-contract`:

```md
# Implementation Plan

## Task 1: RED Tests
- [ ] Step 1: Add test A
- [ ] Step 2: Run RED command
- [ ] Step 3: Commit RED tests

## Task 2: Product Status Module
- [ ] Step 1: Create module
- [ ] Step 2: Wire manifest

## Task 6: OpenSpec Task Sync And Final Verification
- [ ] Step 1: Run focused tests
- [ ] Step 2: Update OpenSpec tasks with verification notes
```

Why this drifts:

- `Task 1..6` is a second task numbering scheme.
- `- [ ]` checkboxes become a second progress ledger.
- `tasks.md` becomes a final handback target instead of the live OpenSpec
  progress source.

## Good Shape: Execution Overlay

```md
# Execution Overlay

Applies to OpenSpec change: `add-product-status-contract`

Authority:
- `tasks.md` is the only progress and completion ledger.
- This file records execution strategy only.
- This file must not define independent task ids.
- This file must not use progress checkboxes.
- If this file conflicts with `tasks.md`, follow `tasks.md`.

## TDD Strategy

RED evidence to collect:
- Missing manifest contract fails with `KeyError: 'product_status'`.
- Missing Markdown section fails with `"## Product Status" not found`.

GREEN sequence:
- Add product-status computation.
- Wire it into `build_manifest`.
- Add Markdown rendering.
- Regenerate status artifacts.

## Module Strategy

Keep `scripts/build_wiki_status.py` as orchestration.

Extract:
- `scripts/wiki_product_status.py`
- `scripts/wiki_status_render.py`

## Commit Strategy

Use small verified commits as recovery points:
- RED tests only.
- Manifest implementation.
- Markdown rendering.
- Generated status artifacts.
- OpenSpec task progress update.

Commit slices are recovery evidence, not progress truth.

## Verification Strategy

Run before completion claim:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_wiki_status
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
openspec validate add-product-status-contract --strict
openspec validate --all
git diff --check
```

## Handoff Rule

On resume:
- Read `tasks.md` first for progress.
- Read this overlay only for execution tactics.
- If they disagree, trust `tasks.md`.
```
