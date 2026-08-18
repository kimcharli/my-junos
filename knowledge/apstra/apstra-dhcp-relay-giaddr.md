---
type: Apstra Configuration
title: Apstra DHCP Relay GIADDR and Windows DHCP Server Interop
description: Apstra DHCP relay sources requests from the VRF loopback (lo0) address, which becomes the GIADDR. Microsoft Windows DHCP Server silently discards requests whose GIADDR falls outside every active scope range, so the relay loopbacks must be authorized via a dedicated fully-excluded scope.
resource: https://www.juniper.net/documentation/us/en/software/apstra4.1/apstra-user-guide/topics/topic-map/dhcp-relay.html
tags: [apstra, dhcp, dhcp-relay, giaddr, windows-server, evpn-vxlan, interop]
generated:
  by: zed-agent/claude-opus-5
  at: 2026-08-18T00:00:00Z
verified:
  by: human:ckim
  at: 2026-08-18T00:00:00Z
sources:
  - resource: https://www.juniper.net/documentation/us/en/software/apstra4.1/apstra-user-guide/topics/topic-map/dhcp-relay.html
    title: Juniper Apstra User Guide - DHCP Relay
  - resource: https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/dhcp-top
    title: Microsoft Windows Server DHCP Documentation
id: KP-INT-004
version: 1.0.0
---

# Apstra DHCP Relay Source Address Behavior

When DHCP relay is enabled on a routed VN (Virtual Network) in an Apstra blueprint, Apstra renders a `forwarding-options dhcp-relay` stanza scoped to the tenant routing-instance (VRF). The relay does **not** source packets from the SVI/IRB gateway address of the client subnet — it sources them from the **VRF loopback (`lo0.<unit>`) address allocated by Apstra to each leaf in that routing instance**.

Consequently, the **GIADDR** field observed by the upstream DHCP server is the leaf's per-VRF `lo0` address, not the client gateway. Practical implications:

* Every leaf (or ESI leaf pair) participating in the VRF presents a **distinct GIADDR**.
* The GIADDR is drawn from the Apstra **loopback resource pool** assigned to the routing zone, which is normally a separate, non-client prefix (e.g. `10.255.x.x/32`).
* Scaling the fabric (adding leaves to the routing zone) **adds new GIADDRs** from that pool.

Verify the rendered behavior on-box:

```cli
show configuration routing-instances <VRF> forwarding-options dhcp-relay
show interfaces lo0 terse
show dhcp relay statistics routing-instance <VRF>
show dhcp relay binding routing-instance <VRF>
```

---

# Apstra REST API Intent Payload

Relay targets are blueprint intent. The set of DHCP server addresses the fabric relays to is managed on the **Apstra Controller**, not per-device.

### HTTP Method & Endpoint
* **Method:** `PUT`
* **Path:** `/api/blueprints/<blueprint_id>/dhcp-servers`

### JSON Payload
```json
{
  "items": [
    "10.10.20.10",
    "10.10.20.11"
  ]
}
```

*(Where each entry is a Windows DHCP Server reachable from the tenant routing zone. The GIADDR presented to these servers is still the per-leaf VRF `lo0` address, which is why the authorization scope below is required.)*

### Alternative GUI Configuration Path

1. Log in to the **Apstra GUI** and open the **Blueprint**, then the **Staged** tab.
2. Navigate to **Virtual → DHCP Servers** (or **Resources → DHCP servers**, version-dependent).
3. Add the DHCP server IP addresses and commit the blueprint.
4. Enable **DHCP service** on each routed Virtual Network that requires relay.

---

# ⚠️ Windows Server Edge Case: Rogue Relay Agent Rejection

**All relay agent IP addresses (GIADDR) must be part of an active DHCP scope IP address range.** Any GIADDR outside of the configured DHCP scope IP address ranges is considered a **rogue relay**, and Windows DHCP Server will **not acknowledge** DHCP client requests forwarded by those relay agents.

Failure signature:

* Clients in the affected VN never receive an OFFER; they fall back to APIPA or time out.
* `show dhcp relay statistics` on the leaf shows DISCOVER/REQUEST packets **transmitted** with **zero** OFFER/ACK received.
* Packet capture at the server NIC shows the inbound DISCOVER arriving — the server receives it and simply does not reply.
* Windows DHCP server event/audit logs show no lease activity for the request.

This is silent by design; there is no error returned to the relay. Because Apstra sources from `lo0` rather than the client gateway, an otherwise-correct DHCP relay design will fail against Windows DHCP Server **unless the loopback range is explicitly authorized**.

---

# Remediation: Relay Authorization Scope

Create a scope whose range covers the GIADDR addresses, exclude the entire range from distribution, and activate it. The scope exists purely to satisfy the GIADDR membership check — no addresses are ever leased from it.

1. In the **DHCP console**, create a **New Scope** covering the Apstra VRF loopback addresses. If the GIADDRs are sequential, a single scope covers them all.
2. Add an **exclusion range** spanning the **entire** scope range, so no address can be handed out.
3. **Activate** the scope. An inactive scope does not authorize relays.
4. Repeat (or widen the range) whenever new leaves are added to the routing zone and draw new loopbacks from the Apstra pool.

Design guidance:

* Size the authorization scope against the **full Apstra loopback pool** for the routing zone, not just the currently deployed leaves. This makes fabric expansion a no-op on the Windows side.
* Name the scope explicitly (e.g. `RELAY-AUTH-<routing-zone>`) and document it — a fully-excluded active scope looks like a misconfiguration to an operator who lacks this context.
* Each routing zone with its own loopback pool needs its own authorization scope or an appropriately widened range.
* This constraint is **specific to Microsoft Windows DHCP Server**. ISC DHCP, Infoblox, and Cisco Prime do not enforce GIADDR-in-scope membership as a relay authorization gate.

---

# ⚠️ DO NOT CONFIGURE VIA JUNOS CLI

DHCP relay in an Apstra-managed fabric is blueprint intent. Editing `forwarding-options dhcp-relay` or `lo0` addressing directly on a switch console will:

* Raise a **Configuration Deviation anomaly** in Apstra's continuous validation loop.
* Be flagged as unauthorized drift and reverted/overwritten to the approved staged intent.

Manage relay server IPs and routing-zone loopback pools through the **Apstra GUI/REST API** (Blueprint → Staged → Virtual → DHCP servers, and the routing zone's loopback resource assignment). The correct fix for this interop issue is on the **Windows DHCP Server**, not the switch.
