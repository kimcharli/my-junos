---
type: Apstra Configuration
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

# Apstra REST API Intent Payload

To configure the ESI MAC MSB prefix in an Apstra fabric, the setting must be orchestrated directly on the **Apstra Controller** (not on individual device CLIs) to maintain fabric-wide intent alignment.

### HTTP Method & Endpoint
* **Method:** `PATCH`
* **Path:** `/api/blueprints/<blueprint_id>/fabric-settings`

### JSON Payload
```json
{
  "esi_mac_msb": 8
}
```

*(Where `8` represents a unique, even integer used as the ESI MAC first-octet prefix).*

---

# Alternative GUI Configuration Path

1. Log in to the **Apstra GUI**.
2. Navigate to your active **Blueprint** and click the **Staged** tab.
3. Click on **Settings** and scroll to **Fabric Settings / Fabric Policy**.
4. Edit the policy and configure **ESI MAC MSB** (typically defaults to `2`) to a unique, even value (e.g., `8`).
5. Commit the blueprint changes to push the intent down to the fabric.

---

# ⚠️ WARNING: DO NOT CONFIGURE VIA JUNOS CLI

In an intent-based networking (IBN) platform like Apstra, **direct out-of-band device-level CLI edits are strictly forbidden**:
* **Configuration Deviation Anomaly:** If you run `set interfaces ae1 esi 00:02:...` directly on a switch console, Apstra's continuous validation loop will immediately detect a **Configuration Deviation anomaly**.
* **Automatic Overwrite:** Apstra acts as the authoritative config source and will flag the CLI edit as an unauthorized drift, notifying operators or automatically overwriting the manual CLI changes to restore the switch to its approved staged intent.

---

# Apstra Design & Architectural Rationale

### 1. The "Even Value" Unicast Rule
In Ethernet MAC address formatting, the least significant bit (LSB) of the first byte (Most Significant Byte, MSB) is the **Individual/Group (I/G) flag**:
* **0 (Even):** Represents a **Unicast** address.
* **1 (Odd):** Represents a **Multicast/Broadcast** address.

Because the ESI is mapped directly to generate a virtual system MAC address used for LACP negotiation (LACP System ID) between dual-homed switches, **the first byte of the ESI MAC must be an even value** (such as `02`, `04`, `06`, or `08`). If an odd value is configured (e.g., `03`), the dual-homed switches will advertise a multicast LACP System ID, causing servers to reject LACP synchronization and blocking port-channel negotiation.

### 2. Uniqueness per Virtual Segment
Each redundant switch pair (ESI segment) within the Apstra fabric blueprint must carry a **unique** ESI value. Using a customized prefix (like `08` instead of the default `02`) and varying the lower octets prevents MAC collision loops and ensures deterministic traffic distribution across all-active link paths.
