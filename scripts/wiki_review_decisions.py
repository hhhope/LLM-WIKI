from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_DECISION_RECORD_DIR = Path("wiki/ops/wiki-review-decisions")
DECISION_DATA_START = "<!-- wiki-review-decision-data:start -->"
DECISION_DATA_END = "<!-- wiki-review-decision-data:end -->"

SURGERY_RISK_FLAGS = {
    "openspec_required",
    "drift_risk",
    "adr_risk",
    "relation_weak_evidence",
}
OPENSPEC_RISK_FLAGS = {"openspec_required", "taxonomy_candidate"}

BUCKETS = [
    "accepted_candidates",
    "rejected_candidates",
    "deferred_items",
    "treatment_candidates",
    "surgery_candidates",
    "openspec_required",
]


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


def _limited(items: Any, limit: int | None) -> list[Any]:
    if not isinstance(items, list):
        return []
    if limit is None:
        return items
    return items[: max(0, limit)]


def _detail_ref(detail: dict[str, Any]) -> str:
    return str(detail.get("detail_ref") or detail.get("detail_id") or "unknown")


def _risk_flags(detail: dict[str, Any]) -> list[str]:
    flags = detail.get("risk_flags", [])
    if not isinstance(flags, list):
        return []
    return [str(flag) for flag in flags if str(flag).strip()]


def _judgment(detail: dict[str, Any]) -> dict[str, Any]:
    judgment = detail.get("judgment", {})
    return judgment if isinstance(judgment, dict) else {}


def _judgment_state(detail: dict[str, Any]) -> str:
    return str(_judgment(detail).get("state", ""))


def _reason(detail: dict[str, Any]) -> str:
    reason = detail.get("reason")
    if reason is None:
        reason = _judgment(detail).get("reason", "")
    return str(reason)


def _decision_entry(detail: dict[str, Any]) -> dict[str, Any]:
    entry: dict[str, Any] = {"detail_ref": _detail_ref(detail)}
    if detail.get("path"):
        entry["path"] = str(detail["path"])
    reason = _reason(detail)
    if reason:
        entry["reason"] = reason
    entry["risk_flags"] = _risk_flags(detail)
    if detail.get("rejected_candidates"):
        entry["rejected_candidates"] = detail["rejected_candidates"]
    candidate = detail.get("candidate", {})
    if isinstance(candidate, dict):
        suggested = candidate.get("suggested_frontmatter", {})
        if isinstance(suggested, dict) and suggested:
            entry["suggested_frontmatter"] = {
                str(key): value for key, value in suggested.items() if str(key).strip()
            }
    return entry


def _append(bucket: list[dict[str, Any]], detail: dict[str, Any]) -> None:
    bucket.append(_decision_entry(detail))


def build_review_decision_package(
    adjudication_package: dict[str, Any],
    source_record: str | None = None,
) -> dict[str, Any]:
    package: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "wiki_review_decision_package",
        "source_record": source_record,
        "source_adjudication_summary": adjudication_package.get("summary", {}),
    }
    for bucket in BUCKETS:
        package[bucket] = []

    details = adjudication_package.get("full_detail_set", [])
    if not isinstance(details, list):
        details = []

    for detail in details:
        if not isinstance(detail, dict):
            continue
        risks = set(_risk_flags(detail))
        state = _judgment_state(detail)

        if detail.get("safe_to_apply_frontmatter") is True:
            _append(package["treatment_candidates"], detail)
        if risks & SURGERY_RISK_FLAGS:
            _append(package["surgery_candidates"], detail)
        if risks & OPENSPEC_RISK_FLAGS:
            _append(package["openspec_required"], detail)
        if state == "needs_user_confirmation" or "agent_uncertain" in risks:
            _append(package["deferred_items"], detail)
        if state == "reject" or bool(detail.get("rejected_candidates")):
            _append(package["rejected_candidates"], detail)
        if state == "accept" and not risks:
            _append(package["accepted_candidates"], detail)

    package["summary"] = {
        "source_detail_count": len(details),
        **{f"{bucket}_count": len(package[bucket]) for bucket in BUCKETS},
    }
    package["proof_boundary_notes"] = [
        "This is draft review routing only, not human approval.",
        "It does not write frontmatter, taxonomy, relations, MOC, or OpenSpec state.",
    ]
    return package


def _format_entry(item: dict[str, Any]) -> str:
    detail_ref = str(item.get("detail_ref", "unknown"))
    path = str(item.get("path", ""))
    prefix = f"{detail_ref} `{path}`" if path else detail_ref
    parts = [prefix]
    risk_flags = item.get("risk_flags", [])
    if isinstance(risk_flags, list) and risk_flags:
        parts.append("risks=" + ", ".join(str(flag) for flag in risk_flags))
    reason = str(item.get("reason", ""))
    if reason:
        parts.append(reason)
    return ": ".join([parts[0], "; ".join(parts[1:])]) if len(parts) > 1 else parts[0]


def _bucket_lines(items: Any, limit: int | None) -> list[str]:
    limited = _limited(items, limit)
    if not limited:
        return ["- None"]
    return [f"- {_format_entry(item)}" for item in limited if isinstance(item, dict)]


