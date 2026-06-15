<div align="center">

# 🧛‍♂️ VAMPIRE BITE

### *One Bite. One Vulnerability. The Web Bleeds.*

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey.svg)]()
[![Payloads](https://img.shields.io/badge/XSS-1500%2B-orange.svg)]()
[![SQLi](https://img.shields.io/badge/SQLi-800%2B-red.svg)]()

**Complete Web Security Scanner | Port Scan | Admin Finder | XSS/SQLi Tester | Auto Payload Generator**

</div>

---

## 🩸 What is Vampire Bite?

Vampire Bite is a **complete, all-in-one security assessment tool** for web applications. It combines:
- 🔍 **Port scanning** (25+ ports)
- 🖥️ **Server & technology detection**
- 📁 **Sensitive file finder**
- 👑 **Admin panel discovery** (Fixed - No duplicates, follows redirects)
- 📂 **Open directory enumeration**
- 💀 **Backdoor hunter**
- 🛡️ **Security headers check**
- ⚡ **XSS testing (1500+ payloads)**
- 💉 **SQLi testing (800+ payloads)**
- 📊 **HTML report generation**

> **One command. One target. The web bleeds.**

---

## ⚡ Features

| Category | Features |
|----------|----------|
| **🔍 Network Recon** | • 25+ port scanner with multi-threading<br>• Service detection & banner grabbing |
| **🖥️ Web Discovery** | • Web server detection (Apache/Nginx/LiteSpeed/IIS)<br>• Technology stack (PHP, ASP.NET, React, Vue) |
| **🛡️ Security Headers** | • CSP, HSTS, X-Frame-Options, X-XSS-Protection |
| **📁 Reconnaissance** | • Sensitive files (robots.txt, .git/config, .env, backup.sql)<br>• Admin panels (45+ paths with redirect following)<br>• Open directories (/backup, /temp, /uploads)<br>• Backdoors (shell.php, c99.php, r57.php) |
| **⚡ Vulnerability Testing** | • XSS testing with 1500+ payloads<br>• SQL Injection testing with 800+ payloads<br>• Error-based detection<br>• Time-based blind detection |
| **📊 Reporting** | • Professional HTML reports<br>• Real-time color-coded terminal output<br>• Progress indicators |

---

## 🚀 Quick Start

### One-Line Installation

```bash
git clone https://github.com/Lord-Vampire/Vampire-Bite.git
cd Vampire-Bite
python vampire_bite.py
```

> **No manual dependency installation required.** The tool auto-installs everything on first run.

---

## 💀 Menu Options

```
╔════════════════════════════════════════════════════════════════════════════════╗
║  [1] 🧛‍♂️ VAMPIRE BITE - COMPLETE SCAN (All Features)                         ║
║  [2] 🔍 QUICK SCAN (Ports + Web Server Only)                                  ║
║  [0] 🚪 EXIT                                                                  ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

### Option 1: COMPLETE SCAN
- Port scanning (25+ ports)
- Web server & technology detection
- Security headers check
- Sensitive files discovery
- Admin panel finder (with redirect following, no duplicates)
- Open directory enumeration
- Backdoor hunter
- XSS testing (1500+ payloads)
- SQLi testing (800+ payloads)
- HTML report generation

### Option 2: QUICK SCAN
- Port scanning only
- Web server detection
- Fast reconnaissance

---

## ✨ What's New in v36

| Improvement | Description |
|-------------|-------------|
| **Fixed Admin Panel Detection** | No more duplicate or fake admin panels |
| **Redirect Following** | Follows redirects to find real admin panel URLs |
| **Homepage Filter** | Homepage is no longer reported as an admin panel |
| **Duplicate Prevention** | Same URL won't appear multiple times |

---

## 📊 Example Output

```bash
┌─[VAMPIRE]~[> 1
Target URL: https://example.com

==================================================================================
🧛‍♂️ VAMPIRE BITE COMPLETE SCAN: https://example.com
==================================================================================

┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: PORT SCANNING                                   │
└─────────────────────────────────────────────────────────────┘
      🔴 Port 80 [HTTP] OPEN
      🔴 Port 443 [HTTPS] OPEN
      🔴 Port 22 [SSH] OPEN

┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: WEB SERVER & TECHNOLOGY                         │
└─────────────────────────────────────────────────────────────┘
      [+] Server: nginx/1.24.0
      [+] PHP detected

┌─────────────────────────────────────────────────────────────┐
│  PHASE 4: RECONNAISSANCE (Files, Admin, Backdoors)        │
└─────────────────────────────────────────────────────────────┘
      [!] Found: /robots.txt
      [✔] ADMIN PANEL: /admin → https://example.com/admin/login
      [📁] OPEN DIRECTORY: /backup
      [!] BACKDOOR FOUND: /shell.php

┌─────────────────────────────────────────────────────────────┐
│  PHASE 5: XSS & SQLi TESTING                              │
└─────────────────────────────────────────────────────────────┘
      [*] Testing XSS on form (1500+ payloads)...
        [!] XSS FOUND! <script>alert('XSS')</script>
        [!] SQLi FOUND! ' OR '1'='1 (evidence: mysql)

==================================================================================
📊 VAMPIRE BITE COMPLETE SUMMARY
==================================================================================
  Target: https://example.com
  Duration: 45.2s
  Open Ports: 3
  Web Server: nginx/1.24.0
  Technologies: PHP
  Admin Panels: 1
  Open Dirs: 1
  Backdoors: 1
  XSS Vulnerable: 3
  SQLi Vulnerable: 2
==================================================================================
```

---

## 🔧 Requirements (Auto-Installed)

| Dependency | Purpose |
|------------|---------|
| Python 3.7+ | Core runtime |
| requests | HTTP requests |
| colorama | Terminal colors |
| beautifulsoup4 | HTML parsing |

---

## 📁 Project Structure

```
Vampire-Bite/
├── vampire_bite.py          # Main application
├── README.md                # Documentation
└── LICENSE                  # MIT License
```

> **No external payload files needed.** The tool generates all payloads internally.

---

## 📊 Payload Statistics

| Category | Count | Source |
|----------|-------|--------|
| **XSS Payloads** | ~1,500 | Auto-generated |
| **SQLi Payloads** | ~800 | Auto-generated |
| **Total** | ~2,300 | Internal generator |

---

## ⚠️ Legal Disclaimer

```
THIS SOFTWARE IS PROVIDED FOR EDUCATIONAL AND AUTHORIZED SECURITY TESTING ONLY.

By using this tool, you agree to:
- Only scan systems you own or have explicit written permission to test
- Comply with all applicable laws and regulations
- Accept full responsibility for any damage or consequences

The author (LORD VAMPIRE) assumes no liability for misuse.
```

---

## 👑 Author

**LORD VAMPIRE** — Team Lord Leader

[![GitHub](https://img.shields.io/badge/GitHub-Lord--Vampire-black?logo=github&style=for-the-badge)](https://github.com/Lord-Vampire)
[![Instagram](https://img.shields.io/badge/Instagram-@hamiavalofficial-purple?logo=instagram&style=for-the-badge)](https://instagram.com/hamiavalofficial)

- GitHub: [@Lord-Vampire](https://github.com/Lord-Vampire)
- Instagram: [@hamiavalofficial](https://instagram.com/hamiavalofficial)

---

## 💰 Support the Project

If you find Vampire Bite useful, you can support its continued development with cryptocurrency donations.

### Cryptocurrency Addresses

| Network | Address |
|---------|---------|
| **TRON (TRC-20)** | `TRVPZZmXwzysR7GccpmhR6Zd4euk5jPvzV` |

> ⚠️ **Important:** Send only TRON (TRC-20) tokens to this address.

**Supported tokens:** TRX, USDT (TRC-20), any TRC-20 token

---

## ⭐ Show Your Support

If this tool helped you find a vulnerability or taught you something new:

```bash
git star https://github.com/Lord-Vampire/Vampire-Bite
```

**Follow me on GitHub and Instagram for more security tools and updates!**

| Platform | Link |
|----------|------|
| 🐺 GitHub | [@Lord-Vampire](https://github.com/Lord-Vampire) |
| 📸 Instagram | [@hamiavalofficial](https://instagram.com/hamiavalofficial) |

---

## 📜 License

**MIT License** — Free for security research. See [LICENSE](LICENSE) for details.

---

**One Bite. One Vulnerability. The Web Bleeds.** 🩸

---

<div align="center">

**Built with 🩸 by LORD VAMPIRE | Team Lord**

</div>
