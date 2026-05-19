#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.wiki_content_adjudication import build_adjudication_package
from scripts.wiki_review_decisions import (
    BUCKETS,
    build_review_decision_package,
    write_review_decision_record,
)


def _apply_limit(payload: dict, limit: int) -> None:
    bounded = max(0, limit)
    for bucket in BUCKETS:
        payload[bucket] = payload.get(bucket, [])[:bounded]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build wiki review decision package.")
    parser.add_argument("--root", default=ROOT)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--source-record", help="Source wiki-doctor record path to cite.")
    parser.add_argument(
        "--write-decision-record",
        action="store_true",
        help="Compatibility flag. Default behavior already writes a Markdown confirmation record.",
    )
    parser.add_argument(
        "--stdout-json-only",
        action="store_true",
        help="Emit the JSON review-decision package only and do not write a confirmation record.",
    )
    parser.add_argument(
        "--decision-record-dir",
        help="Directory for --write-decision-record output. Defaults to wiki/ops/wiki-review-decisions under --root.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    adjudication_package = build_adjudication_package(root)
    payload = build_review_decision_package(
        adjudication_package,
        source_record=args.source_record,
    )
    limit = max(0, args.limit)
    if args.stdout_json_only:
        preview_payload = copy.deepcopy(payload)
        _apply_limit(preview_payload, limit)
        print(json.dumps(preview_payload, ensure_ascii=False, indent=2))
        return

    record_path = write_review_decision_record(
        payload,
        root,
        output_dir=Path(args.decision_record_dir).resolve() if args.decision_record_dir else None,
        limit=None,
    )
    summary_payload = {
        "generated_at": payload.get("generated_at"),
        "mode": "wiki_review_decision_summary",
        "source_record": payload.get("source_record"),
        "decision_record_path": record_path.as_posix(),
        "preview_limit": limit,
        "summary": payload.get("summary", {}),
        "proof_boundary_notes": payload.get("proof_boundary_notes", []),
    }
    print(json.dumps(summary_payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
