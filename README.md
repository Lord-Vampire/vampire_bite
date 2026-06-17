<div align="center">

# 🧛 VAMPIRE BITE

### *One Bite. One Vulnerability. The Web Bleeds.*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey.svg)]()
[![Version](https://img.shields.io/badge/Version-3.0-purple.svg)]()

**Professional Web Security Scanner | Zero Config | All-in-One**

</div>

---

## 🩸 What is Vampire Bite?

Vampire Bite is a **professional-grade web application security scanner** designed for penetration testers, security researchers, and bug bounty hunters. It combines **multiple scanning techniques** into one powerful tool.

> **One command. One target. The web bleeds.**

---

## ⚡ Features

| Category | Features |
|----------|----------|
| **🔍 Network Recon** | • 25+ port scanner with multi-threading<br>• Service detection & banner grabbing<br>• OS fingerprinting |
| **🖥️ Web Discovery** | • Web server detection (Apache/Nginx/LiteSpeed/IIS)<br>• CMS detection (WordPress, Joomla, Drupal)<br>• Technology stack (PHP, ASP.NET, React, Vue, Angular) |
| **🛡️ Vulnerability Testing** | • XSS (Reflected, Stored, DOM)<br>• SQL Injection (Error, Union, Time, Boolean)<br>• LFI / RFI<br>• Command Injection<br>• SSRF, XXE, CSRF, IDOR<br>• Open Redirect |
| **🔓 Security Analysis** | • Security headers check<br>• JWT analysis<br>• CORS misconfiguration<br>• Session security<br>• SSL/TLS analysis |
| **📁 Reconnaissance** | • Sensitive files (.env, .git, backup)<br>• Admin panels discovery<br>• Open directories<br>• Backdoor detection |
| **📊 Reporting** | • Professional HTML reports<br>• JSON export<br>• Real-time color output |

---

## 🚀 Quick Start

### One-Line Installation

```bash
git clone https://github.com/Lord-Vampire/vampire_bite.git
cd vampire_bite
python req.py
python vampire_bite.py
```

> **Auto-installs all dependencies on first run**

---

## 💀 Usage

### Basic Scan

```bash
python vampire_bite.py https://target.com
```

### Advanced Scan

```bash
python vampire_bite.py https://target.com --waf-evasion --verify-vulns
```

### With Proxy

```bash
python vampire_bite.py https://target.com --proxy http://127.0.0.1:8080
```

### Custom Headers

```bash
python vampire_bite.py https://target.com --headers '{"X-API-Key": "secret"}'
```

---

## 📖 Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `target` | Target URL (required) | - |
| `--delay` | Request delay (seconds) | 1.0 |
| `--timeout` | HTTP timeout | 10.0 |
| `--max-workers` | Max threads | 100 |
| `--ports` | Custom ports to scan | Common ports |
| `--proxy` | Proxy URL | - |
| `--headers` | Custom headers JSON | - |
| `--cookies` | Cookies string | - |
| `--verify-vulns` | Verify with headless browser | False |
| `--waf-evasion` | Enable WAF evasion | False |
| `--js-rendering` | Enable JavaScript rendering | False |
| `--no-port-scan` | Skip port scan | False |
| `--no-content` | Skip content discovery | False |
| `--no-vulns` | Skip vulnerability scan | False |

---

## 📁 Project Structure

```
vampire_bite/
├── vampire_bite.py          # Main scanner
├── req.py                   # Dependency installer
├── README.md                # Documentation
└── LICENSE                  # MIT License
```

---

## 📊 Output

| Format | File | Description |
|--------|------|-------------|
| **HTML** | `vampire_bite_report_*.html` | Interactive report |
| **JSON** | `vampire_bite_report_*.json` | Machine-readable data |

---

## 🔧 Requirements (Auto-Installed)

| Dependency | Purpose |
|------------|---------|
| Python 3.8+ | Core runtime |
| requests | HTTP requests |
| colorama | Terminal colors |
| beautifulsoup4 | HTML parsing |

---

## ⚠️ Legal Disclaimer

```
THIS TOOL IS FOR AUTHORIZED SECURITY TESTING ONLY.

By using this tool, you agree to:
- Only scan systems you own or have explicit written permission
- Comply with all applicable laws and regulations
- Accept full responsibility for any consequences

The author assumes NO liability for misuse.
```

---

## 👑 Author

**LORD VAMPIRE** — Team Lord

[![GitHub](https://img.shields.io/badge/GitHub-Lord--Vampire-black?logo=github&style=for-the-badge)](https://github.com/Lord-Vampire)
[![Instagram](https://img.shields.io/badge/Instagram-@hamiavalofficial-purple?logo=instagram&style=for-the-badge)](https://instagram.com/hamiavalofficial)

---

## 💰 Support the Project

If you find Vampire Bite useful, you can support its development with **TRON (TRC-20)** donations.

### Cryptocurrency Address

| Network | Address |
|---------|---------|
| **TRON (TRC-20)** | `TRVPZZmXwzysR7GccpmhR6Zd4euk5jPvzV` |

> ⚠️ **IMPORTANT:** Send ONLY TRON (TRC-20) tokens to this address.

**Supported Tokens:**
- TRX (TRON)
- USDT (TRC-20)
- Any TRC-20 token

---

## ⭐ Show Your Support

```bash
git star https://github.com/Lord-Vampire/vampire_bite
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
