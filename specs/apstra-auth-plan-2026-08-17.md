# Apstra Authentication OKF Documentation Plan - 2026-08-17

- **Status**: Approved by NetOps Lead on 2026-08-17. Executing in current session.
- **Context**: Standardizes the authentication process for the Juniper Apstra REST API using the Open Knowledge Format (OKF) v0.2 standard. This ensures NetOps teams have a schema-validated, single source of truth for authenticating against the Apstra Controller.

## Scope Rulings
- **In-Scope**:
  - `knowledge/apstra/apstra-auth.md`: Standard OKF document mapping the `POST /api/aaa/login` request payload, response schema, and necessary `AuthToken` authorization header.
  - `knowledge/apstra/index.md`: Reference links to the newly added authentication documentation.
  - Verification using `python tools/validate_okf.py`.
- **Out-of-Scope**:
  - Implementation of live API clients, software clients, or active credential management in this repository.

## Items to Execute
- `knowledge/apstra/apstra-auth.md`:
  - Frontmatter schema properties conformant with `Apstra Configuration` type.
  - Sequential ID `KP-INT-003`.
  - JSON payload codeblock in the markdown body showing username/password credentials login request.
  - Clear sections highlighting endpoint, response status, headers, and architectural context.
- `knowledge/apstra/index.md`:
  - Bulleted reference linking to the newly added `apstra-auth.md`.

## Commit Sequence
1. **Commit 1**: Add the plan file (`specs/apstra-auth-plan-2026-08-17.md`) and update the pointer file (`specs/NEXT.md`).
2. **Commit 2**: Add `knowledge/apstra/apstra-auth.md` and update `knowledge/apstra/index.md`.

## Verification
- Execution of `python tools/validate_okf.py` returns exit code 0 (all checks pass successfully).
