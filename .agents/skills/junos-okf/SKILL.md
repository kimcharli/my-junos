---
name: junos-okf
description: Guidelines and specifications for authoring JUNOS base configurations and compliance audits in Google OKF v0.1 format.
---

# JUNOS OKF v0.1 Authoring & Validation

Use this skill whenever you are tasked with creating, editing, validating, or migrating JUNOS base configurations, operational/security audits, or meta-spec documents in this repository.

---

## 1. Document Structure & Layout

Every knowledge concept is stored as a **single Markdown (.md) file** in the `knowledge/` directory:
* **Base Configurations:** Stored in `knowledge/base-configs/`.
* **Security & Compliance Audits:** Stored in `knowledge/audit-items/`.
* **Meta Specifications:** Stored in `knowledge/meta-docs/`.

---

## 2. Formatting Specifications

### A. Base Configuration File (e.g., `knowledge/base-configs/sys-dns.md`)
Must contain:
1. **YAML Frontmatter** with `type: JUNOS Base Config`.
2. **Markdown Body** containing a single valid ` ```set ` codeblock containing JUNOS set commands.

```markdown
---
type: JUNOS Base Config
title: System DNS Servers configuration
description: Configures standard domain name resolution servers.
resource: https://www.juniper.net/documentation/...
tags: [dns, system]
timestamp: 2026-08-14T12:00:00Z
id: KP-SYS-001
version: 1.0.0
---

# DNS Configuration

```set
set system name-server 8.8.8.8
```
```

### B. Audit File (e.g., `knowledge/audit-items/sec-ssh-only.md`)
Must contain:
1. **YAML Frontmatter** with `type: JUNOS Audit`.
2. Explicit `verification_method` (`xml-xpath` or `cli-regex`).
3. An array of `checks` mapping commands, expected outcomes, optional negation, and remediation commands.

```markdown
---
type: JUNOS Audit
title: Enforce Secure SSH Only
description: Ensures insecure telnet is disabled.
resource: https://www.juniper.net/documentation/...
tags: [ssh, telnet]
timestamp: 2026-08-14T12:00:00Z
id: KP-SEC-001
version: 1.0.0
verification_method: xml-xpath
checks:
  - name: Ensure SSH Service is enabled
    command: show configuration system services | display xml
    expected: /configuration/system/services/ssh
    negate: false
    remediation: set system services ssh
---

# SSH Audit Documentation

This audit rule is enforced to...
```

---

## 3. Local Validation & Testing

Always execute the offline validator tool to verify your changes before submitting:

```bash
python tools/validate_okf.py
```

Ensure validation returns `Total Errors Found: 0` and exits with `0`. Do not commit files that violate the schemas in `schemas/okf-frontmatter-schema.json`.

---

## 4. Spec Updates & Migration Guidelines

Our design utilizes a "Plan to Plan" migration roadmap:
1. **Never Break Backwards Compatibility:** Always pin the specification version (e.g., `version: 1.0.0`) in the YAML frontmatter.
2. **Dual Schema Support:** If the upstream OKF spec publishes a breaking update, update `tools/validate_okf.py` to support *both* formats dynamically based on the file's pinned `version`.
3. **Automated Migration Scripting:** Design automated codemods/scripts in `tools/` (e.g. `migrate_okf_v1_v2.py`) to automate bulk upgrades of files rather than doing manual edits.
