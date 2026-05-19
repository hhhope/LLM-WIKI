---
layer: status
domain: none
canonical_object: wiki-status
artifact_type: generated-status
status: generated
---

# Wiki Status

Generated at: `2026-05-19T10:21:02.257526+00:00`

## Summary

| Metric | Value |
| --- | --- |
| Wiki pages | 17 |
| Source records | 2 |
| Inbox files | 0 |
| Pending inbox files | 0 |
| Active OpenSpec changes | 1 |
| Complete active-dir changes | 1 |

## Wiki Sections

| Section | Pages |
| --- | --- |
| wiki/adr | 2 |
| wiki/domains | 1 |
| wiki/examples | 2 |
| wiki/ops | 6 |
| wiki/reports | 1 |
| wiki/root | 1 |
| wiki/sources | 3 |
| wiki/timeline | 1 |

## Product Status

Contract version: `1`

### Object Types

| Object Type | Count |
| --- | --- |
| governance | 4 |
| output | 1 |
| source | 3 |
| unknown | 11 |

### Readiness

| Readiness | Count |
| --- | --- |
| accepted | 1 |
| draft-only | 16 |

### Source Layers

| Source Layer | Count |
| --- | --- |
| ops | 6 |
| report | 1 |
| source | 3 |
| spec | 4 |
| unknown | 5 |

### Identity Coverage

| Metric | Value |
| --- | --- |
| With identity | 8 |
| Missing identity | 9 |

### Relation Coverage

| Metric | Value |
| --- | --- |
| With relations | 0 |
| Missing relations | 17 |

### Unresolved Product Status Items

- `bootstrap-self-running-wiki-governance`: complete_openspec_change (unresolved -> archive_review)

## Domain Taxonomy Health

Status: `drift`
Config: `wiki/config/frontmatter-taxonomy.yaml`

| Severity | Count |
| --- | --- |
| error | 0 |
| warn | 6 |
| info | 0 |
| total | 6 |

### Taxonomy Drift Samples

- `scripts/check_wiki_frontmatter.py` `warn` `possible_unregistered_producer`: File contains frontmatter-looking text but is not registered in producer_paths.
- `scripts/wiki_medical_case.py` `warn` `possible_unregistered_producer`: File contains frontmatter-looking text but is not registered in producer_paths.
- `scripts/wiki_moc_projection.py` `warn` `possible_unregistered_producer`: File contains frontmatter-looking text but is not registered in producer_paths.
- `scripts/wiki_review_decisions.py` `warn` `possible_unregistered_producer`: File contains frontmatter-looking text but is not registered in producer_paths.
- `scripts/wiki_status_render.py` `warn` `possible_unregistered_producer`: File contains frontmatter-looking text but is not registered in producer_paths.
- `scripts/wiki_treatment.py` `warn` `possible_unregistered_producer`: File contains frontmatter-looking text but is not registered in producer_paths.

## Frontmatter Strict Gate

| Metric | Value |
| --- | --- |
| Enabled | True |
| Passed | False |
| Blocking entries | 0 |
| Score | 75 / 100 |

## Frontmatter Scorecard

| Dimension | Weight | Findings | Points Lost | Passed |
| --- | --- | --- | --- | --- |
| completeness | 40 | 0 | 0 | True |
| taxonomy_validity | 25 | 6 | 25 | False |
| identity_coverage | 20 | 0 | 0 | True |
| relation_shape | 15 | 0 | 0 | True |

## Graph Parse Health

Status: `pass`

| Metric | Value |
| --- | --- |
| Suspicious relation pages | 0 |

### Graph Parse Samples

- None

## Content Enrichment Health

Status: `pass`

| Metric | Value |
| --- | --- |
| Entries | 6 |
| Review needed | 0 |
| High confidence | 6 |
| Medium confidence | 0 |
| Low confidence | 0 |

### Content Enrichment Samples

- None

Content enrichment is preview only. Status does not write frontmatter.

## Content Adjudication Health

Status: `review_needed`
Eval passed: `True`

| Metric | Value |
| --- | --- |
| Candidates | 4 |
| Full details | 4 |
| Review focus | 1 |
| Taxonomy candidates | 0 |
| Drift traces | 1 |

### Content Adjudication Samples

- `wiki/adr/0001-seed-repo-boundaries.md` detail=`detail-0004` reasons=`adr_risk, openspec_required` route=`content-adjudication-review-package`

Content adjudication is review_package output only. Status does not write frontmatter or taxonomy.

## MOC Projection Health

Status: `drift`

| Metric | Value |
| --- | --- |
| Candidates | 7 |
| Create | 7 |
| Update | 0 |
| Noop | 0 |
| Orphan | 0 |

### MOC Projection Samples

- `wiki/moc/domain-wiki.md` `create` kind=`domain` key=`wiki` route=`obsidian-moc-projection`
- `wiki/moc/object-llm-wiki-core-product-contract.md` `create` kind=`object` key=`llm-wiki-core-product-contract` route=`obsidian-moc-projection`
- `wiki/moc/object-llm-wiki-readme-quality-gate.md` `create` kind=`object` key=`llm-wiki-readme-quality-gate` route=`obsidian-moc-projection`
- `wiki/moc/object-llm-wiki-self-evolution-medical-loop.md` `create` kind=`object` key=`llm-wiki-self-evolution-medical-loop` route=`obsidian-moc-projection`
- `wiki/moc/object-seed-repo-boundaries.md` `create` kind=`object` key=`seed-repo-boundaries` route=`obsidian-moc-projection`
- `wiki/moc/object-wiki-medical-case-file.md` `create` kind=`object` key=`wiki-medical-case-file` route=`obsidian-moc-projection`
- `wiki/moc/object-wiki-review-decision-record.md` `create` kind=`object` key=`wiki-review-decision-record` route=`obsidian-moc-projection`

MOC projection health is diagnostic only. Status does not write `wiki/moc` files.

## Pending Inbox Files

- None

## OpenSpec Changes

| Change | State | Tasks | Path |
| --- | --- | --- | --- |
| bootstrap-self-running-wiki-governance | complete | 7/7 | openspec/changes/bootstrap-self-running-wiki-governance/tasks.md |
| repair-wiki-runtime-governance-entry | active | 3/5 | openspec/changes/repair-wiki-runtime-governance-entry/tasks.md |

## Next Actions

- Review complete active-directory OpenSpec changes for archive readiness.
- Continue active OpenSpec changes before starting unrelated implementation.
