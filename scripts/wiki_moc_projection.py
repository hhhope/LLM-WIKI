from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.wiki_moc_lifecycle import grouped_lifecycle_nodes


GENERATED_BEGIN_PREFIX = "<!-- BEGIN GENERATED MOC:"
GENERATED_END = "<!-- END GENERATED MOC -->"
DEFAULT_MOC_DIR = Path("wiki/moc")


@dataclass(frozen=True)
class MocCandidate:
    kind: str
    key: str
    path: str
    title: str
    block_id: str
    lines: tuple[str, ...]


def slugify(value: str) -> str:
    slug = re.sub(r"[^\w._-]+", "-", value.strip().lower(), flags=re.UNICODE)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "unknown"


def page_link_target(page_path: str) -> str:
    return Path(page_path).stem


def moc_link_target(candidate_path: str) -> str:
    return Path(candidate_path).stem


def wikilink(target: str, label: str | None = None) -> str:
    if label and label != target:
        return f"[[{target}|{label}]]"
    return f"[[{target}]]"


def _candidate_path(kind: str, key: str, moc_dir: Path | str = DEFAULT_MOC_DIR) -> str:
    return (Path(moc_dir) / f"{kind}-{slugify(key)}.md").as_posix()


def _candidate(
    *,
    kind: str,
    key: str,
    title: str,
    block_id: str,
    lines: list[str],
    moc_dir: Path | str = DEFAULT_MOC_DIR,
) -> MocCandidate:
    return MocCandidate(
        kind=kind,
        key=key,
        path=_candidate_path(kind, key, moc_dir),
        title=title,
        block_id=block_id,
        lines=tuple(lines),
    )


