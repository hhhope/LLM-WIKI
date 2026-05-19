---
layer: ops
domain: wiki
ops_area: wiki-runtime
canonical_object: wiki-review-decision-record
artifact_type: review-decision-record
status: generated
---

# wiki-confirm Confirmation Record

## Source / 检查来源

- Generated at: 2026-05-19T08:14:29.364770+00:00
- Scan root: `/mnt/d/cloud/LLM-WIKI`
- Detail limit: complete
- Source record: none
- Source package: scripts/build_wiki_content_adjudication.py

## Decision Rules / 确诊标准
- safe_to_apply_frontmatter=true -> treatment_candidates.
- relation_weak_evidence, drift_risk, or adr_risk -> surgery_candidates.
- openspec_required or taxonomy_candidate -> openspec_required.
- agent_uncertain or needs_user_confirmation -> deferred_items.
- reject or rejected candidate details -> rejected_candidates.
- accept with no risk flags -> accepted_candidates.

## Summary
- accepted_candidates_count: 2
- deferred_items_count: 1
- openspec_required_count: 1
- rejected_candidates_count: 0
- source_detail_count: 3
- surgery_candidates_count: 1
- treatment_candidates_count: 2

## Confirmed Buckets / 确诊分流

## Accepted Candidates
- detail-0001 `wiki/ops/llm-wiki-core-product-contract.md`: existing or strongly evidenced candidate without unresolved review risks
- detail-0002 `wiki/ops/llm-wiki-self-evolution-medical-loop.md`: existing or strongly evidenced candidate without unresolved review risks

## Treatment Candidates
- detail-0001 `wiki/ops/llm-wiki-core-product-contract.md`: existing or strongly evidenced candidate without unresolved review risks
- detail-0002 `wiki/ops/llm-wiki-self-evolution-medical-loop.md`: existing or strongly evidenced candidate without unresolved review risks

## Surgery Candidates
- detail-0003 `wiki/adr/0001-seed-repo-boundaries.md`: risks=adr_risk, openspec_required; candidate has review risks: adr_risk, openspec_required

## OpenSpec Required
- detail-0003 `wiki/adr/0001-seed-repo-boundaries.md`: risks=adr_risk, openspec_required; candidate has review risks: adr_risk, openspec_required

## Deferred Items
- detail-0003 `wiki/adr/0001-seed-repo-boundaries.md`: risks=adr_risk, openspec_required; candidate has review risks: adr_risk, openspec_required

## Rejected Candidates
- None

## Abnormal Findings / 异常明细
- detail-0001 `wiki/ops/llm-wiki-core-product-contract.md` buckets=accepted_candidates, treatment_candidates; risks=none: existing or strongly evidenced candidate without unresolved review risks
- detail-0002 `wiki/ops/llm-wiki-self-evolution-medical-loop.md` buckets=accepted_candidates, treatment_candidates; risks=none: existing or strongly evidenced candidate without unresolved review risks
- detail-0003 `wiki/adr/0001-seed-repo-boundaries.md` buckets=deferred_items, surgery_candidates, openspec_required; risks=adr_risk, openspec_required: candidate has review risks: adr_risk, openspec_required

## Medical Advice / 处理建议
- Treatment candidates may enter `wiki-treatment` only after explicit approval.
- Surgery candidates route to `wiki-surgery` planning.
- OpenSpec-required items cannot be handled through treatment alone.
- Deferred items need human review before routing.

## Proof Boundary
- This is draft review routing only, not human approval.
- It does not write frontmatter, taxonomy, relations, MOC, or OpenSpec state.

## Next Actions
- Human review: confirm which candidates are accepted, deferred, rejected, treatment candidates, surgery candidates, or OpenSpec-required.
- Treatment: apply only later, after explicit approval for low-risk frontmatter updates.
- Surgery or OpenSpec: plan structural, taxonomy, relation, MOC, governance, or lifecycle changes separately.

