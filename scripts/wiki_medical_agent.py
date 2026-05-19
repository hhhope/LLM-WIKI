from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

from scripts.wiki_medical_case import (
    DEFAULT_MEDICAL_CASE_DIR,
    attach_recovery_result_to_case,
    load_medical_case_file,
    overwrite_medical_case_file,
)
from scripts.build_wiki_moc_projection import load_graph
from scripts.wiki_moc_projection import build_moc_plan
from scripts.wiki_recovery import build_recovery_package, write_recovery_record
from scripts.wiki_surgery import build_surgery_plan_from_case
from scripts.wiki_treatment import (
    apply_treatment_plan,
    load_case_and_build_treatment_plan,
    update_case_file_with_treatment_result,
    write_treatment_record,
)


@dataclass(frozen=True)
class IntentResult:
    intent: str
    expected_count: int | None = None
    reason: str = ""


@dataclass(frozen=True)
class ActiveCaseResolution:
    status: str
    case_path: Path | None = None
    case_package: dict[str, Any] | None = None
    candidates: tuple[Path, ...] = ()
    blocked_reason: str = ""


@dataclass(frozen=True)
class ActionValidation:
    allowed: bool
    intent: str
    state: str
    allowed_action: str = ""
    blocked_reason: str = ""
    executable_count: int = 0
    expected_count: int | None = None


READ_ONLY_INTENTS = {"status", "diagnose"}
MOC_SIGNALS = ("obsidian", "knowledge-map", "knowledge map", "图谱导航", "知识地图")
MOC_REVIEW_SIGNALS = (
    "preview",
    "review",
    "预览",
    "surgery",
    "手术",
    "分流",
    "审核",
    "审查",
    "复核",
)


def _has_moc_signal(lowered: str) -> bool:
    if re.search(r"\bmoc\b", lowered):
        return True
    return any(signal in lowered for signal in MOC_SIGNALS)


def _is_moc_surgery_preview_request(lowered: str) -> bool:
    has_moc = _has_moc_signal(lowered)
    has_review = any(signal in lowered for signal in MOC_REVIEW_SIGNALS)
    return has_moc and has_review


def classify_medical_intent(text: str) -> IntentResult:
    lowered = text.lower()
    count_match = re.search(r"(\d+)", text)
    expected_count = int(count_match.group(1)) if count_match else None
    if "legacy" in lowered or "debug" in lowered:
        return IntentResult("legacy_debug", expected_count, "explicit legacy/debug request")
    if _is_moc_surgery_preview_request(lowered):
        return IntentResult(
            "moc_surgery_preview",
            expected_count,
            "user requested MOC surgery preview",
        )
    if any(token in lowered for token in ["preview", "dry-run", "dry run", "预览"]):
        return IntentResult("treatment_preview", expected_count, "user requested treatment preview")
    if any(token in lowered for token in ["apply", "应用", "治疗这", "执行治疗"]):
        return IntentResult("treatment_apply", expected_count, "user requested treatment apply")
    if any(token in lowered for token in ["确认", "确诊", "confirmed decisions"]):
        return IntentResult("confirm_decisions", expected_count, "user referenced confirmed decisions")
    if any(token in lowered for token in ["诊断", "doctor"]):
        return IntentResult("diagnose", expected_count, "user requested diagnosis")
    if any(token in lowered for token in ["手术", "surgery"]):
        return IntentResult("surgery_plan", expected_count, "user requested surgery planning")
    if any(token in lowered for token in ["复查", "recovery", "闭环"]):
        return IntentResult("recovery", expected_count, "user requested recovery")
    if any(token in lowered for token in ["归档", "archive"]):
        return IntentResult("archive_check", expected_count, "user requested archive check")
    return IntentResult("status", expected_count, "default status request")


def _case_sort_key(path: Path) -> str:
    return path.name


