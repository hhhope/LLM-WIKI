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
from scripts.wiki_medical_case import build_medical_case_package, write_medical_case_file
from scripts.wiki_review_decisions import build_review_decision_package, load_review_decision_record


def main() -> None:
    parser = argparse.ArgumentParser(description="Build canonical wiki medical case file.")
    parser.add_argument("--root", default=ROOT)
    parser.add_argument("--case-slug")
    parser.add_argument("--source-record")
    parser.add_argument("--confirm-record")
    parser.add_argument(
        "--stdout-json-only",
        action="store_true",
        help="Print case package only and do not write a case file.",
    )
    parser.add_argument(
        "--case-record-dir",
        help="Directory for case file output. Defaults to wiki/ops/wiki-medical-cases under --root.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if args.confirm_record:
        decision_package = load_review_decision_record(args.confirm_record)
    else:
        decision_package = build_review_decision_package(build_adjudication_package(root))
    if args.source_record:
        decision_package["source_record"] = args.source_record
    package = build_medical_case_package(
        decision_package,
        case_slug=args.case_slug,
        confirm_record=args.confirm_record,
    )
    payload = dict(package)

    if not args.stdout_json_only:
        case_path = write_medical_case_file(
            package,
            root,
            output_dir=Path(args.case_record_dir).resolve() if args.case_record_dir else None,
        )
        payload["medical_case_path"] = case_path.as_posix()

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
