from __future__ import annotations

from collections import Counter
from typing import Any

CONTRACT_VERSION = "1"
RELATION_FIELDS = (
    "related_objects",
    "related_sources",
    "derived_from",
    "validates",
    "related_focus_threads",
    "related_reminders",
)


def relation_fields_from_meta(meta: dict[str, Any]) -> dict[str, Any]:
    return {field: meta.get(field) for field in RELATION_FIELDS}


def _object_type_for_page(page: dict[str, Any]) -> str:
    section = page.get("section")
    artifact_type = str(page.get("artifact_type") or "").lower()
    path = str(page.get("path") or "")
    if section == "wiki/sources":
        return "source"
    if section == "wiki/reports":
        return "output"
    if section == "wiki/status":
        return "status"
    if section == "wiki/adr" or path.startswith("openspec/"):
        return "governance"
    if section == "wiki/ops" and any(
        marker in artifact_type
        for marker in ("replay", "validation", "evaluation")
    ):
        return "behavior"
    return "unknown"


def _source_layer_for_page(page: dict[str, Any]) -> str:
    section = page.get("section")
    if section == "wiki/sources":
        return "source"
    if section == "wiki/reports":
        return "report"
    if section == "wiki/status":
        return "generated_status"
    if section == "wiki/adr":
        return "spec"
    if section == "wiki/ops":
        return "ops"
    return "unknown"


def _readiness_for_status(status: object) -> str:
    value = str(status or "").strip().lower().replace("_", "-")
    if value == "accepted":
        return "accepted"
    if value in {"blocked", "unresolved", "invalid", "draft-only"}:
        return value
    return "draft-only"


def _has_identity(page: dict[str, Any]) -> bool:
    return bool(page.get("canonical_object"))


def _has_relation(page: dict[str, Any]) -> bool:
    return any(bool(page.get(field)) for field in RELATION_FIELDS)


def build_product_status(
    pages: list[dict[str, Any]],
    inbox_files: list[dict[str, Any]],
    openspec_changes: list[dict[str, Any]],
) -> dict[str, Any]:
    object_type_counts: Counter[str] = Counter()
    readiness_counts: Counter[str] = Counter()
    source_layer_counts: Counter[str] = Counter()
    unresolved_items: list[dict[str, str]] = []
    with_identity = 0
    missing_identity = 0
    with_relations = 0
    missing_relations = 0

    for page in pages:
        object_type_counts[_object_type_for_page(page)] += 1
        source_layer_counts[_source_layer_for_page(page)] += 1
        readiness_counts[_readiness_for_status(page.get("status"))] += 1
        if _has_identity(page):
            with_identity += 1
        else:
            missing_identity += 1
        if _has_relation(page):
            with_relations += 1
        else:
            missing_relations += 1

    for item in inbox_files:
        if item.get("represented_by_source"):
            continue
        unresolved_items.append(
            {
                "type": "pending_inbox",
                "path": str(item.get("path")),
                "readiness_label": "blocked",
                "status_transition": "evidence_collection",
            }
        )

    for change in openspec_changes:
        object_type_counts["governance"] += 1
        source_layer_counts["spec"] += 1
        if change.get("state") == "complete":
            unresolved_items.append(
                {
                    "type": "complete_openspec_change",
                    "change_id": str(change.get("change_id")),
                    "readiness_label": "unresolved",
                    "status_transition": "archive_review",
                }
            )

    return {
        "contract_version": CONTRACT_VERSION,
        "object_type_counts": dict(sorted(object_type_counts.items())),
        "readiness_counts": dict(sorted(readiness_counts.items())),
        "source_layer_counts": dict(sorted(source_layer_counts.items())),
        "identity_coverage": {
            "with_identity": with_identity,
            "missing_identity": missing_identity,
        },
        "relation_coverage": {
            "with_relations": with_relations,
            "missing_relations": missing_relations,
        },
        "unresolved_items": unresolved_items,
    }
