<div align="center">

# 🧛‍♂️ VAMPIRE BITE

### *One Bite. One Vulnerability. The Web Bleeds.*

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey.svg)]()

**Next-Generation Web Security Scanner | Zero Config | Production Ready**

</div>

---

## 🩸 What is Vampire Bite?

Vampire Bite is a **professional, production-ready security assessment tool** designed for security researchers, penetration testers, and bug bounty hunters. It combines multiple scanning techniques into one powerful weapon.

> **One command. One target. The web bleeds.**

---

## ⚡ Features

| Category | Features |
|----------|----------|
| **🔍 Network Recon** | • 25+ port scanner with multi-threading<br>• Service detection & banner grabbing<br>• OS fingerprinting (TTL analysis) |
| **🖥️ Web Discovery** | • Web server detection (Apache/Nginx/LiteSpeed/IIS)<br>• CMS detection (WordPress, Joomla, Drupal, Magento)<br>• Technology stack (PHP, ASP.NET, React, Vue, Angular) |
| **🛡️ Vulnerability Assessment** | • Security headers analysis (CSP, HSTS, X-Frame-Options)<br>• XSS (Cross-Site Scripting) testing<br>• SQL Injection testing (Error-based)<br>• Blind SQL Injection (Time-based) |
| **🔓 Privilege Escalation** | • Admin panel discovery (45+ paths)<br>• Sensitive file finder (.git/config, .env, backup.sql)<br>• Open directory enumeration<br>• Backdoor detection (web shells, c99, r57) |
| **💀 Exploit Intelligence** | • Real-time GitHub exploit search<br>• Exploit-DB integration<br>• NVD CVE database lookup<br>• Live PoC links |
| **📊 Reporting** | • Professional HTML reports<br>• JSON export for automation<br>• Color-coded terminal output |

---

## 🚀 Quick Start

### One-Line Installation

```bash
git clone https://github.com/YOUR_USERNAME/Vampire-Bite.git

cd Vampire-Bite

python vampire_bite.py

No manual dependency installation required. The tool auto-installs everything.

💀 Menu
╔════════════════════════════════════════════════════════════════════════════════╗
║  [1] 🧛‍♂️ VAMPIRE BITE - FULL SCAN                                              ║
║  [2] 🔍 QUICK SCAN                                                              ║
║  [3] 🌐 ONLINE EXPLOIT SEARCH ONLY                                              ║
║  [0] 🚪 EXIT                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════╝
📊 Example Output
text
==================================================================================
🧛‍♂️ VAMPIRE BITE SCAN: https://example.com
==================================================================================

      🩸 Port 80 [HTTP] OPEN
      🩸 Port 443 [HTTPS] OPEN
      🩸 Server: nginx/1.24.0
      [+] PHP detected
      [✔] ADMIN PANEL: /admin
      [📁] OPEN DIRECTORY: /backup
      [!] BACKDOOR FOUND: /shell.php

==================================================================================
📊 SUMMARY
==================================================================================
  Target: https://example.com
  Duration: 45.2s
  Open Ports: 2
  Admin Panels: 1
  Backdoors: 1
==================================================================================
🔧 Requirements (Auto-Installed)
Python 3.7+

requests

colorama

beautifulsoup4

⚠️ Legal Disclaimer
text
For authorized security testing only.
Only scan systems you own or have permission to test.
👑 Author
LORD VAMPIRE — Team Lord

📜 License
MIT

<div align="center">
Built with 🩸 by LORD VAMPIRE | Team Lord

</div> ```
