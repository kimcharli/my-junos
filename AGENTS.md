# AGENTS.md — Working in this repository

Read this file and [`MANIFEST.md`](MANIFEST.md) before authoring. Together they answer the
questions that would otherwise cost a round of filesystem discovery at the start of every
session: what lives where, what IDs are taken, and what the validator will reject.

**Do not `ls`, `find`, or `grep` the tree to rediscover repository structure or allocated
IDs.** If either file is wrong or stale, fix it as part of your change.

---

## What this repository is

A schema-validated knowledge base of Juniper JUNOS configurations, security audit items, and
Apstra fabric design rules, stored as Markdown with YAML frontmatter per Google's Open
Knowledge Format (OKF) v0.2.

## Repository map

```text
my-junos/
├── AGENTS.md                          # This file: conventions and validator contract
├── MANIFEST.md                        # GENERATED inventory + next free IDs
├── README.md                          # Human-facing overview and integration examples
├── knowledge/                         # All OKF documents (the actual knowledge base)
│   ├── index.md                       # Root portal index
│   ├── apstra/                        # Apstra-orchestrated fabric intent and interop notes
│   ├── base-configs/                  # Golden JUNOS baseline templates
│   ├── audit-items/                   # Compliance / hardening checks
│   └── meta-docs/                     # Internal standards and spec tracking
├── schemas/
│   └── okf-frontmatter-schema.json    # JSON Schema for frontmatter
├── specs/
│   ├── NEXT.md                        # Durable "what's next" pointer, refreshed each session
│   └── *-plan-YYYY-MM-DD.md           # One plan file per batch of work
├── tools/
│   ├── validate_okf.py                # Zero-dependency validator (the gate)
│   ├── okf_manifest.py                # Regenerates MANIFEST.md
│   ├── pre-commit                     # Hook: refresh manifest, then validate
│   └── setup_hooks.sh                 # Installs the hook into .git/hooks
└── .agents/skills/                    # Project-local Zed agent skills
```

`graphify-out/` is untracked local tooling output. Ignore it.

---

## ID allocation

Every document carries a unique `id` matching `^KP-(SYS|SEC|INT|RT|PRO|META)-\d{3}$`.

| Prefix | Domain |
| --- | --- |
| `KP-SYS` | System / base platform services |
| `KP-SEC` | Security hardening and compliance audits |
| `KP-INT` | Integration / fabric orchestration (Apstra) |
| `KP-RT` | Routing protocols and policy |
| `KP-PRO` | Provisioning and lifecycle workflows |
| `KP-META` | Meta: indexes, specs, tracking |

**To claim an ID, read the "Next Free IDs" table in [`MANIFEST.md`](MANIFEST.md).** Do not
grep for `^id:`. IDs are sequential per prefix and never reused.

---

## Frontmatter contract

Required on every document: `type`, `title`, `description`, `resource`, `tags`, `generated`,
`id`, `version`.

```yaml
---
type: Apstra Configuration          # see the type table below
title: Human-readable document title
description: One or two sentences describing what this document establishes.
resource: https://authoritative-source.example/doc
tags: [apstra, dhcp, interop]
generated:
  by: zed-agent/<model>
  at: 2026-08-18T00:00:00Z
verified:                            # optional; object or array of objects
  by: human:ckim
  at: 2026-08-18T00:00:00Z
sources:                             # optional; each entry requires `resource`
  - resource: https://vendor.example/reference
    title: Vendor reference title
id: KP-INT-004
version: 1.0.0                       # semver
---
```

Optional: `status` (`draft` | `stable` | `deprecated`), `stale_after` (`YYYY-MM-DD`),
`verified`, `sources`.

**`timestamp` is not a schema property.** Older drafts and some skill text still reference it;
it is wrong. Use `generated.at`, and `verified.at` for human sign-off.

---

## Document types and the body rules the validator enforces

`tools/validate_okf.py` enforces per-type requirements on the **markdown body** that are not
expressed in the JSON schema. This is the single most common reason a new document fails.

| `type` | Directory | Body requirement enforced by the validator |
| --- | --- | --- |
| `JUNOS Base Config` | `knowledge/base-configs/` | Must contain a ` ```set ` fenced codeblock |
| `JUNOS Audit` | `knowledge/audit-items/` | Must declare `verification_method` and `checks` in frontmatter |
| `Apstra Configuration` | `knowledge/apstra/` | Must contain a ` ```json ` fenced codeblock (the API intent payload) |
| `meta` | anywhere | Index / tracking documents; no body codeblock requirement |

Notes:

* `Apstra Configuration` documents are **controller intent**, not device CLI. Present the REST
  API method/endpoint plus a JSON payload, and a GUI path as the alternative. Include a warning
  against direct Junos CLI edits — Apstra flags them as Configuration Deviation anomalies. Even
  an interop or field-note document of this type still needs a `json` payload block to pass.
* `checks` entries require `name`, `command`, and `expected`; `negate` and `remediation` are
  optional but expected in practice.

---

## Authoring workflow

1. **Plan first for any multi-item batch.** Write `specs/<slug>-plan-YYYY-MM-DD.md` covering
   context, scope rulings (in and out), items, commit sequence, and verification. Commit the
   plan on its own before writing content.
2. **Author** the document(s). Claim IDs from `MANIFEST.md`.
3. **Update the section index** (`knowledge/<section>/index.md`) with a link to the new
   document, and bump that index's `version`.
4. **Validate** before committing:
   ```bash
   python tools/okf_manifest.py      # refresh MANIFEST.md
   python tools/validate_okf.py      # must exit 0
   ```
5. **Commit** in the sequence the plan declares. Conventional Commits (`docs:`, `feat:`).
6. **Refresh `specs/NEXT.md`** so the next session resumes without rediscovery.

---

## ⚠️ Validation is currently manual

This clone has `core.hooksPath` pointed at a user-global hooks directory
(`git config --get core.hooksPath`). When that is set, **git ignores `.git/hooks/` entirely**,
so `tools/setup_hooks.sh` has no effect and `tools/pre-commit` never runs.

Until that is reconciled, **you must run `python tools/validate_okf.py` yourself before every
commit.** Do not assume a hook caught anything. Run `sh tools/setup_hooks.sh` to see whether
the override is active — it reports the conflict rather than failing silently.

---

## Conventions worth preserving

* Documents are portable and self-contained; cross-link with relative Markdown links.
* Prefer authoritative vendor documentation for `resource`. If a behavior is field-verified
  rather than documented, say so plainly in the body instead of inventing a citation.
* Record vendor interop edge cases with their **failure signature** (what the operator actually
  observes), not just the fix. Silent failures are the ones worth writing down.
* Never fabricate API endpoints, CLI syntax, or GUI navigation paths. If unverified, mark it.
