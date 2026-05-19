#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.wiki_medical_agent import build_status_payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the wiki medical agent state controller.")
    parser.add_argument("--root", default=ROOT)
    parser.add_argument("--intent-text", required=True, help="Natural-language user intent to route.")
    parser.add_argument("--approved-domain", action="append", default=[])
    parser.add_argument("--approved-detail", action="append", default=[])
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    payload = build_status_payload(Path(args.root).resolve(), args.intent_text)
    if payload["intent"] == "treatment_apply" and args.apply and payload.get("allowed"):
        if not args.approved_domain and not args.approved_detail:
            payload.update(
                {
                    "allowed": False,
                    "blocked_reason": "missing_explicit_treatment_approval",
                    "next_action": "missing_explicit_treatment_approval",
                }
            )
        else:
            from scripts.wiki_medical_agent import apply_confirmed_treatment_and_recover

            result = apply_confirmed_treatment_and_recover(
                Path(args.root).resolve(),
                payload["case_path"],
                approved_domains=set(args.approved_domain),
                approved_detail_refs=set(args.approved_detail),
            )
            payload.update(result)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
