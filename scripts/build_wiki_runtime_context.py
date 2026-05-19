#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UTILIZATION_DERIVER = ROOT / "scripts" / "derive_wiki_utilization.py"


def load_utilization() -> dict:
    if len(sys.argv) > 2:
        raise SystemExit("usage: build_wiki_runtime_context.py [utilization-json-path]")
    if len(sys.argv) == 2:
        payload_path = Path(sys.argv[1]).resolve()
        return json.loads(payload_path.read_text(encoding="utf-8"))

    completed = subprocess.run(
        [sys.executable, str(UTILIZATION_DERIVER)],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return json.loads(completed.stdout)


def context_entry(item: dict) -> dict:
    return {
        "canonical_object": item["canonical_object"],
        "usage_guidance": item["usage_guidance"],
        "reasons": item["reasons"],
        "source_utilization_band": item["utilization_band"],
        "source_semantic_score": item["source_semantic_score"],
    }


def build_runtime_context(utilization: dict) -> dict:
    preferred = []
    supporting = []
    blocked = []

    for item in utilization.get("object_utilization", []):
        entry = context_entry(item)
        if item["utilization_band"] == "preferred":
            preferred.append(entry)
        elif item["utilization_band"] == "cautious":
            supporting.append(entry)
        else:
            blocked.append(entry)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_utilization_summary": utilization.get("summary", {}),
        "summary": {
            "preferred_count": len(preferred),
            "supporting_count": len(supporting),
            "blocked_count": len(blocked),
            "caution_active": utilization.get("repository_caution", {}).get("caution_active", False),
        },
        "preferred_context": preferred,
        "supporting_context": supporting,
        "blocked_context": blocked,
        "runtime_caution": {
            "repository_caution": utilization.get("repository_caution", {}),
            "direct_source_inspection_required": True,
            "read_order_hint": [
                "preferred_context",
                "supporting_context",
                "blocked_context",
            ],
        },
        "runtime_notes": [
            "This bundle is bounded runtime guidance only.",
            "Preferred context should be read first, but does not replace source inspection.",
            "Supporting context is useful only with explicit caution.",
            "Blocked context should not anchor stronger runtime judgments yet.",
        ],
    }
    return payload


def main() -> None:
    utilization = load_utilization()
    print(json.dumps(build_runtime_context(utilization), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
