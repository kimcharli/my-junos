---
type: Apstra Configuration
title: Apstra Controller REST API Authentication
description: Documents the authentication API endpoint and token usage required to interact with the Juniper Apstra REST API.
resource: https://www.juniper.net/documentation/us/en/software/apstra4.1/apstra-user-guide/topics/topic-map/apstra-rest-api.html
tags: [apstra, authentication, aaa, api]
generated:
  by: zed-agent/gemini-3.5-flash
  at: 2026-08-17T18:39:21Z
verified:
  by: human:ckim
  at: 2026-08-17T18:39:21Z
id: KP-INT-003
version: 1.0.0
---

# Apstra API AAA Login Endpoint

To perform configuration or operational queries on the Juniper Apstra Controller, clients must first authenticate to retrieve a temporary JSON Web Token (JWT).

### HTTP Method & Endpoint
* **Method:** `POST`
* **Path:** `/api/aaa/login`

### JSON Request Payload
```json
{
  "username": "string",
  "password": "string"
}
```

---

# AAA Authentication Response

A successful login request returns an HTTP status code of `201 Created` along with the token details in the response body.

### Response Body Example
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IkNoYXJsaWUiLCJ1c2VyX3Nlc3Npb24iOiI4MGJmODRhZC0yNmY3LTRjOTUtODg2Mi03MDhlODAyNjYxYWMiLCJjcmVhdGVkX2F0IjoiMjAyNi0wOC0xN1QxODozOToyMS45OTY4MDgiLCJleHAiOjE3ODcwNzgzNjF9.BlbK17W05pVOB0Vw8WMWyppq2GJz6ERc41g09MgusYGCaitImbvpyGe9XF88Z9WtAig4BoO7mICS2EkRpBYOew",
  "id": "258fada1-ec47-4eba-930d-fe64227b82cd"
}
```

---

# Authenticating Subsequent API Requests

For all subsequent REST API requests, the client must supply the retrieved token in the custom HTTP header.

### Required Request Headers
* **AuthToken:** `[token_value]`
* **Content-Type:** `application/json`

---

# Architectural Context & Rules

1. **Token Lifespan:** The token expiration (`exp`) is embedded inside the JWT. Always handle token expiration gracefully by requesting a new token when receiving an HTTP `401 Unauthorized` response.
2. **Secure Controller Connection:** Ensure all API communication uses HTTPS (`https://<controller-ip>:<port>`). In production environments, verify the SSL certificate of the Apstra Controller.
