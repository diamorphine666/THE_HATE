# THE_HATE C2

**DNS Tunneling + Image Hosting (imgbb) Covert Command & Control**

[![License: Educational Use Only](https://img.shields.io/badge/License-Educational%20Use%20Only-red.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

THE_HATE C2 is a proof-of-concept covert C2 channel that blends malicious traffic with legitimate DNS queries and HTTPS uploads to imgbb. Commands are embedded into cover images, uploaded to a free image hosting service, and retrieved by the agent via DNS TXT records.

> **⚠️ DISCLAIMER:** This tool is for **educational purposes only**. Use only on systems you own or have explicit permission to test. The author is not responsible for any misuse or damage.

---

## 🔍 How It Works

1. **Operator** enters a command in the server CLI.
2. **Server** embeds the command into a JPEG/PNG cover image (appends after `FFD9` marker), uploads it to imgbb, and receives a public URL.
3. **Server** responds to a DNS TXT query (e.g., `check.yourdomain.com`) with the **base64-encoded imgbb URL**.
4. **Agent** periodically resolves the DNS name, extracts the URL, downloads the image from imgbb, and retrieves the command.
5. **Agent** executes the command, captures output, embeds it into **another cover image**, uploads to imgbb, and sends the new URL back via DNS TXT record.
6. **Server** decodes the output and displays it to the operator.

All traffic looks like normal DNS requests + HTTPS to `imgbb.com` – no raw TCP beaconing, no fixed C2 IPs.

---

## 🚀 Features

- **Stealth** – no direct C2 communication; traffic blends with DNS and image hosting.
- **Resilience** – uses free, public image hosting (imgbb) as a dead‑drop resolver.
- **Asynchronous** – non‑blocking DNS server and HTTP client.
- **Extensible** – easy to switch image host or add encryption (AES‑GCM).
- **Lightweight** – pure Python, minimal dependencies.

---
!!! You need register on imgbb and get your API token for use. (replace placeholder in client.py and server.py)
