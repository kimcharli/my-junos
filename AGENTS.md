# AGENTS.md — Working in this repository

Schema-validated knowledge base of Juniper JUNOS configs, security audits, and Apstra fabric
design rules: Markdown + YAML frontmatter, Google Open Knowledge Format (OKF) v0.2.

**Do not `ls`, `find`, or `grep` to rediscover structure or IDs.** This file is the map;
[`MANIFEST.md`](MANIFEST.md) is the generated inventory and ID registry. Fix them if stale.

```text
my-junos/
├── MANIFEST.md          # GENERATED: document inventory + next free IDs
├── knowledge/           # All OKF documents
│   ├── apstra/          # Apstra controller intent and interop notes
│   ├── base-configs/    # Golden JUNOS baseline templates
│   ├── audit-items/     # Compliance / hardening checks
│   └── meta-docs/       # Internal standards and spec tracking
├── schemas/             # okf-frontmatter-schema.json
├── specs/               # NEXT.md pointer, plan files, decision records
└── tools/               # okf_new.py, okf_manifest.py, validate_okf.py
```

## Authoring workflow

1. **Plan first for multi-item batches**: write `specs/<slug>-plan-YYYY-MM-DD.md` (context,
   scope rulings, items, commit sequence, verification) and commit it before writing content.
2. **Scaffold** — never hand-write frontmatter:
   ```bash
   python tools/okf_new.py {base-config|audit|apstra|meta} <slug> --title "..."
   ```
   It claims the next free ID and stamps every required field and body stub. Add
   `--prefix KP-RT|KP-PRO` when the domain differs from the type default.
3. **Write the body**, replacing every `TODO`.
4. **Link it** from `knowledge/<section>/index.md` and bump that index's `version`.
5. **Validate** — this is the gate, and it is manual (see below):
   ```bash
   python tools/okf_manifest.py && python tools/validate_okf.py
   ```
6. **Commit** per the plan's sequence (Conventional Commits), then refresh `specs/NEXT.md`.

## Gotchas that cost a round trip

* `timestamp` is **not** a schema property. `generated` (object: `by`, `at`) is required.
  Scaffolding avoids this entirely.
* The validator enforces **body** rules absent from the JSON schema: `JUNOS Base Config` needs a
  ` ```set ` block; `Apstra Configuration` needs a ` ```json ` block (**including** interop and
  field-note documents); `JUNOS Audit` needs `verification_method` + `checks` in frontmatter.
* `core.hooksPath` is set globally, so git ignores `.git/hooks/` and `tools/pre-commit` **never
  runs**. Nothing validates on your behalf — run step 5 yourself. `sh tools/setup_hooks.sh`
  reports the conflict.

## Conventions

* Apstra documents are **controller intent**, not device CLI; always warn against direct Junos
  CLI edits (Apstra raises Configuration Deviation anomalies).
* Record interop edge cases with their **failure signature** — what the operator observes — not
  just the fix. Silent failures are the ones worth writing down.
* Never fabricate API endpoints, CLI syntax, or GUI paths. If unverified, say so in the body.

## Deeper references (read only when relevant)

* Authoring templates and per-type detail: the `junos-okf` and `knowledge-builder` skills.
* Why docs are split across `AGENTS.md` / skills / `MANIFEST.md`, and the context-budget rules
  governing what may be added here: [`specs/context-budget-decision-2026-08-18.md`](specs/context-budget-decision-2026-08-18.md).
