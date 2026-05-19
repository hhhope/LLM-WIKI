#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from extract_wiki_graph import collect_pages


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_CONTEXT_DERIVER = ROOT / "scripts" / "build_wiki_runtime_context.py"
ARTIFACT_PRIORITY = {
    "method": 0,
    "adr": 1,
    "spec": 2,
    "runtime-rule": 3,
    "example": 4,
    "sample": 5,
    "runtime-validation": 6,
    "replay-harness": 7,
    "replay-validation": 8,
}


def load_runtime_context() -> dict:
    if len(sys.argv) > 2:
        raise SystemExit(
            "usage: resolve_runtime_context_sources.py [runtime-context-json-path]"
        )
    if len(sys.argv) == 2:
        payload_path = Path(sys.argv[1]).resolve()
        return json.loads(payload_path.read_text(encoding="utf-8"))

    completed = subprocess.run(
        [sys.executable, str(RUNTIME_CONTEXT_DERIVER)],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return json.loads(completed.stdout)


def build_source_index() -> dict[str, list[dict]]:
    nodes, _edges, _warnings = collect_pages()
    index: dict[str, list[dict]] = {}
    for node in nodes:
        index.setdefault(node["canonical_object"], []).append(
            {
                "page_path": node["page_path"],
                "artifact_type": node["artifact_type"],
                "source_layer": node["source_layer"],
            }
        )

    for canonical_object in index:
        index[canonical_object].sort(
            key=lambda item: (
                ARTIFACT_PRIORITY.get(item["artifact_type"], 99),
                item["page_path"],
            )
        )

    return index


def integrate_entry(item: dict, source_index: dict[str, list[dict]]) -> dict:
    canonical_object = item["canonical_object"]
    return {
        "canonical_object": canonical_object,
        "usage_guidance": item["usage_guidance"],
        "reasons": item["reasons"],
        "resolved_sources": source_index.get(canonical_object, []),
    }


def build_integrated_runtime(runtime_context: dict) -> dict:
    source_index = build_source_index()

    preferred_sources = [
        integrate_entry(item, source_index)
        for item in runtime_context.get("preferred_context", [])
    ]
    supporting_sources = [
        integrate_entry(item, source_index)
        for item in runtime_context.get("supporting_context", [])
    ]
    blocked_objects = [
        {
            "canonical_object": item["canonical_object"],
            "usage_guidance": item["usage_guidance"],
            "reasons": item["reasons"],
            "blocked_source_refs": source_index.get(item["canonical_object"], []),
            "resolution_skipped": True,
        }
        for item in runtime_context.get("blocked_context", [])
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_runtime_summary": runtime_context.get("summary", {}),
        "summary": {
            "preferred_count": len(preferred_sources),
            "supporting_count": len(supporting_sources),
            "blocked_count": len(blocked_objects),
            "blocked_source_ref_count": sum(
                len(item["blocked_source_refs"]) for item in blocked_objects
            ),
            "caution_active": runtime_context.get("summary", {}).get(
                "caution_active", False
            ),
            "direct_source_inspection_required": runtime_context.get(
                "runtime_caution", {}
            ).get("direct_source_inspection_required", True),
        },
        "preferred_sources": preferred_sources,
        "supporting_sources": supporting_sources,
        "blocked_objects": blocked_objects,
        "source_resolution_notes": [
            "Version 1 resolves repository-local sources only.",
            "Resolved sources are ordered deterministically by artifact priority and path.",
            "Blocked objects remain isolated from first-pass source selection.",
        ],
        "proof_boundary_notes": [
            "This output is bounded repository-local source guidance only.",
            "It does not prove external retrieval integration.",
            "It does not prove autonomous runtime context loading.",
            "It does not prove semantic understanding of unresolved pages.",
        ],
    }


def main() -> None:
    runtime_context = load_runtime_context()
    print(json.dumps(build_integrated_runtime(runtime_context), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
