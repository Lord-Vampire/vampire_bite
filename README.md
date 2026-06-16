
# 🧛 Vampire Bite

**Vampire Bite** - Ultimate Web Application Security Scanner

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-3.0-red.svg)](https://github.com/lord-vampire/vampire_bite)

---

## 📋 Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Command Line Arguments](#command-line-arguments)
- [Scan Phases](#scan-phases)
- [Output Formats](#output-formats)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)
- [License](#license)

---

## 🎯 Introduction

Vampire Bite is a comprehensive web application security scanner designed for penetration testing and vulnerability assessment. It detects a wide range of security issues in web applications, APIs, and network infrastructure.

**Repository:** [github.com/lord-vampire/vampire_bite](https://github.com/lord-vampire/vampire_bite)

---

## ✨ Features

### Web Application Security
- **XSS** - Cross-Site Scripting (Reflected, Stored, DOM-based, Polyglot)
- **SQL Injection** - Error-based, UNION, Time-based, Boolean-based
- **LFI/RFI** - Local/Remote File Inclusion
- **SSRF** - Server-Side Request Forgery
- **XXE** - XML External Entity
- **CSRF** - Cross-Site Request Forgery
- **IDOR** - Insecure Direct Object Reference
- **Command Injection** - OS Command Injection
- **Open Redirect** - URL Redirection

### Authentication & Session
- **JWT Analysis** - Weak algorithms, sensitive data exposure
- **Session Security** - Cookie attributes, SameSite
- **CORS** - Cross-Origin Resource Sharing misconfigurations

### SSL/TLS Analysis
- Weak cipher detection
- Certificate validation
- Protocol vulnerability testing (SSLv2, SSLv3, TLS 1.0/1.1)

### Network Scanning
- **TCP/UDP Port Scanning**
- Service detection
- OS fingerprinting
- Banner grabbing

### Reconnaissance
- Subdomain enumeration
- Technology fingerprinting (30+ frameworks)
- Content discovery (directories, files, admin panels)
- Web crawling with JavaScript rendering

### API Security
- REST API testing
- GraphQL introspection
- WebSocket security

### Advanced Features
- **WAF Evasion** - Encoding, case variation, comment injection
- **Headless Browser Verification** - Confirm XSS with Selenium
- **False Positive Reduction** - Confidence scoring
- **Resume Capability** - State persistence
- **Multi-threading** - Thread-safe operations
- **Rate Limiting** - Adaptive delays

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip

### Quick Install (Auto)
```bash
# Clone repository
git clone https://github.com/lord-vampire/vampire_bite.git
cd vampire_bite

# Auto-install dependencies
python req.py
```

### Manual Install
```bash
pip install requests colorama beautifulsoup4 lxml tldextract \
    dnspython cryptography pyOpenSSL selenium webdriver-manager \
    websocket-client reportlab Jinja2 fake-useragent
```

### Verify Installation
```bash
python -m py_compile vampire_bite_fixed.py
```

---

## 📖 Usage

### Basic Scan
```bash
python vampire_bite_fixed.py https://target.com
```

### Advanced Scan
```bash
python vampire_bite_fixed.py https://target.com \
    --waf-evasion \
    --verify-vulns \
    --delay 1.5 \
    --js-rendering
```

### With Proxy (Burp Suite)
```bash
python vampire_bite_fixed.py https://target.com \
    --proxy http://127.0.0.1:8080
```

### Custom Headers & Cookies
```bash
python vampire_bite_fixed.py https://target.com \
    --cookies "session=abc123;token=xyz" \
    --headers '{"X-API-Key": "secret"}'
```

### Fast Scan (Skip Heavy Operations)
```bash
python vampire_bite_fixed.py https://target.com \
    --no-port-scan \
    --no-subdomains \
    --no-content
```

### Deep Scan
```bash
python vampire_bite_fixed.py https://target.com \
    --js-rendering \
    --crawl-depth 5 \
    --max-urls 1000 \
    --verify-vulns
```

---

## ⚙️ Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `target` | Target URL (required) | - |
| `--delay` | Request delay (seconds) | 1.0 |
| `--timeout` | HTTP timeout | 10.0 |
| `--port-timeout` | Port scan timeout | 2.0 |
| `--max-workers` | Max threads | 100 |
| `--ports` | Custom ports to scan | Common ports |
| `--scan-type` | Port scan type (syn/tcp/udp) | tcp |
| `--proxy` | Proxy URL | - |
| `--cookies` | Cookies string | - |
| `--headers` | Custom headers JSON | - |
| `--user-agent` | Custom User-Agent | Random |
| `--crawl-depth` | Crawl depth | 3 |
| `--max-urls` | Max URLs to crawl | 500 |
| `--verify-vulns` | Verify with headless browser | False |
| `--waf-evasion` | Enable WAF evasion | False |
| `--js-rendering` | Enable JavaScript rendering | False |
| `--verify-ssl` | Verify SSL certificates | False |
| `--no-port-scan` | Skip port scan | False |
| `--no-subdomains` | Skip subdomain enum | False |
| `--no-content` | Skip content discovery | False |
| `--no-vulns` | Skip vulnerability scan | False |
| `--no-forms` | Skip form analysis | False |
| `--test-rfi` | Test RFI (needs external server) | False |
| `--output-dir` | Output directory | . |

---

## 🔍 Scan Phases

```
Phase 1: Reconnaissance & DNS Enumeration
    ├── Hostname resolution
    ├── DNS records (A, AAAA, MX, NS, TXT, SOA, CNAME)
    └── SSL/TLS analysis

Phase 2: Advanced Port Scanning
    ├── TCP/UDP scanning
    ├── Service detection
    └── Banner grabbing

Phase 3: Subdomain Enumeration
    └── 500+ common subdomains

Phase 4: Content Discovery
    ├── Sensitive files (.env, .git, backup, etc.)
    ├── Admin panels
    └── Open directories

Phase 5: Web Crawling & Form Analysis
    ├── JavaScript rendering (optional)
    ├── Form extraction
    └── API endpoint discovery

Phase 6: Comprehensive Vulnerability Scanning
    ├── XSS (URL params, forms, DOM)
    ├── SQL Injection
    ├── LFI/RFI
    ├── SSRF
    ├── Command Injection
    ├── XXE
    ├── CSRF
    ├── IDOR
    ├── Open Redirect
    ├── JWT/CORS
    └── Security headers
```

---

## 📊 Output Formats

Reports are automatically generated in multiple formats:

| Format | File | Description |
|--------|------|-------------|
| **HTML** | `vampire_bite_report_*.html` | Beautiful interactive report |
| **JSON** | `vampire_bite_report_*.json` | Machine-readable data |
| **XML** | `vampire_bite_report_*.xml` | Import to other tools |
| **CSV** | `vampire_bite_report_*.csv` | Spreadsheet analysis |
| **PDF** | `vampire_bite_report_*.pdf` | Professional document |

---

## 📁 Project Structure

```
vampire_bite/
├── vampire_bite_fixed.py      # Main scanner script
├── vampire_payloads.json      # Attack payloads database
├── req.py                     # Dependency installer
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── LICENSE                    # MIT License
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## ⚠️ Disclaimer

**This tool is for authorized security testing only.**

- Always obtain **explicit written permission** before scanning
- Use with caution on production systems
- The authors are not responsible for misuse or damage
- Respect rate limits and be polite to target servers

**Illegal use is strictly prohibited.**

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- OWASP Testing Guide
- PortSwigger Web Security Academy
- SQLMap Project
- Nmap Project

---

<div align="center">

**Made with ❤️ by Security Research Team**

[⭐ Star this repo](https://github.com/lord-vampire/vampire_bite) if you find it useful!

</div>