def resolve_active_case(root: Path | str) -> ActiveCaseResolution:
    root_path = Path(root)
    case_dir = root_path / DEFAULT_MEDICAL_CASE_DIR
    if not case_dir.exists():
        return ActiveCaseResolution(status="no_case")
    candidates: list[Path] = []
    for path in sorted(case_dir.glob("*.md"), key=_case_sort_key):
        try:
            package = load_medical_case_file(path)
        except (OSError, ValueError):
            continue
        if package.get("active", True) is True and str(package.get("status", "")) != "closed":
            candidates.append(path.resolve())
    if not candidates:
        return ActiveCaseResolution(status="no_case")
    if len(candidates) > 1:
        return ActiveCaseResolution(
            status="blocked",
            candidates=tuple(candidates),
            blocked_reason="multiple_active_cases",
        )
    package = load_medical_case_file(candidates[0])
    package["case_path"] = candidates[0].as_posix()
    return ActiveCaseResolution(status="ok", case_path=candidates[0], case_package=package)


def _confirmed_treatment_decisions(case_package: dict[str, Any]) -> list[dict[str, Any]]:
    confirmed = case_package.get("confirmed_decisions", {})
    if not isinstance(confirmed, dict):
        return []
    values = confirmed.get("treatment_candidates", [])
    if not isinstance(values, list):
        return []
    return [item for item in values if isinstance(item, dict)]


def validate_case_action(
    case_package: dict[str, Any],
    intent: str,
    expected_count: int | None = None,
) -> ActionValidation:
    state = str(case_package.get("status", "awaiting_confirmation"))
    treatment_count = len(_confirmed_treatment_decisions(case_package))
    if intent == "status":
        return ActionValidation(
            True,
            intent,
            state,
            allowed_action="report_status",
            executable_count=treatment_count,
        )
    if intent == "diagnose":
        return ActionValidation(
            True,
            intent,
            state,
            allowed_action="run_diagnosis",
            executable_count=treatment_count,
        )
    if intent == "confirm_decisions":
        return ActionValidation(
            True,
            intent,
            state,
            allowed_action="record_confirmed_decisions",
            executable_count=treatment_count,
        )
    if intent == "moc_surgery_preview":
        return ActionValidation(
            True,
            intent,
            state,
            allowed_action="preview_moc_surgery_plan",
            executable_count=treatment_count,
        )
    if intent == "treatment_preview":
        if treatment_count == 0:
            return ActionValidation(
                False,
                intent,
                state,
                blocked_reason="no_executable_confirmed_treatment_decisions",
            )
        return ActionValidation(
            True,
            intent,
            state,
            allowed_action="preview_confirmed_treatments",
            executable_count=treatment_count,
        )
    if intent == "treatment_apply":
        if treatment_count == 0:
            return ActionValidation(
                False,
                intent,
                state,
                blocked_reason="no_executable_confirmed_treatment_decisions",
                executable_count=0,
                expected_count=expected_count,
            )
        if state not in {"ready_for_treatment", "treatment_previewed"}:
            return ActionValidation(
                False,
                intent,
                state,
                blocked_reason="state_does_not_allow_treatment_apply",
                executable_count=treatment_count,
                expected_count=expected_count,
            )
        if expected_count is not None and expected_count != treatment_count:
            return ActionValidation(
                False,
                intent,
                state,
                blocked_reason="confirmed_decision_count_mismatch",
                executable_count=treatment_count,
                expected_count=expected_count,
            )
        return ActionValidation(
            True,
            intent,
            state,
            allowed_action="apply_confirmed_treatments",
            executable_count=treatment_count,
            expected_count=expected_count,
        )
    if intent == "recovery":
        if state not in {"treatment_applied", "recovery_required"}:
            return ActionValidation(
                False,
                intent,
                state,
                blocked_reason="state_does_not_require_recovery",
                executable_count=treatment_count,
            )
        return ActionValidation(
            True,
            intent,
            state,
            allowed_action="run_recovery",
            executable_count=treatment_count,
        )
    if intent == "surgery_plan":
        return ActionValidation(
            True,
            intent,
            state,
            allowed_action="plan_surgery",
            executable_count=treatment_count,
        )
    if intent == "archive_check":
        return ActionValidation(
            True,
            intent,
            state,
            allowed_action="report_archive_readiness",
            executable_count=treatment_count,
        )
    return ActionValidation(
        False,
        intent,
        state,
        blocked_reason="unsupported_intent",
        executable_count=treatment_count,
    )


