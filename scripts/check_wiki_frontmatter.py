#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = Path("wiki/config/frontmatter-taxonomy.yaml")

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.extract_wiki_graph import parse_frontmatter


@dataclass(frozen=True)
class DriftEntry:
    kind: str
    severity: str
    path: str
    message: str
    field: str | None = None
    value: str | None = None
    dimension: str | None = None


def load_taxonomy(root: Path | str = ROOT) -> dict[str, Any]:
    root_path = Path(root)
    config_file = root_path / CONFIG_PATH
    with config_file.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"taxonomy config must be a mapping: {config_file}")
    return data


def severity(config: dict[str, Any], kind: str, default: str = "warn") -> str:
    value = config.get("severity", {}).get(kind, default)
    return str(value)


def rel_path(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def is_under(rel: str, prefix: str) -> bool:
    normalized = prefix.rstrip("/") + "/"
    return rel.startswith(normalized)


def matches_path_glob(rel: str, pattern: str) -> bool:
    if fnmatch.fnmatch(rel, pattern):
        return True
    if "/**/" in pattern:
        direct_pattern = pattern.replace("/**/", "/")
        return fnmatch.fnmatch(rel, direct_pattern)
    return False


def dimension_for_field(field: str) -> str:
    if field in {"canonical_object", "artifact_type"}:
        return "identity_coverage"
    if field in {"related_objects", "derived_from", "validates", "formalizes"}:
        return "relation_shape"
    return "completeness"


def check_content_drift(root: Path | str, config: dict[str, Any]) -> list[DriftEntry]:
    root_path = Path(root)
    wiki_dir = root_path / "wiki"
    if not wiki_dir.exists():
        return []

    forbidden_domains = set(config.get("fields", {}).get("domain", {}).get("forbidden", []))
    known_domains = set(config.get("fields", {}).get("domain", {}).get("known", []))
    sample_paths = set(config.get("sample_migration_paths", []))
    entries: list[DriftEntry] = []

    for path in sorted(wiki_dir.rglob("*.md")):
        rel = rel_path(path, root_path)
        text = path.read_text(encoding="utf-8")
        meta, _body = parse_frontmatter(text)
        domain = meta.get("domain")
        layer = meta.get("layer")
        ops_area = meta.get("ops_area")

        if isinstance(domain, str) and domain in forbidden_domains:
            entries.append(
                DriftEntry(
                    kind="forbidden_domain",
                    severity=severity(config, "forbidden_domain", "error"),
                    path=rel,
                    field="domain",
                    value=domain,
                    dimension="taxonomy_validity",
                    message=f"`domain: {domain}` is forbidden by taxonomy contract.",
                )
            )

        if (
            isinstance(domain, str)
            and domain not in known_domains
            and domain not in forbidden_domains
            and rel in sample_paths
        ):
            entries.append(
                DriftEntry(
                    kind="unknown_domain",
                    severity=severity(config, "unknown_domain", "warn"),
                    path=rel,
                    field="domain",
                    value=domain,
                    dimension="taxonomy_validity",
                    message=f"`domain: {domain}` is not listed in taxonomy known domains.",
                )
            )

        if domain == "unclassified" and meta.get("classification_needed") != "true":
            entries.append(
                DriftEntry(
                    kind="unclassified_without_flag",
                    severity=severity(config, "unclassified_without_flag", "error"),
                    path=rel,
                    field="classification_needed",
                    value=str(meta.get("classification_needed")),
                    dimension="taxonomy_validity",
                    message="`domain: unclassified` requires `classification_needed: true`.",
                )
            )

        if is_under(rel, "wiki/ops") and rel in sample_paths:
            if not domain:
                entries.append(
                    DriftEntry(
                        kind="missing_domain_on_sample_ops_page",
                        severity=severity(config, "missing_domain_on_sample_ops_page", "error"),
                        path=rel,
                        field="domain",
                        value=None,
                        dimension="completeness",
                        message="Sample migration ops page must declare `domain`.",
                    )
                )
            if not ops_area:
                entries.append(
                    DriftEntry(
                        kind="missing_ops_area_on_ops_page",
                        severity=severity(config, "missing_ops_area_on_ops_page", "error"),
                        path=rel,
                        field="ops_area",
                        value=None,
                        dimension="completeness",
                        message="Sample migration ops page must declare `ops_area`.",
                    )
                )
            if layer != "ops":
                entries.append(
                    DriftEntry(
                        kind="missing_layer_on_legacy_page",
                        severity=severity(config, "missing_layer_on_legacy_page", "warn"),
                        path=rel,
                        field="layer",
                        value=str(layer),
                        dimension="completeness",
                        message="Sample migration ops page should declare `layer: ops`.",
                    )
                )

    return entries


def iter_strict_rule_sets(config: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    strict_gate = config.get("strict_gate", {})
    if not strict_gate.get("enabled", False):
        return []
    rule_sets = strict_gate.get("rule_sets", {})
    if not isinstance(rule_sets, dict):
        return []
    return [
        (str(rule_name), rule)
        for rule_name, rule in rule_sets.items()
        if isinstance(rule, dict)
    ]


def matching_rule_sets(rel: str, config: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    matches: list[tuple[str, dict[str, Any]]] = []
    for rule_name, rule in iter_strict_rule_sets(config):
        path_globs = rule.get("path_globs", [])
        if isinstance(path_globs, str):
            path_globs = [path_globs]
        if any(matches_path_glob(rel, str(pattern)) for pattern in path_globs):
            matches.append((rule_name, rule))
    return matches


def check_strict_gate_drift(root: Path | str, config: dict[str, Any]) -> list[DriftEntry]:
    root_path = Path(root)
    wiki_dir = root_path / "wiki"
    if not wiki_dir.exists() or not iter_strict_rule_sets(config):
        return []

    entries: list[DriftEntry] = []
    required_severity = severity(config, "missing_required_field", "error")
    expected_severity = severity(config, "unexpected_field_value", "error")

    for path in sorted(wiki_dir.rglob("*.md")):
        rel = rel_path(path, root_path)
        text = path.read_text(encoding="utf-8")
        meta, _body = parse_frontmatter(text)
        for rule_name, rule in matching_rule_sets(rel, config):
            for field in rule.get("required", []):
                field_name = str(field)
                value = meta.get(field_name)
                if value:
                    continue
                entries.append(
                    DriftEntry(
                        kind="missing_required_field",
                        severity=required_severity,
                        path=rel,
                        field=field_name,
                        value=None,
                        dimension=dimension_for_field(field_name),
                        message=(
                            f"Rule `{rule_name}` requires `{field_name}` "
                            f"for `{rel}`."
                        ),
                    )
                )
            expected = rule.get("expected", {})
            if not isinstance(expected, dict):
                continue
            for field_name, expected_value in expected.items():
                actual_value = meta.get(str(field_name))
                if actual_value == expected_value:
                    continue
                entries.append(
                    DriftEntry(
                        kind="unexpected_field_value",
                        severity=expected_severity,
                        path=rel,
                        field=str(field_name),
                        value=str(actual_value),
                        dimension="taxonomy_validity",
                        message=(
                            f"Rule `{rule_name}` expects `{field_name}: {expected_value}` "
                            f"for `{rel}`, got `{actual_value}`."
                        ),
                    )
                )
    return entries


def expand_registered_producers(root: Path, config: dict[str, Any]) -> list[Path]:
    producer_paths = config.get("producer_paths", {})
    paths: list[Path] = []
    for values in producer_paths.values():
        if not isinstance(values, list):
            continue
        for pattern in values:
            paths.extend(sorted(root.glob(str(pattern))))
    return sorted(path for path in paths if path.is_file())


def check_registered_producer_drift(root: Path | str, config: dict[str, Any]) -> list[DriftEntry]:
    root_path = Path(root)
    forbidden_domains = set(config.get("fields", {}).get("domain", {}).get("forbidden", []))
    entries: list[DriftEntry] = []
    for path in expand_registered_producers(root_path, config):
        rel = rel_path(path, root_path)
        text = path.read_text(encoding="utf-8", errors="ignore")
        for domain in sorted(forbidden_domains):
            if f"domain: {domain}" in text:
                entries.append(
                    DriftEntry(
                        kind="producer_hardcoded_forbidden_domain",
                        severity=severity(config, "producer_hardcoded_forbidden_domain", "error"),
                        path=rel,
                        field="domain",
                        value=domain,
                        dimension="taxonomy_validity",
                        message=f"Registered producer hardcodes forbidden `domain: {domain}`.",
                    )
                )
    return entries


def check_possible_unregistered_producers(root: Path | str, config: dict[str, Any]) -> list[DriftEntry]:
    root_path = Path(root)
    registered = {rel_path(path, root_path) for path in expand_registered_producers(root_path, config)}
    candidate_roots = [root_path / "scripts", root_path / ".codex/skills"]
    entries: list[DriftEntry] = []
    for candidate_root in candidate_roots:
        if not candidate_root.exists():
            continue
        for path in sorted(candidate_root.rglob("*")):
            if not path.is_file() or path.suffix not in {".py", ".md"}:
                continue
            rel = rel_path(path, root_path)
            if rel in registered:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "---" in text and "domain:" in text:
                entries.append(
                    DriftEntry(
                        kind="possible_unregistered_producer",
                        severity=severity(config, "possible_unregistered_producer", "warn"),
                        path=rel,
                        dimension="taxonomy_validity",
                        message="File contains frontmatter-looking text but is not registered in producer_paths.",
                    )
                )
    return entries


def summarize(entries: list[DriftEntry]) -> dict[str, int]:
    summary = {"error": 0, "warn": 0, "info": 0, "total": len(entries)}
    for entry in entries:
        if entry.severity not in summary:
            summary[entry.severity] = 0
        summary[entry.severity] += 1
    return summary


def build_scorecard(entries: list[DriftEntry], config: dict[str, Any]) -> dict[str, Any]:
    dimensions = config.get("scorecard", {}).get("dimensions", {})
    if not isinstance(dimensions, dict):
        dimensions = {}
    blocking_severities = set(config.get("strict_gate", {}).get("blocking_severities", ["error"]))
    minimum = int(config.get("strict_gate", {}).get("minimum_pass_score", 100))
    blocking_entries = [
        entry for entry in entries if entry.severity in blocking_severities
    ]
    dimension_rows: list[dict[str, Any]] = []
    total_lost = 0
    for dimension_name, weight in dimensions.items():
        dimension = str(dimension_name)
        points = int(weight)
        count = sum(1 for entry in entries if entry.dimension == dimension)
        points_lost = points if count else 0
        total_lost += points_lost
        dimension_rows.append(
            {
                "dimension": dimension,
                "weight": points,
                "finding_count": count,
                "points_lost": points_lost,
                "passed": count == 0,
            }
        )
    score = max(0, 100 - total_lost)
    if blocking_entries:
        score = 0
    return {
        "score": score,
        "minimum_pass_score": minimum,
        "passed": score >= minimum and not blocking_entries,
        "blocking_entry_count": len(blocking_entries),
        "dimensions": dimension_rows,
    }


def build_strict_gate(entries: list[DriftEntry], scorecard: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    strict_gate = config.get("strict_gate", {})
    blocking_severities = list(strict_gate.get("blocking_severities", ["error"]))
    blocking_entries = [
        entry for entry in entries if entry.severity in set(blocking_severities)
    ]
    return {
        "enabled": bool(strict_gate.get("enabled", False)),
        "passed": bool(scorecard.get("passed", False)),
        "minimum_pass_score": scorecard.get("minimum_pass_score", 100),
        "blocking_severities": blocking_severities,
        "blocking_entry_count": len(blocking_entries),
    }


def build_report(root: Path | str = ROOT) -> dict[str, Any]:
    root_path = Path(root)
    config = load_taxonomy(root_path)
    entries = [
        *check_strict_gate_drift(root_path, config),
        *check_content_drift(root_path, config),
        *check_registered_producer_drift(root_path, config),
        *check_possible_unregistered_producers(root_path, config),
    ]
    scorecard = build_scorecard(entries, config)
    strict_gate = build_strict_gate(entries, scorecard, config)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": root_path.resolve().as_posix(),
        "config_path": CONFIG_PATH.as_posix(),
        "summary": summarize(entries),
        "entries": [asdict(entry) for entry in entries],
        "taxonomy_version": config.get("version"),
        "strict_gate": strict_gate,
        "scorecard": scorecard,
        "proof_boundary": [
            "This checker validates configured frontmatter shape and taxonomy values.",
            "It does not infer missing business domains from prose.",
            "It does not prove relation target semantics or retrieval quality.",
        ],
    }


def render_markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Wiki Frontmatter Taxonomy Report",
        "",
        f"Generated at: `{report['generated_at']}`",
        f"Root: `{report['root']}`",
        f"Config: `{report['config_path']}`",
        f"Taxonomy version: `{report['taxonomy_version']}`",
        "",
        "## Summary",
        "",
        "| Severity | Count |",
        "| --- | --- |",
    ]
    for key in ["error", "warn", "info", "total"]:
        lines.append(f"| {key} | {report['summary'].get(key, 0)} |")

    strict_gate = report.get("strict_gate", {})
    scorecard = report.get("scorecard", {})
    lines.extend(
        [
            "",
            "## Strict Gate",
            "",
            "| Metric | Value |",
            "| --- | --- |",
            f"| Enabled | {strict_gate.get('enabled', False)} |",
            f"| Passed | {strict_gate.get('passed', False)} |",
            f"| Blocking entries | {strict_gate.get('blocking_entry_count', 0)} |",
            f"| Score | {scorecard.get('score', 0)} / {scorecard.get('minimum_pass_score', 100)} |",
            "",
            "## Scorecard",
            "",
            "| Dimension | Weight | Findings | Points Lost | Passed |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in scorecard.get("dimensions", []):
        lines.append(
            f"| {item['dimension']} | {item['weight']} | {item['finding_count']} | "
            f"{item['points_lost']} | {item['passed']} |"
        )

    lines.extend(["", "## Drift Entries", ""])
    entries = report.get("entries", [])
    if not entries:
        lines.append("- None")
    else:
        for entry in entries:
            field = entry.get("field") or "-"
            value = entry.get("value") or "-"
            lines.append(
                f"- `{entry['path']}` `{entry['severity']}` `{entry['kind']}` "
                f"field=`{field}` value=`{value}`: {entry['message']}"
            )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check wiki frontmatter taxonomy drift.")
    parser.add_argument("--root", default=ROOT)
    parser.add_argument("--json-output", default="/tmp/wiki-frontmatter-taxonomy-report.json")
    parser.add_argument("--markdown-output", default="/tmp/wiki-frontmatter-taxonomy-report.md")
    args = parser.parse_args()

    report = build_report(Path(args.root))
    Path(args.json_output).write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    Path(args.markdown_output).write_text(
        render_markdown_report(report),
        encoding="utf-8",
    )
    return 1 if report["summary"].get("error", 0) else 0


if __name__ == "__main__":
    sys.exit(main())
