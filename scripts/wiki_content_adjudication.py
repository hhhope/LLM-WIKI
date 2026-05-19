from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from scripts.check_wiki_frontmatter import CONFIG_PATH, load_taxonomy
from scripts.wiki_content_enrichment import build_enrichment_preview


REVIEW_RISKS = {
    "taxonomy_candidate",
    "domain_conflict",
    "relation_weak_evidence",
    "adr_risk",
    "drift_risk",
    "openspec_required",
    "agent_uncertain",
}

GENERATED_REVIEW_ARTIFACT_PREFIXES = (
    "wiki/ops/wiki-doctor-runs/",
    "wiki/ops/wiki-review-decisions/",
    "wiki/ops/wiki-medical-cases/",
    "wiki/ops/wiki-treatment-runs/",
    "wiki/ops/wiki-surgery-runs/",
    "wiki/ops/wiki-recovery-runs/",
)


def _is_generated_review_artifact(entry: dict[str, Any]) -> bool:
    path = str(entry.get("path", "")).replace("\\", "/")
    return any(path.startswith(prefix) for prefix in GENERATED_REVIEW_ARTIFACT_PREFIXES)


def _known_taxonomy(root: Path) -> tuple[set[str], set[str]]:
    taxonomy = load_taxonomy(root)
    fields = taxonomy.get("fields", {}) if isinstance(taxonomy, dict) else {}
    domains = {
        str(value)
        for value in fields.get("domain", {}).get("known", [])
        if str(value).strip()
    }
    ops_areas = {
        str(value)
        for value in fields.get("ops_area", {}).get("allowed", [])
        if str(value).strip()
    }
    return domains, ops_areas


def _risk_flags(entry: dict[str, Any], known_domains: set[str], known_ops_areas: set[str]) -> list[str]:
    suggested = entry.get("suggested_frontmatter", {})
    path = str(entry.get("path", ""))
    text = " ".join(
        [
            path,
            str(suggested.get("canonical_object", "")),
            str(suggested.get("artifact_type", "")),
            " ".join(str(item) for item in entry.get("evidence", [])),
        ]
    ).lower()

    risks: set[str] = set()
    domain = str(suggested.get("domain", "")).strip()
    if domain and domain not in known_domains:
        risks.add("taxonomy_candidate")
    if suggested.get("ops_area") and str(suggested["ops_area"]).strip() not in known_ops_areas:
        risks.add("taxonomy_candidate")
    if domain == "unclassified":
        risks.add("agent_uncertain")
    if path.startswith("wiki/adr/") or suggested.get("artifact_type") == "adr":
        risks.add("adr_risk")
    if any(token in text for token in ["drift", "retro", "reanchor"]):
        risks.add("drift_risk")
    if any(token in text for token in ["openspec", "adr", "governance", "runtime behavior"]):
        risks.add("openspec_required")
    relations = entry.get("suggested_relations", {})
    if relations.get("related_objects") and entry.get("confidence") != "high":
        risks.add("relation_weak_evidence")
    if entry.get("needs_review"):
        risks.add("agent_uncertain")
    return sorted(risks)


def _judgment(entry: dict[str, Any], risks: list[str]) -> dict[str, Any]:
    evidence = [str(item) for item in entry.get("evidence", []) if str(item).strip()]
    blocking = set(risks) & {
        "taxonomy_candidate",
        "domain_conflict",
        "adr_risk",
        "drift_risk",
        "openspec_required",
        "agent_uncertain",
    }
    if blocking:
        state = "needs_user_confirmation"
    elif entry.get("confidence") == "high":
        state = "accept"
    elif evidence:
        state = "likely"
    else:
        state = "reject"
    return {
        "state": state,
        "reason": _judgment_reason(state, risks),
        "evidence": evidence,
    }


def _judgment_reason(state: str, risks: list[str]) -> str:
    if state == "accept":
        return "existing or strongly evidenced candidate without unresolved review risks"
    if state == "likely":
        return "candidate has bounded evidence but remains advisory"
    if state == "reject":
        return "candidate lacks enough evidence for adjudication"
    return "candidate has review risks: " + ", ".join(risks)