def validate_resolved_case_action(
    resolution: ActiveCaseResolution,
    intent: str,
    expected_count: int | None = None,
) -> ActionValidation:
    if resolution.status == "ok" and resolution.case_package is not None:
        return validate_case_action(resolution.case_package, intent, expected_count)
    if resolution.status == "no_case":
        if intent in READ_ONLY_INTENTS:
            return ActionValidation(
                True,
                intent,
                "no_case",
                allowed_action="report_status" if intent == "status" else "run_diagnosis",
                expected_count=expected_count,
            )
        return ActionValidation(
            False,
            intent,
            "no_case",
            blocked_reason="no_active_case",
            expected_count=expected_count,
        )
    if resolution.status == "blocked" and resolution.blocked_reason == "multiple_active_cases":
        if intent in READ_ONLY_INTENTS:
            return ActionValidation(
                True,
                intent,
                "multiple_active_cases",
                allowed_action="report_status" if intent == "status" else "run_diagnosis",
                expected_count=expected_count,
            )
        return ActionValidation(
            False,
            intent,
            "multiple_active_cases",
            blocked_reason="multiple_active_cases",
            expected_count=expected_count,
        )
    return ActionValidation(
        False,
        intent,
        resolution.status,
        blocked_reason=resolution.blocked_reason or "case_resolution_failed",
        expected_count=expected_count,
    )


def _sample_moc_items(plan: dict[str, Any], limit: int = 5) -> list[dict[str, Any]]:
    items = plan.get("moc_projection_items", [])
    if not isinstance(items, list):
        return []
    sample: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        sample.append(
            {
                "action": str(item.get("action", "")),
                "kind": str(item.get("kind", "")),
                "key": str(item.get("key", "")),
                "path": str(item.get("path", "")),
                "link_count": int(item.get("link_count", 0) or 0),
            }
        )
        if len(sample) >= limit:
            break
    return sample


