---
name: junos-okf
description: Guidelines and specifications for authoring JUNOS base configurations, Apstra fabric intent, and compliance audits in Google OKF v0.2 format.
---

# JUNOS OKF v0.2 Authoring & Validation

Use this skill whenever you are tasked with creating, editing, validating, or migrating JUNOS base configurations, Apstra fabric intent, operational/security audits, or meta-spec documents in this repository.

> **Read [`AGENTS.md`](../../../AGENTS.md) and [`MANIFEST.md`](../../../MANIFEST.md) first.** They are the authoritative repo map, frontmatter contract, and ID registry. This skill covers authoring technique; those files cover the current state of the repo. Do not `ls`, `find`, or `grep` to rediscover either.

---

## 1. Document Structure & Layout

Every knowledge concept is stored as a **single Markdown (.md) file** in the `knowledge/` directory:
* **Base Configurations:** Stored in `knowledge/base-configs/`.
* **Security & Compliance Audits:** Stored in `knowledge/audit-items/`.
* **Apstra Fabric Intent:** Stored in `knowledge/apstra/`.
* **Meta Specifications:** Stored in `knowledge/meta-docs/`.

Claim the document `id` from the **Next Free IDs** table in `MANIFEST.md`.

---

## 2. Formatting Specifications

All documents require: `type`, `title`, `description`, `resource`, `tags`, `generated`, `id`, `version`.
`generated` is an object (`by`, `at`); `verified` and `sources` are optional. **`timestamp` is not a schema property — do not emit it.**

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
generated:
  by: zed-agent/<model>
  at: 2026-08-14T12:00:00Z
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
generated:
  by: zed-agent/<model>
  at: 2026-08-14T12:00:00Z
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

### C. Apstra Configuration File (e.g., `knowledge/apstra/apstra-esi-mac.md`)
Must contain:
1. **YAML Frontmatter** with `type: Apstra Configuration`.
2. **Markdown Body** containing a ` ```json ` codeblock carrying the controller intent payload, alongside the REST method and endpoint.
3. A GUI navigation alternative and a warning against direct Junos CLI edits (Apstra raises Configuration Deviation anomalies on out-of-band changes).

The `json` codeblock is mandatory for this type — including for interop and field-note documents.

---

## 3. Local Validation & Testing

Always execute the offline tools to verify your changes before committing:

```bash
python tools/okf_manifest.py      # refresh MANIFEST.md
python tools/validate_okf.py      # must exit 0
```

Ensure validation returns `Total Errors Found: 0` and exits with `0`. Do not commit files that violate `schemas/okf-frontmatter-schema.json`.

Note: this clone sets `core.hooksPath` to a user-global directory, so `.git/hooks/` is bypassed and the repo pre-commit hook does **not** run. Validation is manual — see the warning section in `AGENTS.md`.

---

## 4. Spec Updates & Migration Guidelines

Our design utilizes a "Plan to Plan" migration roadmap:
1. **Never Break Backwards Compatibility:** Always pin the specification version (e.g., `version: 1.0.0`) in the YAML frontmatter.
2. **Dual Schema Support:** If the upstream OKF spec publishes a breaking update, update `tools/validate_okf.py` to support *both* formats dynamically based on the file's pinned `version`.
3. **Automated Migration Scripting:** Design automated codemods/scripts in `tools/` (e.g. `migrate_okf_v1_v2.py`) to automate bulk upgrades of files rather than doing manual edits.