def _rejected_candidates(entry: dict[str, Any], risks: list[str]) -> list[dict[str, str]]:
    rejected: list[dict[str, str]] = []
    suggested = entry.get("suggested_frontmatter", {})
    if suggested.get("domain") == "unclassified":
        rejected.append(
            {
                "field": "domain",
                "value": "auto_accept_unclassified",
                "reason": "unclassified domain requires review before structural write",
            }
        )
    if "relation_weak_evidence" in risks:
        rejected.append(
            {
                "field": "related_objects",
                "value": "auto_accept_all_relations",
                "reason": "relation candidates need reviewed evidence",
            }
        )
    return rejected


def _taxonomy_candidates(details: list[dict[str, Any]], known_domains: set[str], known_ops_areas: set[str]) -> list[dict[str, Any]]:
    refs: dict[tuple[str, str], list[str]] = defaultdict(list)
    for detail in details:
        suggested = detail["candidate"].get("suggested_frontmatter", {})
        domain = str(suggested.get("domain", "")).strip()
        if domain and domain not in known_domains:
            refs[("domain", domain)].append(detail["detail_id"])
        ops_area = str(suggested.get("ops_area", "")).strip()
        if ops_area and ops_area not in known_ops_areas:
            refs[("ops_area", ops_area)].append(detail["detail_id"])
    return [
        {
            "field": field,
            "value": value,
            "detail_refs": detail_refs,
            "reason": "value absent from wiki/config/frontmatter-taxonomy.yaml",
        }
        for (field, value), detail_refs in sorted(refs.items())
    ]


def _review_focus(details: list[dict[str, Any]]) -> list[dict[str, Any]]:
    focus = []
    for detail in details:
        if detail["risk_flags"] or detail["judgment"]["state"] in {"reject", "needs_user_confirmation"}:
            focus.append(
                {
                    "detail_ref": detail["detail_id"],
                    "path": detail["path"],
                    "review_reasons": detail["risk_flags"] or [detail["judgment"]["state"]],
                    "recommended_action": "review_candidate_before_structure_write",
                }
            )
    return focus


def _drift_trace(details: list[dict[str, Any]]) -> list[dict[str, Any]]:
    traces = []
    for detail in details:
        risks = set(detail["risk_flags"])
        if risks & {"drift_risk", "adr_risk", "openspec_required"}:
            traces.append(
                {
                    "detail_ref": detail["detail_id"],
                    "path": detail["path"],
                    "risk_flags": sorted(risks & {"drift_risk", "adr_risk", "openspec_required"}),
                    "trigger_evidence": detail["judgment"]["evidence"][:3],
                    "reason": "governance or drift signal requires explicit review",
                }
            )
    return traces


