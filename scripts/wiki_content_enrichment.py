from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from scripts.check_wiki_frontmatter import CONFIG_PATH, load_taxonomy
from scripts.extract_wiki_graph import parse_frontmatter


COVERED_PREFIXES = ("wiki/ops/", "wiki/adr/")
RELATION_FIELDS = ("related_objects", "derived_from", "validates", "formalizes")


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _title_from_body(body: str, fallback: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or fallback
    return fallback


def _strip_date_suffix(stem: str) -> str:
    return re.sub(r"-\d{4}-\d{2}-\d{2}$", "", stem)


def _object_from_stem(stem: str) -> str:
    clean = _strip_date_suffix(stem)
    clean = re.sub(r"^\d{4}-", "", clean)
    for suffix in (
        "-retro",
        "-explore",
        "-intake",
        "-reanchor",
        "-method",
        "-trace",
        "-distill",
    ):
        if clean.endswith(suffix) and len(clean) > len(suffix):
            return clean[: -len(suffix)]
    return clean


def _artifact_from_path(path: Path, rel: str, meta: dict[str, Any]) -> str:
    current = meta.get("artifact_type")
    if isinstance(current, str) and current.strip():
        return current
    if rel.startswith("wiki/adr/"):
        return "adr"
    stem = _strip_date_suffix(path.stem)
    for artifact_type in ("retro", "explore", "intake", "reanchor", "method", "trace", "distill"):
        if stem.endswith(f"-{artifact_type}"):
            return artifact_type
    return "method"


def _derive_object_and_type(path: Path, root: Path, meta: dict[str, Any]) -> tuple[str | None, str | None]:
    canonical_object = meta.get("canonical_object")
    artifact_type = meta.get("artifact_type")
    if isinstance(canonical_object, str) and isinstance(artifact_type, str):
        return canonical_object, artifact_type

    rel = _relative(path, root)
    if rel.startswith("openspec/specs/") and rel.endswith("/spec.md"):
        return rel.split("/")[2], "spec"
    if rel.startswith("wiki/adr/"):
        match = re.match(r"^wiki/adr/\d{4}-(.+)\.md$", rel)
        return (match.group(1) if match else _object_from_stem(path.stem)), "adr"
    if rel.startswith("wiki/examples/") and path.stem.endswith("-example"):
        return path.stem.removesuffix("-example"), "example"
    if rel.startswith("wiki/ops/"):
        return _object_from_stem(path.stem), _artifact_from_path(path, rel, meta)
    return None, None


def _ops_area_from_text(text: str, meta: dict[str, Any]) -> tuple[str, list[str]]:
    current = meta.get("ops_area")
    if isinstance(current, str) and current.strip():
        return current, ["existing ops_area frontmatter"]
    lower = text.lower()
    checks = [
        ("wiki-runtime", ["wiki-runtime", "wiki-react", "decision_trace", "moc", "graph", "frontmatter"]),
        ("learning-capture", ["learning capture", "reading notes", "readme", "github"]),
        ("report-quality", ["report gate", "reader-facing", "public report", "h5"]),
        ("workflow-trace", ["drift", "retro", "trace", "reanchor"]),
        ("agent-governance", ["agents.md", "governance", "skill", "adr"]),
    ]
    for ops_area, keywords in checks:
        matches = [keyword for keyword in keywords if keyword in lower]
        if matches:
            return ops_area, [f"matched keywords: {', '.join(matches[:3])}"]
    return "workflow-trace", ["default ops fallback requires review"]


def _domain_from_text(rel: str, text: str, meta: dict[str, Any], known_domains: set[str]) -> tuple[str, list[str]]:
    current = meta.get("domain")
    if isinstance(current, str) and current.strip() and current != "personal-ops":
        return current, ["existing domain frontmatter"]
    if rel.startswith("wiki/adr/"):
        return "none", ["ADR pages use domain none"]
    lower = text.lower()
    for domain in sorted(known_domains):
        if domain in {"none", "unclassified"}:
            continue
        if domain in lower:
            return domain, [f"matched domain keyword: {domain}"]
    if any(keyword in lower for keyword in ["wiki", "frontmatter", "graph", "moc", "wiki-react"]):
        return "wiki", ["matched wiki runtime keywords"]
    return "unclassified", ["no known domain keyword matched"]


def _existing_objects(root: Path) -> set[str]:
    objects: set[str] = set()
    for base in [root / "wiki" / "ops", root / "wiki" / "adr", root / "wiki" / "examples", root / "openspec" / "specs"]:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            if path.name == "index.md":
                continue
            text = path.read_text(encoding="utf-8")
            meta, _body = parse_frontmatter(text)
            canonical_object, _artifact_type = _derive_object_and_type(path, root, meta)
            if canonical_object:
                objects.add(canonical_object)
    return objects


def _relations_from_text(text: str, meta: dict[str, Any], existing_objects: set[str], current_object: str) -> dict[str, list[str]]:
    relations: dict[str, list[str]] = {}
    for field in RELATION_FIELDS:
        value = meta.get(field)
        if isinstance(value, list):
            relations[field] = [str(item) for item in value if str(item).strip()]
        elif isinstance(value, str) and value.strip():
            relations[field] = [value]

    lower = text.lower()
    related = set(relations.get("related_objects", []))
    for obj in sorted(existing_objects):
        if obj == current_object:
            continue
        if obj.lower() in lower:
            related.add(obj)
    if related:
        relations["related_objects"] = sorted(related)
    return relations


def _confidence(meta: dict[str, Any], suggested: dict[str, str], relations: dict[str, list[str]]) -> tuple[str, bool]:
    required = ["layer", "domain", "canonical_object", "artifact_type"]
    complete_before = all(meta.get(field) for field in required)
    if suggested.get("layer") == "ops":
        complete_before = complete_before and bool(meta.get("ops_area"))
    if complete_before:
        return "high", False
    if relations or suggested.get("domain") not in {"unclassified", None}:
        return "medium", True
    return "low", True


def analyze_page(path: Path, root: Path, existing_objects: set[str], known_domains: set[str]) -> dict[str, Any] | None:
    rel = _relative(path, root)
    if not rel.startswith(COVERED_PREFIXES) or path.name == "index.md":
        return None
    text = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    title = _title_from_body(body, path.stem)
    canonical_object, derived_artifact = _derive_object_and_type(path, root, meta)
    canonical_object = (
        str(meta.get("canonical_object"))
        if isinstance(meta.get("canonical_object"), str) and str(meta.get("canonical_object")).strip()
        else canonical_object
        or _object_from_stem(path.stem)
    )
    artifact_type = _artifact_from_path(path, rel, meta)
    if derived_artifact and not meta.get("artifact_type"):
        artifact_type = derived_artifact

    layer = "adr" if rel.startswith("wiki/adr/") else "ops"
    combined_text = f"{rel}\n{title}\n{text}"
    domain, domain_evidence = _domain_from_text(rel, combined_text, meta, known_domains)
    ops_area, ops_evidence = ("", [])
    if layer == "ops":
        ops_area, ops_evidence = _ops_area_from_text(combined_text, meta)

    suggested = {
        "layer": layer,
        "domain": domain,
        "canonical_object": canonical_object,
        "artifact_type": artifact_type,
    }
    if ops_area:
        suggested["ops_area"] = ops_area
    if domain == "unclassified":
        suggested["classification_needed"] = "true"

    relations = _relations_from_text(combined_text, meta, existing_objects, canonical_object)
    confidence, needs_review = _confidence(meta, suggested, relations)
    evidence = [
        f"path: {rel}",
        f"title: {title}",
        *domain_evidence,
        *ops_evidence,
    ]
    if relations:
        evidence.append("matched existing canonical objects in content/frontmatter")

    return {
        "path": rel,
        "suggested_frontmatter": suggested,
        "suggested_relations": relations,
        "confidence": confidence,
        "needs_review": needs_review,
        "evidence": evidence,
    }


def build_enrichment_preview(root: Path | str) -> dict[str, Any]:
    root_path = Path(root)
    if not (root_path / CONFIG_PATH).exists():
        return {
            "summary": {
                "entry_count": 0,
                "review_needed_count": 0,
                "high_confidence_count": 0,
                "medium_confidence_count": 0,
                "low_confidence_count": 0,
            },
            "entries": [],
            "proof_boundary_notes": [
                "Content enrichment is unavailable because taxonomy config is missing.",
                "It does not write frontmatter.",
            ],
        }
    taxonomy = load_taxonomy(root_path)
    known_domains = {
        str(value)
        for value in taxonomy.get("fields", {}).get("domain", {}).get("known", [])
    }
    existing_objects = _existing_objects(root_path)
    entries = []
    for base in [root_path / "wiki" / "ops", root_path / "wiki" / "adr"]:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            entry = analyze_page(path, root_path, existing_objects, known_domains)
            if entry is not None:
                entries.append(entry)
    review_needed = [entry for entry in entries if entry["needs_review"]]
    return {
        "summary": {
            "entry_count": len(entries),
            "review_needed_count": len(review_needed),
            "high_confidence_count": sum(1 for entry in entries if entry["confidence"] == "high"),
            "medium_confidence_count": sum(1 for entry in entries if entry["confidence"] == "medium"),
            "low_confidence_count": sum(1 for entry in entries if entry["confidence"] == "low"),
        },
        "entries": entries,
        "proof_boundary_notes": [
            "Content enrichment is deterministic preview only.",
            "It does not write frontmatter.",
            "It does not prove semantic truth.",
        ],
    }


def build_enrichment_health(root: Path | str) -> dict[str, Any]:
    preview = build_enrichment_preview(root)
    review_entries = [
        {
            "type": "content_enrichment",
            "path": entry["path"],
            "confidence": entry["confidence"],
            "problem": "review_needed",
            "repair_route": "frontmatter-enrichment-preview",
        }
        for entry in preview["entries"]
        if entry["needs_review"]
    ]
    return {
        "status": "pass" if not review_entries else "review_needed",
        "summary": preview["summary"],
        "entries": review_entries[:20],
        "proof_boundary_notes": preview["proof_boundary_notes"],
    }
