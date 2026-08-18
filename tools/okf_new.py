#!/usr/bin/env python3
"""
Scaffolds a new OKF document with a correct, validator-passing skeleton.

Exists so the frontmatter contract does not have to be memorized or documented
in always-resident context: this script allocates the next free ID, stamps every
required field, and emits the per-type body stub that validate_okf.py demands.

Usage:
    python tools/okf_new.py apstra dhcp-relay-giaddr --title "Apstra DHCP Relay GIADDR"
    python tools/okf_new.py base-config sys-syslog --title "System Syslog Configuration"
    python tools/okf_new.py audit sec-snmp-hardened --title "SNMPv2 Disabled"
    python tools/okf_new.py meta okf-spec-tracking --title "OKF Spec Tracking"

    # Override the ID prefix when the domain differs from the type default:
    python tools/okf_new.py base-config rt-bgp-policy --prefix KP-RT --title "BGP Policy"

Refuses to overwrite an existing file. Regenerates MANIFEST.md on success.
"""
import argparse
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from okf_manifest import collect_documents, next_free_ids  # noqa: E402

TEMPLATES = {
    "base-config": {
        "directory": "knowledge/base-configs",
        "doc_type": "JUNOS Base Config",
        "prefix": "KP-SYS",
        "resource": "https://www.juniper.net/documentation/",
        "tags": "[TODO, TODO]",
        "extra_frontmatter": "",
        "body": """# Configuration Rationale

TODO: explain what this baseline establishes and why.

# JUNOS Configuration Snippet

```set
set TODO
```
""",
    },
    "audit": {
        "directory": "knowledge/audit-items",
        "doc_type": "JUNOS Audit",
        "prefix": "KP-SEC",
        "resource": "https://www.juniper.net/documentation/",
        "tags": "[TODO, TODO]",
        "extra_frontmatter": """verification_method: cli-regex
checks:
  - name: TODO name of check
    command: TODO show command
    expected: TODO expected regex or xpath
    negate: false
    remediation: TODO set/delete commands
""",
        "body": """# Audit Rationale

TODO: explain the secure design rationale and what drift this detects.

# Remediation Notes

TODO: describe what an operator should do when this check fails.
""",
    },
    "apstra": {
        "directory": "knowledge/apstra",
        "doc_type": "Apstra Configuration",
        "prefix": "KP-INT",
        "resource": "https://www.juniper.net/documentation/us/en/software/apstra4.1/",
        "tags": "[apstra, TODO]",
        "extra_frontmatter": "",
        "body": """# Apstra REST API Intent Payload

TODO: describe the intent. Verify the endpoint below against your Apstra version.

### HTTP Method & Endpoint
* **Method:** `TODO`
* **Path:** `/api/blueprints/<blueprint_id>/TODO`

### JSON Payload
```json
{
  "TODO": "TODO"
}
```

### Alternative GUI Configuration Path

1. Log in to the **Apstra GUI** and open the **Blueprint**, then the **Staged** tab.
2. TODO: navigation path.
3. Commit the blueprint changes to push intent to the fabric.

---

# ⚠️ DO NOT CONFIGURE VIA JUNOS CLI

Direct device-level CLI edits raise a **Configuration Deviation anomaly** in Apstra's
continuous validation loop and will be reverted or overwritten to match staged intent.
""",
    },
    "meta": {
        "directory": "knowledge/meta-docs",
        "doc_type": "meta",
        "prefix": "KP-META",
        "resource": "https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing",
        "tags": "[meta, TODO]",
        "extra_frontmatter": "",
        "body": """# Overview

TODO: describe what this document tracks or standardizes.
""",
    },
}


def build_document(template, title, doc_id, generated_by, now):
    frontmatter = [
        "---",
        f"type: {template['doc_type']}",
        f"title: {title}",
        "description: TODO one or two sentences describing what this document establishes.",
        f"resource: {template['resource']}",
        f"tags: {template['tags']}",
        "generated:",
        f"  by: {generated_by}",
        f"  at: {now}",
        f"id: {doc_id}",
        "version: 1.0.0",
    ]
    if template["extra_frontmatter"]:
        frontmatter.append(template["extra_frontmatter"].rstrip("\n"))
    frontmatter.append("---")
    return "\n".join(frontmatter) + "\n\n" + template["body"]


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a validator-passing OKF document skeleton."
    )
    parser.add_argument("kind", choices=sorted(TEMPLATES), help="Document template to use")
    parser.add_argument("slug", help="Filename slug, without the .md extension")
    parser.add_argument("--title", help="Document title (defaults to the slug)")
    parser.add_argument(
        "--prefix",
        help="Override the ID prefix (e.g. KP-RT, KP-PRO) when the domain differs from the type default",
    )
    parser.add_argument(
        "--by",
        default="zed-agent",
        help="Value for generated.by (default: zed-agent)",
    )
    args = parser.parse_args()

    template = TEMPLATES[args.kind]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, ".."))
    knowledge_dir = os.path.join(root_dir, "knowledge")

    docs = collect_documents(knowledge_dir, root_dir)
    next_ids = next_free_ids(docs)

    prefix = args.prefix or template["prefix"]
    if prefix not in next_ids:
        print(f"[-] Unknown ID prefix '{prefix}'. Valid: {', '.join(sorted(next_ids))}")
        return 1
    doc_id = next_ids[prefix]

    slug = args.slug[:-3] if args.slug.endswith(".md") else args.slug
    rel_path = os.path.join(template["directory"], slug + ".md")
    abs_path = os.path.join(root_dir, rel_path)

    if os.path.exists(abs_path):
        print(f"[-] Refusing to overwrite existing document: {rel_path}")
        return 1

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    title = args.title or slug.replace("-", " ").title()
    content = build_document(template, title, doc_id, args.by, now)

    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[+] Created {rel_path} with id {doc_id}.")
    print("[+] Next steps:")
    print("    1. Replace every TODO, including description, resource, and tags.")
    print(f"    2. Link it from {template['directory']}/index.md and bump that index version.")
    print("    3. python tools/okf_manifest.py && python tools/validate_okf.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
