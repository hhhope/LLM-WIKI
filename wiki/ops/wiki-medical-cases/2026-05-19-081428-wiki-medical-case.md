---
layer: ops
domain: wiki
ops_area: wiki-runtime
canonical_object: wiki-medical-case-file
artifact_type: medical-case
status: awaiting_confirmation
case_slug: wiki-medical-case
created_at: 2026-05-19
---

# wiki-medical-case

## Case Source
- Generated at: 2026-05-19T08:14:28.707024+00:00
- Scan root: `/mnt/d/cloud/LLM-WIKI`
- Source record: ``
- Confirm record: ``

## Diagnosis
- candidate_count: 3
- drift_trace_count: 1
- full_detail_count: 3
- review_focus_count: 1
- taxonomy_candidate_count: 0

## Proposed Decisions
### Treatment Candidates
- None
### Surgery Candidates
- None
### Openspec Required
- None
### Blockers
- None

## Confirmed Decisions
### Accepted Candidates
- detail-0001 `wiki/ops/llm-wiki-core-product-contract.md`: existing or strongly evidenced candidate without unresolved review risks
- detail-0002 `wiki/ops/llm-wiki-self-evolution-medical-loop.md`: existing or strongly evidenced candidate without unresolved review risks
### Rejected Candidates
- None
### Deferred Items
- detail-0003 `wiki/adr/0001-seed-repo-boundaries.md`: risks=adr_risk, openspec_required; candidate has review risks: adr_risk, openspec_required
### Treatment Candidates
- detail-0001 `wiki/ops/llm-wiki-core-product-contract.md`: existing or strongly evidenced candidate without unresolved review risks
- detail-0002 `wiki/ops/llm-wiki-self-evolution-medical-loop.md`: existing or strongly evidenced candidate without unresolved review risks
### Surgery Candidates
- detail-0003 `wiki/adr/0001-seed-repo-boundaries.md`: risks=adr_risk, openspec_required; candidate has review risks: adr_risk, openspec_required
### Openspec Required
- detail-0003 `wiki/adr/0001-seed-repo-boundaries.md`: risks=adr_risk, openspec_required; candidate has review risks: adr_risk, openspec_required

## Treatment
- Status: pending
- Candidate count: 2

## Surgery Plan
- Status: pending
- Candidate count: 2

## Recovery
- Status: pending

## Archive / Next Action
- Status: awaiting_confirmation
- Next action: awaiting_confirmation

## Evidence Attachments
### Doctor
- None
### Confirm
- None
### Treatment
- None
### Surgery
- None
### Recovery
- None

## Proof Boundary
- This is the canonical case file for review routing.
- Confirmed Decisions are the authority for surgery planning.
- Stage records are evidence attachments, not competing sources of truth.

## Machine Case Data
<!-- wiki-medical-case-data:start -->
```json
{
  "active": true,
  "archive_next_action": {
    "next_action": "awaiting_confirmation",
    "reason": "Confirmed Decisions require human review before treatment or surgery.",
    "status": "awaiting_confirmation"
  },
  "case_slug": "wiki-medical-case",
  "case_source": {
    "confirm_record": "",
    "source_decision_summary": {
      "accepted_candidates_count": 2,
      "deferred_items_count": 1,
      "openspec_required_count": 1,
      "rejected_candidates_count": 0,
      "source_detail_count": 3,
      "surgery_candidates_count": 1,
      "treatment_candidates_count": 2
    },
    "source_record": ""
  },
  "confirmed_decisions": {
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
    "rejected_candidates": [],
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
  },
  "current_intent": {},
  "diagnosis": {
    "source_adjudication_summary": {
      "candidate_count": 3,
      "drift_trace_count": 1,
      "full_detail_count": 3,
      "review_focus_count": 1,
      "taxonomy_candidate_count": 0
    }
  },
  "evidence_attachments": {
    "confirm": [],
    "doctor": [],
    "recovery": [],
    "surgery": [],
    "treatment": []
  },
  "generated_at": "2026-05-19T08:14:28.707024+00:00",
  "mode": "wiki_medical_case",
  "proof_boundary_notes": [
    "This is the canonical case file for review routing.",
    "Confirmed Decisions are the authority for surgery planning.",
    "Stage records are evidence attachments, not competing sources of truth."
  ],
  "proposed_decisions": {
    "blockers": [],
    "openspec_required": [],
    "surgery_candidates": [],
    "treatment_candidates": []
  },
  "recovery": {
    "records": [],
    "status": "pending"
  },
  "status": "awaiting_confirmation",
  "surgery_plan": {
    "candidate_count": 2,
    "records": [],
    "status": "pending"
  },
  "treatment": {
    "candidate_count": 2,
    "records": [],
    "status": "pending"
  }
}
```
<!-- wiki-medical-case-data:end -->
