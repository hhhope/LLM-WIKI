from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


DEFAULT_RECOVERY_RECORD_DIR = Path("wiki/ops/wiki-recovery-runs")
CommandRunner = Callable[[list[str], Path], tuple[int, str, str]]


def default_recovery_checks(root: Path | str) -> list[dict[str, Any]]:
    root_path = Path(root)
    tmp_prefix = Path("/tmp")
    return [
        {
            "check_id": "frontmatter_precheck",
            "command": [
                sys.executable,
                "scripts/wiki_gate_precheck.py",
                "--root",
                str(root_path),
                "--mode",
                "frontmatter",
                "--full-json-output",
                str(tmp_prefix / "wiki-recovery-frontmatter.json"),
                "--full-markdown-output",
                str(tmp_prefix / "wiki-recovery-frontmatter.md"),
            ],
        },
        {
            "check_id": "doctor_adjudication",
            "command": [
                sys.executable,
                "scripts/build_wiki_content_adjudication.py",
                "--root",
                str(root_path),
                "--limit",
                "0",
            ],
        },
        {
            "check_id": "review_decisions",
            "command": [
                sys.executable,
                "scripts/build_wiki_review_decisions.py",
                "--root",
                str(root_path),
                "--limit",
                "0",
            ],
        },
        {
            "check_id": "surgery_plan",
            "command": [
                sys.executable,
                "scripts/build_wiki_surgery.py",
                "--root",
                str(root_path),
            ],
        },
    ]


def _run_subprocess(command: list[str], cwd: Path) -> tuple[int, str, str]:
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    return completed.returncode, completed.stdout, completed.stderr


def _tail(text: str, limit: int = 1200) -> str:
    if len(text) <= limit:
        return text
    return text[-limit:]


def _parse_stdout_summary(stdout: str) -> dict[str, Any]:
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        return {}
    if not isinstance(payload, dict):
        return {}
    summary: dict[str, Any] = {}
    if isinstance(payload.get("summary"), dict):
        summary.update(payload["summary"])
    for key in ("status", "mode", "passed", "applied"):
        if key in payload:
            summary[key] = payload[key]
    eval_result = payload.get("eval_result")
    if isinstance(eval_result, dict):
        summary["eval_passed"] = eval_result.get("passed")
        summary["eval_error_count"] = len(eval_result.get("errors", []))
        summary["eval_warning_count"] = len(eval_result.get("warnings", []))
    return summary


def build_recovery_package(
    root: Path | str,
    checks: list[dict[str, Any]] | None = None,
    runner: CommandRunner | None = None,
    frontmatter_targets: list[str] | None = None,
) -> dict[str, Any]:
    root_path = Path(root).resolve()
    run = runner or _run_subprocess
    selected_checks = checks if checks is not None else default_recovery_checks(root_path)
    results: list[dict[str, Any]] = []

    for check in selected_checks:
        command = [str(part) for part in check.get("command", [])]
        exit_code, stdout, stderr = run(command, root_path)
        results.append(
            {
                "check_id": str(check.get("check_id", "unknown")),
                "command": command,
                "exit_code": int(exit_code),
                "passed": int(exit_code) == 0,
                "parsed_summary": _parse_stdout_summary(stdout),
                "stdout_tail": _tail(stdout),
                "stderr_tail": _tail(stderr),
            }
        )

    failed = [item for item in results if not item["passed"]]
    passed = not failed
    frontmatter_status = _build_frontmatter_status(
        root_path,
        results,
        frontmatter_targets or [],
        run,
    )
    if frontmatter_status and frontmatter_status["targets_passed"] and not frontmatter_status["repository"]["passed"]:
        next_route = "blocked_by_repository_frontmatter_debt"
    elif passed:
        next_route = "archive-ready"
    else:
        next_route = "blocked_by_recovery_findings"
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "wiki_recovery_package",
        "passed": passed,
        "next_route": next_route,
        "summary": {
            "check_count": len(results),
            "passed_count": len(results) - len(failed),
            "failed_count": len(failed),
        },
        "checks": results,
        **({"frontmatter_status": frontmatter_status} if frontmatter_status else {}),
        "proof_boundary_notes": [
            "Recovery records check results only.",
            "It does not apply treatment or surgery.",
            "It does not write frontmatter, taxonomy config, relations, MOC pages, ADR decisions, status files, or OpenSpec state.",
            "Nonzero checks are preserved as findings instead of hidden.",
        ],
    }


def _target_precheck_command(root_path: Path, target: str) -> list[str]:
    return [
        sys.executable,
        "scripts/wiki_gate_precheck.py",
        "--root",
        str(root_path),
        "--mode",
        "frontmatter",
        "--target",
        target,
        "--full-json-output",
        str(Path("/tmp") / "wiki-recovery-target-frontmatter.json"),
        "--full-markdown-output",
        str(Path("/tmp") / "wiki-recovery-target-frontmatter.md"),
    ]


