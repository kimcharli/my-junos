#!/usr/bin/env python3
"""
Generates MANIFEST.md: the authoritative inventory of the OKF knowledge base.

Exists so agents and humans can answer "what documents exist?" and "what is the
next free KP-* ID?" by reading one file, instead of walking the tree and
grepping frontmatter on every session.

Frontmatter parsing is imported from validate_okf.py so the manifest and the
validator can never disagree about what a document declares.

Usage:
    python tools/okf_manifest.py            # regenerate MANIFEST.md in place
    python tools/okf_manifest.py --check    # exit 1 if MANIFEST.md is stale
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_okf import extract_frontmatter, load_yaml  # noqa: E402

# Prefixes are fixed by the id pattern in schemas/okf-frontmatter-schema.json.
ID_PREFIXES = {
    "KP-SYS": "System / base platform services",
    "KP-SEC": "Security hardening and compliance audits",
    "KP-INT": "Integration / fabric orchestration (Apstra)",
    "KP-RT": "Routing protocols and policy",
    "KP-PRO": "Provisioning and lifecycle workflows",
    "KP-META": "Meta: indexes, specs, tracking",
}

ID_RE = re.compile(r"^(KP-(?:SYS|SEC|INT|RT|PRO|META))-(\d{3})$")


def collect_documents(knowledge_dir, root_dir):
    """Walk knowledge/ and return one record per OKF markdown document."""
    docs = []
    for dirpath, _dirnames, filenames in os.walk(knowledge_dir):
        for filename in sorted(filenames):
            if not filename.endswith(".md"):
                continue
            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root_dir)

            frontmatter_str, _body = extract_frontmatter(filepath)
            if frontmatter_str is None:
                docs.append({"path": rel_path, "error": "missing frontmatter"})
                continue
            try:
                data = load_yaml(frontmatter_str) or {}
            except Exception as exc:
                docs.append({"path": rel_path, "error": f"unparseable frontmatter: {exc}"})
                continue

            docs.append(
                {
                    "path": rel_path,
                    "id": data.get("id", ""),
                    "type": data.get("type", ""),
                    "title": data.get("title", ""),
                    "version": data.get("version", ""),
                    "status": data.get("status", ""),
                    "tags": data.get("tags") or [],
                    "error": None,
                }
            )
    return sorted(docs, key=lambda d: d["path"])


def next_free_ids(docs):
    """Map each known prefix to its next unallocated sequential ID."""
    highest = {prefix: 0 for prefix in ID_PREFIXES}
    for doc in docs:
        match = ID_RE.match(str(doc.get("id", "")))
        if match:
            prefix, number = match.group(1), int(match.group(2))
            highest[prefix] = max(highest[prefix], number)
    return {prefix: f"{prefix}-{highest[prefix] + 1:03d}" for prefix in ID_PREFIXES}


def find_duplicate_ids(docs):
    seen = {}
    for doc in docs:
        doc_id = doc.get("id")
        if doc_id:
            seen.setdefault(doc_id, []).append(doc["path"])
    return {k: v for k, v in seen.items() if len(v) > 1}


def escape_cell(value):
    return str(value).replace("|", "\\|")


def render(docs, root_dir):
    duplicates = find_duplicate_ids(docs)
    broken = [d for d in docs if d.get("error")]
    next_ids = next_free_ids(docs)

    lines = []
    lines.append("# OKF Knowledge Manifest")
    lines.append("")
    lines.append(
        "> **Generated file — do not edit by hand.** "
        "Regenerate with `python tools/okf_manifest.py`. "
        "The pre-commit hook refreshes and stages it automatically."
    )
    lines.append("")
    lines.append(
        "This is the authoritative inventory of the knowledge base. Read it instead of "
        "walking `knowledge/` or grepping frontmatter for `id:`. Authoring conventions "
        "and validator rules live in [`AGENTS.md`](AGENTS.md)."
    )
    lines.append("")

    lines.append("## Next Free IDs")
    lines.append("")
    lines.append("Claim the ID listed here when authoring a new document in that domain.")
    lines.append("")
    lines.append("| Prefix | Domain | Next free ID |")
    lines.append("| --- | --- | --- |")
    for prefix, domain in ID_PREFIXES.items():
        lines.append(f"| `{prefix}` | {domain} | `{next_ids[prefix]}` |")
    lines.append("")

    lines.append("## Documents")
    lines.append("")

    by_dir = {}
    for doc in docs:
        by_dir.setdefault(os.path.dirname(doc["path"]), []).append(doc)

    for directory in sorted(by_dir):
        lines.append(f"### `{directory}/`")
        lines.append("")
        lines.append("| ID | Type | Title | Version | Document |")
        lines.append("| --- | --- | --- | --- | --- |")
        for doc in by_dir[directory]:
            if doc.get("error"):
                lines.append(
                    f"| — | — | **INVALID: {escape_cell(doc['error'])}** | — "
                    f"| [`{os.path.basename(doc['path'])}`]({doc['path']}) |"
                )
                continue
            lines.append(
                f"| `{escape_cell(doc['id'])}` "
                f"| {escape_cell(doc['type'])} "
                f"| {escape_cell(doc['title'])} "
                f"| `{escape_cell(doc['version'])}` "
                f"| [`{os.path.basename(doc['path'])}`]({doc['path']}) |"
            )
        lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append(f"* **Total documents:** {len(docs)}")
    type_counts = {}
    for doc in docs:
        if not doc.get("error"):
            type_counts[doc["type"]] = type_counts.get(doc["type"], 0) + 1
    for doc_type in sorted(type_counts):
        lines.append(f"* **{doc_type}:** {type_counts[doc_type]}")

    if duplicates:
        lines.append("")
        lines.append("## ⚠️ Duplicate IDs")
        lines.append("")
        for doc_id, paths in sorted(duplicates.items()):
            lines.append(f"* `{doc_id}` — {', '.join('`' + p + '`' for p in paths)}")

    if broken:
        lines.append("")
        lines.append("## ⚠️ Unparseable Documents")
        lines.append("")
        for doc in broken:
            lines.append(f"* `{doc['path']}` — {doc['error']}")

    lines.append("")
    return "\n".join(lines)


def main():
    check_only = "--check" in sys.argv[1:]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, ".."))
    knowledge_dir = os.path.join(root_dir, "knowledge")
    manifest_path = os.path.join(root_dir, "MANIFEST.md")

    if not os.path.isdir(knowledge_dir):
        print(f"[-] Knowledge directory not found: {knowledge_dir}")
        return 1

    docs = collect_documents(knowledge_dir, root_dir)
    rendered = render(docs, root_dir)

    existing = None
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            existing = f.read()

    if check_only:
        if existing != rendered:
            print("[-] MANIFEST.md is stale. Run: python tools/okf_manifest.py")
            return 1
        print(f"[+] MANIFEST.md is up to date ({len(docs)} documents).")
        return 0

    if existing == rendered:
        print(f"[+] MANIFEST.md already up to date ({len(docs)} documents).")
    else:
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        print(f"[+] Wrote MANIFEST.md ({len(docs)} documents).")

    duplicates = find_duplicate_ids(docs)
    if duplicates:
        print(f"[-] Duplicate IDs detected: {', '.join(sorted(duplicates))}")
        return 1

    broken = [d for d in docs if d.get("error")]
    if broken:
        print(f"[-] {len(broken)} document(s) have unparseable frontmatter.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
