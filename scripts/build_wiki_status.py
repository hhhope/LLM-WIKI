#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_wiki_frontmatter import build_report as build_taxonomy_report
from scripts.extract_wiki_graph import RELATION_FIELDS as GRAPH_RELATION_FIELDS
from scripts.extract_wiki_graph import collect_pages as collect_graph_pages
from scripts.extract_wiki_graph import normalize_relation_value, parse_frontmatter
from scripts.wiki_content_adjudication import build_adjudication_health
from scripts.wiki_content_enrichment import build_enrichment_health
from scripts.wiki_moc_projection import build_moc_health
from scripts.wiki_product_status import build_product_status, relation_fields_from_meta
from scripts.wiki_status_render import render_status_markdown


DEFAULT_OUTPUT_DIR = Path("wiki/status")
GENERATED_STATUS_DIR = "wiki/status/"
TASK_PATTERN = re.compile(r"^\s*-\s+\[(?P<mark>[ xX])\]\s+")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _wiki_section(rel_path: str) -> str:
    parts = rel_path.split("/")
    if len(parts) >= 3:
        return "/".join(parts[:2])
    if len(parts) == 2:
        return "wiki/root"
    return "wiki"


def _normal_source_path(value: object) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    path = value.strip()
    if path.startswith("inbox/"):
        return path
    return f"inbox/{path}"


def _raw_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return ""
    return parts[0].removeprefix("---\n")


def _raw_has_frontmatter_field(raw_meta: str, field: str) -> bool:
    return bool(re.search(rf"(?m)^{re.escape(field)}\s*:", raw_meta))


