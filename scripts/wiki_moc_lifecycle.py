from __future__ import annotations

from collections import defaultdict
from typing import Any


LEARNING_TYPES = {
    "article-evidence-matrix",
    "explore",
    "explore-trace",
    "explore_trace",
    "intake",
    "learning-note",
    "reading-notes",
}
METHOD_TYPES = {
    "artifact-grouping-view",
    "method",
    "ops-model",
    "ops-overview",
    "playbook",
    "product-contract",
    "relation-reading-view",
}
EVIDENCE_TYPES = {
    "diagnosis",
    "distill",
    "recovery",
    "replay-harness",
    "replay-validation",
    "retro",
    "review",
    "review-decision",
    "skill_fix_evidence",
    "surgery-plan",
    "treatment",
    "trace",
}

STAGES = (
    ("sources-learning", "Sources / Learning"),
    ("specification", "Specification"),
    ("decisions", "Decisions"),
    ("methods-runtime", "Methods / Runtime"),
    ("evidence-replay", "Evidence / Replay"),
    ("other", "Other"),
)


def lifecycle_stage(node: dict[str, Any]) -> str:
    artifact_type = str(node.get("artifact_type") or "").strip()
    source_layer = str(node.get("source_layer") or "").strip()

    if source_layer == "openspec/specs" or artifact_type == "spec":
        return "specification"
    if source_layer == "wiki/adr" or artifact_type == "adr":
        return "decisions"
    if artifact_type in LEARNING_TYPES:
        return "sources-learning"
    if artifact_type in METHOD_TYPES:
        return "methods-runtime"
    if artifact_type in EVIDENCE_TYPES:
        return "evidence-replay"
    return "other"


def grouped_lifecycle_nodes(nodes: list[dict[str, Any]]) -> list[tuple[str, list[dict[str, Any]]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in nodes:
        grouped[lifecycle_stage(node)].append(node)

    sections = []
    for stage_key, stage_label in STAGES:
        stage_nodes = grouped.get(stage_key, [])
        if stage_nodes:
            sections.append((stage_label, stage_nodes))
    return sections
