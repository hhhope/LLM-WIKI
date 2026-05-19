#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTO_ROUTING_DERIVER = ROOT / "scripts" / "derive_runtime_auto_routing.py"
MAX_EXCERPT_CHARS = 480


def load_runtime_auto_routing() -> dict:
    if len(sys.argv) > 2:
        raise SystemExit(
            "usage: build_runtime_context_injection.py [runtime-auto-routing-json-path]"
        )
    if len(sys.argv) == 2:
        payload_path = Path(sys.argv[1]).resolve()
        return json.loads(payload_path.read_text(encoding="utf-8"))

    completed = subprocess.run(
        [sys.executable, str(AUTO_ROUTING_DERIVER)],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return json.loads(completed.stdout)


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return text
    return parts[1]


def extract_title(body: str, fallback: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return fallback


def build_excerpt(body: str) -> str:
    collapsed = re.sub(r"\s+", " ", body).strip()
    if len(collapsed) <= MAX_EXCERPT_CHARS:
        return collapsed
    return collapsed[: MAX_EXCERPT_CHARS - 3].rstrip() + "..."


def inject_source(source: dict) -> dict:
    page_path = source["page_path"]
    path = ROOT / page_path
    text = path.read_text(encoding="utf-8")
    body = strip_frontmatter(text)
    path_obj = Path(page_path)
    fallback = path_obj.parent.name if path_obj.stem == "spec" else path_obj.stem
    return {
        "page_path": page_path,
        "artifact_type": source["artifact_type"],
        "source_layer": source["source_layer"],
        "title": extract_title(body, fallback),
        "excerpt": build_excerpt(body),
    }


def inject_entry(item: dict) -> dict:
    return {
        "canonical_object": item["canonical_object"],
        "usage_guidance": item["usage_guidance"],
        "reasons": item["reasons"],
        "injected_sources": [inject_source(source) for source in item.get("route_sources", [])],
    }


def build_context_injection(auto_routing: dict) -> dict:
    injected_first_pass = [
        inject_entry(item) for item in auto_routing.get("open_first", [])
    ]
    secondary_context = [
        inject_entry(item) for item in auto_routing.get("open_next", [])
    ]
    excluded_objects = [
        {
            "canonical_object": item["canonical_object"],
            "usage_guidance": item["usage_guidance"],
            "reasons": item["reasons"],
            "excluded_source_refs": item.get("blocked_source_refs", []),
            "injection_excluded": True,
        }
        for item in auto_routing.get("do_not_open_first", [])
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_routing_summary": auto_routing.get("summary", {}),
        "summary": {
            "injected_first_pass_count": len(injected_first_pass),
            "secondary_context_count": len(secondary_context),
            "excluded_count": len(excluded_objects),
            "injected_first_pass_source_count": sum(
                len(item["injected_sources"]) for item in injected_first_pass
            ),
            "secondary_context_source_count": sum(
                len(item["injected_sources"]) for item in secondary_context
            ),
            "excluded_source_ref_count": sum(
                len(item["excluded_source_refs"]) for item in excluded_objects
            ),
            "caution_active": auto_routing.get("summary", {}).get(
                "caution_active", False
            ),
            "direct_source_inspection_required": auto_routing.get("summary", {}).get(
                "direct_source_inspection_required", True
            ),
        },
        "injected_first_pass": injected_first_pass,
        "secondary_context": secondary_context,
        "excluded_objects": excluded_objects,
        "injection_notes": [
            "Version 1 injects bounded excerpts rather than full page bodies.",
            "Version 1 keeps open_first in injected_first_pass and open_next in secondary_context.",
            "Excluded objects remain outside first-pass injection.",
        ],
        "proof_boundary_notes": [
            "This output is bounded repository-local injected-context guidance only.",
            "It does not prove automatic context injection across all entrypoints.",
            "It does not prove runtime autonomy.",
            "It does not prove unresolved-page understanding.",
        ],
    }


def main() -> None:
    auto_routing = load_runtime_auto_routing()
    print(json.dumps(build_context_injection(auto_routing), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
