#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELATION_ANALYZER = ROOT / "scripts" / "analyze_wiki_relations.py"
FORMAL_TYPES = {"method", "spec", "adr"}


def load_relation_analysis() -> dict:
    if len(sys.argv) > 2:
        raise SystemExit("usage: score_wiki_semantics.py [relation-analysis-json-path]")
    if len(sys.argv) == 2:
        payload_path = Path(sys.argv[1]).resolve()
        return json.loads(payload_path.read_text(encoding="utf-8"))

    completed = subprocess.run(
        [sys.executable, str(RELATION_ANALYZER)],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return json.loads(completed.stdout)


def cross_layer_score(layer_count: int) -> int:
    if layer_count >= 3:
        return 3
    if layer_count == 2:
        return 2
    return 0


def artifact_variety_score(type_count: int) -> int:
    if type_count >= 4:
        return 2
    if type_count >= 2:
        return 1
    return 0


def relation_presence_score(relation_count: int) -> int:
    if relation_count >= 3:
        return 2
    if relation_count >= 1:
        return 1
    return 0


def formalization_depth_score(artifact_types: list[str]) -> int:
    return min(3, sum(1 for artifact_type in artifact_types if artifact_type in FORMAL_TYPES))


def score_band(score: int) -> str:
    if score >= 7:
        return "strong"
    if score >= 4:
        return "moderate"
    return "weak"


def unresolved_pressure(total: int) -> str:
    if total >= 50:
        return "high"
    if total >= 20:
        return "medium"
    return "low"


def build_scores(relation_analysis: dict) -> dict:
    objects = relation_analysis.get("object_coverage", [])
    unresolved_total = relation_analysis.get("unresolved_warning_summary", {}).get("total", 0)
    scored_objects = []

    for obj in objects:
        layer_count = len(obj["source_layers"])
        type_count = len(obj["artifact_types"])
        relation_count = obj["relation_count"]
        factors = {
            "cross_layer_presence": cross_layer_score(layer_count),
            "artifact_type_variety": artifact_variety_score(type_count),
            "relation_presence": relation_presence_score(relation_count),
            "formalization_depth": formalization_depth_score(obj["artifact_types"]),
        }
        semantic_score = sum(factors.values())
        scored_objects.append(
            {
                "canonical_object": obj["canonical_object"],
                "semantic_score": semantic_score,
                "score_band": score_band(semantic_score),
                "factor_breakdown": factors,
                "coverage_snapshot": {
                    "node_count": obj["node_count"],
                    "source_layers": obj["source_layers"],
                    "artifact_types": obj["artifact_types"],
                    "relation_count": relation_count,
                },
            }
        )

    scored_objects.sort(key=lambda item: (-item["semantic_score"], item["canonical_object"]))

    scores = [item["semantic_score"] for item in scored_objects]
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_relation_analysis_summary": relation_analysis.get("summary", {}),
        "summary": {
            "scored_object_count": len(scored_objects),
            "score_range": {
                "min": min(scores) if scores else 0,
                "max": max(scores) if scores else 0,
            },
            "band_counts": {
                "strong": sum(1 for item in scored_objects if item["score_band"] == "strong"),
                "moderate": sum(1 for item in scored_objects if item["score_band"] == "moderate"),
                "weak": sum(1 for item in scored_objects if item["score_band"] == "weak"),
            },
        },
        "repository_context": {
            "unresolved_warning_total": unresolved_total,
            "unresolved_warning_pressure": unresolved_pressure(unresolved_total),
            "unresolved_warning_by_layer": relation_analysis.get("unresolved_warning_summary", {}).get("by_layer", {}),
        },
        "object_scores": scored_objects,
        "scoring_notes": [
            "Scores are bounded repository-evidence signals only.",
            "Version 1 uses explicit rule-based factors rather than embeddings or LLM scoring.",
            "A higher score means stronger repository evidence for that canonical object, not retrieval proof.",
            "Unresolved warnings still limit stronger semantic claims.",
        ],
    }
    return payload


def main() -> None:
    relation_analysis = load_relation_analysis()
    print(json.dumps(build_scores(relation_analysis), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
