---
name: okf-release-check
description: Guides agents on tracking upstream OKF (Frictionless Data & Google OKF) spec updates and formulating plan-to-plan migration paths.
---

# OKF Specification Tracking & Migration Planning

Use this skill when checking for changes or updates in upstream **Open Knowledge Format (OKF)** / **Frictionless Data** or **Google Cloud OKF v0.1** specifications, or when structuring a plan-to-plan migration strategy.

---

## 1. Upstream Spec Analysis

1. **Verify Official Sources:** Query or inspect the official channels:
   * **Frictionless Data Spec Portal:** [https://specs.frictionlessdata.io/](https://specs.frictionlessdata.io/)
   * **Specs GitHub Repository:** [https://github.com/frictionlessdata/specs](https://github.com/frictionlessdata/specs)
   * **Google Cloud Data Blog:** [https://cloud.google.com/blog/products/data-analytics](https://cloud.google.com/blog/products/data-analytics)
2. **Compare Active Schema:** Examine our local schemas (e.g., `schemas/okf-frontmatter-schema.json`) to map differences in metadata parameters or requirements.
3. **Assess Impact Level:**
   * **Backward-Compatible (Patch/Minor):** Add optional key validation.
   * **Breaking Change (Major):** Triggers the Migration Plan (Phase 2).

---

## 2. "Plan-to-Plan" Migration Strategy

When a breaking major specification change is identified, do not execute bulk manual edits immediately. Instead, outline a "plan-to-plan" adaptation structure:

### Phase A: Schema Version Pinning
Ensure all current files explicitly preserve their target version identifier in their metadata frontmatter (e.g., `version: 1.0.0`).

### Phase B: Dual-Schema Parser Adaptations
Update the local parsing engine (e.g., `tools/validate_okf.py`) to parse and validate files dynamically according to their specified version, allowing legacy and modern specification versions to seamlessly co-exist.

### Phase C: Automated Migration Codemod
Rather than manually updating many files, draft an automated script (e.g., `tools/migrate_okf_v1_v2.py`) that reads old yaml/markdown formats, translates key/value specifications to the modern syntax, and writes compliant files back to disk.

### Phase D: CI/CD Guardrails & Deprecation
Enable automated testing to block new pull requests using deprecated specifications. Once all files are fully migrated, cleanly remove the legacy validation logic.
