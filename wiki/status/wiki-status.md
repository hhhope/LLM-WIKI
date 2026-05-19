---
layer: status
domain: none
canonical_object: wiki-status
artifact_type: generated-status
status: generated
---

# Wiki Status

Generated at: `2026-05-19T11:11:15.153989+00:00`

## Summary

| Metric | Value |
| --- | --- |
| Wiki pages | 22 |
| Source records | 3 |
| Inbox files | 0 |
| Pending inbox files | 0 |
| Active OpenSpec changes | 0 |
| Complete active-dir changes | 3 |

## Wiki Sections

| Section | Pages |
| --- | --- |
| wiki/adr | 2 |
| wiki/domains | 1 |
| wiki/examples | 5 |
| wiki/ops | 7 |
| wiki/reports | 1 |
| wiki/root | 1 |
| wiki/sources | 4 |
| wiki/timeline | 1 |

## Product Status

Contract version: `1`

### Object Types

| Object Type | Count |
| --- | --- |
| governance | 5 |
| output | 1 |
| source | 4 |
| unknown | 15 |

### Readiness

| Readiness | Count |
| --- | --- |
| accepted | 1 |
| draft-only | 21 |

### Source Layers

| Source Layer | Count |
| --- | --- |
| ops | 7 |
| report | 1 |
| source | 4 |
| spec | 5 |
| unknown | 8 |

### Identity Coverage

| Metric | Value |
| --- | --- |
| With identity | 12 |
| Missing identity | 10 |

### Relation Coverage

| Metric | Value |
| --- | --- |
| With relations | 1 |
| Missing relations | 21 |

### Unresolved Product Status Items

- `bootstrap-self-running-wiki-governance`: complete_openspec_change (unresolved -> archive_review)
- `consolidate-learning-explore-gates`: complete_openspec_change (unresolved -> archive_review)
- `repair-wiki-runtime-governance-entry`: complete_openspec_change (unresolved -> archive_review)

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
| Entries | 7 |
| Review needed | 0 |
| High confidence | 7 |
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
| Candidates | 5 |
| Full details | 5 |
| Review focus | 1 |
| Taxonomy candidates | 0 |
| Drift traces | 1 |

### Content Adjudication Samples

- `wiki/adr/0001-seed-repo-boundaries.md` detail=`detail-0005` reasons=`adr_risk, openspec_required` route=`content-adjudication-review-package`

Content adjudication is review_package output only. Status does not write frontmatter or taxonomy.

## MOC Projection Health

Status: `drift`

| Metric | Value |
| --- | --- |
| Candidates | 13 |
| Create | 13 |
| Update | 0 |
| Noop | 0 |
| Orphan | 0 |

### MOC Projection Samples

- `wiki/moc/domain-public-report-output.md` `create` kind=`domain` key=`public-report-output` route=`obsidian-moc-projection`
- `wiki/moc/domain-wiki.md` `create` kind=`domain` key=`wiki` route=`obsidian-moc-projection`
- `wiki/moc/object-agentic-product-engineering-collaboration-our-operating-system.md` `create` kind=`object` key=`agentic-product-engineering-collaboration-our-operating-system` route=`obsidian-moc-projection`
- `wiki/moc/object-agentic-product-engineering-collaboration-workway-brainstorming-drift.md` `create` kind=`object` key=`agentic-product-engineering-collaboration-workway-brainstorming-drift` route=`obsidian-moc-projection`
- `wiki/moc/object-lixiang-luoyonghao-reading-board-example.md` `create` kind=`object` key=`lixiang-luoyonghao-reading-board-example` route=`obsidian-moc-projection`
- `wiki/moc/object-llm-wiki-core-product-contract.md` `create` kind=`object` key=`llm-wiki-core-product-contract` route=`obsidian-moc-projection`
- `wiki/moc/object-llm-wiki-readme-quality-gate.md` `create` kind=`object` key=`llm-wiki-readme-quality-gate` route=`obsidian-moc-projection`
- `wiki/moc/object-llm-wiki-self-evolution-medical-loop.md` `create` kind=`object` key=`llm-wiki-self-evolution-medical-loop` route=`obsidian-moc-projection`
- `wiki/moc/object-seed-repo-boundaries.md` `create` kind=`object` key=`seed-repo-boundaries` route=`obsidian-moc-projection`
- `wiki/moc/object-wiki-medical-case-file.md` `create` kind=`object` key=`wiki-medical-case-file` route=`obsidian-moc-projection`
- `wiki/moc/object-wiki-review-decision-record.md` `create` kind=`object` key=`wiki-review-decision-record` route=`obsidian-moc-projection`
- `wiki/moc/relation-derived_from.md` `create` kind=`relation` key=`derived_from` route=`obsidian-moc-projection`
- `wiki/moc/relation-related_objects.md` `create` kind=`relation` key=`related_objects` route=`obsidian-moc-projection`

MOC projection health is diagnostic only. Status does not write `wiki/moc` files.

## Pending Inbox Files

- None

## OpenSpec Changes

| Change | State | Tasks | Path |
| --- | --- | --- | --- |
| bootstrap-self-running-wiki-governance | complete | 7/7 | openspec/changes/bootstrap-self-running-wiki-governance/tasks.md |
| consolidate-learning-explore-gates | complete | 7/7 | openspec/changes/consolidate-learning-explore-gates/tasks.md |
| repair-wiki-runtime-governance-entry | complete | 5/5 | openspec/changes/repair-wiki-runtime-governance-entry/tasks.md |

## Next Actions

- Review complete active-directory OpenSpec changes for archive readiness.
