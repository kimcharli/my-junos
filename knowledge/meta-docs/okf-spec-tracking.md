---
type: meta
title: OKF Specification Tracking and Migration Framework
description: Documents the official Open Knowledge Format (Frictionless Data & Google OKF v0.1) specification, how releases are tracked, and how migration is planned.
resource: https://specs.frictionlessdata.io/
tags: [okf, specifications, standards, migration-planning]
timestamp: 2026-08-14T12:00:00Z
id: KP-META-001
version: 1.0.0
---

# OKF Specification Tracking & Migration Framework

This document serves as meta-knowledge within the repository to define how the official **Open Knowledge Format (OKF)** / **Frictionless Data** and **Google Cloud OKF v0.1** specifications are adopted, how changes are tracked, and how future migrations are structured.

---

## 1. The OKF Specifications

Our JUNOS repository aligns with both:
* **Google Cloud OKF v0.1 Specification:** Represents knowledge as lightweight markdown files with YAML frontmatter. This matches human-readability and direct agent ingestion.
* **Frictionless Data Specifications:** Defines how multiple files/assets are grouped and packaged (Data Packages).

---

## 2. Release & Change Tracking

To stay aligned with upstream developments, the core engineering team tracks changes using the following official channels:

| Resource | Target Content | Frequency |
|---|---|---|
| [Google Cloud Blog](https://cloud.google.com/blog/products/data-analytics) | Official announcements regarding Google OKF schema versions. | Semi-annually |
| [Official Specs Portal](https://specs.frictionlessdata.io/) | Core Frictionless Specs documentation and standards. | Semi-annually |
| [Specs GitHub Repository](https://github.com/frictionlessdata/specs) | Active proposals (RFPs), issues, and release logs. | Quarterly |

### Versioning Classification
Upstream specification changes are classified by their impact:
* **Patch (x.x.Y):** Non-breaking adjustments or documentation fixes. *Action: No migration required.*
* **Minor (x.Y.x):** Non-breaking additions of new optional metadata properties or validation types. *Action: Update `tools/validate_okf.py` to support new optional keys if valuable.*
* **Major (Y.x.x):** Breaking structural revisions (e.g., changing metadata property names or validation rules). *Action: Triggers the Migration Plan.*

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