## Machine Decision Data
<!-- wiki-review-decision-data:start -->
```json
{
  "accepted_candidates": [
    {
      "detail_ref": "detail-0001",
      "path": "wiki/ops/llm-wiki-core-product-contract.md",
      "reason": "existing or strongly evidenced candidate without unresolved review risks",
      "risk_flags": [],
      "suggested_frontmatter": {
        "artifact_type": "product-contract",
        "canonical_object": "llm-wiki-core-product-contract",
        "domain": "wiki",
        "layer": "ops",
        "ops_area": "wiki-runtime"
      }
    },
    {
      "detail_ref": "detail-0002",
      "path": "wiki/ops/llm-wiki-self-evolution-medical-loop.md",
      "reason": "existing or strongly evidenced candidate without unresolved review risks",
      "risk_flags": [],
      "suggested_frontmatter": {
        "artifact_type": "ops-model",
        "canonical_object": "llm-wiki-self-evolution-medical-loop",
        "domain": "wiki",
        "layer": "ops",
        "ops_area": "wiki-runtime"
      }
    }
  ],
  "deferred_items": [
    {
      "detail_ref": "detail-0003",
      "path": "wiki/adr/0001-seed-repo-boundaries.md",
      "reason": "candidate has review risks: adr_risk, openspec_required",
      "risk_flags": [
        "adr_risk",
        "openspec_required"
      ],
      "suggested_frontmatter": {
        "artifact_type": "adr",
        "canonical_object": "seed-repo-boundaries",
        "domain": "none",
        "layer": "adr"
      }
    }
  ],
  "generated_at": "2026-05-19T08:14:29.364770+00:00",
  "mode": "wiki_review_decision_package",
  "openspec_required": [
    {
      "detail_ref": "detail-0003",
      "path": "wiki/adr/0001-seed-repo-boundaries.md",
      "reason": "candidate has review risks: adr_risk, openspec_required",
      "risk_flags": [
        "adr_risk",
        "openspec_required"
      ],
      "suggested_frontmatter": {
        "artifact_type": "adr",
        "canonical_object": "seed-repo-boundaries",
        "domain": "none",
        "layer": "adr"
      }
    }
  ],
  "proof_boundary_notes": [
    "This is draft review routing only, not human approval.",
    "It does not write frontmatter, taxonomy, relations, MOC, or OpenSpec state."
  ],
  "rejected_candidates": [],
  "source_adjudication_summary": {
    "candidate_count": 3,
    "drift_trace_count": 1,
    "full_detail_count": 3,
    "review_focus_count": 1,
    "taxonomy_candidate_count": 0
  },
  "source_record": null,
  "summary": {
    "accepted_candidates_count": 2,
    "deferred_items_count": 1,
    "openspec_required_count": 1,
    "rejected_candidates_count": 0,
    "source_detail_count": 3,
    "surgery_candidates_count": 1,
    "treatment_candidates_count": 2
  },
  "surgery_candidates": [
    {
      "detail_ref": "detail-0003",
      "path": "wiki/adr/0001-seed-repo-boundaries.md",
      "reason": "candidate has review risks: adr_risk, openspec_required",
      "risk_flags": [
        "adr_risk",
        "openspec_required"
      ],
      "suggested_frontmatter": {
        "artifact_type": "adr",
        "canonical_object": "seed-repo-boundaries",
        "domain": "none",
        "layer": "adr"
      }
    }
  ],
  "treatment_candidates": [
    {
      "detail_ref": "detail-0001",
      "path": "wiki/ops/llm-wiki-core-product-contract.md",
      "reason": "existing or strongly evidenced candidate without unresolved review risks",
      "risk_flags": [],
      "suggested_frontmatter": {
        "artifact_type": "product-contract",
        "canonical_object": "llm-wiki-core-product-contract",
        "domain": "wiki",
        "layer": "ops",
        "ops_area": "wiki-runtime"
      }
    },
    {
      "detail_ref": "detail-0002",
      "path": "wiki/ops/llm-wiki-self-evolution-medical-loop.md",
      "reason": "existing or strongly evidenced candidate without unresolved review risks",
      "risk_flags": [],
      "suggested_frontmatter": {
        "artifact_type": "ops-model",
        "canonical_object": "llm-wiki-self-evolution-medical-loop",
        "domain": "wiki",
        "layer": "ops",
        "ops_area": "wiki-runtime"
      }
    }
  ]
}
```
<!-- wiki-review-decision-data:end -->
