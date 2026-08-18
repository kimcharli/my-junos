# OKF Knowledge Manifest

> **Generated file — do not edit by hand.** Regenerate with `python tools/okf_manifest.py`. The pre-commit hook refreshes and stages it automatically.

This is the authoritative inventory of the knowledge base. Read it instead of walking `knowledge/` or grepping frontmatter for `id:`. Authoring conventions and validator rules live in [`AGENTS.md`](AGENTS.md).

## Next Free IDs

Claim the ID listed here when authoring a new document in that domain.

| Prefix | Domain | Next free ID |
| --- | --- | --- |
| `KP-SYS` | System / base platform services | `KP-SYS-003` |
| `KP-SEC` | Security hardening and compliance audits | `KP-SEC-004` |
| `KP-INT` | Integration / fabric orchestration (Apstra) | `KP-INT-005` |
| `KP-RT` | Routing protocols and policy | `KP-RT-001` |
| `KP-PRO` | Provisioning and lifecycle workflows | `KP-PRO-001` |
| `KP-META` | Meta: indexes, specs, tracking | `KP-META-007` |

## Documents

### `knowledge/`

| ID | Type | Title | Version | Document |
| --- | --- | --- | --- | --- |
| `KP-META-002` | meta | JUNOS OKF Knowledge Base Index | `1.0.0` | [`index.md`](knowledge/index.md) |

### `knowledge/apstra/`

| ID | Type | Title | Version | Document |
| --- | --- | --- | --- | --- |
| `KP-INT-003` | Apstra Configuration | Apstra Controller REST API Authentication | `1.0.0` | [`apstra-auth.md`](knowledge/apstra/apstra-auth.md) |
| `KP-INT-004` | Apstra Configuration | Apstra DHCP Relay GIADDR and Windows DHCP Server Interop | `1.0.0` | [`apstra-dhcp-relay-giaddr.md`](knowledge/apstra/apstra-dhcp-relay-giaddr.md) |
| `KP-INT-001` | Apstra Configuration | Apstra EVPN ESI MAC MSB Configuration | `1.0.0` | [`apstra-esi-mac.md`](knowledge/apstra/apstra-esi-mac.md) |
| `KP-INT-002` | Apstra Configuration | Apstra Fabric IP Links MTU Configuration | `1.0.0` | [`apstra-ip-link-mtu.md`](knowledge/apstra/apstra-ip-link-mtu.md) |
| `KP-META-006` | meta | Apstra Fabric Configurations Index | `1.2.0` | [`index.md`](knowledge/apstra/index.md) |

### `knowledge/audit-items/`

| ID | Type | Title | Version | Document |
| --- | --- | --- | --- | --- |
| `KP-META-004` | meta | JUNOS Compliance Audit Items Index | `1.0.0` | [`index.md`](knowledge/audit-items/index.md) |
| `KP-SEC-003` | JUNOS Audit | Ensure No DDoS Protection Packet Drops | `1.0.0` | [`sec-ddos-protection.md`](knowledge/audit-items/sec-ddos-protection.md) |
| `KP-SEC-001` | JUNOS Audit | Enforce Secure SSH Only (Disable Telnet/Plain Services) | `1.0.0` | [`sec-ssh-only.md`](knowledge/audit-items/sec-ssh-only.md) |
| `KP-SEC-002` | JUNOS Audit | Ensure Telnet Management is Disabled | `1.0.0` | [`sec-telnet-disabled.md`](knowledge/audit-items/sec-telnet-disabled.md) |

### `knowledge/base-configs/`

| ID | Type | Title | Version | Document |
| --- | --- | --- | --- | --- |
| `KP-META-003` | meta | JUNOS Base Configurations Index | `1.0.0` | [`index.md`](knowledge/base-configs/index.md) |
| `KP-SYS-001` | JUNOS Base Config | System DNS Servers configuration | `1.0.0` | [`sys-dns.md`](knowledge/base-configs/sys-dns.md) |
| `KP-SYS-002` | JUNOS Base Config | System NTP Synchronization configuration | `1.0.0` | [`sys-ntp.md`](knowledge/base-configs/sys-ntp.md) |

### `knowledge/meta-docs/`

| ID | Type | Title | Version | Document |
| --- | --- | --- | --- | --- |
| `KP-META-005` | meta | OKF Meta Specifications Index | `1.0.0` | [`index.md`](knowledge/meta-docs/index.md) |
| `KP-META-001` | meta | OKF Specification Tracking and Migration Framework | `1.0.0` | [`okf-spec-tracking.md`](knowledge/meta-docs/okf-spec-tracking.md) |

## Summary

* **Total documents:** 15
* **Apstra Configuration:** 4
* **JUNOS Audit:** 3
* **JUNOS Base Config:** 2
* **meta:** 6
