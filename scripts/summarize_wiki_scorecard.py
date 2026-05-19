#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEMANTIC_SCORER = ROOT / "scripts" / "score_wiki_semantics.py"
UTILIZATION_DERIVER = ROOT / "scripts" / "derive_wiki_utilization.py"
DEFAULT_LIMIT = 12


def run_json(command: list[str]) -> dict:
    completed = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return json.loads(completed.stdout)


def load_payload(path: str | None, fallback_command: list[str]) -> dict:
    if path:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    return run_json(fallback_command)


def utilization_for(scores_path: str | None, scores: dict) -> dict:
    if scores_path:
        return run_json([sys.executable, str(UTILIZATION_DERIVER), scores_path])

    import tempfile

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json") as handle:
        json.dump(scores, handle, ensure_ascii=False)
        handle.flush()
        return run_json([sys.executable, str(UTILIZATION_DERIVER), handle.name])


def normalize_focus(value: str | None) -> str | None:
    return value.strip().lower() if value and value.strip() else None


def inspection_actions(score: dict, utilization: dict) -> list[str]:
    coverage = score.get("coverage_snapshot", {})
    layers = ", ".join(coverage.get("source_layers", [])) or "no source layers"
    artifact_types = ", ".join(coverage.get("artifact_types", [])) or "no artifact types"
    actions = [
        f"Inspect explicit source layers: {layers}.",
        f"Check artifact types before using as an anchor: {artifact_types}.",
    ]
    if utilization.get("utilization_band") == "blocked":
        actions.append("Do not anchor execution on this object until coverage improves.")
    elif utilization.get("utilization_band") == "cautious":
        actions.append("Use only as supporting context with direct source inspection.")
    else:
        actions.append("Use as a first-pass candidate, then verify source pages directly.")
    return actions


def summarize_scorecard(scores: dict, utilization: dict, focus: str | None = None, limit: int = DEFAULT_LIMIT) -> dict:
    normalized_focus = normalize_focus(focus)
    utilization_by_object = {
        item["canonical_object"]: item
        for item in utilization.get("object_utilization", [])
    }
    diagnostics = []

    for score in scores.get("object_scores", []):
        canonical_object = score["canonical_object"]
        if normalized_focus and normalized_focus not in canonical_object.lower():
            continue
        utilization_item = utilization_by_object.get(canonical_object, {})
        diagnostics.append(
            {
                "canonical_object": canonical_object,
                "semantic_score": score["semantic_score"],
                "score_band": score["score_band"],
                "utilization_band": utilization_item.get("utilization_band", "unknown"),
                "reasons": utilization_item.get("reasons", []),
                "coverage_snapshot": score.get("coverage_snapshot", {}),
                "factor_breakdown": score.get("factor_breakdown", {}),
                "next_inspection_actions": inspection_actions(score, utilization_item),
            }
        )

    band_priority = {"preferred": 0, "cautious": 1, "blocked": 2, "unknown": 3}
    diagnostics.sort(
        key=lambda item: (
            band_priority.get(item["utilization_band"], 3),
            -item["semantic_score"],
            item["canonical_object"],
        )
    )
    diagnostics = diagnostics[:limit]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "focus": focus or None,
        "source_scoring_summary": scores.get("summary", {}),
        "source_utilization_summary": utilization.get("summary", {}),
        "repository_caution": utilization.get("repository_caution", {}),
        "summary": {
            "displayed_diagnostic_count": len(diagnostics),
            "scored_object_count": scores.get("summary", {}).get("scored_object_count", 0),
            "score_band_counts": scores.get("summary", {}).get("band_counts", {}),
            "utilization_band_counts": utilization.get("summary", {}).get("band_counts", {}),
            "caution_active": utilization.get("repository_caution", {}).get(
                "caution_active", False
            ),
        },
        "diagnostics": diagnostics,
        "proof_boundary_notes": [
            "This is bounded repository-evidence diagnostics only.",
            "It uses explicit rule-based scores, no embeddings, and no hidden semantic ranking.",
            "Score bands do not prove retrieval quality or permission to skip source inspection.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("focus", nargs="?", help="optional canonical object focus")
    parser.add_argument("--scores", help="path to semantic-scoring JSON")
    parser.add_argument("--utilization", help="path to utilization JSON")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    args = parser.parse_args()

    scores = load_payload(args.scores, [sys.executable, str(SEMANTIC_SCORER)])
    utilization = (
        load_payload(args.utilization, [sys.executable, str(UTILIZATION_DERIVER)])
        if args.utilization
        else utilization_for(args.scores, scores)
    )
    print(
        json.dumps(
            summarize_scorecard(scores, utilization, args.focus, args.limit),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