def evaluate_adjudication_package(package: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    taxonomy_refs = {
        ref
        for item in package.get("taxonomy_candidate_set", [])
        for ref in item.get("detail_refs", [])
    }
    focus_refs = {item.get("detail_ref") for item in package.get("review_focus_set", [])}

    for detail in package.get("full_detail_set", []):
        detail_id = str(detail.get("detail_id", ""))
        risks = set(detail.get("risk_flags", []))
        judgment = detail.get("judgment", {})
        evidence = judgment.get("evidence", [])
        if not evidence:
            errors.append(f"{detail_id}: judgment missing evidence")
        if "taxonomy_candidate" in risks and detail_id not in taxonomy_refs:
            errors.append(f"{detail_id}: taxonomy_candidate risk missing taxonomy candidate entry")
        if risks and detail_id not in focus_refs:
            errors.append(f"{detail_id}: risk detail missing review focus entry")
        suggested = detail.get("candidate", {}).get("suggested_frontmatter", {})
        path = str(detail.get("path", ""))
        if suggested.get("domain") == "unclassified" and "agent_uncertain" not in risks:
            errors.append(f"{detail_id}: unclassified domain missing agent_uncertain risk")
        if path.startswith("wiki/adr/") and "adr_risk" not in risks:
            errors.append(f"{detail_id}: ADR page missing adr_risk")
        risk_text = " ".join([path, str(suggested.get("artifact_type", ""))]).lower()
        if any(token in risk_text for token in ["drift", "retro", "reanchor"]) and "drift_risk" not in risks:
            errors.append(f"{detail_id}: drift page missing drift_risk")
        if detail.get("safe_to_apply_frontmatter") and risks:
            errors.append(f"{detail_id}: safe_to_apply_frontmatter true with unresolved risks")
        if "relation_weak_evidence" in risks:
            warnings.append(f"{detail_id}: relation candidate needs reviewed evidence")

    return {
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
    }


def build_adjudication_package(root: Path | str) -> dict[str, Any]:
    root_path = Path(root)
    if not (root_path / CONFIG_PATH).exists():
        package = {
            "summary": {
                "candidate_count": 0,
                "full_detail_count": 0,
                "review_focus_count": 0,
                "taxonomy_candidate_count": 0,
                "drift_trace_count": 0,
            },
            "candidate_set": [],
            "full_detail_set": [],
            "agent_judgment_set": [],
            "taxonomy_candidate_set": [],
            "review_focus_set": [],
            "drift_trace_set": [],
            "proof_boundary_notes": [
                "Content adjudication is unavailable because taxonomy config is missing.",
                "It does not write frontmatter.",
            ],
        }
        package["eval_result"] = evaluate_adjudication_package(package)
        return package

    preview = build_enrichment_preview(root_path)
    candidates = [
        entry
        for entry in preview.get("entries", [])
        if not _is_generated_review_artifact(entry)
    ]
    known_domains, known_ops_areas = _known_taxonomy(root_path)
    details = []
    for index, entry in enumerate(candidates, start=1):
        detail_id = f"detail-{index:04d}"
        risks = _risk_flags(entry, known_domains, known_ops_areas)
        judgment = _judgment(entry, risks)
        details.append(
            {
                "detail_id": detail_id,
                "path": entry["path"],
                "candidate": entry,
                "judgment": judgment,
                "risk_flags": risks,
                "rejected_candidates": _rejected_candidates(entry, risks),
                "safe_to_apply_frontmatter": judgment["state"] in {"accept", "likely"} and not risks,
            }
        )

    taxonomy_candidates = _taxonomy_candidates(details, known_domains, known_ops_areas)
    focus = _review_focus(details)
    drift_trace = _drift_trace(details)
    package = {
        "summary": {
            "candidate_count": len(candidates),
            "full_detail_count": len(details),
            "review_focus_count": len(focus),
            "taxonomy_candidate_count": len(taxonomy_candidates),
            "drift_trace_count": len(drift_trace),
        },
        "candidate_set": candidates,
        "full_detail_set": details,
        "agent_judgment_set": [
            {
                "detail_ref": detail["detail_id"],
                "path": detail["path"],
                "judgment": detail["judgment"],
                "risk_flags": detail["risk_flags"],
                "safe_to_apply_frontmatter": detail["safe_to_apply_frontmatter"],
            }
            for detail in details
        ],
        "taxonomy_candidate_set": taxonomy_candidates,
        "review_focus_set": focus,
        "drift_trace_set": drift_trace,
        "proof_boundary_notes": [
            "Content adjudication is deterministic review output only.",
            "It does not write frontmatter.",
            "It does not mutate taxonomy config.",
            "It does not prove hidden semantic truth.",
        ],
    }
    package["eval_result"] = evaluate_adjudication_package(package)
    return package


def build_adjudication_health(root: Path | str) -> dict[str, Any]:
    package = build_adjudication_package(root)
    eval_result = package.get("eval_result", {})
    focus_entries = [
        {
            "type": "content_adjudication",
            "path": item.get("path", "unknown"),
            "detail_ref": item.get("detail_ref", "unknown"),
            "problem": "review_needed",
            "review_reasons": item.get("review_reasons", []),
            "repair_route": "content-adjudication-review-package",
        }
        for item in package.get("review_focus_set", [])
    ]
    status = "pass"
    if not eval_result.get("passed", True):
        status = "eval_failed"
    elif focus_entries:
        status = "review_needed"
    return {
        "status": status,
        "summary": package["summary"],
        "eval_result": eval_result,
        "entries": focus_entries[:20],
        "proof_boundary_notes": package.get("proof_boundary_notes", []),
    }
