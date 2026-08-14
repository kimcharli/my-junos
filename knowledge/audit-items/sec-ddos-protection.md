---
type: JUNOS Audit
title: Ensure No DDoS Protection Packet Drops
description: Verifies that the router or switch ddos-protection protocols statistics are clean and no control plane packets are being dropped.
resource: https://www.juniper.net/documentation/us/en/software/junos/security-mgmt/topics/topic-map/ddos-protection-overview.html
tags: [ddos, control-plane, security-hardening]
timestamp: 2026-08-14T12:00:00Z
id: KP-SEC-003
version: 1.0.0
verification_method: cli-regex
checks:
  - name: Check for non-zero DDoS protection packet drops
    command: show ddos-protection protocols statistics terse
    expected: \s+[1-9]\d*$
    negate: true
    remediation: Request inspection of DDoS logs using 'show ddos-protection protocols violations' and adapt rate-limits if traffic is legitimate.
---

# JUNOS Compliance Audit Documentation

This audit item monitors the device's built-in control plane Distributed Denial of Service (DDoS) protection statistics. 

## Rationale
JUNOS devices protect their Routing Engine (RE) by rate-limiting protocol traffic (e.g., BGP, ARP, LACP) sent from the packet forwarding engine. If packets are being dropped, it indicates either:
1. An active denial-of-service attack or anomaly targeting the device control plane.
2. Under-provisioned rate limits for legitimate network protocol scale.

## Verification Mechanics
* **Command:** `show ddos-protection protocols statistics terse`
* **Pattern Matching:** Looks for any protocol lines that end with a non-zero integer in the "Dropped packets" column (e.g., `bgp 1245 15`).
* **Compliance Action:** If any non-zero drop counts are detected, the audit reports a non-compliant state and prompts immediate operator analysis.
