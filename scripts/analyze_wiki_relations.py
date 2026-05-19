#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXTRACTOR = ROOT / "scripts" / "extract_wiki_graph.py"


def load_graph_payload() -> dict:
    if len(sys.argv) > 2:
        raise SystemExit("usage: analyze_wiki_relations.py [graph-json-path]")
    if len(sys.argv) == 2:
        graph_path = Path(sys.argv[1]).resolve()
        return json.loads(graph_path.read_text(encoding="utf-8"))

    completed = subprocess.run(
        [sys.executable, str(EXTRACTOR)],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return json.loads(completed.stdout)


def warning_layer(warning: str) -> str:
    _, _, path = warning.partition(":")
    if path.startswith("wiki/ops/"):
        return "wiki/ops"
    if path.startswith("wiki/adr/"):
        return "wiki/adr"
    if path.startswith("wiki/examples/"):
        return "wiki/examples"
    if path.startswith("openspec/specs/"):
        return "openspec/specs"
    return "other"


def analyze(graph: dict) -> dict:
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    warnings = graph.get("warnings", [])

    object_layers: dict[str, set[str]] = defaultdict(set)
    object_types: dict[str, set[str]] = defaultdict(set)
    object_relations: Counter[str] = Counter()
    artifact_type_distribution: Counter[str] = Counter()
    relation_type_distribution: Counter[str] = Counter()
    warning_distribution: Counter[str] = Counter()
    path_to_object: dict[str, str] = {}

    for node in nodes:
        canonical_object = node["canonical_object"]
        source_layer = node["source_layer"]
        artifact_type = node["artifact_type"]
        object_layers[canonical_object].add(source_layer)
        object_types[canonical_object].add(artifact_type)
        artifact_type_distribution[artifact_type] += 1
        path_to_object[node["page_path"]] = canonical_object

    for edge in edges:
        relation_type_distribution[edge["relation_type"]] += 1
        source_object = path_to_object.get(edge["source_page_path"])
        if source_object:
            object_relations[source_object] += 1

    for warning in warnings:
        warning_distribution[warning_layer(warning)] += 1

    object_coverage = []
    for canonical_object in sorted(object_layers):
        layers = sorted(object_layers[canonical_object])
        artifact_types = sorted(object_types[canonical_object])
        object_coverage.append(
            {
                "canonical_object": canonical_object,
                "node_count": sum(
                    1
                    for node in nodes
                    if node["canonical_object"] == canonical_object
                ),
                "source_layers": layers,
                "artifact_types": artifact_types,
                "relation_count": object_relations.get(canonical_object, 0),
                "cross_layer": len(layers) > 1,
            }
        )

    cross_layer_objects = sorted(
        item["canonical_object"]
        for item in object_coverage
        if item["cross_layer"]
    )

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_graph_summary": graph.get("summary", {}),
        "covered_layers": graph.get("covered_layers", []),
        "summary": {
            "canonical_object_count": len(object_coverage),
            "cross_layer_object_count": len(cross_layer_objects),
            "analyzed_node_count": len(nodes),
            "analyzed_edge_count": len(edges),
            "unresolved_warning_count": len(warnings),
        },
        "object_coverage": object_coverage,
        "artifact_type_distribution": dict(sorted(artifact_type_distribution.items())),
        "relation_type_distribution": dict(sorted(relation_type_distribution.items())),
        "unresolved_warning_summary": {
            "total": len(warnings),
            "by_layer": dict(sorted(warning_distribution.items())),
        },
        "analysis_notes": [
            "This artifact is structural analysis only.",
            "Cross-layer coverage means the object appears in more than one covered layer.",
            "Unresolved warnings remain unresolved structure, not semantic understanding.",
            "Relation analysis is stronger than raw extraction, but weaker than rollout proof or retrieval proof.",
        ],
    }
    return payload


def main() -> None:
    graph = load_graph_payload()
    print(json.dumps(analyze(graph), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