def _target_status_from_stdout(path: str, stdout: str, exit_code: int) -> dict[str, Any]:
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        payload = {}
    target = payload.get("target", {}) if isinstance(payload, dict) else {}
    if not isinstance(target, dict):
        target = {}
    entry_count = int(target.get("entry_count", 0) or 0)
    return {
        "path": str(target.get("path") or path),
        "passed": entry_count == 0,
        "entry_count": entry_count,
        "exit_code": int(exit_code),
    }


def _build_frontmatter_status(
    root_path: Path,
    check_results: list[dict[str, Any]],
    targets: list[str],
    runner: CommandRunner,
) -> dict[str, Any] | None:
    frontmatter_check = next(
        (item for item in check_results if item.get("check_id") == "frontmatter_precheck"),
        None,
    )
    if frontmatter_check is None and not targets:
        return None
    target_rows = []
    for target in targets:
        command = _target_precheck_command(root_path, str(target))
        exit_code, stdout, _stderr = runner(command, root_path)
        target_rows.append(_target_status_from_stdout(str(target), stdout, exit_code))
    repository_summary = (
        frontmatter_check.get("parsed_summary", {}) if isinstance(frontmatter_check, dict) else {}
    )
    repository_passed = bool(frontmatter_check.get("passed", False)) if isinstance(frontmatter_check, dict) else False
    return {
        "repository": {
            "passed": repository_passed,
            "summary": repository_summary if isinstance(repository_summary, dict) else {},
        },
        "targets_passed": all(item["passed"] for item in target_rows) if target_rows else False,
        "targets": target_rows,
    }


def _timestamp_slug(timestamp: datetime | str | None) -> str:
    if timestamp is None:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
    if isinstance(timestamp, datetime):
        return timestamp.astimezone(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return timestamp
    return parsed.astimezone(timezone.utc).strftime("%Y-%m-%d-%H%M%S")


def next_recovery_record_path(output_dir: Path, timestamp: datetime | str | None = None) -> Path:
    slug = _timestamp_slug(timestamp)
    base = output_dir / f"{slug}-recovery.md"
    if not base.exists():
        return base
    counter = 2
    while True:
        candidate = output_dir / f"{slug}-recovery-{counter}.md"
        if not candidate.exists():
            return candidate
        counter += 1


def render_recovery_record_markdown(package: dict[str, Any], scan_root: Path | str) -> str:
    lines = [
        "# wiki-recovery Record",
        "",
        "## Source",
        f"- Generated at: {package.get('generated_at', 'unknown')}",
        f"- Scan root: `{Path(scan_root)}`",
        f"- Passed: {package.get('passed', False)}",
        f"- Next route: {package.get('next_route', 'unknown')}",
        "",
        "## Summary",
    ]
    for key, value in sorted(package.get("summary", {}).items()):
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Check Results"])
    checks = package.get("checks", [])
    if not checks:
        lines.append("- None")
    for check in checks:
        if not isinstance(check, dict):
            continue
        command = " ".join(str(part) for part in check.get("command", []))
        lines.append(
            f"- {check.get('check_id', 'unknown')}: exit={check.get('exit_code')} "
            f"passed={check.get('passed')} command=`{command}`"
        )
        summary = check.get("parsed_summary", {})
        if isinstance(summary, dict) and summary:
            lines.append(f"  - summary: `{json.dumps(summary, ensure_ascii=False, sort_keys=True)}`")

    frontmatter_status = package.get("frontmatter_status", {})
    if isinstance(frontmatter_status, dict):
        repository = frontmatter_status.get("repository", {})
        lines.extend(["", "## Frontmatter Status"])
        if isinstance(repository, dict):
            lines.append(f"- Repository passed: {repository.get('passed', False)}")
            summary = repository.get("summary", {})
            if isinstance(summary, dict) and summary:
                lines.append(f"- Repository summary: `{json.dumps(summary, ensure_ascii=False, sort_keys=True)}`")
        lines.append(f"- Targets passed: {frontmatter_status.get('targets_passed', False)}")
        targets = frontmatter_status.get("targets", [])
        if isinstance(targets, list) and targets:
            for target in targets:
                if not isinstance(target, dict):
                    continue
                lines.append(
                    f"  - `{target.get('path', '')}` passed={target.get('passed', False)} "
                    f"entry_count={target.get('entry_count', 0)}"
                )

    lines.extend(["", "## Proof Boundary"])
    for note in package.get("proof_boundary_notes", []):
        lines.append(f"- {note}")
    return "\n".join(lines) + "\n"


def write_recovery_record(
    package: dict[str, Any],
    root: Path | str,
    output_dir: Path | str | None = None,
    timestamp: datetime | str | None = None,
) -> Path:
    root_path = Path(root)
    target_dir = Path(output_dir) if output_dir is not None else root_path / DEFAULT_RECOVERY_RECORD_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    markdown = render_recovery_record_markdown(package, scan_root=root_path)
    while True:
        target = next_recovery_record_path(target_dir, timestamp=timestamp)
        try:
            with target.open("x", encoding="utf-8") as handle:
                handle.write(markdown)
            return target.resolve()
        except FileExistsError:
            continue
