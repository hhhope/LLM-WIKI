#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.wiki_content_adjudication import build_adjudication_package
from scripts.wiki_surgery import (
    build_surgery_plan,
    load_case_and_build_surgery_plan,
    update_case_file_with_surgery_plan,
    write_surgery_record,
)


def _load_moc_plan(path: str | None) -> dict | None:
    if not path:
        return None
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Build wiki surgery plan.")
    parser.add_argument("--root", default=ROOT)
    parser.add_argument("--moc-plan", help="Optional MOC projection dry-run JSON.")
    parser.add_argument("--case-file", help="Canonical wiki medical case file to use as surgery input.")
    parser.add_argument(
        "--update-case-file",
        action="store_true",
        help="Write the generated surgery plan back into --case-file.",
    )
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument(
        "--write-surgery-record",
        action="store_true",
        help="Write Markdown surgery plan record. Default behavior is stdout JSON only.",
    )
    parser.add_argument(
        "--surgery-record-dir",
        help="Directory for --write-surgery-record output. Defaults to wiki/ops/wiki-surgery-runs under --root.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    moc_plan = _load_moc_plan(args.moc_plan)
    if args.case_file:
        plan = load_case_and_build_surgery_plan(args.case_file, moc_plan=moc_plan)
    else:
        plan = build_surgery_plan(
            build_adjudication_package(root),
            moc_plan=moc_plan,
        )
    payload = dict(plan)
    record_path = None

    if args.write_surgery_record:
        record_path = write_surgery_record(
            plan,
            root,
            output_dir=Path(args.surgery_record_dir).resolve() if args.surgery_record_dir else None,
            limit=max(0, args.limit),
        )
        payload["surgery_record_path"] = record_path.as_posix()

    if args.update_case_file:
        if not args.case_file:
            parser.error("--update-case-file requires --case-file")
        updated_path = update_case_file_with_surgery_plan(
            args.case_file,
            plan,
            root,
            surgery_record=record_path.as_posix() if record_path else None,
        )
        payload["updated_case_file"] = updated_path.as_posix()

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
