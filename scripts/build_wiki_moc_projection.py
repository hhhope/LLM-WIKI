#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAPH_EXTRACTOR = ROOT / "scripts" / "extract_wiki_graph.py"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.wiki_moc_projection import apply_moc_plan, build_moc_plan


def load_graph(root: Path, graph_path: str | None) -> dict:
    if graph_path:
        return json.loads(Path(graph_path).read_text(encoding="utf-8"))
    completed = subprocess.run(
        [sys.executable, str(GRAPH_EXTRACTOR)],
        check=True,
        capture_output=True,
        text=True,
        cwd=root,
    )
    return json.loads(completed.stdout)


def main() -> None:
    parser = argparse.ArgumentParser(description="Preview or apply Obsidian MOC projection.")
    parser.add_argument("--root", default=ROOT)
    parser.add_argument("--graph", help="optional graph JSON path")
    parser.add_argument("--moc-dir", default="wiki/moc")
    parser.add_argument("--apply", action="store_true", help="write generated MOC blocks")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    graph = load_graph(root, args.graph)
    plan = (
        apply_moc_plan(root, graph, args.moc_dir)
        if args.apply
        else build_moc_plan(root, graph, args.moc_dir)
    )
    plan["generated_at"] = datetime.now(timezone.utc).isoformat()
    plan["mode"] = "apply" if args.apply else "dry-run"
    print(json.dumps(plan, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
