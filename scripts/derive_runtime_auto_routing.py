#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTEGRATION_DERIVER = ROOT / "scripts" / "resolve_runtime_context_sources.py"


def load_source_integrated_runtime() -> dict:
    if len(sys.argv) > 2:
        raise SystemExit(
            "usage: derive_runtime_auto_routing.py [source-integrated-runtime-json-path]"
        )
    if len(sys.argv) == 2:
        payload_path = Path(sys.argv[1]).resolve()
        return json.loads(payload_path.read_text(encoding="utf-8"))

    completed = subprocess.run(
        [sys.executable, str(SOURCE_INTEGRATION_DERIVER)],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return json.loads(completed.stdout)


def route_entry(item: dict) -> dict:
    return {
        "canonical_object": item["canonical_object"],
        "usage_guidance": item["usage_guidance"],
        "reasons": item["reasons"],
        "route_sources": item.get("resolved_sources", []),
    }


def build_runtime_auto_routing(source_runtime: dict) -> dict:
    open_first = [
        route_entry(item) for item in source_runtime.get("preferred_sources", [])
    ]
    open_next = [
        route_entry(item) for item in source_runtime.get("supporting_sources", [])
    ]
    do_not_open_first = [
        {
            "canonical_object": item["canonical_object"],
            "usage_guidance": item["usage_guidance"],
            "reasons": item["reasons"],
            "blocked_source_refs": item.get("blocked_source_refs", []),
            "routing_blocked": True,
        }
        for item in source_runtime.get("blocked_objects", [])
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_runtime_summary": source_runtime.get("summary", {}),
        "summary": {
            "open_first_count": len(open_first),
            "open_next_count": len(open_next),
            "blocked_count": len(do_not_open_first),
            "open_first_source_count": sum(
                len(item["route_sources"]) for item in open_first
            ),
            "open_next_source_count": sum(
                len(item["route_sources"]) for item in open_next
            ),
            "blocked_source_ref_count": sum(
                len(item["blocked_source_refs"]) for item in do_not_open_first
            ),
            "caution_active": source_runtime.get("summary", {}).get(
                "caution_active", False
            ),
            "direct_source_inspection_required": source_runtime.get("summary", {}).get(
                "direct_source_inspection_required", True
            ),
        },
        "open_first": open_first,
        "open_next": open_next,
        "do_not_open_first": do_not_open_first,
        "routing_notes": [
            "Version 1 keeps preferred sources in open_first and supporting sources in open_next.",
            "Version 1 preserves source-integration ordering and does not re-rank routed sources.",
            "Blocked objects remain excluded from first-pass route generation.",
        ],
        "proof_boundary_notes": [
            "This output is bounded repository-local runtime routing guidance only.",
            "It does not prove automatic context injection.",
            "It does not prove external retrieval integration.",
            "It does not prove runtime autonomy.",
        ],
    }


def main() -> None:
    source_runtime = load_source_integrated_runtime()
    print(json.dumps(build_runtime_auto_routing(source_runtime), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
