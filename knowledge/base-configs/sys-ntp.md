---
type: JUNOS Base Config
title: System NTP Synchronization configuration
description: Configures NTP servers for robust system clock synchronization.
resource: https://www.juniper.net/documentation/us/en/software/junos/time-management/topics/topic-map/ntp-configuring.html
tags: [ntp, clock-synchronization, system-services]
generated:
  by: zed-agent/gemini-3.5-flash
  at: 2026-08-14T12:00:00Z
verified:
  by: human:ckim
  at: 2026-08-14T12:00:00Z
id: KP-SYS-002
version: 1.0.0
---

# JUNOS Configuration Snippet

```set
set system ntp server 216.58.217.16 prefer
set system ntp server time.google.com
```
