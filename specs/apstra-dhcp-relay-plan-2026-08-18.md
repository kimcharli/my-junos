# Apstra DHCP Relay GIADDR OKF Documentation Plan - 2026-08-18

- **Status**: Approved by NetOps Lead on 2026-08-18. Executing in current session.
- **Context**: Apstra-generated DHCP relay configurations source relay packets from the routing-instance (VRF) `lo0` address, which becomes the GIADDR seen by the DHCP server. Microsoft Windows DHCP Server rejects any GIADDR that does not fall inside an active scope range, treating the relay as a rogue agent. This interop edge case has caused silent DHCP failures in the field and must be captured as durable knowledge.

## Scope Rulings
- **In-Scope**:
  - `knowledge/apstra/apstra-dhcp-relay-giaddr.md`: OKF document describing the Apstra DHCP relay GIADDR sourcing behavior, the Windows DHCP Server rogue-relay edge case, and the authorization-scope workaround.
  - `knowledge/apstra/index.md`: Reference link to the newly added document.
  - `specs/NEXT.md`: Pointer refresh.
  - Verification using `python tools/validate_okf.py`.
- **Out-of-Scope**:
  - Windows Server DHCP automation (PowerShell scope provisioning scripts).
  - Changing the Apstra relay source-address selection behavior itself; it is not operator-tunable per-VRF.
  - ISC / Infoblox / Cisco DHCP server behavior, which does not enforce the same GIADDR check.

## Items to Execute
- `knowledge/apstra/apstra-dhcp-relay-giaddr.md`:
  - Frontmatter conformant with the `Apstra Configuration` type.
  - Sequential ID `KP-INT-004`, version `1.0.0`.
  - `sources` entries for the Juniper Apstra DHCP relay documentation and the Microsoft DHCP scope documentation.
  - Body sections: Apstra relay behavior and GIADDR derivation, the Windows Server rogue-relay edge case, the authorization-scope remediation procedure, Junos-side verification commands, and the standard Apstra CLI-drift warning.
- `knowledge/apstra/index.md`:
  - Bulleted reference linking to `apstra-dhcp-relay-giaddr.md`; version bump.

## Commit Sequence
1. **Commit 1**: Add the plan file (`specs/apstra-dhcp-relay-plan-2026-08-18.md`) and update the pointer file (`specs/NEXT.md`).
2. **Commit 2**: Add `knowledge/apstra/apstra-dhcp-relay-giaddr.md` and update `knowledge/apstra/index.md`.

## Verification
- Execution of `python tools/validate_okf.py` returns exit code 0 (all checks pass successfully).
