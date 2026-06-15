<div align="center">

# 🧛‍♂️ VAMPIRE BITE

### *One Bite. One Vulnerability. The Web Bleeds.*

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey.svg)]()
[![Payloads](https://img.shields.io/badge/Payloads-8000%2B-orange.svg)]()
[![XSS](https://img.shields.io/badge/XSS-5000%2B-red.svg)]()
[![SQLi](https://img.shields.io/badge/SQLi-3000%2B-red.svg)]()

**Professional Web Security Scanner | 8000+ Payloads | Zero Config | Production Ready**

</div>

---

## 🩸 What is Vampire Bite?

Vampire Bite is a **professional, production-ready security assessment tool** designed for security researchers, penetration testers, and bug bounty hunters. It combines **5000+ XSS payloads** and **3000+ SQLi payloads** with **multiple detection mechanisms** to find vulnerabilities that other scanners miss.

> **One command. One target. The web bleeds.**

---

## ⚡ Features

| Category | Features |
|----------|----------|
| **🔍 Network Recon** | - 25+ port scanner with multi-threading<br>- Service detection & banner grabbing<br>- OS fingerprinting (TTL analysis) |
| **🖥️ Web Discovery** | - Web server detection (Apache/Nginx/LiteSpeed/IIS)<br>- CMS detection (WordPress, Joomla, Drupal, Magento)<br>- Technology stack (PHP, ASP.NET, React, Vue, Angular) |
| **🛡️ XSS Testing (5000+)** | - Reflected XSS \| DOM XSS \| Blind XSS<br>- Event Handlers \| Tag Breaking \| Encoded Payloads<br>- Polyglot \| HTML5 \| Framework (Angular/React/Vue)<br>- WAF Bypass Techniques |
| **💉 SQLi Testing (3000+)** | - Error-Based (MySQL/MSSQL/PostgreSQL/Oracle)<br>- Time-Based Blind \| Boolean-Based Blind<br>- Union-Based \| Stacked Queries \| Out-of-Band<br>- Comment Variations \| Case Variations |
| **🔓 Privilege Escalation** | - Admin panel discovery (45+ paths)<br>- Sensitive file finder (`.git/config`, `.env`, `backup.sql`)<br>- Open directory enumeration<br>- Backdoor detection (web shells, c99, r57) |
| **💀 Exploit Intelligence** | - Real-time GitHub exploit search<br>- Exploit-DB integration<br>- NVD CVE database lookup<br>- Live PoC links |
| **📊 Detection Mechanisms** | - Reflection detection \| Error-based detection<br>- Time-based detection \| Boolean-based detection<br>- Union-based detection \| Stacked query detection<br>- DOM analysis \| Banner grabbing |
| **📋 Reporting** | - Professional HTML reports<br>- JSON export for automation<br>- Real-time color-coded terminal output<br>- Progress indicators |

---

## 🚀 Quick Start

### One-Line Installation

```bash
git clone https://github.com/Lord-Vampire/Vampire-Bite.git
cd Vampire-Bite
python vampire_bite.py
No manual dependency installation required. The tool auto-installs everything on first run.

💀 Menu Options
text
╔════════════════════════════════════════════════════════════════════════════════╗
║  [1] 🧛‍♂️ VAMPIRE BITE - MEGA SCAN (Full Payload Database)                    ║
║  [2] 🔍 QUICK SCAN (Forms Only)                                               ║
║  [0] 🚪 EXIT                                                                  ║
╚════════════════════════════════════════════════════════════════════════════════╝
Option 1: MEGA SCAN
Extracts all forms from the target

Tests 5000+ XSS payloads with 7 detection mechanisms

Tests 3000+ SQLi payloads with 6 detection mechanisms

Generates HTML and JSON reports

Shows real-time progress with counters

Option 2: QUICK SCAN
Only extracts and displays forms

No payload testing

Fast reconnaissance

📊 Example Output
bash
┌─[VAMPIRE]~[> 1
Target URL: http://testphp.vulnweb.com

==================================================================================
🧛‍♂️ VAMPIRE BITE MEGA SCAN: http://testphp.vulnweb.com
==================================================================================

┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: FORM EXTRACTION                                 │
└─────────────────────────────────────────────────────────────┘
  [*] Extracting forms...
      [+] Found 3 forms with 12 inputs

┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: XSS TESTING (5000+ PAYLOADS)                     │
└─────────────────────────────────────────────────────────────┘
  [*] Testing Form 1/3
      [*] Testing XSS on form (5123 payloads)...
        [*] Progress: 1000/5123 payloads tested
        [!] XSS FOUND! <script>alert('XSS')</script>
        [*] Progress: 2000/5123 payloads tested
        [!] XSS FOUND! <img src=x onerror=alert('XSS')>
        [*] Completed: 5123/5123 XSS payloads tested

┌─────────────────────────────────────────────────────────────┐
│  PHASE 3: SQL INJECTION TESTING (3000+ PAYLOADS)           │
└─────────────────────────────────────────────────────────────┘
  [*] Testing Form 1/3
      [*] Testing SQLi on form (3124 payloads)...
        [*] Progress: 500/3124 payloads tested
        [!] SQLi FOUND! ' OR '1'='1 (evidence: mysql)
        [*] Progress: 1500/3124 payloads tested
        [!] TIME-BASED SQLi! Delay: 5.2s
        [*] Completed: 3124/3124 SQLi payloads tested

==================================================================================
📊 VAMPIRE BITE MEGA SUMMARY
==================================================================================
  Target: http://testphp.vulnweb.com
  Duration: 156.2s
  Forms Found: 3
  XSS Payloads Tested: 5123
  SQLi Payloads Tested: 3124

  🔥 XSS VULNERABLE: 12 found
    → <script>alert('XSS')</script>
    → <img src=x onerror=alert('XSS')>
    → <svg onload=alert('XSS')>

  🔥 SQL INJECTION VULNERABLE: 8 found
    → ' OR '1'='1 (evidence: mysql)
    → 1' AND SLEEP(5)-- (delay: 5.2s)
    → ' UNION SELECT NULL--
==================================================================================
🛠️ Detection Mechanisms
XSS Detection (7 Mechanisms)
Mechanism	Description	Detection Method
Reflected	Payload reflected in response	payload in response.text
DOM	JavaScript execution	location.hash, document.write
Event Handler	HTML events	onload=, onerror=
Tag Breaking	Breaking out of tags	"><script>
Encoded	URL encoded payloads	%3Cscript%3E
Polyglot	Multi-context payloads	Combined techniques
Blind	Callback to external server	src=http://evil.com
SQL Injection Detection (6 Mechanisms)
Mechanism	Description	Detection Method
Error-Based	Database error messages	mysql, sql syntax, ora-
Time-Based	Response delay	time.time() comparison
Boolean-Based	True/False response	Compare response length
Union-Based	UNION SELECT tests	Response contains column names
Stacked Queries	Multiple queries	; DROP TABLE
Out-of-Band	External communication	LOAD_FILE
📁 Project Structure
text
Vampire-Bite/
├── vampire_bite.py          # Main application (8000+ payloads)
├── README.md                # Documentation
├── LICENSE                  # MIT License
└── reports/                 # Generated reports (auto-created)
🔧 Requirements (Auto-Installed)
Dependency	Purpose
Python 3.7+	Core runtime
requests	HTTP requests
colorama	Terminal colors
beautifulsoup4	HTML parsing
📊 Payload Statistics
Category	Count
XSS Payloads	~5,000
├─ Basic Script Tags	50+
├─ Event Handlers	100+
├─ Tag Breaking	50+
├─ JavaScript Pseudo	30+
├─ Encoded	30+
├─ DOM XSS	20+
├─ Polyglot	10+
├─ HTML5	30+
├─ Framework (Angular/React/Vue)	20+
└─ WAF Bypass	50+
SQLi Payloads	~3,000
├─ Error-Based (MySQL/MSSQL/PostgreSQL/Oracle)	200+
├─ Time-Based Blind	50+
├─ Boolean-Based Blind	50+
├─ Union-Based	50+
├─ Stacked Queries	30+
├─ Out-of-Band	10+
└─ Comment Variations	100+
Total	~8,000+
⚠️ Legal Disclaimer
text
THIS SOFTWARE IS PROVIDED FOR EDUCATIONAL AND AUTHORIZED SECURITY TESTING ONLY.

By using this tool, you agree to:
- Only scan systems you own or have explicit written permission to test
- Comply with all applicable laws and regulations
- Accept full responsibility for any damage or consequences

The author (LORD VAMPIRE) assumes no liability for misuse.
👑 Author
LORD VAMPIRE — Team Lord Leader

https://img.shields.io/badge/GitHub-Lord--Vampire-black?logo=github&style=for-the-badge
https://img.shields.io/badge/Instagram-@hamiavalofficial-purple?logo=instagram&style=for-the-badge

GitHub: @Lord-Vampire

Instagram: @hamiavalofficial

Project: Vampire Bite

⭐ Show Your Support
If this tool helped you find a vulnerability or taught you something new:

bash
git star https://github.com/Lord-Vampire/Vampire-Bite
Follow me on GitHub and Instagram for more security tools and updates!

Platform	Link
🐺 GitHub	@Lord-Vampire
📸 Instagram	@hamiavalofficial
📜 License
MIT License — Free for security research. See LICENSE for details.

One Bite. One Vulnerability. The Web Bleeds. 🩸

<div align="center">
Built with 🩸 by LORD VAMPIRE | Team Lord

</div> ```
