---
type: Apstra Configuration
title: Apstra Fabric IP Links MTU Configuration
description: Recommends configuring the MTU for IP links to Generic Systems under Fabric Settings/Fabric Policy as 9170 to match the internal Fabric MTU, instead of leaving it empty (which defaults to 1500).
resource: https://www.juniper.net/documentation/us/en/software/apstra4.1/apstra-user-guide/topics/topic-map/evpn-vxlan-dci.html
tags: [apstra, fabric-settings, mtu, jumbo-frames, interfaces]
generated:
  by: zed-agent/gemini-3.5-flash
  at: 2026-08-14T12:00:00Z
verified:
  by: human:ckim
  at: 2026-08-14T12:00:00Z
id: KP-INT-002
version: 1.0.0
---

# Apstra REST API Intent Payload

To configure the MTU for links to Generic Systems (external routers, firewalls, or hypervisors) in an Apstra fabric, the change must be orchestrated directly on the **Apstra Controller** (not on the device CLI) to preserve the single source of truth.

### HTTP Method & Endpoint
* **Method:** `PATCH`
* **Path:** `/api/blueprints/<blueprint_id>/fabric-settings`

### JSON Payload
```json
{
  "external_router_mtu": 9170
}
```

---

# Alternative GUI Configuration Path

1. Log in to the **Apstra GUI**.
2. Navigate to your active **Blueprint** and click the **Staged** tab.
3. Click on **Settings** and scroll to **Fabric Settings / Fabric Policy**.
4. Edit the policy and set **MTU for IP links to Generic Systems** (often labeled or mapped as *External Router MTU*) to `9170`.
5. Commit the blueprint changes to push the intent down to the fabric.

---

# ⚠️ WARNING: DO NOT CONFIGURE VIA JUNOS CLI

In an intent-based networking (IBN) platform like Apstra, **direct out-of-band device-level CLI edits are strictly forbidden**:
* **Configuration Deviation Anomaly:** If you run `set interfaces <interface> mtu 9170` directly on the switch console, Apstra's continuous validation loop will immediately detect a **Configuration Deviation anomaly**.
* **Automatic Overwrite:** Apstra acts as the authoritative config source and will flag the CLI edit as an unauthorized drift, notifying operators or automatically overwriting the manual CLI changes to restore the switch to its approved staged intent.
