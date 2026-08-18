---
name: knowledge-builder
description: Analyzes raw, incoming configurations or operational checklists and converts them into validated, incremental OKF-compliant Markdown files.
---

# Knowledge Conversion & Ingestion

Use this skill when you receive new, raw, or unstructured configuration items, checklists, or compliance rules, and need to translate and append them incrementally to the OKF knowledge base.

> **Read [`AGENTS.md`](../../../AGENTS.md) and [`MANIFEST.md`](../../../MANIFEST.md) first.** They hold the repo map, the frontmatter contract, the per-type body rules the validator enforces, and the ID registry. Do not `ls`, `find`, or `grep` the tree to rediscover any of it.

---

## 1. Input Analysis

1. **Classify Knowledge Type:**
   * **Base Configuration:** Input defines recommended CLI commands or standard templates (e.g., syslog, interface configuration).
   * **Compliance Audit:** Input defines rules, states, or patterns to verify (e.g., checking that SNMPv2 is disabled).
   * **Apstra Configuration:** Input concerns fabric-wide intent orchestrated by the Apstra controller, or a vendor interop behavior affecting an Apstra-managed fabric.
2. **Assign a Unique ID:** Take it from the **Next Free IDs** table in `MANIFEST.md`. Do not grep for `^id:`.

---

## 2. Document Construction

Generate a single Markdown file in Google OKF v0.2 format. Required frontmatter on every type: `type`, `title`, `description`, `resource`, `tags`, `generated`, `id`, `version`. `generated` is an object with `by` and `at`. **`timestamp` is not a schema property — emitting it will not satisfy the required `generated` field.**

### A. For Base Configurations
* Create the file under `knowledge/base-configs/<slug>.md`.
  ```yaml
  type: JUNOS Base Config
  title: [Descriptive Title]
  description: [Detailed description]
  resource: [Official Documentation Link]
  tags: [tags, list]
  generated:
    by: zed-agent/<model>
    at: [ISO-8601 Timestamp]
  id: KP-SYS-XXX
  version: 1.0.0
  ```
* In the body, document the configuration and wrap the commands cleanly inside a ` ```set ` block. **Required by the validator.**

### B. For Compliance Audits
* Create the file under `knowledge/audit-items/<slug>.md`.
  ```yaml
  type: JUNOS Audit
  title: [Descriptive Title]
  description: [Detailed description]
  resource: [Official Link]
  tags: [tags, list]
  generated:
    by: zed-agent/<model>
    at: [ISO-8601 Timestamp]
  id: KP-SEC-XXX
  version: 1.0.0
  verification_method: [cli-regex or xml-xpath]
  checks:
    - name: [Name of check]
      command: [CLI command to run]
      expected: [Expected output regex or xpath element]
      negate: [true or false]
      remediation: [CLI set/delete commands to correct drift]
  ```
* In the body, write human-readable documentation explaining the secure design rationale.

### C. For Apstra Configurations
* Create the file under `knowledge/apstra/<slug>.md` with `type: Apstra Configuration` and an `KP-INT-XXX` id.
* In the body, present the REST method and endpoint, a ` ```json ` intent payload block (**required by the validator, including for interop field notes**), a GUI navigation alternative, and a warning against direct Junos CLI edits.
* When recording a vendor interop edge case, document the **failure signature** the operator actually observes, not just the remediation.

---

## 3. Post-Ingestion Quality Assurance

1. Save the newly constructed `.md` file.
2. Link it from the section index (`knowledge/<section>/index.md`) and bump that index's `version`.
3. Regenerate the manifest and run the validator:
   ```bash
   python tools/okf_manifest.py
   python tools/validate_okf.py
   ```
4. Fix any schema or body-rule errors before finalizing the ingestion. Validation is manual in this clone — `core.hooksPath` is overridden, so the repo pre-commit hook does not run.
