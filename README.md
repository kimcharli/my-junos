# JUNOS Open Knowledge Format (OKF) Repository

> ⚠️ **UNDER CONSTRUCTION:** This repository is currently in the bootstrapping and initialization phase. It is under active development and is **NOT** a finalized production-ready repository. All configuration models and compliance audit structures are experimental and subject to change.

A structured, modular, and schema-validated repository for Juniper JUNOS configurations and security/operational compliance audits. 

This repository aligns with **Google Cloud's Open Knowledge Format (OKF v0.2)** standard, representing key knowledge concepts as **portable, human-readable Markdown files with structured YAML frontmatter**.

> **Contributing (humans and agents):** read [`AGENTS.md`](AGENTS.md) for the authoring contract and
> [`MANIFEST.md`](MANIFEST.md) for the document inventory and next free `KP-*` IDs.

---

## Directory Structure

```text
my-junos/
├── AGENTS.md                          # Authoring contract: layout, IDs, validator rules
├── MANIFEST.md                        # GENERATED inventory + next free IDs
├── schemas/
│   └── okf-frontmatter-schema.json    # Schema validating OKF v0.2 frontmatter
├── knowledge/
│   ├── apstra/                        # Apstra fabric intent and interop notes
│   │   ├── apstra-auth.md
│   │   ├── apstra-dhcp-relay-giaddr.md
│   │   ├── apstra-esi-mac.md
│   │   └── apstra-ip-link-mtu.md
│   ├── base-configs/                  # Base configuration templates in Markdown
│   │   ├── sys-dns.md
│   │   └── sys-ntp.md
│   ├── audit-items/                   # Compliance/hardening audit checks
│   │   ├── sec-ddos-protection.md
│   │   ├── sec-ssh-only.md
│   │   └── sec-telnet-disabled.md
│   └── meta-docs/                     # Meta-knowledge and tracking specifications
│       └── okf-spec-tracking.md
├── specs/                             # Plan files and the NEXT.md session pointer
├── tools/
│   ├── validate_okf.py                # Offline zero-dependency CLI validator
│   ├── okf_new.py                    # Scaffolds a new document with next free ID
│   ├── okf_manifest.py               # Regenerates MANIFEST.md
│   ├── pre-commit                     # Hook: refresh manifest, then validate
│   └── setup_hooks.sh                 # Installs the hook into .git/hooks
└── README.md                          # Repository overview and integration docs
```

---

## The OKF v0.2 Format

In accordance with OKF v0.2:
1. **Just Markdown:** Readable on any device, editable in any editor, and native to GitHub or local LLM contexts.
2. **Just Files:** Portable concept files linked together with normal markdown links `[Title](/path/to/file.md)`.
3. **Structured Frontmatter:** Frontmatter stores queryable fields: `type`, `title`, `description`, `resource`, `tags`, `generated`, `id`, and `version`.

### Concept Document Example (`knowledge/base-configs/sys-dns.md`)
```markdown
---
type: JUNOS Base Config
title: System DNS Servers configuration
description: Configures standard domain name resolution servers for name lookups.
resource: https://www.juniper.net/documentation/us/en/software/junos/user-access/topics/topic-map/dns-service-configuring.html
tags: [dns, name-resolution, system-services]
generated:
  by: zed-agent/<model>
  at: 2026-08-14T12:00:00Z
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

Scaffold the document rather than hand-writing frontmatter — the generator claims the next free
ID from [`MANIFEST.md`](MANIFEST.md) and emits a skeleton that already passes validation:

```bash
python tools/okf_new.py base-config sys-syslog --title "System Syslog Configuration"
python tools/okf_new.py audit sec-snmp-hardened --title "SNMPv2 Disabled"
python tools/okf_new.py apstra apstra-dhcp-relay-giaddr --title "Apstra DHCP Relay GIADDR"
python tools/okf_new.py meta okf-spec-tracking --title "OKF Spec Tracking"
```

Then replace every `TODO`, link the document from its section `index.md`, and validate.

### 1. Base Configuration
Lands in `knowledge/base-configs/` with `type: JUNOS Base Config`; write your commands inside the ` ```set ... ``` ` block.

### 2. Audit Check
Lands in `knowledge/audit-items/` with `type: JUNOS Audit`; fill in `verification_method` (`cli-regex` or `xml-xpath`) and the `checks` array.

### 3. Apstra Fabric Intent
Lands in `knowledge/apstra/` with `type: Apstra Configuration`; supply the REST endpoint and the ` ```json ... ``` ` intent payload.

---

## Running Validation

The repository includes zero-dependency Python scripts. `okf_manifest.py` regenerates the inventory; `validate_okf.py` validates frontmatter against `schemas/okf-frontmatter-schema.json` and enforces per-type JUNOS/Apstra codeblock constraints.

```bash
python tools/okf_manifest.py      # refresh MANIFEST.md
python tools/validate_okf.py      # must exit 0
```

`tools/pre-commit` runs both automatically, but note that if `core.hooksPath` is set in your git
config, git bypasses `.git/hooks/` and the hook will not run. `sh tools/setup_hooks.sh` reports
this conflict. When it applies, run the two commands above manually before each commit.

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