def _sorted_nodes(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(nodes, key=lambda node: (node.get("page_path", ""), node.get("artifact_type", "")))


def _path_to_node(nodes: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        str(node.get("page_path")): node
        for node in nodes
        if isinstance(node.get("page_path"), str)
    }


def _object_keys(nodes: list[dict[str, Any]]) -> set[str]:
    return {
        str(node["canonical_object"])
        for node in nodes
        if isinstance(node.get("canonical_object"), str)
        and str(node.get("canonical_object")).strip()
    }


def _node_line(node: dict[str, Any]) -> str:
    return (
        f"- {wikilink(page_link_target(node['page_path']))} "
        f"({node.get('source_layer', 'unknown')} / {node.get('artifact_type', 'unknown')})"
    )


def _object_lines(nodes: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for label, grouped_nodes in grouped_lifecycle_nodes(nodes):
        if lines:
            lines.append("")
        lines.append(f"## {label}")
        lines.extend(_node_line(node) for node in _sorted_nodes(grouped_nodes))
    return lines


def _link_count(lines: tuple[str, ...] | list[str]) -> int:
    return sum(1 for line in lines if line.startswith("- "))


def build_moc_candidates(graph: dict[str, Any], moc_dir: Path | str = DEFAULT_MOC_DIR) -> list[MocCandidate]:
    nodes = [node for node in graph.get("nodes", []) if isinstance(node, dict)]
    edges = [edge for edge in graph.get("edges", []) if isinstance(edge, dict)]
    candidates: list[MocCandidate] = []

    domain_nodes: dict[str, list[dict[str, Any]]] = defaultdict(list)
    object_nodes: dict[str, list[dict[str, Any]]] = defaultdict(list)
    relation_edges: dict[str, list[dict[str, Any]]] = defaultdict(list)
    path_node = _path_to_node(nodes)
    object_keys = _object_keys(nodes)

    for node in nodes:
        domain = str(node.get("domain") or "").strip()
        if domain and domain not in {"none", "unclassified", "personal-ops"}:
            domain_nodes[domain].append(node)
        canonical_object = str(node.get("canonical_object") or "").strip()
        if canonical_object:
            object_nodes[canonical_object].append(node)

    for edge in edges:
        relation_type = str(edge.get("relation_type") or "").strip()
        if relation_type:
            relation_edges[relation_type].append(edge)

    for domain, grouped_nodes in sorted(domain_nodes.items()):
        lines = [
            f"- {wikilink(page_link_target(node['page_path']))}"
            for node in _sorted_nodes(grouped_nodes)
        ]
        candidates.append(
            _candidate(
                kind="domain",
                key=domain,
                title=f"domain-{domain}",
                block_id=f"domain={domain}",
                lines=lines,
                moc_dir=moc_dir,
            )
        )

    for canonical_object, grouped_nodes in sorted(object_nodes.items()):
        lines = _object_lines(grouped_nodes)
        candidates.append(
            _candidate(
                kind="object",
                key=canonical_object,
                title=f"object-{canonical_object}",
                block_id=f"object={canonical_object}",
                lines=lines,
                moc_dir=moc_dir,
            )
        )

    for relation_type, grouped_edges in sorted(relation_edges.items()):
        relation_lines = []
        for edge in sorted(
            grouped_edges,
            key=lambda item: (
                str(item.get("source_page_path", "")),
                str(item.get("target", "")),
            ),
        ):
            source_path = str(edge.get("source_page_path") or "")
            target = str(edge.get("target") or "").strip()
            source_node = path_node.get(source_path, {})
            source_label = str(source_node.get("canonical_object") or page_link_target(source_path))
            source_link = wikilink(page_link_target(source_path), source_label)
            if target in object_keys:
                target_link = wikilink(f"object-{slugify(target)}", target)
            elif target.endswith(".md") or "/" in target:
                target_link = wikilink(page_link_target(target))
            else:
                target_link = wikilink(f"object-{slugify(target)}", target)
            relation_lines.append(f"- {source_link} -> {target_link}")
        candidates.append(
            _candidate(
                kind="relation",
                key=relation_type,
                title=f"relation-{relation_type}",
                block_id=f"relation={relation_type}",
                lines=relation_lines,
                moc_dir=moc_dir,
            )
        )

    return candidates


def render_moc_candidate(candidate: MocCandidate) -> str:
    lines = [
        "---",
        "layer: ops",
        "domain: wiki",
        "ops_area: wiki-runtime",
        f"canonical_object: obsidian-moc-{candidate.kind}-{slugify(candidate.key)}",
        "artifact_type: generated-moc",
        "status: generated",
        "---",
        "",
        f"# {candidate.title}",
        "",
        f"{GENERATED_BEGIN_PREFIX} {candidate.block_id} -->",
        *candidate.lines,
        GENERATED_END,
        "",
    ]
    return "\n".join(lines)


def _generated_block(text: str) -> str | None:
    begin = text.find(GENERATED_BEGIN_PREFIX)
    if begin == -1:
        return None
    end = text.find(GENERATED_END, begin)
    if end == -1:
        return None
    return text[begin : end + len(GENERATED_END)]


def _rendered_block(candidate: MocCandidate) -> str:
    rendered = render_moc_candidate(candidate)
    block = _generated_block(rendered)
    if block is None:
        raise ValueError(f"rendered candidate missing generated block: {candidate.path}")
    return block


def merge_generated_block(existing: str, candidate: MocCandidate) -> str:
    new_block = _rendered_block(candidate)
    existing_block = _generated_block(existing)
    if existing_block is None:
        separator = "" if existing.endswith("\n") or not existing else "\n\n"
        return f"{existing}{separator}{new_block}\n"
    return existing.replace(existing_block, new_block)


def build_moc_plan(root: Path | str, graph: dict[str, Any], moc_dir: Path | str = DEFAULT_MOC_DIR) -> dict[str, Any]:
    root_path = Path(root)
    candidates = build_moc_candidates(graph, moc_dir)
    candidate_paths = {candidate.path for candidate in candidates}
    entries: list[dict[str, Any]] = []

    for candidate in candidates:
        path = root_path / candidate.path
        rendered = render_moc_candidate(candidate)
        if not path.exists():
            action = "create"
        else:
            existing = path.read_text(encoding="utf-8")
            action = "noop" if merge_generated_block(existing, candidate) == existing else "update"
        entries.append(
            {
                "action": action,
                "kind": candidate.kind,
                "key": candidate.key,
                "path": candidate.path,
                "link_count": _link_count(candidate.lines),
                "preview": rendered,
            }
        )

    existing_moc_paths = []
    moc_root = root_path / moc_dir
    if moc_root.exists():
        existing_moc_paths = [
            path.relative_to(root_path).as_posix()
            for path in sorted(moc_root.glob("*.md"))
        ]
    for path in existing_moc_paths:
        if path not in candidate_paths:
            entries.append(
                {
                    "action": "orphan",
                    "kind": "unknown",
                    "key": Path(path).stem,
                    "path": path,
                    "link_count": 0,
                    "preview": "",
                }
            )

    summary = {
        "candidate_count": len(candidates),
        "create_count": sum(1 for entry in entries if entry["action"] == "create"),
        "update_count": sum(1 for entry in entries if entry["action"] == "update"),
        "noop_count": sum(1 for entry in entries if entry["action"] == "noop"),
        "orphan_count": sum(1 for entry in entries if entry["action"] == "orphan"),
    }
    return {
        "summary": summary,
        "entries": entries,
        "proof_boundary_notes": [
            "MOC projection is derived from explicit graph/frontmatter structure.",
            "Dry-run and preview plans do not write files.",
            "Generated blocks are the only writer-owned region of MOC pages.",
        ],
    }


def apply_moc_plan(root: Path | str, graph: dict[str, Any], moc_dir: Path | str = DEFAULT_MOC_DIR) -> dict[str, Any]:
    root_path = Path(root)
    plan = build_moc_plan(root_path, graph, moc_dir)
    for entry in plan["entries"]:
        if entry["action"] not in {"create", "update"}:
            continue
        path = root_path / entry["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        candidate = next(
            candidate
            for candidate in build_moc_candidates(graph, moc_dir)
            if candidate.path == entry["path"]
        )
        if entry["action"] == "create":
            path.write_text(render_moc_candidate(candidate), encoding="utf-8")
        else:
            path.write_text(
                merge_generated_block(path.read_text(encoding="utf-8"), candidate),
                encoding="utf-8",
            )
    return plan


def build_moc_health(root: Path | str, graph: dict[str, Any], moc_dir: Path | str = DEFAULT_MOC_DIR) -> dict[str, Any]:
    plan = build_moc_plan(root, graph, moc_dir)
    entries = [
        {
            "type": "moc_projection",
            "path": entry["path"],
            "kind": entry["kind"],
            "key": entry["key"],
            "problem": entry["action"],
            "link_count": entry["link_count"],
            "repair_route": "obsidian-moc-projection",
        }
        for entry in plan["entries"]
        if entry["action"] != "noop"
    ]
    return {
        "status": "pass" if not entries else "drift",
        "summary": plan["summary"],
        "entries": entries[:20],
        "proof_boundary_notes": plan["proof_boundary_notes"],
    }
