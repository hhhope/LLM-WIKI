from __future__ import annotations

import copy
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_MEDICAL_CASE_DIR = Path("wiki/ops/wiki-medical-cases")
CASE_DATA_START = "<!-- wiki-medical-case-data:start -->"
CASE_DATA_END = "<!-- wiki-medical-case-data:end -->"

DECISION_BUCKETS = (
    "accepted_candidates",
    "rejected_candidates",
    "deferred_items",
    "treatment_candidates",
    "surgery_candidates",
    "openspec_required",
)

CASE_STATUSES = {
    "diagnosis_ready",
    "awaiting_confirmation",
    "ready_for_treatment",
    "treatment_previewed",
    "treatment_applied",
    "recovery_required",
    "surgery_required",
    "surgery_planned",
    "blocked",
    "archive_ready",
    "followup_required",
}


def _iso_timestamp(timestamp: datetime | str | None = None) -> str:
    if timestamp is None:
        return datetime.now(timezone.utc).isoformat()
    if isinstance(timestamp, datetime):
        return timestamp.astimezone(timezone.utc).isoformat()
    return timestamp


def _timestamp_slug(timestamp: datetime | str | None) -> str:
    if timestamp is None:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
    if isinstance(timestamp, datetime):
        return timestamp.astimezone(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return timestamp
    return parsed.astimezone(timezone.utc).strftime("%Y-%m-%d-%H%M%S")


def _slugify(value: str | None) -> str:
    text = str(value or "wiki-medical-case").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "wiki-medical-case"


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _copy_bucket(source: dict[str, Any], key: str) -> list[dict[str, Any]]:
    return [copy.deepcopy(item) for item in _as_list(source.get(key)) if isinstance(item, dict)]


def _item_dedupe_key(item: dict[str, Any]) -> str:
    ref = item.get("detail_ref") or item.get("detail_id")
    if ref:
        return f"ref:{ref}"
    return "json:" + json.dumps(item, ensure_ascii=False, sort_keys=True)


def _attachment_list(*values: str | Path | None) -> list[str]:
    attachments: list[str] = []
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if text:
            attachments.append(text)
    return attachments


def build_medical_case_package(
    decision_package: dict[str, Any],
    case_slug: str | None = None,
    confirm_record: str | Path | None = None,
    treatment_records: list[str | Path] | None = None,
    surgery_records: list[str | Path] | None = None,
    recovery_records: list[str | Path] | None = None,
    timestamp: datetime | str | None = None,
) -> dict[str, Any]:
    generated_at = _iso_timestamp(timestamp or decision_package.get("generated_at"))
    normalized_slug = _slugify(case_slug or "wiki-medical-case")
    source_record = decision_package.get("source_record")
    confirmed_decisions = {
        bucket: _copy_bucket(decision_package, bucket) for bucket in DECISION_BUCKETS
    }

    return {
        "generated_at": generated_at,
        "mode": "wiki_medical_case",
        "case_slug": normalized_slug,
        "status": "awaiting_confirmation",
        "active": True,
        "current_intent": {},
        "case_source": {
            "source_record": str(source_record) if source_record else "",
            "confirm_record": str(confirm_record) if confirm_record else "",
            "source_decision_summary": copy.deepcopy(decision_package.get("summary", {})),
        },
        "diagnosis": {
            "source_adjudication_summary": copy.deepcopy(
                decision_package.get("source_adjudication_summary", {})
            ),
        },
        "proposed_decisions": {
            "treatment_candidates": [],
            "surgery_candidates": [],
            "openspec_required": [],
            "blockers": [],
        },
        "confirmed_decisions": confirmed_decisions,
        "treatment": {
            "status": "pending",
            "candidate_count": len(confirmed_decisions["treatment_candidates"]),
            "records": [str(path) for path in (treatment_records or [])],
        },
        "surgery_plan": {
            "status": "pending",
            "candidate_count": len(confirmed_decisions["surgery_candidates"])
            + len(confirmed_decisions["openspec_required"]),
            "records": [str(path) for path in (surgery_records or [])],
        },
        "recovery": {
            "status": "pending",
            "records": [str(path) for path in (recovery_records or [])],
        },
        "archive_next_action": {
            "status": "awaiting_confirmation",
            "next_action": "awaiting_confirmation",
            "reason": "Confirmed Decisions require human review before treatment or surgery.",
        },
        "evidence_attachments": {
            "doctor": _attachment_list(source_record),
            "confirm": _attachment_list(confirm_record),
            "treatment": [str(path) for path in (treatment_records or [])],
            "surgery": [str(path) for path in (surgery_records or [])],
            "recovery": [str(path) for path in (recovery_records or [])],
        },
        "proof_boundary_notes": [
            "This is the canonical case file for review routing.",
            "Confirmed Decisions are the authority for surgery planning.",
            "Stage records are evidence attachments, not competing sources of truth.",
        ],
    }


def _normalize_next_action(next_route: str | None, passed: bool | None = None) -> str:
    route = str(next_route or "").strip().replace("-", "_")
    if route == "archive_ready" and passed is True:
        return "archive_ready"
    if route == "blocked_by_recovery_findings":
        return "blocked"
    if route in {"awaiting_confirmation", "surgery_required", "blocked", "followup_required"}:
        return route
    return "blocked"


def _recovery_proposed_decisions(recovery_package: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    proposed: dict[str, list[dict[str, Any]]] = {
        "treatment_candidates": [],
        "surgery_candidates": [],
        "openspec_required": [],
        "blockers": [],
    }
    nested = recovery_package.get("proposed_decisions", {})
    sources = [nested] if isinstance(nested, dict) else []
    sources.append(recovery_package)
    for source in sources:
        if not isinstance(source, dict):
            continue
        for key in proposed:
            proposed[key].extend(_copy_bucket(source, key))
    return proposed


def _merge_proposed_decisions(
    target: dict[str, Any],
    additions: dict[str, list[dict[str, Any]]],
) -> bool:
    changed = False
    for key, items in additions.items():
        bucket = target.setdefault(key, [])
        if not isinstance(bucket, list):
            bucket = []
            target[key] = bucket
        seen = {
            _item_dedupe_key(item)
            for item in bucket
            if isinstance(item, dict)
        }
        for item in items:
            dedupe_key = _item_dedupe_key(item)
            if dedupe_key in seen:
                continue
            bucket.append(copy.deepcopy(item))
            seen.add(dedupe_key)
            changed = True
    return changed


def attach_recovery_result_to_case(
    case_package: dict[str, Any],
    recovery_package: dict[str, Any],
    recovery_record: str | Path | None = None,
) -> dict[str, Any]:
    updated = copy.deepcopy(case_package)
    record_text = str(recovery_record) if recovery_record else ""
    records = list(_as_list(updated.get("recovery", {}).get("records")))
    attachments = updated.setdefault("evidence_attachments", {}).setdefault("recovery", [])
    if record_text and record_text not in records:
        records.append(record_text)
    if record_text and record_text not in attachments:
        attachments.append(record_text)
    next_action = _normalize_next_action(
        str(recovery_package.get("next_route", "")),
        recovery_package.get("passed") is True,
    )
    proposed = updated.setdefault("proposed_decisions", {})
    if not isinstance(proposed, dict):
        proposed = {}
        updated["proposed_decisions"] = proposed
    has_new_proposals = _merge_proposed_decisions(
        proposed,
        _recovery_proposed_decisions(recovery_package),
    )
    if has_new_proposals:
        next_action = "awaiting_confirmation"
    updated["recovery"] = {
        "status": "completed",
        "records": records,
        "summary": copy.deepcopy(recovery_package.get("summary", {})),
        "result": copy.deepcopy(recovery_package),
    }
    updated["status"] = next_action
    updated["archive_next_action"] = {
        "status": next_action,
        "next_action": next_action,
        "reason": "Recovery result set the next medical-loop action.",
    }
    return updated


def attach_surgery_plan_to_case(
    case_package: dict[str, Any],
    surgery_plan: dict[str, Any],
    surgery_record: str | Path | None = None,
) -> dict[str, Any]:
    updated = copy.deepcopy(case_package)
    records = list(_as_list(updated.get("surgery_plan", {}).get("records")))
    attachments = updated.setdefault("evidence_attachments", {}).setdefault("surgery", [])
    record_text = str(surgery_record) if surgery_record else ""
    if record_text and record_text not in records:
        records.append(record_text)
    if record_text and record_text not in attachments:
        attachments.append(record_text)
    updated["surgery_plan"] = {
        "status": surgery_plan.get("status", "planned"),
        "source": "confirmed_decisions",
        "summary": copy.deepcopy(surgery_plan.get("summary", {})),
        "records": records,
        "plan": copy.deepcopy(surgery_plan),
    }
    return updated


def _frontmatter_lines(package: dict[str, Any]) -> list[str]:
    created_at = str(package.get("generated_at", "")).split("T", 1)[0] or datetime.now(timezone.utc).date().isoformat()
    return [
        "---",
        "layer: ops",
        "domain: wiki",
        "ops_area: wiki-runtime",
        "canonical_object: wiki-medical-case-file",
        "artifact_type: medical-case",
        f"status: {package.get('status', 'active')}",
        f"case_slug: {package.get('case_slug', 'wiki-medical-case')}",
        f"created_at: {created_at}",
        "---",
        "",
    ]


def _item_line(item: dict[str, Any]) -> str:
    ref = str(item.get("detail_ref") or item.get("detail_id") or "unknown")
    path = str(item.get("path", ""))
    prefix = f"{ref} `{path}`" if path else ref
    parts = []
    risks = item.get("risk_flags", [])
    if isinstance(risks, list) and risks:
        parts.append("risks=" + ", ".join(str(risk) for risk in risks))
    if item.get("reason"):
        parts.append(str(item["reason"]))
    return f"- {prefix}: {'; '.join(parts)}" if parts else f"- {prefix}"


def _bucket_lines(title: str, items: list[dict[str, Any]]) -> list[str]:
    lines = [f"### {title}"]
    lines.extend([_item_line(item) for item in items] or ["- None"])
    return lines


def render_medical_case_markdown(package: dict[str, Any], scan_root: Path | str) -> str:
    source = package.get("case_source", {})
    diagnosis = package.get("diagnosis", {})
    confirmed = package.get("confirmed_decisions", {})
    evidence = package.get("evidence_attachments", {})

    lines = _frontmatter_lines(package)
    lines.extend(
        [
            "# wiki-medical-case",
            "",
            "## Case Source",
            f"- Generated at: {package.get('generated_at', 'unknown')}",
            f"- Scan root: `{Path(scan_root)}`",
            f"- Source record: `{source.get('source_record', '')}`",
            f"- Confirm record: `{source.get('confirm_record', '')}`",
            "",
            "## Diagnosis",
        ]
    )
    summary = diagnosis.get("source_adjudication_summary", {})
    if isinstance(summary, dict) and summary:
        for key, value in sorted(summary.items()):
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- None")

    proposed = package.get("proposed_decisions", {})
    lines.extend(["", "## Proposed Decisions"])
    if isinstance(proposed, dict):
        for key in ("treatment_candidates", "surgery_candidates", "openspec_required", "blockers"):
            lines.extend(_bucket_lines(key.replace("_", " ").title(), _copy_bucket(proposed, key)))
    else:
        lines.append("- None")

    lines.extend(["", "## Confirmed Decisions"])
    for bucket in DECISION_BUCKETS:
        lines.extend(_bucket_lines(bucket.replace("_", " ").title(), _copy_bucket(confirmed, bucket)))

    lines.extend(["", "## Treatment"])
    treatment = package.get("treatment", {})
    lines.append(f"- Status: {treatment.get('status', 'pending')}")
    lines.append(f"- Candidate count: {treatment.get('candidate_count', 0)}")

    lines.extend(["", "## Surgery Plan"])
    surgery = package.get("surgery_plan", {})
    lines.append(f"- Status: {surgery.get('status', 'pending')}")
    lines.append(f"- Candidate count: {surgery.get('candidate_count', 0)}")
    if isinstance(surgery.get("summary"), dict):
        for key, value in sorted(surgery["summary"].items()):
            lines.append(f"- {key}: {value}")

    lines.extend(["", "## Recovery"])
    recovery = package.get("recovery", {})
    lines.append(f"- Status: {recovery.get('status', 'pending')}")

    lines.extend(["", "## Archive / Next Action"])
    archive = package.get("archive_next_action", {})
    lines.append(f"- Status: {archive.get('status', 'pending')}")
    lines.append(f"- Next action: {archive.get('next_action', '')}")

    lines.extend(["", "## Evidence Attachments"])
    if isinstance(evidence, dict):
        for key in ("doctor", "confirm", "treatment", "surgery", "recovery"):
            values = _as_list(evidence.get(key))
            lines.append(f"### {key.title()}")
            lines.extend([f"- `{value}`" for value in values] or ["- None"])

    lines.extend(["", "## Proof Boundary"])
    for note in _as_list(package.get("proof_boundary_notes")):
        lines.append(f"- {note}")

    machine_json = json.dumps(package, ensure_ascii=False, indent=2, sort_keys=True)
    lines.extend(
        [
            "",
            "## Machine Case Data",
            CASE_DATA_START,
            "```json",
            machine_json,
            "```",
            CASE_DATA_END,
        ]
    )
    return "\n".join(lines) + "\n"


def next_medical_case_path(
    output_dir: Path,
    case_slug: str | None = None,
    timestamp: datetime | str | None = None,
) -> Path:
    slug = _timestamp_slug(timestamp)
    case_part = _slugify(case_slug)
    base = output_dir / f"{slug}-{case_part}.md"
    if not base.exists():
        return base
    counter = 2
    while True:
        candidate = output_dir / f"{slug}-{case_part}-{counter}.md"
        if not candidate.exists():
            return candidate
        counter += 1


def write_medical_case_file(
    package: dict[str, Any],
    root: Path | str,
    output_dir: Path | str | None = None,
    timestamp: datetime | str | None = None,
) -> Path:
    root_path = Path(root)
    target_dir = Path(output_dir) if output_dir is not None else root_path / DEFAULT_MEDICAL_CASE_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    markdown = render_medical_case_markdown(package, scan_root=root_path)
    while True:
        target = next_medical_case_path(target_dir, case_slug=str(package.get("case_slug", "")), timestamp=timestamp)
        try:
            with target.open("x", encoding="utf-8") as handle:
                handle.write(markdown)
            return target.resolve()
        except FileExistsError:
            continue


def overwrite_medical_case_file(path: Path | str, package: dict[str, Any], scan_root: Path | str) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".tmp")
    tmp.write_text(render_medical_case_markdown(package, scan_root=scan_root), encoding="utf-8")
    tmp.replace(target)
    return target.resolve()


def load_medical_case_file(path: Path | str) -> dict[str, Any]:
    text = Path(path).read_text(encoding="utf-8")
    start = text.find(CASE_DATA_START)
    end = text.find(CASE_DATA_END)
    if start < 0 or end < 0 or end <= start:
        raise ValueError(f"medical case data block not found: {path}")
    data = text[start + len(CASE_DATA_START) : end].strip()
    if data.startswith("```json"):
        data = data[len("```json") :].strip()
    if data.endswith("```"):
        data = data[:-3].strip()
    payload = json.loads(data)
    if not isinstance(payload, dict):
        raise ValueError(f"medical case data is not an object: {path}")
    return payload
