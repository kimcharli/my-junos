---
type: JUNOS Audit
title: Enforce Secure SSH Only (Disable Telnet/Plain Services)
description: Ensures only SSH is enabled for device management, while insecure telnet services are disabled.
resource: https://www.juniper.net/documentation/us/en/software/junos/user-access/topics/topic-map/ssh-connection-configuring.html
tags: [ssh, telnet, security-hardening]
generated:
  by: human:NetOps Core Team
  at: 2026-08-14T12:00:00Z
id: KP-SEC-001
version: 1.0.0
verification_method: xml-xpath
checks:
  - name: Ensure SSH Service is enabled
    command: show configuration system services | display xml
    expected: /configuration/system/services/ssh
    negate: false
    remediation: set system services ssh
  - name: Ensure Telnet Service is disabled
    command: show configuration system services | display xml
    expected: /configuration/system/services/telnet
    negate: true
    remediation: delete system services telnet
---

# JUNOS Compliance Audit Documentation

This audit rule ensures cleartext, insecure management interfaces (specifically Telnet) are disabled and replaced by encrypted, secure SSH sessions.
