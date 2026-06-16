<div align="center">

# 🧛‍♂️ VAMPIRE BITE

### *One Bite. One Vulnerability. The Web Bleeds.*

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey.svg)]()
[![Version](https://img.shields.io/badge/Version-47.0-purple.svg)]()
[![Payloads](https://img.shields.io/badge/Adaptive_Payloads-Yes-orange.svg)]()
[![WAF](https://img.shields.io/badge/WAF_Detection-Yes-red.svg)]()

**Professional Web Security Scanner | Smart Crawler | Adaptive Payloads | WAF Detection**

</div>

---

## 🩸 What is Vampire Bite?

Vampire Bite is a **professional-grade security assessment tool** for web applications. It combines:
- 🔍 **Smart Crawler** - automatically discovers all input points
- 🎯 **Adaptive Payloads** - context-aware XSS and database-specific SQLi
- 🛡️ **WAF Detection** - identifies Cloudflare, ModSecurity, and more
- 📊 **Professional Reports** - HTML and JSON formats
- ⚡ **Multi-threading** - fast port scanning
- 🧠 **Technology Detection** - CMS, framework, language, database

> **One command. One target. The web bleeds.**

---

## ⚡ Features

| Category | Features |
|----------|----------|
| **🔍 Network Recon** | • 25+ port scanner with multi-threading<br>• Service detection & banner grabbing |
| **🕷️ Smart Crawler** | • Automatic form extraction<br>• URL parameter discovery<br>• Endpoint detection<br>• Link crawling |
| **🖥️ Tech Detection** | • Web server detection (Apache/Nginx/LiteSpeed/IIS)<br>• CMS detection (WordPress, Joomla, Drupal)<br>• Framework detection (React, Vue, Angular)<br>• Language detection (PHP, ASP.NET, Java)<br>• Database detection (MySQL, PostgreSQL, MSSQL) |
| **🛡️ WAF Detection** | • Cloudflare<br>• ModSecurity<br>• AWS WAF<br>• Sucuri<br>• Akamai<br>• Imperva<br>• F5<br>• Barracuda<br>• Wordfence |
| **⚡ Adaptive XSS** | • Context-aware payloads (HTML, Attribute, URL, JSON, XML)<br>• WAF bypass techniques<br>• Multiple encoding<br>• Case variations |
| **💉 Adaptive SQLi** | • Database-specific payloads (MySQL, MSSQL, PostgreSQL, Oracle, SQLite)<br>• Error-based detection<br>• Time-based blind detection<br>• Boolean-based detection<br>• Union-based detection |
| **📊 Reporting** | • Professional HTML reports<br>• JSON export for automation<br>• Real-time color-coded terminal output<br>• Progress indicators |

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
║  [1] 🧛‍♂️ VAMPIRE BITE PRO - Complete Scan (Best)                            ║
║  [2] 🔍 Quick Scan (Ports + Server Only)                                     ║
║  [0] 🚪 Exit                                                                 ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

### Option 1: PRO COMPLETE SCAN
- **Phase 1:** Port scanning (25+ ports)
- **Phase 2:** WAF detection
- **Phase 3:** Technology detection
- **Phase 4:** Smart crawling (finds all forms, parameters, endpoints)
- **Phase 5:** Adaptive vulnerability testing (XSS + SQLi)
- **Phase 6:** HTML + JSON report generation

### Option 2: QUICK SCAN
- Port scanning only
- Web server detection
- Fast reconnaissance

---

## 📊 Example Output

```bash
┌─[VAMPIRE]~[> 1
Target URL: https://example.com

==================================================================================
🧛‍♂️ VAMPIRE BITE PRO SCAN: https://example.com
==================================================================================

┌─────────────────────────────────────────────────────────────┐
│  PHASE 1/6: PORT SCANNING                                   │
└─────────────────────────────────────────────────────────────┘
      🔴 Port 80 [HTTP] OPEN
      🔴 Port 443 [HTTPS] OPEN

┌─────────────────────────────────────────────────────────────┐
│  PHASE 2/6: WAF DETECTION                                   │
└─────────────────────────────────────────────────────────────┘
      [WAF] Detected: Cloudflare
      [WAF] Using bypass techniques...

┌─────────────────────────────────────────────────────────────┐
│  PHASE 3/6: TECHNOLOGY DETECTION                            │
└─────────────────────────────────────────────────────────────┘
      [WEB] Server: nginx/1.24.0
      [TECH] PHP detected
      [TECH] WordPress detected
      [TECH] MySQL detected

┌─────────────────────────────────────────────────────────────┐
│  PHASE 4/6: SMART CRAWLING                                  │
└─────────────────────────────────────────────────────────────┘
      [CRAWL] Found form: https://example.com/login.php
      [CRAWL] Found form: https://example.com/search
      [CRAWL] Found 3 forms, 5 parameters, 2 endpoints

┌─────────────────────────────────────────────────────────────┐
│  PHASE 5/6: ADAPTIVE VULNERABILITY TESTING                  │
└─────────────────────────────────────────────────────────────┘
      [TEST] Testing form: https://example.com/login.php
        [XSS] 💀 Found in username: <script>alert(1)</script>
        [SQLi] 💀 Found in username: ' OR '1'='1 (evidence: mysql)

==================================================================================
📊 SCAN COMPLETE!
==================================================================================
  Target: https://example.com
  Duration: 45.2s
  Open Ports: 2
  Web Server: nginx/1.24.0
  Technologies: PHP, WordPress, MySQL
  WAF Detected: Cloudflare
  Forms Found: 3
  XSS Vulnerable: 2
  SQLi Vulnerable: 1
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
| urllib3 | HTTP connection |

---

## 📁 Project Structure

```
Vampire-Bite/
├── vampire_bite.py          # Main application
├── README.md                # Documentation
└── LICENSE                  # MIT License
```

> **No external payload files needed.** The tool generates all payloads dynamically based on context.

---

## 📊 Adaptive Testing

### XSS Contexts

| Context | Description | Example Payload |
|---------|-------------|-----------------|
| **HTML** | Inside HTML tags | `<svg/onload=alert(1)>` |
| **Attribute** | Inside HTML attributes | `" onmouseover=alert(1) "` |
| **URL** | Inside URL | `javascript:alert(1)` |
| **JSON** | Inside JSON data | `{"key":"<script>alert(1)</script>"}` |
| **XML** | Inside XML | `<![CDATA[<script>alert(1)</script>]]>` |

### SQLi Database Types

| Database | Specific Payloads |
|----------|-------------------|
| **MySQL** | `UNION SELECT @@version`, `LOAD_FILE()` |
| **MSSQL** | `WAITFOR DELAY`, `xp_cmdshell` |
| **PostgreSQL** | `pg_sleep()`, `CAST()` |
| **Oracle** | `CTXSYS.DRITHSX.SN`, `UTL_INADDR` |
| **SQLite** | `UNION SELECT sql FROM sqlite_master` |

---

## 🛡️ WAF Detection

| WAF | Signatures |
|-----|------------|
| Cloudflare | `cf-ray`, `__cfduid` |
| ModSecurity | `modsecurity`, `owasp` |
| AWS WAF | `x-amzn-requestid` |
| Sucuri | `sucuri`, `x-sucuri-id` |
| Akamai | `akamai`, `x-akamai` |
| Imperva | `imperva`, `incapsula` |
| F5 | `f5`, `big-ip` |
| Wordfence | `wordfence`, `wf-` |

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

### Cryptocurrency Addresses

| Network | Address |
|---------|---------|
| **TRON (TRC-20)** | `TRVPZZmXwzysR7GccpmhR6Zd4euk5jPvzV` |

> ⚠️ Send only TRON (TRC-20) tokens: TRX, USDT, or any TRC-20 token.

---

## ⭐ Show Your Support

```bash
git star https://github.com/Lord-Vampire/Vampire-Bite
```

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
---

## ✅ تفا
