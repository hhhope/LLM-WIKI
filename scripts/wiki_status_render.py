from __future__ import annotations

from typing import Any


def _markdown_table(headers: list[str], rows: list[list[object]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(str(cell) for cell in row) + " |" for row in rows)
    return lines


def _counter_rows(counter: dict[str, int]) -> list[list[object]]:
    return [[key, value] for key, value in sorted(counter.items())] or [["none", 0]]


def _render_product_status(product_status: dict[str, Any]) -> list[str]:
    identity = product_status["identity_coverage"]
    relation = product_status["relation_coverage"]
    unresolved = product_status["unresolved_items"]
    lines = [
        "",
        "## Product Status",
        "",
        f"Contract version: `{product_status['contract_version']}`",
        "",
        "### Object Types",
        "",
        *_markdown_table(["Object Type", "Count"], _counter_rows(product_status["object_type_counts"])),
        "",
        "### Readiness",
        "",
        *_markdown_table(["Readiness", "Count"], _counter_rows(product_status["readiness_counts"])),
        "",
        "### Source Layers",
        "",
        *_markdown_table(["Source Layer", "Count"], _counter_rows(product_status["source_layer_counts"])),
        "",
        "### Identity Coverage",
        "",
        *_markdown_table(
            ["Metric", "Value"],
            [
                ["With identity", identity["with_identity"]],
                ["Missing identity", identity["missing_identity"]],
            ],
        ),
        "",
        "### Relation Coverage",
        "",
        *_markdown_table(
            ["Metric", "Value"],
            [
                ["With relations", relation["with_relations"]],
                ["Missing relations", relation["missing_relations"]],
            ],
        ),
        "",
        "### Unresolved Product Status Items",
        "",
    ]
    if unresolved:
        for item in unresolved:
            item_type = item.get("type", "unknown")
            target = item.get("path") or item.get("change_id") or "unknown"
            lines.append(
                f"- `{target}`: {item_type} "
                f"({item['readiness_label']} -> {item['status_transition']})"
            )
    else:
        lines.append("- None")
    return lines


def _render_domain_taxonomy_health(health: dict[str, Any]) -> list[str]:
    summary = health.get("summary", {})
    lines = [
        "",
        "## Domain Taxonomy Health",
        "",
        f"Status: `{health.get('status', 'unknown')}`",
        f"Config: `{health.get('config_path', 'wiki/config/frontmatter-taxonomy.yaml')}`",
        "",
        *_markdown_table(
            ["Severity", "Count"],
            [
                ["error", summary.get("error", 0)],
                ["warn", summary.get("warn", 0)],
                ["info", summary.get("info", 0)],
                ["total", summary.get("total", 0)],
            ],
        ),
        "",
        "### Taxonomy Drift Samples",
        "",
    ]
    entries = health.get("entries", [])
    if entries:
        for entry in entries:
            lines.append(
                f"- `{entry.get('path', 'unknown')}` `{entry.get('severity', 'unknown')}` "
                f"`{entry.get('kind', 'unknown')}`: {entry.get('message', '')}"
            )
    else:
        lines.append("- None")
    return lines


def _render_frontmatter_strict_gate(health: dict[str, Any]) -> list[str]:
    strict_gate = health.get("strict_gate", {})
    scorecard = health.get("scorecard", {})
    lines = [
        "",
        "## Frontmatter Strict Gate",
        "",
        *_markdown_table(
            ["Metric", "Value"],
            [
                ["Enabled", strict_gate.get("enabled", False)],
                ["Passed", strict_gate.get("passed", False)],
                ["Blocking entries", strict_gate.get("blocking_entry_count", 0)],
                [
                    "Score",
                    f"{scorecard.get('score', 0)} / {scorecard.get('minimum_pass_score', 100)}",
                ],
            ],
        ),
        "",
        "## Frontmatter Scorecard",
        "",
    ]
    dimensions = scorecard.get("dimensions", [])
    if dimensions:
        lines.extend(
            _markdown_table(
                ["Dimension", "Weight", "Findings", "Points Lost", "Passed"],
                [
                    [
                        item.get("dimension"),
                        item.get("weight"),
                        item.get("finding_count"),
                        item.get("points_lost"),
                        item.get("passed"),
                    ]
                    for item in dimensions
                ],
            )
        )
    else:
        lines.append("- None")
    return lines


def _render_graph_parse_health(health: dict[str, Any]) -> list[str]:
    summary = health.get("summary", {})
    lines = [
        "",
        "## Graph Parse Health",
        "",
        f"Status: `{health.get('status', 'unknown')}`",
        "",
        *_markdown_table(
            ["Metric", "Value"],
            [["Suspicious relation pages", summary.get("total", 0)]],
        ),
        "",
        "### Graph Parse Samples",
        "",
    ]
    entries = health.get("entries", [])
    if entries:
        for entry in entries:
            fields = ", ".join(entry.get("fields", []))
            lines.append(
                f"- `{entry.get('path', 'unknown')}` fields=`{fields}` "
                f"route=`{entry.get('repair_route', 'unknown')}`: {entry.get('problem', '')}"
            )
    else:
        lines.append("- None")
    return lines


def _render_moc_projection_health(health: dict[str, Any]) -> list[str]:
    summary = health.get("summary", {})
    lines = [
        "",
        "## MOC Projection Health",
        "",
        f"Status: `{health.get('status', 'unknown')}`",
        "",
        *_markdown_table(
            ["Metric", "Value"],
            [
                ["Candidates", summary.get("candidate_count", 0)],
                ["Create", summary.get("create_count", 0)],
                ["Update", summary.get("update_count", 0)],
                ["Noop", summary.get("noop_count", 0)],
                ["Orphan", summary.get("orphan_count", 0)],
            ],
        ),
        "",
        "### MOC Projection Samples",
        "",
    ]
    entries = health.get("entries", [])
    if entries:
        for entry in entries:
            lines.append(
                f"- `{entry.get('path', 'unknown')}` `{entry.get('problem', 'unknown')}` "
                f"kind=`{entry.get('kind', 'unknown')}` key=`{entry.get('key', 'unknown')}` "
                f"route=`{entry.get('repair_route', 'unknown')}`"
            )
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "MOC projection health is diagnostic only. Status does not write `wiki/moc` files.",
        ]
    )
    return lines