def build_moc_surgery_preview_payload(
    root: Path | str,
    case_path: Path | str,
    moc_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    root_path = Path(root).resolve()
    case_file = Path(case_path).resolve()
    if root_path not in case_file.parents and case_file != root_path:
        raise ValueError("case path escapes root")
    case_package = load_medical_case_file(case_file)
    case_package["case_path"] = case_file.as_posix()
    if moc_plan is None:
        graph = load_graph(root_path, None)
        moc_plan = build_moc_plan(root_path, graph)
    surgery_plan = build_surgery_plan_from_case(case_package, moc_plan=moc_plan)
    moc_summary = dict(moc_plan.get("summary", {})) if isinstance(moc_plan, dict) else {}
    surgery_summary = surgery_plan.get("summary", {})
    moc_projection_count = 0
    if isinstance(surgery_summary, dict):
        moc_projection_count = int(surgery_summary.get("moc_projection_count", 0) or 0)
    return {
        "moc_projection": moc_summary,
        "surgery_preview": {
            "moc_projection_count": moc_projection_count,
            "sample_items": _sample_moc_items(surgery_plan),
        },
        "next_action": (
            "review_moc_surgery_preview"
            if moc_projection_count > 0
            else "moc_projection_clean"
        ),
    }


def build_status_payload(root: Path | str, intent_text: str) -> dict[str, Any]:
    intent = classify_medical_intent(intent_text)
    resolution = resolve_active_case(root)
    validation = validate_resolved_case_action(resolution, intent.intent, intent.expected_count)
    payload: dict[str, Any] = {
        "intent": intent.intent,
        "case_path": resolution.case_path.as_posix() if resolution.case_path else "",
        "state": validation.state,
        "allowed": validation.allowed,
        "allowed_action": validation.allowed_action,
        "blocked_reason": validation.blocked_reason,
        "next_action": validation.allowed_action or validation.blocked_reason,
    }
    if resolution.status == "no_case":
        payload["next_action"] = "diagnose"
    if resolution.status == "blocked":
        payload["candidate_cases"] = [path.as_posix() for path in resolution.candidates]
        payload["next_action"] = "select_active_case"
    if resolution.case_package is not None:
        archive = resolution.case_package.get("archive_next_action", {})
        next_action = archive.get("next_action") if isinstance(archive, dict) else ""
        payload["executable_count"] = validation.executable_count
        payload["expected_count"] = validation.expected_count
        if validation.allowed and intent.intent == "moc_surgery_preview" and resolution.case_path is not None:
            payload.update(build_moc_surgery_preview_payload(root, resolution.case_path))
        elif validation.allowed and next_action:
            payload["next_action"] = str(next_action)
    return payload


def apply_confirmed_treatment_and_recover(
    root: Path | str,
    case_path: Path | str,
    approved_domains: set[str] | None = None,
    approved_detail_refs: set[str] | None = None,
) -> dict[str, Any]:
    root_path = Path(root).resolve()
    case_file = Path(case_path).resolve()
    if root_path not in case_file.parents and case_file != root_path:
        raise ValueError("case path escapes root")
    if not (approved_domains or approved_detail_refs):
        raise ValueError("missing explicit treatment approval")
    resolution = resolve_active_case(root_path)
    if resolution.status != "ok" or resolution.case_path is None or resolution.case_package is None:
        raise ValueError(resolution.blocked_reason or resolution.status)
    if resolution.case_path.resolve() != case_file:
        raise ValueError("supplied case path is not the active case")
    validation = validate_case_action(resolution.case_package, "treatment_apply")
    if not validation.allowed:
        raise ValueError(validation.blocked_reason or "treatment_apply_not_allowed")
    plan = load_case_and_build_treatment_plan(
        case_file,
        approved_domains=approved_domains or set(),
        approved_detail_refs=approved_detail_refs or set(),
    )
    result = apply_treatment_plan(root_path, plan, apply=True)
    treatment_record = write_treatment_record(plan, result, root_path)
    update_case_file_with_treatment_result(
        case_file,
        plan,
        result,
        root_path,
        treatment_record=treatment_record.as_posix(),
    )
    if result["summary"]["blocked_count"] > 0:
        case_package = load_medical_case_file(case_file)
        case_package["status"] = "blocked"
        case_package["archive_next_action"] = {
            "status": "blocked",
            "next_action": "blocked",
            "reason": "treatment blocked results must be resolved before recovery.",
        }
        overwrite_medical_case_file(case_file, case_package, root_path)
        return {
            "applied": result["summary"]["applied_count"],
            "blocked": result["summary"]["blocked_count"],
            "treatment_record": treatment_record.as_posix(),
            "next_action": "blocked",
        }
    recovery = build_recovery_package(
        root_path,
        frontmatter_targets=[
            str(item.get("path", ""))
            for item in plan.get("treatment_items", [])
            if isinstance(item, dict) and str(item.get("path", "")).strip()
        ],
    )
    recovery_record = write_recovery_record(recovery, root_path)
    case_package = load_medical_case_file(case_file)
    updated_case = attach_recovery_result_to_case(
        case_package,
        recovery,
        recovery_record=recovery_record.as_posix(),
    )
    overwrite_medical_case_file(case_file, updated_case, root_path)
    next_action = updated_case.get("archive_next_action", {}).get("next_action", "")
    return {
        "applied": result["summary"]["applied_count"],
        "blocked": result["summary"]["blocked_count"],
        "treatment_record": treatment_record.as_posix(),
        "recovery": {
            "status": updated_case["recovery"]["status"],
            "record": recovery_record.as_posix(),
            "passed": recovery.get("passed", False),
        },
        "next_action": next_action,
    }
