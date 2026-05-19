#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTEXT_INJECTION_DERIVER = ROOT / "scripts" / "build_runtime_context_injection.py"
GRAPH_EXTRACTOR = ROOT / "scripts" / "extract_wiki_graph.py"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.wiki_moc_projection import build_moc_plan
from scripts.wiki_content_enrichment import build_enrichment_preview
from scripts.wiki_content_adjudication import build_adjudication_package


def load_context_injection() -> dict:
    if len(sys.argv) > 2:
        raise SystemExit(
            "usage: derive_self_directed_execution.py [context-injection-json-path]"
        )
    if len(sys.argv) == 2:
        payload_path = Path(sys.argv[1]).resolve()
        return json.loads(payload_path.read_text(encoding="utf-8"))

    completed = subprocess.run(
        [sys.executable, str(CONTEXT_INJECTION_DERIVER)],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    return json.loads(completed.stdout)


def build_action_sources(item: dict, source_key: str = "injected_sources") -> list[dict]:
    action_sources = []
    for source in item.get(source_key, []):
        action_source = {
            "page_path": source["page_path"],
            "artifact_type": source["artifact_type"],
            "source_layer": source["source_layer"],
        }
        if "title" in source:
            action_source["title"] = source["title"]
        action_sources.append(action_source)
    return action_sources


def execute_entry(item: dict) -> dict:
    return {
        "canonical_object": item["canonical_object"],
        "execution_guidance": "Inspect these injected sources and apply them as the first-pass execution basis.",
        "reasons": item["reasons"],
        "action_type": "inspect_and_apply_context",
        "action_sources": build_action_sources(item),
    }


def followup_entry(item: dict) -> dict:
    return {
        "canonical_object": item["canonical_object"],
        "execution_guidance": "Inspect these injected sources only after first-pass execution is stable.",
        "reasons": item["reasons"],
        "action_type": "inspect_before_followup",
        "action_sources": build_action_sources(item),
    }


def blocked_entry(item: dict) -> dict:
    return {
        "canonical_object": item["canonical_object"],
        "execution_guidance": "Do not execute from this object during first-pass execution.",
        "reasons": item["reasons"],
        "action_type": "blocked_from_first_pass_execution",
        "action_sources": build_action_sources(item, "excluded_source_refs"),
    }


def build_self_directed_execution(context_injection: dict) -> dict:
    execute_now = [
        execute_entry(item)
        for item in context_injection.get("injected_first_pass", [])
    ]
    defer_for_followup = [
        followup_entry(item)
        for item in context_injection.get("secondary_context", [])
    ]
    do_not_execute = [
        blocked_entry(item)
        for item in context_injection.get("excluded_objects", [])
    ]
    graph = json.loads(
        subprocess.run(
            [sys.executable, str(GRAPH_EXTRACTOR)],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        ).stdout
    )
    moc_projection_preview = build_moc_plan(ROOT, graph)
    enrichment_preview = build_enrichment_preview(ROOT)
    adjudication_package = build_adjudication_package(ROOT)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_injection_summary": context_injection.get("summary", {}),
        "summary": {
            "execute_now_count": len(execute_now),
            "deferred_count": len(defer_for_followup),
            "blocked_count": len(do_not_execute),
            "execute_now_source_count": sum(
                len(item["action_sources"]) for item in execute_now
            ),
            "deferred_source_count": sum(
                len(item["action_sources"]) for item in defer_for_followup
            ),
            "blocked_source_count": sum(
                len(item["action_sources"]) for item in do_not_execute
            ),
            "caution_active": context_injection.get("summary", {}).get(
                "caution_active", False
            ),
            "direct_source_inspection_required": context_injection.get("summary", {}).get(
                "direct_source_inspection_required", True
            ),
        },
        "execute_now": execute_now,
        "defer_for_followup": defer_for_followup,
        "do_not_execute": do_not_execute,
        "moc_projection_preview": {
            "summary": moc_projection_preview["summary"],
            "entries": [
                {
                    "action": entry["action"],
                    "kind": entry["kind"],
                    "key": entry["key"],
                    "path": entry["path"],
                    "link_count": entry["link_count"],
                }
                for entry in moc_projection_preview["entries"][:20]
            ],
            "execution_boundary": "preview_only",
        },
        "content_enrichment_preview": {
            "summary": enrichment_preview["summary"],
            "entries": enrichment_preview["entries"][:20],
            "execution_boundary": "preview_only",
        },
        "content_adjudication_review_package": {
            "summary": adjudication_package["summary"],
            "eval_result": adjudication_package["eval_result"],
            "review_focus_set": adjudication_package["review_focus_set"][:20],
            "drift_trace_set": adjudication_package["drift_trace_set"][:20],
            "execution_boundary": "review_only",
        },
        "execution_notes": [
            "Version 1 derives bounded actions from injected context only.",
            "Execute-now actions come only from injected_first_pass context.",
            "Blocked objects remain outside first-pass execution.",
            "MOC projection preview is inspect-only; use the explicit generator with --apply to write files.",
            "Content enrichment preview is inspect-only; reviewed frontmatter edits are a separate write action.",
            "Content adjudication review package is inspect-only; it does not decide or apply semantic truth.",
        ],
        "proof_boundary_notes": [
            "This output is bounded repository-local execution guidance only.",
            "It does not prove unrestricted agent autonomy.",
            "It does not prove external retrieval integration.",
            "It does not prove unresolved-page understanding.",
        ],
    }


def main() -> None:
    context_injection = load_context_injection()
    print(
        json.dumps(
            build_self_directed_execution(context_injection),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
