# JUNOS Open Knowledge Format (OKF) Repository

> ⚠️ **UNDER CONSTRUCTION:** This repository is currently in the bootstrapping and initialization phase. It is under active development and is **NOT** a finalized production-ready repository. All configuration models and compliance audit structures are experimental and subject to change.

A structured, modular, and schema-validated repository for Juniper JUNOS configurations and security/operational compliance audits. 

This repository aligns with **Google Cloud's Open Knowledge Format (OKF v0.1)** standard, representing key knowledge concepts as **portable, human-readable Markdown files with structured YAML frontmatter**.

---

## Directory Structure

```text
my-junos/
├── schemas/
│   └── okf-frontmatter-schema.json    # Schema validating OKF v0.1 frontmatter
├── knowledge/
│   ├── base-configs/                  # Base configuration templates in Markdown
│   │   ├── sys-dns.md
│   │   └── sys-ntp.md
│   ├── audit-items/                   # Compliance/hardening audit checks
│   │   ├── sec-ssh-only.md
│   │   └── sec-telnet-disabled.md
│   └── meta-docs/                     # Meta-knowledge and tracking specifications
│       └── okf-spec-tracking.md
├── tools/
│   └── validate_okf.py                # Offline zero-dependency CLI validator
└── README.md                          # Repository overview and integration docs
```

---

## The OKF v0.1 Format

In accordance with OKF v0.1:
1. **Just Markdown:** Readable on any device, editable in any editor, and native to GitHub or local LLM contexts.
2. **Just Files:** Portable concept files linked together with normal markdown links `[Title](/path/to/file.md)`.
3. **Structured Frontmatter:** Frontmatter stores queryable fields: `type`, `title`, `description`, `resource`, `tags`, and `timestamp`.

### Concept Document Example (`knowledge/base-configs/sys-dns.md`)
```markdown
---
type: JUNOS Base Config
title: System DNS Servers configuration
description: Configures standard domain name resolution servers for name lookups.
resource: https://www.juniper.net/documentation/us/en/software/junos/user-access/topics/topic-map/dns-service-configuring.html
tags: [dns, name-resolution, system-services]
timestamp: 2026-08-14T12:00:00Z
id: KP-SYS-001
version: 1.0.0
---

# JUNOS Configuration Snippet

```set
set system name-server 8.8.8.8
set system name-server 1.1.1.1
```
```

---

## Adding Incremental Items

Adding new JUNOS knowledge items is simple:

### 1. Adding a Base Configuration
Create a new Markdown file in `knowledge/base-configs/` (e.g., `syslog-config.md`). Include the mandatory frontmatter fields with `type: JUNOS Base Config` and write your configuration commands within a ` ```set ... ``` ` block.

### 2. Adding an Audit Check
Create a new Markdown file in `knowledge/audit-items/` (e.g., `snmp-hardened.md`). Set `type: JUNOS Audit`, and declare `verification_method` (either `cli-regex` or `xml-xpath`) along with your array of `checks` in the frontmatter.

---

## Running Validation

The repository includes a zero-dependency Python script to validate your markdown files recursively. It validates frontmatter against `schemas/okf-frontmatter-schema.json` and ensures proper JUNOS codeblock constraints.

Run the validation suite:
```bash
python tools/validate_okf.py
```

---

## Automation Pipeline Integration

Since the data is stored in standard Markdown and structured YAML, it acts as a modular single-source-of-truth for deployment engines:

### Ansible Integration
Your Ansible playbooks can parse frontmatter or ingest the underlying `.md` files to extract the set commands:
```yaml
- name: Extract set configuration from OKF Markdown
  ansible.builtin.shell: |
    sed -n '/^```set/,/^```/p' "knowledge/base-configs/sys-dns.md" | grep -v '```'
  register: config_set_commands

- name: Apply Golden Base Configuration to Juniper Device
  junipernetworks.junos.junos_config:
    lines: "{{ config_set_commands.stdout_lines }}"
    format: set
```

### PyEZ Integration
Python scripts can read the YAML frontmatter of your `JUNOS Audit` documents and execute compliance checks over NETCONF:
```python
import re
from jnpr.junos import Device

# Parse checks from a compliance audit .md file...
# Run commands on device and assert output matches 'expected' pattern
```
