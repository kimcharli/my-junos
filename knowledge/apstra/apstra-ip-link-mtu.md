---
type: JUNOS Base Config
title: Apstra Fabric IP Links MTU Configuration
description: Recommends configuring the Default IP Links MTU to Generic Systems as 9170 to match the internal Fabric MTU, instead of leaving it empty (which defaults to 1500).
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

# JUNOS Configuration Snippet

In Apstra-orchestrated fabrics, the interface MTU of physical IP links connecting leaves, spines, or external generic systems (such as firewalls, routers, or hypervisors) is configured at the physical layer. To enable high-performance jumbo frame traversal without fragmentation, apply the `9170` MTU value:

```set
set interfaces et-0/0/1 mtu 9170
```

*(Where `et-0/0/1` represents the high-speed interface connecting to the generic system).*

---

# Apstra Design & Architectural Rationale

### 1. Default Behavior vs. Recommended Practice
In Apstra fabric blueprints, when creating or configuring IP links under **Default IP Links to Generic Systems**, the MTU field is **empty** by default. 
* **The Default Empty Behavior:** Leaves the interface MTU unset in the blueprint, which defaults to standard Ethernet MTU (**`1500` bytes**) in the generated device configuration.
* **The Recommended Practice:** Manually override the empty field and configure the Generic System MTU to **`9170` bytes**.

### 2. Impact of MTU Mismatches in EVPN-VXLAN
EVPN-VXLAN encapsulation adds a **50-byte** overhead to standard IP packets (including the outer Ethernet, IP, UDP, and VXLAN headers). 
* **Packet Fragmentation:** If generic interfaces remain at `1500` bytes while the core fabric transports VXLAN packets, high-throughput packets will be forced to undergo CPU-intensive IP fragmentation at leaf boundaries or be dropped entirely.
* **End-to-End Performance:** Matching the Generic System IP Link MTU to the core Fabric MTU of **`9170`** ensures seamless end-to-end traversal of jumbo frames (up to 9000 bytes payload) without fragmentation, maximizing packet forwarding engine (PFE) throughput.
