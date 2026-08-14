---
type: meta
title: OKF Specification Tracking and Migration Framework
description: Documents the official Google Cloud Open Knowledge Format (OKF v0.2) specification, how releases are tracked, and how migration is planned.
resource: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
tags: [okf, specifications, standards, migration-planning]
generated:
  by: zed-agent/gemini-3.5-flash
  at: 2026-08-14T12:00:00Z
verified:
  by: human:ckim
  at: 2026-08-14T12:00:00Z
id: KP-META-001
version: 1.0.0
---

# OKF Specification Tracking & Migration Framework

This document serves as meta-knowledge within the repository to define how the official **Google Cloud Open Knowledge Format (OKF)** specifications are adopted, how changes are tracked, and how future migrations are structured.

---

## 1. The OKF Specification

Our JUNOS repository aligns with:
* **Google Cloud OKF v0.2 Specification:** Represents knowledge as lightweight markdown files with YAML frontmatter. This matches human-readability and direct agent ingestion.

### Key Pillars of OKF v0.2
Unlike simple markdown wikis, OKF v0.2 introduces structured, queryable frontmatter metadata to address:
1. **Provenance (`sources`):** Records the materials a concept derives from, including liveness signals like `usage_count` and `last_modified`.
2. **Trust (`generated` and `verified`):** Separates who generated the content (agents or humans) from who verified its correctness (automated processes or human reviewers).
3. **Lifecycle (`status` and `stale_after`):** Documents maturity (`draft | stable | deprecated`) and absolute dates indicating when content becomes stale.
4. **Attested Computations (`Attested Computation`):** Houses runnable computation mappings, parameters, and attesters to verify execution receipts.

---

## 2. Release & Change Tracking

To stay aligned with upstream developments, the core engineering team tracks changes using the following official channels:

| Channel Type | Resource URL | Target Content | Frequency |
|---|---|---|---|
| **Primary (Spec Repository)** | [GCP Knowledge Catalog OKF Spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) | Authoritative, versioned specifications and rules. | Quarterly |
| **Supplemental (Blog)** | [Google Cloud Blog Portal](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) | Conceptual context, high-level roadmaps, and announcements. | Semi-annually |

### Versioning Classification
Upstream specification changes are classified by their impact:
* **Patch (x.x.Y):** Non-breaking adjustments or documentation fixes. *Action: No migration required.*
* **Minor (x.Y.x):** Non-breaking additions of new optional metadata properties or validation types. *Action: Update `tools/validate_okf.py` to support new optional keys if valuable.*
* **Major (Y.x.x):** Breaking structural revisions (e.g., renaming metadata property names or validation rules). *Action: Triggers the Migration Plan.*

---

## 3. Migration Plan (Plan to Plan)

Since future major revisions of the OKF specifications are unknown, we adopt a **proactive, phased meta-plan** to evaluate, adapt, and transition when a major release occurs.

### Phase 1: Impact Assessment
When a major release is detected:
1. Establish a temporary working group/ticket to document differences between the current schema and the target schema.
2. Determine if the changes require metadata translation, structural refactoring, or validator engine logic rewrites.

### Phase 2: Adaptation & Version-Pinning
To prevent repository breakage:
1. Ensure all markdown files continue to explicitly pin their compatible version in YAML frontmatter.
2. Update the validator script (`tools/validate_okf.py`) to run validation conditionally based on the pinned version, enabling **dual-schema support**.

### Phase 3: Migration Codemod Design
Rather than manually updating hundreds of files:
1. Write a bulk migration script (codemod) in `tools/` (e.g., `migrate_okf_v1_v2.py`).
2. The script must parse old formats, map keys/structures to the new specification, and write clean, validated markdown files back to disk.
