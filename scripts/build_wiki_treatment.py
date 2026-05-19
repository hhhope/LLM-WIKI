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
from scripts.wiki_treatment import (
    apply_treatment_plan,
    build_treatment_plan,
    load_case_and_build_treatment_plan,
    update_case_file_with_treatment_result,
    write_treatment_record,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build or apply wiki treatment plan.")
    parser.add_argument("--root", default=ROOT)
    parser.add_argument("--case-file", help="Canonical wiki medical case file to use as treatment input.")
    parser.add_argument(
        "--update-case-file",
        action="store_true",
        help="Write the generated treatment result back into --case-file.",
    )
    parser.add_argument("--approved-domain", action="append", default=[])
    parser.add_argument("--approved-detail", action="append", default=[])
    parser.add_argument("--apply", action="store_true", help="Apply approved frontmatter treatment.")
    parser.add_argument(
        "--legacy-preview",
        action="store_true",
        help="Allow raw adjudication treatment preview without --case-file. Evidence only; not authoritative.",
    )
    parser.add_argument(
        "--write-treatment-record",
        action="store_true",
        help="Write Markdown treatment record. Default behavior is stdout JSON only.",
    )
    parser.add_argument(
        "--treatment-record-dir",
        help="Directory for --write-treatment-record output. Defaults to wiki/ops/wiki-treatment-runs under --root.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if args.apply and not args.case_file:
        parser.error("--apply requires --case-file")
    if args.update_case_file and not args.case_file:
        parser.error("--update-case-file requires --case-file")
    if not args.case_file and not args.legacy_preview:
        parser.error("raw treatment preview without --case-file requires --legacy-preview")

    if args.case_file:
        plan = load_case_and_build_treatment_plan(
            args.case_file,
            approved_domains=set(args.approved_domain),
            approved_detail_refs=set(args.approved_detail),
        )
    else:
        adjudication_package = build_adjudication_package(root)
        plan = build_treatment_plan(
            adjudication_package,
            approved_domains=set(args.approved_domain),
            approved_detail_refs=set(args.approved_detail),
        )
    result = apply_treatment_plan(root, plan, apply=args.apply)
    legacy_preview = args.legacy_preview and not args.case_file
    payload = {"applied": args.apply, "legacy_preview": legacy_preview, "plan": plan, "result": result}
    if legacy_preview:
        payload["authority"] = "legacy_debug_evidence_only"
    record_path = None

    if args.write_treatment_record:
        record_path = write_treatment_record(
            plan,
            result,
            root,
            output_dir=Path(args.treatment_record_dir).resolve() if args.treatment_record_dir else None,
        )
        payload["treatment_record_path"] = record_path.as_posix()

    if args.update_case_file:
        updated_path = update_case_file_with_treatment_result(
            args.case_file,
            plan,
            result,
            root,
            treatment_record=record_path.as_posix() if record_path else None,
        )
        payload["updated_case_file"] = updated_path.as_posix()

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
