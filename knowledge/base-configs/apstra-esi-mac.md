---
type: JUNOS Base Config
title: Apstra EVPN ESI MAC MSB Configuration
description: Configures the Ethernet Segment Identifier (ESI) MAC Most Significant Byte (MSB) to a unique, even value as required by Apstra reference blueprints.
resource: https://www.juniper.net/documentation/us/en/software/apstra4.1/apstra-user-guide/topics/topic-map/evpn-vxlan-dci.html
tags: [apstra, evpn-vxlan, esi, multihoming]
generated:
  by: zed-agent/gemini-3.5-flash
  at: 2026-08-14T12:00:00Z
verified:
  by: human:ckim
  at: 2026-08-14T12:00:00Z
id: KP-INT-001
version: 1.0.0
---

# JUNOS Configuration Snippet

In an EVPN-VXLAN multi-homing fabric managed by Juniper Apstra, Aggregate Ethernet interfaces participating in LACP-active multi-homing must be configured with identical ESI parameters. The first octet (Most Significant Byte, or MSB) must be an **even value** (default is `02`) to comply with unicast MAC address formatting constraints:

```set
set interfaces ae1 esi 00:02:00:00:00:00:00:00:00:01
set interfaces ae1 esi all-active
```

---

# Apstra Design & Architectural Rationale

### 1. The "Even Value" Unicast Rule
In Ethernet MAC address formatting, the least significant bit (LSB) of the first byte (Most Significant Byte, MSB) is the **Individual/Group (I/G) flag**:
* **0 (Even):** Represents a **Unicast** address.
* **1 (Odd):** Represents a **Multicast/Broadcast** address.

Because the ESI is mapped directly to generate a virtual system MAC address used for LACP negotiation (LACP System ID) between dual-homed switches, **the first byte of the ESI MAC must be an even value** (such as `02`, `04`, or `06`). If an odd value is configured (e.g., `03`), the dual-homed switches will advertise a multicast LACP System ID, causing servers to reject LACP synchronization and blocking port-channel negotiation.

### 2. Uniqueness per Virtual Segment
Each redundant switch pair (ESI segment) within the Apstra fabric blueprint must carry a **unique** ESI value. Using the default `02` prefix and varying the lower octets prevents MAC collision loops and ensures deterministic traffic distribution across all-active link paths.
