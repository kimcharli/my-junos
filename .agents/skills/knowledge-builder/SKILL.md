---
name: knowledge-builder
description: Analyzes raw, incoming configurations or operational checklists and converts them into validated, incremental OKF-compliant Markdown files.
---

# Knowledge Conversion & Ingestion

Use this skill when you receive new, raw, or unstructured configuration items, checklists, or compliance rules, and need to translate and append them incrementally to the OKF knowledge base.

---

## 1. Input Analysis

1. **Classify Knowledge Type:**
   * **Base Configuration:** If the input defines recommended CLI commands or standard templates (e.g., Syslog configurations, interface configurations).
   * **Compliance Audit:** If the input defines rules, states, or compliance patterns to verify (e.g., checking if SNMPv2 is disabled).
2. **Assign a Unique ID:** Locate the latest assigned IDs in the repository, and generate a new sequential ID (e.g., `KP-SYS-003`, `KP-SEC-003`).

---

## 2. Document Construction

Generate a single Markdown file matching the Google OKF v0.1 format:

### A. For Base Configurations
* Create the file under `knowledge/base-configs/<slug>.md`.
* Compile the required frontmatter:
  ```yaml
  type: JUNOS Base Config
  title: [Descriptive Title]
  description: [Detailed description]
  resource: [Official Documentation Link]
  tags: [tags, list]
  timestamp: [ISO-8601 Timestamp]
  id: KP-SYS-XXX
  version: 1.0.0
  ```
* In the body, document the configuration and wrap the commands cleanly inside a ` ```set ` block.

### B. For Compliance Audits
* Create the file under `knowledge/audit-items/<slug>.md`.
* Compile the required frontmatter including the audit directives:
  ```yaml
  type: JUNOS Audit
  title: [Descriptive Title]
  description: [Detailed description]
  resource: [Official Link]
  tags: [tags, list]
  timestamp: [ISO-8601 Timestamp]
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

---

## 3. Post-Ingestion Quality Assurance

1. Save the newly constructed `.md` file.
2. Run the offline validator to ensure the new file is fully conformant:
   ```bash
   python tools/validate_okf.py
   ```
3. Fix any schema errors before finalizing the ingestion.