def _collect_wiki_pages(root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    wiki_dir = root / "wiki"
    pages: list[dict[str, Any]] = []
    source_records: list[dict[str, Any]] = []
    if not wiki_dir.exists():
        return pages, source_records

    for path in sorted(wiki_dir.rglob("*.md")):
        rel = _relative(path, root)
        if rel.startswith(GENERATED_STATUS_DIR):
            continue
        text = path.read_text(encoding="utf-8")
        meta, _body = parse_frontmatter(text)
        record = {
            "path": rel,
            "section": _wiki_section(rel),
            "sha256": _sha256(path),
            "bytes": path.stat().st_size,
            "title": meta.get("title"),
            "domain": meta.get("domain"),
            "canonical_object": meta.get("canonical_object"),
            "artifact_type": meta.get("artifact_type"),
            "status": meta.get("status"),
            **relation_fields_from_meta(meta),
        }
        pages.append(record)

        if rel.startswith("wiki/sources/") and path.name != "index.md":
            source_records.append(
                {
                    "path": rel,
                    "source_path": _normal_source_path(meta.get("source_path")),
                    "source_type": meta.get("source_type"),
                    "domain": meta.get("domain"),
                    "status": meta.get("status"),
                }
            )

    return pages, source_records


def _collect_inbox_files(root: Path, source_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    inbox_dir = root / "inbox"
    represented_paths = {
        record["source_path"]
        for record in source_records
        if isinstance(record.get("source_path"), str)
    }
    inbox_files: list[dict[str, Any]] = []
    if not inbox_dir.exists():
        return inbox_files

    for path in sorted(item for item in inbox_dir.rglob("*") if item.is_file()):
        if path.name.lower() == "readme.md":
            continue
        rel = _relative(path, root)
        inbox_files.append(
            {
                "path": rel,
                "sha256": _sha256(path),
                "bytes": path.stat().st_size,
                "represented_by_source": rel in represented_paths,
            }
        )
    return inbox_files


def _parse_task_counts(tasks_path: Path) -> tuple[int, int]:
    done = 0
    open_count = 0
    for line in tasks_path.read_text(encoding="utf-8").splitlines():
        match = TASK_PATTERN.match(line)
        if not match:
            continue
        if match.group("mark").lower() == "x":
            done += 1
        else:
            open_count += 1
    return done, open_count


def _collect_openspec_changes(root: Path) -> list[dict[str, Any]]:
    changes_dir = root / "openspec" / "changes"
    changes: list[dict[str, Any]] = []
    if not changes_dir.exists():
        return changes

    for tasks_path in sorted(changes_dir.glob("*/tasks.md")):
        change_id = tasks_path.parent.name
        if change_id == "archive":
            continue
        done, open_count = _parse_task_counts(tasks_path)
        total = done + open_count
        state = "complete" if total > 0 and open_count == 0 else "active"
        changes.append(
            {
                "change_id": change_id,
                "state": state,
                "done_tasks": done,
                "open_tasks": open_count,
                "total_tasks": total,
                "tasks_path": _relative(tasks_path, root),
            }
        )
    return changes


def _collect_domain_taxonomy_health(root: Path) -> dict[str, Any]:
    config_path = root / "wiki" / "config" / "frontmatter-taxonomy.yaml"
    if not config_path.exists():
        return {
            "status": "unavailable",
            "config_path": "wiki/config/frontmatter-taxonomy.yaml",
            "summary": {"error": 0, "warn": 0, "info": 0, "total": 0},
            "entries": [],
        }

    report = build_taxonomy_report(root)
    entries = report.get("entries", [])
    return {
        "status": "pass" if report["summary"].get("total", 0) == 0 else "drift",
        "config_path": report["config_path"],
        "taxonomy_version": report.get("taxonomy_version"),
        "summary": report["summary"],
        "strict_gate": report.get("strict_gate", {}),
        "scorecard": report.get("scorecard", {}),
        "entries": entries[:10],
    }


def _collect_graph_parse_health(root: Path) -> dict[str, Any]:
    wiki_dir = root / "wiki"
    entries: list[dict[str, Any]] = []
    if not wiki_dir.exists():
        return {"status": "pass", "summary": {"total": 0}, "entries": []}

    for path in sorted(wiki_dir.rglob("*.md")):
        rel = _relative(path, root)
        if rel.startswith(GENERATED_STATUS_DIR):
            continue
        text = path.read_text(encoding="utf-8")
        raw_meta = _raw_frontmatter(text)
        if not raw_meta:
            continue
        meta, _body = parse_frontmatter(text)
        empty_raw_relation_fields = [
            field
            for field in GRAPH_RELATION_FIELDS
            if _raw_has_frontmatter_field(raw_meta, field)
            and not normalize_relation_value(meta.get(field))
        ]
        if not empty_raw_relation_fields:
            continue
        entries.append(
            {
                "type": "graph_parse_health",
                "path": rel,
                "fields": empty_raw_relation_fields,
                "problem": "raw relation frontmatter exists, but parsed relation value is empty",
                "repair_route": "runtime-parser-fix",
            }
        )

    return {
        "status": "pass" if not entries else "drift",
        "summary": {"total": len(entries)},
        "entries": entries[:10],
    }


def _moc_projection_graph(root: Path) -> dict[str, Any]:
    nodes, edges, warnings = collect_graph_pages(root)
    return {
        "summary": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "warning_count": len(warnings),
        },
        "nodes": nodes,
        "edges": edges,
        "warnings": warnings,
    }


def build_manifest(root: Path | str) -> dict[str, Any]:
    root_path = Path(root).resolve()
    pages, source_records = _collect_wiki_pages(root_path)
    inbox_files = _collect_inbox_files(root_path, source_records)
    changes = _collect_openspec_changes(root_path)
    section_counts = Counter(page["section"] for page in pages)
    pending_inbox_files = [
        item["path"]
        for item in inbox_files
        if not item["represented_by_source"]
    ]
    active_changes = [item for item in changes if item["state"] == "active"]
    complete_changes = [item for item in changes if item["state"] == "complete"]
    product_status = build_product_status(pages, inbox_files, changes)
    domain_taxonomy_health = _collect_domain_taxonomy_health(root_path)
    graph_parse_health = _collect_graph_parse_health(root_path)
    content_enrichment_health = build_enrichment_health(root_path)
    content_adjudication_health = build_adjudication_health(root_path)
    moc_projection_health = build_moc_health(root_path, _moc_projection_graph(root_path))

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": root_path.as_posix(),
        "summary": {
            "wiki_page_count": len(pages),
            "source_record_count": len(source_records),
            "inbox_file_count": len(inbox_files),
            "pending_inbox_count": len(pending_inbox_files),
            "active_change_count": len(active_changes),
            "complete_change_count": len(complete_changes),
            "wiki_sections": dict(sorted(section_counts.items())),
        },
        "wiki_pages": pages,
        "source_records": source_records,
        "inbox_files": inbox_files,
        "pending_inbox_files": pending_inbox_files,
        "openspec_changes": changes,
        "product_status": product_status,
        "domain_taxonomy_health": domain_taxonomy_health,
        "graph_parse_health": graph_parse_health,
        "content_enrichment_health": content_enrichment_health,
        "content_adjudication_health": content_adjudication_health,
        "moc_projection_health": moc_projection_health,
    }


def write_status_outputs(root: Path | str, output_dir: Path | str = DEFAULT_OUTPUT_DIR) -> tuple[Path, Path]:
    root_path = Path(root).resolve()
    output_path = Path(output_dir)
    if not output_path.is_absolute():
        output_path = root_path / output_path
    output_path.mkdir(parents=True, exist_ok=True)

    manifest = build_manifest(root_path)
    manifest_path = output_path / "manifest.json"
    status_path = output_path / "wiki-status.md"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    status_path.write_text(render_status_markdown(manifest), encoding="utf-8")
    return manifest_path, status_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Build wiki manifest and status report.")
    parser.add_argument("--root", default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    manifest_path, status_path = write_status_outputs(Path(args.root), Path(args.output_dir))
    print(f"Wrote {manifest_path}")
    print(f"Wrote {status_path}")


if __name__ == "__main__":
    main()
