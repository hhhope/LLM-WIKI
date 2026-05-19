#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEMANTIC_SCORER = ROOT / "scripts" / "score_wiki_semantics.py"


def load_semantic_scores() -> dict:
    if len(sys.argv) > 2:
        raise SystemExit("usage: derive_wiki_utilization.py [semantic-scoring-json-path]")
    if len(sys.argv) == 2:
        payload_path = Path(sys.argv[1]).resolve()
        return json.loads(payload_path.read_text(encoding="utf-8"))

    completed = subprocess.run(
        [sys.executable, str(SEMANTIC_SCORER)],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return json.loads(completed.stdout)


def classify_object(item: dict, repo_pressure: str) -> tuple[str, list[str], str]:
    score = item["semantic_score"]
    factors = item["factor_breakdown"]
    layers = item["coverage_snapshot"]["source_layers"]
    reasons: list[str] = []

    if score >= 8 and factors["cross_layer_presence"] >= 2 and factors["formalization_depth"] >= 2:
        band = "preferred"
        reasons.append("strong bounded semantic score")
        reasons.append("cross-layer evidence is present")
        reasons.append("formalization depth is sufficient")
        guidance = "Use as a first-pass high-confidence context candidate, but keep direct source inspection for final claims."
    elif score >= 7 or len(layers) > 1:
        band = "cautious"
        reasons.append("object has some usable repository evidence")
        reasons.append("repository conditions still limit stronger trust")
        if len(layers) <= 1:
            reasons.append("coverage remains narrow")
        if factors["formalization_depth"] <= 1:
            reasons.append("formalization depth remains thin")
        guidance = "Use only as supporting context and keep stronger caution during interpretation."
    else:
        band = "blocked"
        reasons.append("object remains too thin for stronger agent use")
        if len(layers) <= 1:
            reasons.append("single-layer evidence only")
        guidance = "Do not treat this object as a strong context anchor yet."

    if repo_pressure == "high":
        reasons.append("repository-wide unresolved pressure is high")
    elif repo_pressure == "medium":
        reasons.append("repository-wide unresolved pressure is medium")

    return band, reasons, guidance


def build_utilization(scores: dict) -> dict:
    repo_context = scores.get("repository_context", {})
    repo_pressure = repo_context.get("unresolved_warning_pressure", "low")
    objects = scores.get("object_scores", [])
    utilization = []

    for item in objects:
        band, reasons, guidance = classify_object(item, repo_pressure)
        utilization.append(
            {
                "canonical_object": item["canonical_object"],
                "utilization_band": band,
                "reasons": reasons,
                "source_semantic_score": item["semantic_score"],
                "usage_guidance": guidance,
            }
        )

    counts = {
        "preferred": sum(1 for item in utilization if item["utilization_band"] == "preferred"),
        "cautious": sum(1 for item in utilization if item["utilization_band"] == "cautious"),
        "blocked": sum(1 for item in utilization if item["utilization_band"] == "blocked"),
    }

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_semantic_scoring_summary": scores.get("summary", {}),
        "summary": {
            "object_count": len(utilization),
            "band_counts": counts,
        },
        "repository_caution": {
            "unresolved_warning_pressure": repo_pressure,
            "caution_active": repo_pressure in {"high", "medium"},
            "unresolved_warning_total": repo_context.get("unresolved_warning_total", 0),
        },
        "object_utilization": utilization,
        "utilization_notes": [
            "Utilization output is bounded usage guidance only.",
            "Preferred means better current candidate for agent reading, not retrieval proof.",
            "Cautious means usable only with explicit interpretive caution.",
            "Blocked means the object should not anchor stronger agent judgments yet.",
        ],
    }
    return payload


def main() -> None:
    scores = load_semantic_scores()
    print(json.dumps(build_utilization(scores), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
