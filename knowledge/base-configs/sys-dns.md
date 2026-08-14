---
type: JUNOS Base Config
title: System DNS Servers configuration
description: Configures standard domain name resolution servers for name lookups.
resource: https://www.juniper.net/documentation/us/en/software/junos/user-access/topics/topic-map/dns-service-configuring.html
tags: [dns, name-resolution, system-services]
generated:
  by: human:NetOps Core Team
  at: 2026-08-14T12:00:00Z
id: KP-SYS-001
version: 1.0.0
---

# JUNOS Configuration Snippet

```set
set system name-server 8.8.8.8
set system name-server 1.1.1.1
```
