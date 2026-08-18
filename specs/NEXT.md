# NEXT

- **Active Goal**: Incremental authoring of JUNOS baseline configs, Apstra fabric intent, and security audit items.
- **Completed**: OKF framework layout, schemas, validation engine, and initial baseline configs / security audit items. Added Apstra REST API authentication baselines (August 17, 2026). Added Apstra DHCP relay GIADDR / Windows DHCP Server interop knowledge, `AGENTS.md` + generated `MANIFEST.md`, and the `okf_new.py` scaffolder so sessions start without filesystem discovery (August 18, 2026).
- **Plan File**: `specs/agent-context-bootstrap-plan-2026-08-18.md` (Successfully executed)
- **Start Here**: `AGENTS.md` for the workflow, `MANIFEST.md` for the next free `KP-*` ID. Scaffold new documents with `python tools/okf_new.py`; do not hand-write frontmatter.
- **Decision Records**: `specs/context-budget-decision-2026-08-18.md` governs what may be added to `AGENTS.md` and why detail belongs in skills instead. Read before growing the always-injected context.
- **Open Item**: `core.hooksPath` is set globally to `~/.config/git/hooks`, so `.git/hooks/` is bypassed and `tools/pre-commit` never runs. Validation is manual until this is reconciled. `sh tools/setup_hooks.sh` reports the conflict.
- **Prior Plans**: `specs/apstra-dhcp-relay-plan-2026-08-18.md` (Successfully executed), `specs/apstra-auth-plan-2026-08-17.md` (Successfully executed), `specs/junos-okf-plan-2026-08-14.md` (Successfully executed)
