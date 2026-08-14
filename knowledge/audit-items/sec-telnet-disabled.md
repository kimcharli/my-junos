---
type: JUNOS Audit
title: Ensure Telnet Management is Disabled
description: Plaintext Telnet management protocol must be completely disabled to avoid credential leakage.
resource: https://www.juniper.net/documentation/us/en/software/junos/user-access/topics/topic-map/telnet-connection-disabling.html
tags: [telnet, cleartext, security-hardening]
timestamp: 2026-08-14T12:00:00Z
id: KP-SEC-002
version: 1.0.0
verification_method: cli-regex
checks:
  - name: Check Telnet is not in running services
    command: show configuration system services
    expected: telnet
    negate: true
    remediation: delete system services telnet
---

# JUNOS Compliance Audit Documentation

This item matches command strings inside running service definitions to check for plain Telnet usage.