def _render_content_enrichment_health(health: dict[str, Any]) -> list[str]:
    summary = health.get("summary", {})
    lines = [
        "",
        "## Content Enrichment Health",
        "",
        f"Status: `{health.get('status', 'unknown')}`",
        "",
        *_markdown_table(
            ["Metric", "Value"],
            [
                ["Entries", summary.get("entry_count", 0)],
                ["Review needed", summary.get("review_needed_count", 0)],
                ["High confidence", summary.get("high_confidence_count", 0)],
                ["Medium confidence", summary.get("medium_confidence_count", 0)],
                ["Low confidence", summary.get("low_confidence_count", 0)],
            ],
        ),
        "",
        "### Content Enrichment Samples",
        "",
    ]
    entries = health.get("entries", [])
    if entries:
        for entry in entries:
            lines.append(
                f"- `{entry.get('path', 'unknown')}` confidence=`{entry.get('confidence', 'unknown')}` "
                f"route=`{entry.get('repair_route', 'unknown')}`"
            )
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "Content enrichment is preview only. Status does not write frontmatter.",
        ]
    )
    return lines


def _render_content_adjudication_health(health: dict[str, Any]) -> list[str]:
    summary = health.get("summary", {})
    eval_result = health.get("eval_result", {})
    lines = [
        "",
        "## Content Adjudication Health",
        "",
        f"Status: `{health.get('status', 'unknown')}`",
        f"Eval passed: `{eval_result.get('passed', False)}`",
        "",
        *_markdown_table(
            ["Metric", "Value"],
            [
                ["Candidates", summary.get("candidate_count", 0)],
                ["Full details", summary.get("full_detail_count", 0)],
                ["Review focus", summary.get("review_focus_count", 0)],
                ["Taxonomy candidates", summary.get("taxonomy_candidate_count", 0)],
                ["Drift traces", summary.get("drift_trace_count", 0)],
            ],
        ),
        "",
        "### Content Adjudication Samples",
        "",
    ]
    entries = health.get("entries", [])
    if entries:
        for entry in entries:
            reasons = ", ".join(entry.get("review_reasons", []))
            lines.append(
                f"- `{entry.get('path', 'unknown')}` detail=`{entry.get('detail_ref', 'unknown')}` "
                f"reasons=`{reasons}` route=`{entry.get('repair_route', 'unknown')}`"
            )
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "Content adjudication is review_package output only. Status does not write frontmatter or taxonomy.",
        ]
    )
    return lines