def _abnormal_lines(package: dict[str, Any], limit: int | None) -> list[str]:
    by_ref: dict[str, dict[str, Any]] = {}
    memberships: dict[str, list[str]] = {}
    for bucket in BUCKETS:
        for item in package.get(bucket, []):
            if not isinstance(item, dict):
                continue
            detail_ref = str(item.get("detail_ref", "unknown"))
            by_ref.setdefault(detail_ref, item)
            memberships.setdefault(detail_ref, []).append(bucket)
    if not by_ref:
        return ["- None"]
    lines = []
    for detail_ref in list(by_ref)[: None if limit is None else max(0, limit)]:
        item = by_ref[detail_ref]
        risk_flags = item.get("risk_flags", [])
        risk_text = ", ".join(str(flag) for flag in risk_flags) if isinstance(risk_flags, list) and risk_flags else "none"
        bucket_text = ", ".join(memberships.get(detail_ref, [])) or "none"
        path = str(item.get("path", ""))
        reason = str(item.get("reason", ""))
        lines.append(f"- {detail_ref} `{path}` buckets={bucket_text}; risks={risk_text}: {reason}")
    return lines


def render_review_decision_markdown(package: dict[str, Any], scan_root: Path | str, limit: int | None) -> str:
    summary = package.get("summary", {})
    generated_at = str(package.get("generated_at", "unknown"))
    detail_limit = "complete" if limit is None else str(limit)
    lines = [
        "# wiki-confirm Confirmation Record",
        "",
        "## Source / 检查来源",
        "",
        f"- Generated at: {generated_at}",
        f"- Scan root: `{Path(scan_root)}`",
        f"- Detail limit: {detail_limit}",
        f"- Source record: {package.get('source_record') or 'none'}",
        "- Source package: scripts/build_wiki_content_adjudication.py",
        "",
        "## Decision Rules / 确诊标准",
        "- safe_to_apply_frontmatter=true -> treatment_candidates.",
        "- relation_weak_evidence, drift_risk, or adr_risk -> surgery_candidates.",
        "- openspec_required or taxonomy_candidate -> openspec_required.",
        "- agent_uncertain or needs_user_confirmation -> deferred_items.",
        "- reject or rejected candidate details -> rejected_candidates.",
        "- accept with no risk flags -> accepted_candidates.",
        "",
        "## Summary",
    ]

    if isinstance(summary, dict) and summary:
        for key in sorted(summary):
            lines.append(f"- {key}: {summary[key]}")
    else:
        lines.append("- None")

    lines.extend(["", "## Confirmed Buckets / 确诊分流"])
    sections = [
        ("Accepted Candidates", "accepted_candidates"),
        ("Treatment Candidates", "treatment_candidates"),
        ("Surgery Candidates", "surgery_candidates"),
        ("OpenSpec Required", "openspec_required"),
        ("Deferred Items", "deferred_items"),
        ("Rejected Candidates", "rejected_candidates"),
    ]
    for title, bucket in sections:
        lines.extend(["", f"## {title}"])
        lines.extend(_bucket_lines(package.get(bucket, []), limit))

    lines.extend(["", "## Abnormal Findings / 异常明细"])
    lines.extend(_abnormal_lines(package, limit))

    lines.extend(
        [
            "",
            "## Medical Advice / 处理建议",
            "- Treatment candidates may enter `wiki-treatment` only after explicit approval.",
            "- Surgery candidates route to `wiki-surgery` planning.",
            "- OpenSpec-required items cannot be handled through treatment alone.",
            "- Deferred items need human review before routing.",
            "",
            "## Proof Boundary",
            "- This is draft review routing only, not human approval.",
            "- It does not write frontmatter, taxonomy, relations, MOC, or OpenSpec state.",
            "",
            "## Next Actions",
            "- Human review: confirm which candidates are accepted, deferred, rejected, treatment candidates, surgery candidates, or OpenSpec-required.",
            "- Treatment: apply only later, after explicit approval for low-risk frontmatter updates.",
            "- Surgery or OpenSpec: plan structural, taxonomy, relation, MOC, governance, or lifecycle changes separately.",
        ]
    )
    machine_json = json.dumps(package, ensure_ascii=False, indent=2, sort_keys=True)
    lines.extend(
        [
            "",
            "## Machine Decision Data",
            DECISION_DATA_START,
            "```json",
            machine_json,
            "```",
            DECISION_DATA_END,
        ]
    )
    return "\n".join(lines) + "\n"


def load_review_decision_record(path: Path | str) -> dict[str, Any]:
    text = Path(path).read_text(encoding="utf-8")
    start = text.find(DECISION_DATA_START)
    end = text.find(DECISION_DATA_END)
    if start < 0 or end < 0 or end <= start:
        raise ValueError(f"review decision data block not found: {path}")
    data = text[start + len(DECISION_DATA_START) : end].strip()
    if data.startswith("```json"):
        data = data[len("```json") :].strip()
    if data.endswith("```"):
        data = data[:-3].strip()
    payload = json.loads(data)
    if not isinstance(payload, dict):
        raise ValueError(f"review decision data is not an object: {path}")
    return payload


def next_review_decision_record_path(output_dir: Path, timestamp: datetime | str | None = None) -> Path:
    slug = _timestamp_slug(timestamp)
    base = output_dir / f"{slug}-review-decisions.md"
    if not base.exists():
        return base
    counter = 2
    while True:
        candidate = output_dir / f"{slug}-review-decisions-{counter}.md"
        if not candidate.exists():
            return candidate
        counter += 1


def write_review_decision_record(
    package: dict[str, Any],
    root: Path | str,
    output_dir: Path | str | None = None,
    timestamp: datetime | str | None = None,
    limit: int | None = None,
) -> Path:
    root_path = Path(root)
    target_dir = Path(output_dir) if output_dir is not None else root_path / DEFAULT_DECISION_RECORD_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    markdown = render_review_decision_markdown(package, scan_root=root_path, limit=limit)

    while True:
        target = next_review_decision_record_path(target_dir, timestamp=timestamp)
        try:
            with target.open("x", encoding="utf-8") as handle:
                handle.write(markdown)
            return target.resolve()
        except FileExistsError:
            continue