def render_status_markdown(manifest: dict[str, Any]) -> str:
    summary = manifest["summary"]
    lines = [
        "---",
        "layer: status",
        "domain: none",
        "canonical_object: wiki-status",
        "artifact_type: generated-status",
        "status: generated",
        "---",
        "",
        "# Wiki Status",
        "",
        f"Generated at: `{manifest['generated_at']}`",
        "",
        "## Summary",
        "",
        *_markdown_table(
            ["Metric", "Value"],
            [
                ["Wiki pages", summary["wiki_page_count"]],
                ["Source records", summary["source_record_count"]],
                ["Inbox files", summary["inbox_file_count"]],
                ["Pending inbox files", summary["pending_inbox_count"]],
                ["Active OpenSpec changes", summary["active_change_count"]],
                ["Complete active-dir changes", summary["complete_change_count"]],
            ],
        ),
        "",
        "## Wiki Sections",
        "",
    ]
    section_rows = [
        [section, count]
        for section, count in sorted(summary["wiki_sections"].items())
    ]
    lines.extend(_markdown_table(["Section", "Pages"], section_rows or [["none", 0]]))
    lines.extend(_render_product_status(manifest["product_status"]))
    lines.extend(_render_domain_taxonomy_health(manifest.get("domain_taxonomy_health", {})))
    lines.extend(_render_frontmatter_strict_gate(manifest.get("domain_taxonomy_health", {})))
    lines.extend(_render_graph_parse_health(manifest.get("graph_parse_health", {})))
    lines.extend(_render_content_enrichment_health(manifest.get("content_enrichment_health", {})))
    lines.extend(_render_content_adjudication_health(manifest.get("content_adjudication_health", {})))
    lines.extend(_render_moc_projection_health(manifest.get("moc_projection_health", {})))
    lines.extend(["", "## Pending Inbox Files", ""])
    pending = manifest["pending_inbox_files"]
    if pending:
        lines.extend(f"- `{path}`" for path in pending)
    else:
        lines.append("- None")

    lines.extend(["", "## OpenSpec Changes", ""])
    change_rows = [
        [
            item["change_id"],
            item["state"],
            f"{item['done_tasks']}/{item['total_tasks']}",
            item["tasks_path"],
        ]
        for item in manifest["openspec_changes"]
    ]
    lines.extend(_markdown_table(["Change", "State", "Tasks", "Path"], change_rows or [["none", "-", "-", "-"]]))

    lines.extend(["", "## Next Actions", ""])
    if summary["pending_inbox_count"]:
        lines.append("- Create or link source records for pending inbox files.")
    if summary["complete_change_count"]:
        lines.append("- Review complete active-directory OpenSpec changes for archive readiness.")
    if summary["active_change_count"]:
        lines.append("- Continue active OpenSpec changes before starting unrelated implementation.")
    if not (
        summary["pending_inbox_count"]
        or summary["complete_change_count"]
        or summary["active_change_count"]
    ):
        lines.append("- No generated status actions.")
    lines.append("")
    return "\n".join(lines)
