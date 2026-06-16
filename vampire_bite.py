#!/usr/bin/env python3
"""
Vampire Bite Pro v3.0 - Ultimate Professional Security Scanner
Author: Security Research Team
Version: 3.0.0 - Complete Rewrite

FEATURES:
  - Web Application Security: XSS, SQLi, LFI, RFI, SSRF, XXE, CSRF, IDOR, Command Injection, Open Redirect
  - Advanced Network Scanning: SYN Stealth, TCP Connect, UDP, Service Detection, OS Fingerprinting
  - Content Discovery: Directory Brute-forcing, API Discovery, Subdomain Enumeration
  - Deep Technology Fingerprinting: 30+ frameworks/platforms
  - SSL/TLS Analysis: Weak Cipher Detection, Certificate Validation, Protocol Vulnerability Testing
  - Authentication Testing: JWT Analysis, Session Security
  - API Security: REST, GraphQL, WebSocket
  - Advanced Crawling: JavaScript Rendering, AJAX, SPA Support
  - WAF Evasion: Encoding, Case Variation, Comment Injection, Null Bytes
  - Smart False Positive Reduction: Confidence Scoring, Verification
  - Professional Reporting: HTML, JSON, XML, CSV, PDF
  - Resume Capability: State Persistence
  - Rate Limiting & Politeness: Adaptive Delays, robots.txt Respect
  - Multi-threading: Thread-safe Operations
"""

import subprocess
import sys
import os
import json
import re
import socket
import time
import random
import hashlib
import base64
import html as html_module
import threading
import ssl
import ipaddress
import urllib3
from datetime import datetime
from urllib.parse import urlparse, urljoin, quote, parse_qs, urlencode, unquote
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple, Set, Any
from enum import Enum
import logging
import argparse
import signal
import string
import itertools
import xml.etree.ElementTree as ET
from collections import defaultdict, Counter
import warnings
warnings.filterwarnings('ignore')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# =============================================================================
# DEPENDENCY MANAGEMENT
# =============================================================================

def auto_install(pkg):
    """Auto-install a package using pip."""
    import subprocess
    import sys
    methods = [
        [sys.executable, "-m", "pip", "install", pkg, "--quiet", "--upgrade"],
        [sys.executable, "-m", "pip", "install", pkg, "--upgrade"],
        [sys.executable, "-m", "pip", "install", pkg],
    ]
    for cmd in methods:
        try:
            subprocess.check_call(cmd, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            return True
        except:
            continue
    print("[ERROR] Could not auto-install " + pkg)
    print("[INFO] Please install manually: python -m pip install " + pkg)
    return False
def check_deps():
    """Check and auto-install all required dependencies."""
    deps = {
        "requests": "requests",
        "colorama": "colorama",
        "bs4": "beautifulsoup4",
        "lxml": "lxml",
        "tldextract": "tldextract",
        "dnspython": "dnspython",
        "cryptography": "cryptography",
        "pyOpenSSL": "pyOpenSSL",
        "selenium": "selenium",
        "webdriver_manager": "webdriver-manager",
        "websocket": "websocket-client",
        "reportlab": "reportlab",
        "jinja2": "Jinja2",
        "fake_useragent": "fake-useragent",
    }

    # Create requirements.txt file next to the script
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    req_file = os.path.join(script_dir, "requirements.txt")
    if not os.path.exists(req_file):
        with open(req_file, "w") as f:
            f.write("requests\ncolorama\nbeautifulsoup4\nlxml\ntldextract\n")
            f.write("dnspython\ncryptography\npyOpenSSL\nselenium\n")
            f.write("webdriver-manager\nwebsocket-client\nreportlab\n")
            f.write("Jinja2\nfake-useragent\n")

    missing = []
    for mod, pkg in deps.items():
        try:
            __import__(mod.replace('-', '_'))
        except ImportError:
            missing.append(pkg)

    if missing:
        print("[INFO] Missing dependencies: " + ", ".join(missing))
        print("[INFO] Attempting auto-install...")
        for pkg in missing:
            auto_install(pkg)

        still_missing = []
        for mod, pkg in deps.items():
            try:
                __import__(mod.replace('-', '_'))
            except ImportError:
                still_missing.append(pkg)

        if still_missing:
            print("[ERROR] Failed to install: " + ", ".join(still_missing))
            print("[INFO] Please run: python -m pip install -r requirements.txt")
            print("[INFO] Or install manually:")
            for pkg in still_missing:
                print("    python -m pip install " + pkg)
            sys.exit(1)

    print("[OK] All dependencies are installed.")

# =============================================================================
# PAYLOAD LOADER
# =============================================================================

def _load_payloads():
    """Load all scanner payloads from JSON file."""
    import os, json
    script_dir = os.path.dirname(os.path.abspath(__file__))
    payload_file = os.path.join(script_dir, "vampire_payloads.json")
    try:
        with open(payload_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Error loading payloads: " + str(e))
        return {}

_PAYLOADS = _load_payloads()


import requests
from colorama import init, Fore, Back, Style
from bs4 import BeautifulSoup
import tldextract
import dns.resolver
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import websocket
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from jinja2 import Template
from fake_useragent import UserAgent

init(autoreset=True)

# =============================================================================
# LOGGING
# =============================================================================

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA + Style.BRIGHT
    }
    def format(self, record):
        color = self.COLORS.get(record.levelname, '')
        reset = Style.RESET_ALL
        record.levelname = color + record.levelname + reset
        return super().format(record)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('vampire_bite_pro_v3.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s'))

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# =============================================================================
# ENUMS & DATA CLASSES
# =============================================================================

class Severity(Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Info"

class VulnType(Enum):
    XSS = "Cross-Site Scripting"
    SQLI = "SQL Injection"
    LFI = "Local File Inclusion"
    RFI = "Remote File Inclusion"
    SSRF = "Server-Side Request Forgery"
    IDOR = "Insecure Direct Object Reference"
    XXE = "XML External Entity"
    CSRF = "Cross-Site Request Forgery"
    CMD_INJECTION = "Command Injection"
    OPEN_REDIRECT = "Open Redirect"
    PATH_TRAVERSAL = "Path Traversal"
    INSECURE_DESERIALIZATION = "Insecure Deserialization"
    JWT_WEAK = "JWT Weakness"
    CORS = "CORS Misconfiguration"
    SECURITY_HEADERS = "Missing Security Headers"
    SSL_TLS = "SSL/TLS Weakness"
    INFO_DISCLOSURE = "Information Disclosure"
    OPEN_PORT = "Open Port"
    WEAK_PASSWORD = "Weak Password"
    BACKUP_FILE = "Backup File Exposure"
    API_VULN = "API Vulnerability"
    GRAPHQL = "GraphQL Vulnerability"
    WEBSOCKET = "WebSocket Vulnerability"
    RACE_CONDITION = "Race Condition"
    BUSINESS_LOGIC = "Business Logic Flaw"

@dataclass
class Vulnerability:
    type: VulnType
    severity: Severity
    title: str
    description: str
    url: str
    parameter: str = ""
    payload: str = ""
    evidence: str = ""
    remediation: str = ""
    cvss_score: float = 0.0
    cvss_vector: str = ""
    cwe_id: str = ""
    confidence: float = 0.0
    verified: bool = False
    references: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "type": self.type.value,
            "severity": self.severity.value,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "parameter": self.parameter,
            "payload": self.payload,
            "evidence": self.evidence,
            "remediation": self.remediation,
            "cvss_score": self.cvss_score,
            "cvss_vector": self.cvss_vector,
            "cwe_id": self.cwe_id,
            "confidence": self.confidence,
            "verified": self.verified,
            "references": self.references,
            "tags": self.tags
        }

@dataclass
class ScanResult:
    target: str = ""
    ip: str = ""
    scan_time: str = ""
    duration: float = 0.0
    open_ports: List[Dict] = field(default_factory=list)
    technologies: List[str] = field(default_factory=list)
    web_server: str = ""
    waf_detected: str = ""
    ssl_info: Dict = field(default_factory=dict)
    vulnerabilities: List[Vulnerability] = field(default_factory=list)
    sensitive_files: List[Dict] = field(default_factory=list)
    admin_panels: List[Dict] = field(default_factory=list)
    open_directories: List[Dict] = field(default_factory=list)
    forms: List[Dict] = field(default_factory=list)
    cookies: List[Dict] = field(default_factory=list)
    headers: Dict = field(default_factory=dict)
    dns_info: Dict = field(default_factory=dict)
    subdomains: List[str] = field(default_factory=list)
    api_endpoints: List[Dict] = field(default_factory=list)
    js_files: List[str] = field(default_factory=list)
    endpoints: List[str] = field(default_factory=list)
    crawl_data: Dict = field(default_factory=dict)
    auth_findings: List[Dict] = field(default_factory=list)
    rate_limit_info: Dict = field(default_factory=dict)

    def to_dict(self):
        return {
            "target": self.target,
            "ip": self.ip,
            "scan_time": self.scan_time,
            "duration": self.duration,
            "open_ports": self.open_ports,
            "technologies": self.technologies,
            "web_server": self.web_server,
            "waf_detected": self.waf_detected,
            "ssl_info": self.ssl_info,
            "vulnerabilities": [v.to_dict() for v in self.vulnerabilities],
            "sensitive_files": self.sensitive_files,
            "admin_panels": self.admin_panels,
            "open_directories": self.open_directories,
            "forms": self.forms,
            "cookies": self.cookies,
            "headers": self.headers,
            "dns_info": self.dns_info,
            "subdomains": self.subdomains,
            "api_endpoints": self.api_endpoints,
            "js_files": self.js_files,
            "endpoints": self.endpoints,
            "crawl_data": self.crawl_data,
            "auth_findings": self.auth_findings,
            "rate_limit_info": self.rate_limit_info
        }

# =============================================================================
# CVSS CALCULATOR
# =============================================================================

class CVSSCalculator:
    @staticmethod
    def calculate(cvss_vector: str) -> float:
        try:
            metrics = {}
            for metric in cvss_vector.split('/'):
                if ':' in metric:
                    k, v = metric.split(':')
                    metrics[k] = v
            av = {'N': 0.85, 'A': 0.62, 'L': 0.55, 'P': 0.2}.get(metrics.get('AV', 'N'), 0.85)
            ac = {'L': 0.77, 'H': 0.44}.get(metrics.get('AC', 'L'), 0.77)
            pr = {'N': 0.85, 'L': 0.62, 'H': 0.27}.get(metrics.get('PR', 'N'), 0.85)
            ui = {'N': 0.85, 'R': 0.62}.get(metrics.get('UI', 'N'), 0.85)
            s = {'U': 6.42, 'C': 7.52}.get(metrics.get('S', 'U'), 6.42)
            c = {'H': 0.56, 'L': 0.22, 'N': 0}.get(metrics.get('C', 'N'), 0)
            i = {'H': 0.56, 'L': 0.22, 'N': 0}.get(metrics.get('I', 'N'), 0)
            a = {'H': 0.56, 'L': 0.22, 'N': 0}.get(metrics.get('A', 'N'), 0)
            impact = 1 - ((1 - c) * (1 - i) * (1 - a))
            if metrics.get('S') == 'C':
                impact = 1.08 * (impact - 0.029) - 3.25 * pow(impact - 0.02, 15)
            else:
                impact = 6.42 * impact
            exploitability = 8.22 * av * ac * pr * ui
            if impact <= 0:
                return 0.0
            score = min(impact + exploitability, 10)
            return round(score, 1)
        except:
            return 0.0

# =============================================================================
# WAF DETECTOR (ENHANCED)
# =============================================================================

class WAFDetector:
    WAF_SIGNATURES = {
        "Cloudflare": {
            "headers": ["cf-ray", "cf-cache-status", "cf-request-id", "server: cloudflare"],
            "cookies": ["__cfduid", "cf_clearance", "__cf_bm"],
            "body": ["cloudflare", "cf-browser-verification", "attention required", "cloudflare ray id"]
        },
        "AWS WAF": {
            "headers": ["x-amzn-requestid", "x-amz-id-2", "awselb"],
            "cookies": ["aws-waf-token"],
            "body": ["aws waf", "amazon web services"]
        },
        "ModSecurity": {
            "headers": ["mod_security", "modsecurity", "noyb"],
            "cookies": [],
            "body": ["mod_security", "not acceptable", "406 not acceptable"]
        },
        "Sucuri": {
            "headers": ["x-sucuri-id", "x-sucuri-cache", "server: sucuri"],
            "cookies": ["sucuri"],
            "body": ["sucuri website firewall", "access denied"]
        },
        "Incapsula": {
            "headers": ["x-iinfo", "incap-ses", "visid_incap"],
            "cookies": ["incap_ses", "visid_incap"],
            "body": ["incapsula incident id", "incapsula"]
        },
        "Akamai": {
            "headers": ["akamai", "x-akamai-transformed", "ak_bmsc"],
            "cookies": ["ak_bmsc"],
            "body": ["akamai"]
        },
        "F5 BIG-IP ASM": {
            "headers": ["bigip", "f5", "x-waf-event-info", "x-cnection"],
            "cookies": [],
            "body": ["the requested url was rejected", "please consult with your administrator"]
        },
        "Barracuda": {
            "headers": ["barra"],
            "cookies": [],
            "body": ["you are blocked", "barracuda"]
        },
        "Wordfence": {
            "headers": [],
            "cookies": [],
            "body": ["generated by wordfence", "wordfence"]
        },
        "Imperva": {
            "headers": ["x-iinfo", "x-cdn", "imperva"],
            "cookies": ["incap_ses"],
            "body": ["imperva", "incapsula"]
        },
        "Fortinet": {
            "headers": ["fortigate", "fortiweb"],
            "cookies": [],
            "body": ["fortinet", "fortigate"]
        },
        "Radware": {
            "headers": ["x-rdwr"],
            "cookies": [],
            "body": ["radware", "appwall"]
        },
        "DenyAll": {
            "headers": ["sessioncookie"],
            "cookies": [],
            "body": ["denyall", "condition intercepted"]
        },
        "Citrix NetScaler": {
            "headers": ["ns_cookietest", "ns_af"],
            "cookies": ["ns_cookietest", "citrix_ns_id"],
            "body": ["citrix", "netscaler"]
        },
        "Reblaze": {
            "headers": ["x-reblaze"],
            "cookies": [],
            "body": ["reblaze", "access denied"]
        }
    }

    @classmethod
    def detect(cls, response_headers, response_text="", response_status=0):
        detected = []
        headers_str = str(response_headers).lower()
        text_lower = response_text.lower()
        for waf_name, signatures in cls.WAF_SIGNATURES.items():
            score = 0
            for header in signatures["headers"]:
                if header.lower() in headers_str:
                    score += 2
            for cookie in signatures["cookies"]:
                if cookie.lower() in headers_str or cookie.lower() in text_lower:
                    score += 2
            for body_text in signatures["body"]:
                if body_text.lower() in text_lower:
                    score += 1
            if score >= 2:
                detected.append((waf_name, score))
        detected.sort(key=lambda x: x[1], reverse=True)
        return ", ".join([w[0] for w in detected]) if detected else "None Detected"

# =============================================================================
# WAF EVASION
# =============================================================================

class WAFEvasion:
    ENCODINGS = {
        'url': lambda x: quote(x, safe=''),
        'double_url': lambda x: quote(quote(x, safe=''), safe=''),
        'unicode': lambda x: ''.join('\\u{0:04x}'.format(ord(c)) for c in x),
        'html_entities': lambda x: ''.join('&#{0};'.format(ord(c)) for c in x),
        'hex': lambda x: ''.join('%{0:02x}'.format(ord(c)) for c in x),
        'base64': lambda x: base64.b64encode(x.encode()).decode(),
    }

    CASE_VARIATIONS = [
        lambda x: x.lower(),
        lambda x: x.upper(),
        lambda x: x.title(),
        lambda x: ''.join(random.choice([c.upper(), c.lower()]) for c in x),
    ]

    @classmethod
    def evade(cls, payload: str, technique: str = "random") -> List[str]:
        variations = [payload]
        if technique in ["random", "encoding"]:
            for name, encoder in cls.ENCODINGS.items():
                try:
                    variations.append(encoder(payload))
                except:
                    pass
        if technique in ["random", "case"]:
            for case_func in cls.CASE_VARIATIONS:
                variations.append(case_func(payload))
        if technique in ["random", "concatenation"]:
            if '<script>' in payload.lower():
                parts = payload.replace('<script>', '').replace('</script>', '').split('alert')
                if len(parts) > 1:
                    concat = '<scr' + 'ipt>' + parts[0] + 'aler' + 't' + parts[1] + '</scr' + 'ipt>'
                    variations.append(concat)
        if technique in ["random", "comment"]:
            commented = payload.replace(' ', '<!-- -->')
            variations.append(commented)
            null_payload = payload.replace('', '\\x00')
            variations.append(null_payload)
        return list(set(variations))

# =============================================================================
# XSS SCANNER (COMPREHENSIVE)
# =============================================================================

class XSSScanner:
    PAYLOADS = _PAYLOADS.get("xss", {})

    def __init__(self, session, config=None):
        self.session = session
        self.config = config or {}
        self.evader = WAFEvasion()
        self.verified_vulns = []
        self.lock = threading.Lock()

    def _find_context(self, response_text, payload):
        if payload not in response_text:
            return None
        idx = response_text.find(payload)
        surrounding = response_text[max(0, idx-200):min(len(response_text), idx+len(payload)+200)]
        if re.search(r'<[^>]*>' + re.escape(payload), surrounding, re.IGNORECASE):
            return "html"
        attr_pattern = r'\\w+\\s*=\\s*["\'][^"\']*' + re.escape(payload)
        if re.search(attr_pattern, surrounding, re.IGNORECASE):
            return "attribute"
        if re.search(r'<script[^>]*>.*?' + re.escape(payload), surrounding, re.IGNORECASE | re.DOTALL):
            return "javascript"
        if re.search(r'href\\s*=\\s*["\'][^"\']*' + re.escape(payload), surrounding, re.IGNORECASE):
            return "url"
        return "unknown"

    def _is_executable(self, context, payload, response_text):
        executable_patterns = {
            "html": ["<script>", "<img", "<svg", "<body", "<iframe", "<input", "<video", "<audio", "<marquee", "<details"],
            "attribute": ["onerror=", "onload=", "onmouseover=", "onfocus=", "onmouseenter=", "onpointerdown=", "onpointerup=", "onpointerenter=", "onpointerleave=", "onpointermove=", "onpointerover="],
            "javascript": ["alert(", "confirm(", "prompt(", "eval(", "document.cookie", "window.location"],
            "url": ["javascript:", "data:text/html", "vbscript:", "mocha:", "livescript:"]
        }
        patterns = executable_patterns.get(context, [])
        return any(p.lower() in response_text.lower() for p in patterns)

    def _verify_xss(self, url, param, payload, context):
        try:
            options = ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            driver.get(url)
            time.sleep(2)
            try:
                alert = driver.switch_to.alert
                alert_text = alert.text
                alert.accept()
                if 'XSS_VBP' in alert_text:
                    driver.quit()
                    return True
            except:
                pass
            if driver.execute_script("return document.querySelector('script') !== null"):
                driver.quit()
                return True
            driver.quit()
            return False
        except Exception as e:
            logger.debug("XSS verification error: " + str(e))
            return False

    def test_url_parameter(self, url, param):
        findings = []
        parsed = urlparse(url)
        base_params = parse_qs(parsed.query)
        for context_type, payloads in self.PAYLOADS.items():
            for payload in payloads:
                variations = self.evader.evade(payload, "random") if self.config.get('waf_evasion', True) else [payload]
                for variation in variations:
                    test_params = base_params.copy()
                    test_params[param] = [variation]
                    new_query = urlencode(test_params, doseq=True)
                    test_url = parsed._replace(query=new_query).geturl()
                    try:
                        r = self.session.get(test_url, timeout=10, allow_redirects=False)
                        if r.status_code in [301, 302, 307, 308]:
                            r = self.session.get(test_url, timeout=10)
                        context = self._find_context(r.text, variation)
                        if context and self._is_executable(context, variation, r.text):
                            verified = False
                            if self.config.get('verify_vulns', True):
                                verified = self._verify_xss(test_url, param, variation, context)
                            confidence = 0.9 if verified else 0.7
                            finding = Vulnerability(
                                type=VulnType.XSS,
                                severity=Severity.HIGH if verified else Severity.MEDIUM,
                                title=("Verified " if verified else "Potential ") + "XSS in " + param + " (" + context + " context)",
                                description="Cross-Site Scripting vulnerability found in '" + param + "' parameter. Payload executes in " + context + " context. " + ("Verified with headless browser." if verified else "Potential - needs manual verification."),
                                url=test_url,
                                parameter=param,
                                payload=variation[:100],
                                evidence="Context: " + context + ", Payload reflected in response, " + ("Alert triggered" if verified else "Payload found in response"),
                                remediation="Implement context-aware output encoding. Use Content Security Policy (CSP). Validate and sanitize all user inputs. Use HTML sanitization libraries.",
                                cvss_score=6.1 if not verified else 8.8,
                                cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L" if not verified else "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
                                cwe_id="CWE-79",
                                confidence=confidence,
                                verified=verified,
                                references=[
                                    "https://owasp.org/www-community/attacks/xss/",
                                    "https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html",
                                    "https://portswigger.net/web-security/cross-site-scripting"
                                ],
                                tags=["xss", context, "reflected"]
                            )
                            with self.lock:
                                if not any(f.url == finding.url and f.parameter == finding.parameter for f in self.verified_vulns):
                                    self.verified_vulns.append(finding)
                                    findings.append(finding)
                    except Exception as e:
                        logger.debug("XSS test error for " + param + ": " + str(e))
                    time.sleep(self.config.get('delay', 0.5))
        return findings

    def test_form(self, form, base_url):
        findings = []
        action = form.get('action', base_url)
        if action.startswith('/'):
            action = urljoin(base_url, action)
        method = form.get('method', 'GET').upper()
        inputs = form.get('inputs', [])
        for payload in self.PAYLOADS["html_context"] + self.PAYLOADS["polyglot"]:
            data = {}
            for inp in inputs:
                if inp.get('type') not in ['submit', 'button', 'hidden']:
                    data[inp['name']] = payload
            try:
                if method == 'POST':
                    r = self.session.post(action, data=data, timeout=10)
                else:
                    r = self.session.get(action, params=data, timeout=10)
                context = self._find_context(r.text, payload)
                if context and self._is_executable(context, payload, r.text):
                    verified = False
                    if self.config.get('verify_vulns', True):
                        verified = self._verify_xss(action, str(list(data.keys())), payload, context)
                    confidence = 0.85 if verified else 0.65
                    finding = Vulnerability(
                        type=VulnType.XSS,
                        severity=Severity.HIGH if verified else Severity.MEDIUM,
                        title=("Verified " if verified else "Potential ") + "XSS in form at " + action,
                        description="XSS vulnerability found in form submission. Payload executes in " + context + " context. " + ("Verified with headless browser." if verified else "Potential - needs manual verification."),
                        url=action,
                        parameter=str(list(data.keys())),
                        payload=payload[:100],
                        evidence="Context: " + context + ", Form submitted and payload executed",
                        remediation="Implement context-aware output encoding. Use CSP. Validate inputs server-side. Use anti-CSRF tokens.",
                        cvss_score=6.1 if not verified else 8.8,
                        cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L" if not verified else "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
                        cwe_id="CWE-79",
                        confidence=confidence,
                        verified=verified,
                        references=[
                            "https://owasp.org/www-community/attacks/xss/",
                            "https://portswigger.net/web-security/cross-site-scripting"
                        ],
                        tags=["xss", context, "stored" if method == 'POST' else "reflected"]
                    )
                    with self.lock:
                        if not any(f.url == finding.url and f.parameter == finding.parameter for f in self.verified_vulns):
                            self.verified_vulns.append(finding)
                            findings.append(finding)
            except Exception as e:
                logger.debug("Form XSS test error: " + str(e))
            time.sleep(self.config.get('delay', 0.5))
        return findings

    def test_dom_xss(self, url):
        findings = []
        dom_payloads = _PAYLOADS.get("dom_xss", [])
        for payload in dom_payloads:
            test_url = url + payload
            try:
                options = ChromeOptions()
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
                driver.get(test_url)
                time.sleep(2)
                try:
                    alert = driver.switch_to.alert
                    alert_text = alert.text
                    alert.accept()
                    if 'DOM_XSS' in alert_text:
                        finding = Vulnerability(
                            type=VulnType.XSS,
                            severity=Severity.HIGH,
                            title="DOM-based XSS detected",
                            description="DOM-based XSS vulnerability found. The application processes user input through JavaScript without proper sanitization.",
                            url=test_url,
                            parameter="URL fragment/hash",
                            payload=payload,
                            evidence="Alert triggered with text: " + alert_text,
                            remediation="Sanitize all user input before DOM manipulation. Use DOMPurify or similar libraries. Avoid dangerous JavaScript functions like eval(), innerHTML with user input.",
                            cvss_score=8.8,
                            cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
                            cwe_id="CWE-79",
                            confidence=0.95,
                            verified=True,
                            references=[
                                "https://owasp.org/www-community/attacks/DOM_Based_XSS/",
                                "https://portswigger.net/web-security/cross-site-scripting/dom-based"
                            ],
                            tags=["xss", "dom-based", "verified"]
                        )
                        findings.append(finding)
                except:
                    pass
                driver.quit()
            except Exception as e:
                logger.debug("DOM XSS test error: " + str(e))
        return findings

# =============================================================================
# SQL INJECTION SCANNER (COMPREHENSIVE)
# =============================================================================

class SQLiScanner:
    PAYLOADS = _PAYLOADS.get("sqli", {})

    ERROR_PATTERNS = {
        "MySQL": ["mysql_fetch", "mysqli_", "you have an error in your sql syntax", "warning: mysql", "mysql error"],
        "PostgreSQL": ["postgresql", "pg_query", "pg_exec", "warning: pg_", "pg_connect"],
        "MSSQL": ["microsoft sql server", "mssql", "odbc sql server driver", "sql server", "unclosed quotation mark"],
        "Oracle": ["ora-", "oracle", "pl/sql", "oci_", "ora-01756", "ora-00933"],
        "SQLite": ["sqlite3", "sqlite_query", "sqlite_", "no such table", "near \".\": syntax error"],
        "Generic": ["sql syntax", "syntax error", "unexpected token", "unclosed quotation mark"],
    }

    def __init__(self, session, config=None):
        self.session = session
        self.config = config or {}
        self.lock = threading.Lock()
        self.verified_vulns = []

    def _detect_error(self, response_text):
        text_lower = response_text.lower()
        for db_type, patterns in self.ERROR_PATTERNS.items():
            for pattern in patterns:
                if pattern.lower() in text_lower:
                    return True, db_type
        return False, ""

    def _test_time_based(self, url, param, payload):
        parsed = urlparse(url)
        base_params = parse_qs(parsed.query)
        normal_params = base_params.copy()
        normal_params[param] = ["1"]
        normal_query = urlencode(normal_params, doseq=True)
        normal_url = parsed._replace(query=normal_query).geturl()
        start = time.time()
        try:
            self.session.get(normal_url, timeout=10)
        except:
            return False
        normal_time = time.time() - start
        test_params = base_params.copy()
        test_params[param] = [payload]
        test_query = urlencode(test_params, doseq=True)
        test_url = parsed._replace(query=test_query).geturl()
        start = time.time()
        try:
            self.session.get(test_url, timeout=15)
        except:
            elapsed = time.time() - start
            return elapsed >= 4.5
        elapsed = time.time() - start
        return elapsed >= 4.5 and elapsed > normal_time * 3

    def _test_boolean_based(self, url, param):
        parsed = urlparse(url)
        base_params = parse_qs(parsed.query)
        true_params = base_params.copy()
        true_params[param] = ["' AND '1'='1"]
        true_query = urlencode(true_params, doseq=True)
        true_url = parsed._replace(query=true_query).geturl()
        false_params = base_params.copy()
        false_params[param] = ["' AND '1'='2"]
        false_query = urlencode(false_params, doseq=True)
        false_url = parsed._replace(query=false_query).geturl()
        try:
            r_true = self.session.get(true_url, timeout=10)
            r_false = self.session.get(false_url, timeout=10)
            if len(r_true.text) != len(r_false.text):
                diff_ratio = abs(len(r_true.text) - len(r_false.text)) / max(len(r_true.text), len(r_false.text), 1)
                if diff_ratio > 0.1:
                    return True
        except Exception as e:
            logger.debug("Boolean test error: " + str(e))
        return False

    def _test_union_based(self, url, param):
        parsed = urlparse(url)
        base_params = parse_qs(parsed.query)
        for payload in self.PAYLOADS["union_based"]:
            test_params = base_params.copy()
            test_params[param] = [payload]
            test_query = urlencode(test_params, doseq=True)
            test_url = parsed._replace(query=test_query).geturl()
            try:
                r = self.session.get(test_url, timeout=10)
                union_indicators = ["NULL" in r.text and "NULL" not in payload, "test" in r.text.lower() and "test" in payload]
                if any(union_indicators):
                    return True, payload
            except:
                pass
        return False, ""

    def test_url_parameter(self, url, param):
        findings = []
        # Phase 1: Error-based
        for payload in self.PAYLOADS["error_based"]:
            parsed = urlparse(url)
            base_params = parse_qs(parsed.query)
            base_params[param] = [payload]
            new_query = urlencode(base_params, doseq=True)
            test_url = parsed._replace(query=new_query).geturl()
            try:
                r = self.session.get(test_url, timeout=10)
                has_error, db_type = self._detect_error(r.text)
                if has_error:
                    finding = Vulnerability(
                        type=VulnType.SQLI, severity=Severity.CRITICAL,
                        title="Error-Based SQL Injection in " + param,
                        description="SQL Injection vulnerability found in '" + param + "' parameter. Database type: " + db_type + ".",
                        url=test_url, parameter=param, payload=payload,
                        evidence="Database error detected: " + db_type,
                        remediation="Use parameterized queries/prepared statements. Implement input validation. Apply principle of least privilege.",
                        cvss_score=9.8, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                        cwe_id="CWE-89", confidence=0.95, verified=True,
                        references=["https://owasp.org/www-community/attacks/SQL_Injection/", "https://portswigger.net/web-security/sql-injection"],
                        tags=["sqli", "error-based", db_type.lower()]
                    )
                    with self.lock:
                        if not any(f.url == finding.url and f.parameter == finding.parameter for f in self.verified_vulns):
                            self.verified_vulns.append(finding)
                            findings.append(finding)
                    break
            except Exception as e:
                logger.debug("SQLi error test: " + str(e))
            time.sleep(self.config.get('delay', 0.5))
        # Phase 2: Union-based
        if not findings:
            union_result, union_payload = self._test_union_based(url, param)
            if union_result:
                finding = Vulnerability(
                    type=VulnType.SQLI, severity=Severity.CRITICAL,
                    title="UNION-Based SQL Injection in " + param,
                    description="UNION-based SQL Injection found in '" + param + "' parameter.",
                    url=url, parameter=param, payload=union_payload,
                    evidence="UNION SELECT payload returned different content structure",
                    remediation="Use parameterized queries. Implement strict input validation.",
                    cvss_score=9.1, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N",
                    cwe_id="CWE-89", confidence=0.85, verified=True,
                    references=["https://portswigger.net/web-security/sql-injection/union-attacks"],
                    tags=["sqli", "union-based", "data-extraction"]
                )
                with self.lock:
                    if not any(f.url == finding.url and f.parameter == finding.parameter for f in self.verified_vulns):
                        self.verified_vulns.append(finding)
                        findings.append(finding)
        # Phase 3: Time-based
        if not findings:
            for payload in self.PAYLOADS["time_based"]:
                if self._test_time_based(url, param, payload):
                    finding = Vulnerability(
                        type=VulnType.SQLI, severity=Severity.CRITICAL,
                        title="Time-Based Blind SQL Injection in " + param,
                        description="Blind SQL Injection found in '" + param + "' parameter using time delay.",
                        url=url, parameter=param, payload=payload,
                        evidence="Response delayed by 5+ seconds",
                        remediation="Use parameterized queries. Implement strict input validation.",
                        cvss_score=8.1, cvss_vector="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N",
                        cwe_id="CWE-89", confidence=0.9, verified=True,
                        references=["https://portswigger.net/web-security/sql-injection/blind"],
                        tags=["sqli", "blind", "time-based"]
                    )
                    with self.lock:
                        if not any(f.url == finding.url and f.parameter == finding.parameter for f in self.verified_vulns):
                            self.verified_vulns.append(finding)
                            findings.append(finding)
                    break
                time.sleep(self.config.get('delay', 0.5))
        # Phase 4: Boolean-based
        if not findings:
            if self._test_boolean_based(url, param):
                finding = Vulnerability(
                    type=VulnType.SQLI, severity=Severity.HIGH,
                    title="Boolean-Based Blind SQL Injection in " + param,
                    description="Boolean-based blind SQL Injection found in '" + param + "' parameter.",
                    url=url, parameter=param, payload="' AND '1'='1 vs ' AND '1'='2",
                    evidence="Different response sizes for true/false conditions",
                    remediation="Use parameterized queries. Implement input validation.",
                    cvss_score=7.5, cvss_vector="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N",
                    cwe_id="CWE-89", confidence=0.8, verified=True,
                    references=["https://portswigger.net/web-security/sql-injection/blind"],
                    tags=["sqli", "blind", "boolean-based"]
                )
                with self.lock:
                    if not any(f.url == finding.url and f.parameter == finding.parameter for f in self.verified_vulns):
                        self.verified_vulns.append(finding)
                        findings.append(finding)
        return findings

# =============================================================================
# LFI/RFI SCANNER
# =============================================================================

class LFIRFIScanner:
    LFI_PAYLOADS = _PAYLOADS.get("lfi", [])

    RFI_PAYLOADS = _PAYLOADS.get("rfi", [])

    LFI_INDICATORS = [
        "root:", ":/bin/bash", ":/bin/sh", "daemon:", "bin:",
        "[extensions]", "[fonts]", "[files]", "for 16-bit app support",
        "PATH=", "HOME=", "USER=", "SHELL=", "<?php", "<?=", "<?xml",
    ]

    def __init__(self, session, config=None):
        self.session = session
        self.config = config or {}
        self.lock = threading.Lock()
        self.verified_vulns = []

    def _is_lfi_vulnerable(self, response_text):
        text_lower = response_text.lower()
        for indicator in self.LFI_INDICATORS:
            if indicator.lower() in text_lower:
                return True, indicator
        return False, ""

    def test_url_parameter(self, url, param):
        findings = []
        parsed = urlparse(url)
        base_params = parse_qs(parsed.query)
        # Test LFI
        for payload in self.LFI_PAYLOADS:
            test_params = base_params.copy()
            test_params[param] = [payload]
            test_query = urlencode(test_params, doseq=True)
            test_url = parsed._replace(query=test_query).geturl()
            try:
                r = self.session.get(test_url, timeout=10)
                is_vuln, indicator = self._is_lfi_vulnerable(r.text)
                if is_vuln:
                    finding = Vulnerability(
                        type=VulnType.LFI, severity=Severity.HIGH,
                        title="Local File Inclusion in " + param,
                        description="LFI vulnerability found in '" + param + "' parameter. The application allows reading arbitrary local files.",
                        url=test_url, parameter=param, payload=payload,
                        evidence="File content detected: " + indicator,
                        remediation="Validate and sanitize file paths. Use allowlists. Disable dangerous PHP wrappers. Use chroot jail.",
                        cvss_score=7.5, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
                        cwe_id="CWE-22", confidence=0.9, verified=True,
                        references=["https://owasp.org/www-community/attacks/Path_Traversal/", "https://portswigger.net/web-security/file-path-traversal"],
                        tags=["lfi", "path-traversal"]
                    )
                    with self.lock:
                        if not any(f.url == finding.url and f.parameter == finding.parameter for f in self.verified_vulns):
                            self.verified_vulns.append(finding)
                            findings.append(finding)
                    break
            except Exception as e:
                logger.debug("LFI test error: " + str(e))
            time.sleep(self.config.get('delay', 0.5))
        # Test RFI
        if self.config.get('test_rfi', False):
            for payload in self.RFI_PAYLOADS:
                test_params = base_params.copy()
                test_params[param] = [payload]
                test_query = urlencode(test_params, doseq=True)
                test_url = parsed._replace(query=test_query).geturl()
                try:
                    r = self.session.get(test_url, timeout=10)
                    if any(indicator in r.text.lower() for indicator in ["shell", "cmd", "exec", "system"]):
                        finding = Vulnerability(
                            type=VulnType.RFI, severity=Severity.CRITICAL,
                            title="Remote File Inclusion in " + param,
                            description="RFI vulnerability found in '" + param + "' parameter.",
                            url=test_url, parameter=param, payload=payload,
                            evidence="Remote file inclusion detected",
                            remediation="Disable remote file inclusion. Validate file paths. Disable allow_url_fopen.",
                            cvss_score=9.8, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                            cwe_id="CWE-98", confidence=0.7, verified=False,
                            references=["https://owasp.org/www-community/vulnerabilities/Remote_File_Inclusion"],
                            tags=["rfi", "remote-file-inclusion"]
                        )
                        with self.lock:
                            if not any(f.url == finding.url and f.parameter == finding.parameter for f in self.verified_vulns):
                                self.verified_vulns.append(finding)
                                findings.append(finding)
                        break
                except Exception as e:
                    logger.debug("RFI test error: " + str(e))
                time.sleep(self.config.get('delay', 0.5))
        return findings

# =============================================================================
# SSRF SCANNER
# =============================================================================

class SSRFScanner:
    SSRF_PAYLOADS = _PAYLOADS.get("ssrf", [])

    SSRF_INDICATORS = [
        "ssh", "mysql", "redis", "nginx", "apache", "ami-id", "instance-id",
        "hostname", "local-ipv4", "metadata", "google", "compute", "root:",
        "daemon:", "PATH=", "SHELL=",
    ]

    def __init__(self, session, config=None):
        self.session = session
        self.config = config or {}
        self.lock = threading.Lock()
        self.verified_vulns = []

    def test_url_parameter(self, url, param):
        findings = []
        parsed = urlparse(url)
        base_params = parse_qs(parsed.query)
        for payload in self.SSRF_PAYLOADS:
            test_params = base_params.copy()
            test_params[param] = [payload]
            test_query = urlencode(test_params, doseq=True)
            test_url = parsed._replace(query=test_query).geturl()
            try:
                start = time.time()
                r = self.session.get(test_url, timeout=10, allow_redirects=False)
                elapsed = time.time() - start
                text_lower = r.text.lower()
                for indicator in self.SSRF_INDICATORS:
                    if indicator.lower() in text_lower:
                        finding = Vulnerability(
                            type=VulnType.SSRF, severity=Severity.HIGH,
                            title="Server-Side Request Forgery in " + param,
                            description="SSRF vulnerability found in '" + param + "' parameter.",
                            url=test_url, parameter=param, payload=payload,
                            evidence="Internal service response detected: " + indicator,
                            remediation="Validate and sanitize all URLs. Use allowlists. Implement network segmentation.",
                            cvss_score=8.6, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
                            cwe_id="CWE-918", confidence=0.85, verified=True,
                            references=["https://owasp.org/www-community/attacks/Server_Side_Request_Forgery/", "https://portswigger.net/web-security/ssrf"],
                            tags=["ssrf", "internal-access"]
                        )
                        with self.lock:
                            if not any(f.url == finding.url and f.parameter == finding.parameter for f in self.verified_vulns):
                                self.verified_vulns.append(finding)
                                findings.append(finding)
                        break
                if elapsed > 3 and not any(f.url == test_url for f in findings):
                    finding = Vulnerability(
                        type=VulnType.SSRF, severity=Severity.MEDIUM,
                        title="Potential Blind SSRF in " + param,
                        description="Potential blind SSRF in '" + param + "' parameter.",
                        url=test_url, parameter=param, payload=payload,
                        evidence="Response time: " + str(round(elapsed, 2)) + "s",
                        remediation="Validate and sanitize all URLs. Use allowlists.",
                        cvss_score=5.3, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:N",
                        cwe_id="CWE-918", confidence=0.6, verified=False,
                        references=["https://portswigger.net/web-security/ssrf/blind"],
                        tags=["ssrf", "blind"]
                    )
                    with self.lock:
                        if not any(f.url == finding.url and f.parameter == finding.parameter for f in self.verified_vulns):
                            self.verified_vulns.append(finding)
                            findings.append(finding)
            except Exception as e:
                logger.debug("SSRF test error: " + str(e))
            time.sleep(self.config.get('delay', 0.5))
        return findings

# =============================================================================
# COMMAND INJECTION SCANNER
# =============================================================================

class CommandInjectionScanner:
    PAYLOADS = _PAYLOADS.get("cmd_injection", [])

    INDICATORS = [
        "uid=", "gid=", "groups=", "root:", "daemon:", "bin:",
        "windows", "microsoft", "[extensions]", "whoami", "administrator", "system",
        "linux", "darwin", "freebsd",
    ]

    def __init__(self, session, config=None):
        self.session = session
        self.config = config or {}
        self.lock = threading.Lock()
        self.verified_vulns = []

    def test_url_parameter(self, url, param):
        findings = []
        parsed = urlparse(url)
        base_params = parse_qs(parsed.query)
        for payload in self.PAYLOADS:
            test_params = base_params.copy()
            test_params[param] = [payload]
            test_query = urlencode(test_params, doseq=True)
            test_url = parsed._replace(query=test_query).geturl()
            try:
                start = time.time()
                r = self.session.get(test_url, timeout=15)
                elapsed = time.time() - start
                text_lower = r.text.lower()
                for indicator in self.INDICATORS:
                    if indicator.lower() in text_lower:
                        finding = Vulnerability(
                            type=VulnType.CMD_INJECTION, severity=Severity.CRITICAL,
                            title="Command Injection in " + param,
                            description="Command Injection vulnerability found in '" + param + "' parameter.",
                            url=test_url, parameter=param, payload=payload,
                            evidence="Command output detected: " + indicator,
                            remediation="Never pass user input to system commands. Use parameterized APIs. Implement strict input validation.",
                            cvss_score=9.8, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                            cwe_id="CWE-78", confidence=0.95, verified=True,
                            references=["https://owasp.org/www-community/attacks/Command_Injection/", "https://portswigger.net/web-security/os-command-injection"],
                            tags=["command-injection", "rce", "os-command"]
                        )
                        with self.lock:
                            if not any(f.url == finding.url and f.parameter == finding.parameter for f in self.verified_vulns):
                                self.verified_vulns.append(finding)
                                findings.append(finding)
                        break
                if elapsed > 4.5 and not any(f.url == test_url for f in findings):
                    finding = Vulnerability(
                        type=VulnType.CMD_INJECTION, severity=Severity.HIGH,
                        title="Potential Time-Based Command Injection in " + param,
                        description="Potential command injection in '" + param + "' parameter.",
                        url=test_url, parameter=param, payload=payload,
                        evidence="Response time: " + str(round(elapsed, 2)) + "s",
                        remediation="Never pass user input to system commands. Use parameterized APIs.",
                        cvss_score=8.1, cvss_vector="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H",
                        cwe_id="CWE-78", confidence=0.7, verified=False,
                        references=["https://owasp.org/www-community/attacks/Command_Injection/"],
                        tags=["command-injection", "blind", "time-based"]
                    )
                    with self.lock:
                        if not any(f.url == finding.url and f.parameter == finding.parameter for f in self.verified_vulns):
                            self.verified_vulns.append(finding)
                            findings.append(finding)
            except Exception as e:
                logger.debug("Command injection test error: " + str(e))
            time.sleep(self.config.get('delay', 0.5))
        return findings

# =============================================================================
# XXE SCANNER
# =============================================================================

class XXEScanner:
    PAYLOADS = _PAYLOADS.get("xxe", [])

    INDICATORS = [
        "root:", "daemon:", "bin:", "[extensions]", "[fonts]", "[files]",
        "PATH=", "HOME=", "USER=", "ami-id", "instance-id", "hostname", "local-ipv4",
        "<?php", "PD9waH",
    ]

    def __init__(self, session, config=None):
        self.session = session
        self.config = config or {}
        self.lock = threading.Lock()
        self.verified_vulns = []

    def test_endpoint(self, url, method="POST", content_type="application/xml"):
        findings = []
        for payload in self.PAYLOADS:
            try:
                headers = {'Content-Type': content_type}
                if method == "POST":
                    r = self.session.post(url, data=payload, headers=headers, timeout=10)
                else:
                    r = self.session.get(url, params={'xml': payload}, timeout=10)
                text_lower = r.text.lower()
                for indicator in self.INDICATORS:
                    if indicator.lower() in text_lower:
                        finding = Vulnerability(
                            type=VulnType.XXE, severity=Severity.CRITICAL,
                            title="XML External Entity (XXE) Injection",
                            description="XXE vulnerability found. The application processes XML input without disabling external entities.",
                            url=url, parameter="XML body", payload=payload[:100] + "...",
                            evidence="File content detected: " + indicator,
                            remediation="Disable external entities in XML parser. Use allowlists for DTDs. Use JSON instead of XML.",
                            cvss_score=9.1, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                            cwe_id="CWE-611", confidence=0.9, verified=True,
                            references=["https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing", "https://portswigger.net/web-security/xxe"],
                            tags=["xxe", "xml", "data-extraction"]
                        )
                        with self.lock:
                            if not any(f.url == finding.url for f in self.verified_vulns):
                                self.verified_vulns.append(finding)
                                findings.append(finding)
                        break
            except Exception as e:
                logger.debug("XXE test error: " + str(e))
            time.sleep(self.config.get('delay', 0.5))
        return findings

# =============================================================================
# CSRF SCANNER
# =============================================================================

class CSRFScanner:
    def __init__(self, session, config=None):
        self.session = session
        self.config = config or {}
        self.lock = threading.Lock()
        self.verified_vulns = []

    def test_form(self, form, base_url):
        findings = []
        action = form.get('action', base_url)
        if action.startswith('/'):
            action = urljoin(base_url, action)
        method = form.get('method', 'GET').upper()
        inputs = form.get('inputs', [])
        if method != 'POST':
            return findings
        has_csrf_token = False
        csrf_patterns = ['csrf', 'token', 'nonce', '_token', 'authenticity']
        for inp in inputs:
            name = inp.get('name', '').lower()
            if any(pattern in name for pattern in csrf_patterns):
                has_csrf_token = True
                break
        r = self.session.get(base_url, timeout=10)
        cookies = r.cookies
        has_samesite = False
        for cookie in cookies:
            if cookie.get_nonstandard_attr('SameSite'):
                has_samesite = True
                break
        if not has_csrf_token and not has_samesite:
            finding = Vulnerability(
                type=VulnType.CSRF, severity=Severity.MEDIUM,
                title="Missing CSRF Protection",
                description="Form lacks CSRF protection. No anti-CSRF token found and no SameSite cookie attribute.",
                url=action, parameter="Form submission", payload="",
                evidence="No CSRF token in form inputs. No SameSite cookie attribute detected.",
                remediation="Implement anti-CSRF tokens for all state-changing operations. Use SameSite cookie attribute.",
                cvss_score=6.5, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:N",
                cwe_id="CWE-352", confidence=0.8, verified=False,
                references=["https://owasp.org/www-community/attacks/csrf", "https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html"],
                tags=["csrf", "missing-protection"]
            )
            with self.lock:
                if not any(f.url == finding.url for f in self.verified_vulns):
                    self.verified_vulns.append(finding)
                    findings.append(finding)
        return findings

# =============================================================================
# OPEN REDIRECT SCANNER
# =============================================================================

class OpenRedirectScanner:
    PAYLOADS = _PAYLOADS.get("open_redirect", [])

    def __init__(self, session, config=None):
        self.session = session
        self.config = config or {}
        self.lock = threading.Lock()
        self.verified_vulns = []

    def test_url_parameter(self, url, param):
        findings = []
        parsed = urlparse(url)
        base_params = parse_qs(parsed.query)
        for payload in self.PAYLOADS:
            test_params = base_params.copy()
            test_params[param] = [payload]
            test_query = urlencode(test_params, doseq=True)
            test_url = parsed._replace(query=test_query).geturl()
            try:
                r = self.session.get(test_url, timeout=10, allow_redirects=False)
                if r.status_code in [301, 302, 303, 307, 308]:
                    location = r.headers.get('Location', '')
                    if 'evil.com' in location or 'javascript:' in location:
                        finding = Vulnerability(
                            type=VulnType.OPEN_REDIRECT, severity=Severity.MEDIUM,
                            title="Open Redirect in " + param,
                            description="Open Redirect vulnerability found in '" + param + "' parameter.",
                            url=test_url, parameter=param, payload=payload,
                            evidence="Redirect to: " + location,
                            remediation="Validate redirect URLs against allowlist. Use relative URLs only. Implement redirect confirmation page.",
                            cvss_score=6.1, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N",
                            cwe_id="CWE-601", confidence=0.9, verified=True,
                            references=["https://owasp.org/www-community/attacks/URL_Redirection_to_Untrusted_Site", "https://portswigger.net/web-security/dom-based/open-redirection"],
                            tags=["open-redirect", "url-redirection"]
                        )
                        with self.lock:
                            if not any(f.url == finding.url and f.parameter == finding.parameter for f in self.verified_vulns):
                                self.verified_vulns.append(finding)
                                findings.append(finding)
                        break
            except Exception as e:
                logger.debug("Open redirect test error: " + str(e))
            time.sleep(self.config.get('delay', 0.5))
        return findings

# =============================================================================
# IDOR SCANNER
# =============================================================================

class IDORScanner:
    def __init__(self, session, config=None):
        self.session = session
        self.config = config or {}
        self.lock = threading.Lock()
        self.verified_vulns = []

    def test_numeric_parameters(self, url, param):
        findings = []
        parsed = urlparse(url)
        base_params = parse_qs(parsed.query)
        original_value = base_params.get(param, ['1'])[0]
        try:
            test_values = [str(int(original_value) + i) for i in range(1, 5)]
        except:
            return findings
        responses = []
        for value in test_values:
            test_params = base_params.copy()
            test_params[param] = [value]
            test_query = urlencode(test_params, doseq=True)
            test_url = parsed._replace(query=test_query).geturl()
            try:
                r = self.session.get(test_url, timeout=10)
                responses.append((value, r.status_code, len(r.text), r.text[:500]))
            except:
                pass
            time.sleep(self.config.get('delay', 0.5))
        if len(responses) > 1:
            status_codes = [r[1] for r in responses]
            content_lengths = [r[2] for r in responses]
            if all(s == 200 for s in status_codes) and max(content_lengths) - min(content_lengths) < 100:
                finding = Vulnerability(
                    type=VulnType.IDOR, severity=Severity.HIGH,
                    title="Insecure Direct Object Reference in " + param,
                    description="IDOR vulnerability found in '" + param + "' parameter. Sequential IDs return valid data for different objects.",
                    url=url, parameter=param, payload="Sequential IDs: " + ", ".join(test_values),
                    evidence="All IDs returned 200 OK with similar content sizes: " + str(content_lengths),
                    remediation="Implement proper access control checks. Use indirect reference maps (UUIDs). Validate user permissions.",
                    cvss_score=7.5, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
                    cwe_id="CWE-639", confidence=0.75, verified=False,
                    references=["https://owasp.org/www-community/vulnerabilities/Insecure_Direct_Object_Reference", "https://portswigger.net/web-security/access-control/idor"],
                    tags=["idor", "access-control", "authorization"]
                )
                with self.lock:
                    if not any(f.url == finding.url and f.parameter == finding.parameter for f in self.verified_vulns):
                        self.verified_vulns.append(finding)
                        findings.append(finding)
        return findings

# =============================================================================
# JWT SCANNER
# =============================================================================

class JWTScanner:
    def __init__(self, session, config=None):
        self.session = session
        self.config = config or {}
        self.lock = threading.Lock()
        self.verified_vulns = []

    def analyze_jwt(self, token, url=""):
        findings = []
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return findings
            header = json.loads(base64.b64decode(parts[0] + '==').decode())
            payload = json.loads(base64.b64decode(parts[1] + '==').decode())
            alg = header.get('alg', '').upper()
            if alg in ['NONE', 'NULL', 'none']:
                finding = Vulnerability(
                    type=VulnType.JWT_WEAK, severity=Severity.CRITICAL,
                    title="JWT Algorithm 'none' Attack",
                    description="JWT accepts 'none' algorithm. An attacker can forge tokens by removing the signature.",
                    url=url, parameter="JWT token", payload=token[:50] + "...",
                    evidence="Algorithm: none",
                    remediation="Reject tokens with 'none' algorithm. Validate algorithm against allowlist.",
                    cvss_score=9.1, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N",
                    cwe_id="CWE-327", confidence=0.95, verified=True,
                    references=["https://owasp.org/www-community/attacks/JWT_Security", "https://portswigger.net/web-security/jwt"],
                    tags=["jwt", "algorithm-none", "authentication"]
                )
                findings.append(finding)
            if alg in ['HS256', 'HS384', 'HS512']:
                finding = Vulnerability(
                    type=VulnType.JWT_WEAK, severity=Severity.MEDIUM,
                    title="JWT Using Symmetric Algorithm",
                    description="JWT uses HMAC algorithm. If secret key is weak, it can be brute-forced.",
                    url=url, parameter="JWT token", payload=token[:50] + "...",
                    evidence="Algorithm: " + alg,
                    remediation="Use asymmetric algorithms (RS256, ES256). Ensure strong secret key.",
                    cvss_score=5.3, cvss_vector="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N",
                    cwe_id="CWE-327", confidence=0.6, verified=False,
                    references=["https://owasp.org/www-community/attacks/JWT_Security", "https://portswigger.net/web-security/jwt/algorithm-confusion"],
                    tags=["jwt", "weak-algorithm", "symmetric"]
                )
                findings.append(finding)
            sensitive_keys = ['password', 'secret', 'key', 'admin', 'role', 'privilege']
            for key in payload:
                if any(s in key.lower() for s in sensitive_keys):
                    finding = Vulnerability(
                        type=VulnType.INFO_DISCLOSURE, severity=Severity.MEDIUM,
                        title="Sensitive Data in JWT Payload",
                        description="JWT payload contains potentially sensitive key: '" + key + "'",
                        url=url, parameter="JWT token", payload=token[:50] + "...",
                        evidence="Payload contains: " + key,
                        remediation="Do not include sensitive data in JWT payload. Use token references instead.",
                        cvss_score=5.3, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N",
                        cwe_id="CWE-311", confidence=0.7, verified=False,
                        references=["https://owasp.org/www-community/attacks/JWT_Security"],
                        tags=["jwt", "info-disclosure", "sensitive-data"]
                    )
                    findings.append(finding)
        except Exception as e:
            logger.debug("JWT analysis error: " + str(e))
        return findings

# =============================================================================
# CORS SCANNER
# =============================================================================

class CORSScanner:
    def __init__(self, session, config=None):
        self.session = session
        self.config = config or {}
        self.lock = threading.Lock()
        self.verified_vulns = []

    def test_cors(self, url):
        findings = []
        dangerous_origins = [
            "https://evil.com", "http://evil.com", "null", "https://attacker.com",
            "https://subdomain.target.com", "https://target.com.evil.com",
        ]
        for origin in dangerous_origins:
            try:
                headers = {'Origin': origin}
                r = self.session.get(url, headers=headers, timeout=10)
                acao = r.headers.get('Access-Control-Allow-Origin', '')
                acac = r.headers.get('Access-Control-Allow-Credentials', '')
                if acao == '*' and acac.lower() == 'true':
                    finding = Vulnerability(
                        type=VulnType.CORS, severity=Severity.HIGH,
                        title="CORS Misconfiguration: Wildcard with Credentials",
                        description="Access-Control-Allow-Origin is * while Access-Control-Allow-Credentials is true. This allows any site to make authenticated requests.",
                        url=url, parameter="CORS headers", payload="Origin: " + origin,
                        evidence="Access-Control-Allow-Origin: * AND Access-Control-Allow-Credentials: true",
                        remediation="Never use wildcard (*) with credentials. Validate Origin against allowlist.",
                        cvss_score=7.5, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N",
                        cwe_id="CWE-942", confidence=0.95, verified=True,
                        references=["https://portswigger.net/web-security/cors", "https://owasp.org/www-community/attacks/CORS_OriginHeaderScrutiny"],
                        tags=["cors", "misconfiguration", "credentials"]
                    )
                    findings.append(finding)
                elif acao == origin:
                    finding = Vulnerability(
                        type=VulnType.CORS, severity=Severity.MEDIUM,
                        title="CORS Reflects Arbitrary Origin",
                        description="The application reflects arbitrary Origin headers, allowing cross-origin requests from any domain.",
                        url=url, parameter="CORS headers", payload="Origin: " + origin,
                        evidence="Access-Control-Allow-Origin: " + origin,
                        remediation="Validate Origin against strict allowlist. Do not reflect arbitrary origins.",
                        cvss_score=5.3, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N",
                        cwe_id="CWE-942", confidence=0.85, verified=True,
                        references=["https://portswigger.net/web-security/cors", "https://owasp.org/www-community/attacks/CORS_OriginHeaderScrutiny"],
                        tags=["cors", "arbitrary-origin", "reflected"]
                    )
                    findings.append(finding)
            except Exception as e:
                logger.debug("CORS test error: " + str(e))
        return findings

# =============================================================================
# SECURITY HEADERS SCANNER
# =============================================================================

class SecurityHeadersScanner:
    REQUIRED_HEADERS = {
        'Strict-Transport-Security': {
            'severity': Severity.MEDIUM, 'title': 'Missing HSTS Header',
            'description': 'HTTP Strict Transport Security (HSTS) header is missing. The site is vulnerable to SSL stripping attacks.',
            'remediation': 'Add Strict-Transport-Security header with max-age of at least 31536000 seconds.',
            'cvss': 5.3, 'vector': 'CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N', 'cwe': 'CWE-319'
        },
        'Content-Security-Policy': {
            'severity': Severity.MEDIUM, 'title': 'Missing CSP Header',
            'description': 'Content Security Policy (CSP) header is missing. The site is more vulnerable to XSS attacks.',
            'remediation': 'Implement CSP header with strict directives. Start with report-only mode.',
            'cvss': 5.3, 'vector': 'CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N', 'cwe': 'CWE-693'
        },
        'X-Frame-Options': {
            'severity': Severity.MEDIUM, 'title': 'Missing X-Frame-Options Header',
            'description': 'X-Frame-Options header is missing. The site is vulnerable to clickjacking attacks.',
            'remediation': 'Add X-Frame-Options: DENY or SAMEORIGIN. Alternatively use CSP frame-ancestors directive.',
            'cvss': 5.3, 'vector': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N', 'cwe': 'CWE-1021'
        },
        'X-Content-Type-Options': {
            'severity': Severity.LOW, 'title': 'Missing X-Content-Type-Options Header',
            'description': 'X-Content-Type-Options header is missing. The site may be vulnerable to MIME sniffing attacks.',
            'remediation': 'Add X-Content-Type-Options: nosniff header.',
            'cvss': 3.7, 'vector': 'CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N', 'cwe': 'CWE-693'
        },
        'Referrer-Policy': {
            'severity': Severity.LOW, 'title': 'Missing Referrer-Policy Header',
            'description': 'Referrer-Policy header is missing. Sensitive information may leak through referrer headers.',
            'remediation': 'Add Referrer-Policy: strict-origin-when-cross-origin or no-referrer.',
            'cvss': 3.7, 'vector': 'CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N', 'cwe': 'CWE-200'
        },
        'Permissions-Policy': {
            'severity': Severity.LOW, 'title': 'Missing Permissions-Policy Header',
            'description': 'Permissions-Policy header is missing. Browser features may be abused.',
            'remediation': 'Add Permissions-Policy header to restrict browser features.',
            'cvss': 3.1, 'vector': 'CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N', 'cwe': 'CWE-693'
        },
    }

    def __init__(self, session, config=None):
        self.session = session
        self.config = config or {}

    def scan_headers(self, url):
        findings = []
        try:
            r = self.session.get(url, timeout=10)
            headers = dict(r.headers)
            for header_name, info in self.REQUIRED_HEADERS.items():
                if header_name not in headers:
                    finding = Vulnerability(
                        type=VulnType.SECURITY_HEADERS, severity=info['severity'],
                        title=info['title'], description=info['description'],
                        url=url, parameter="HTTP headers", payload="",
                        evidence="Header '" + header_name + "' not found in response",
                        remediation=info['remediation'], cvss_score=info['cvss'],
                        cvss_vector=info['vector'], cwe_id=info['cwe'],
                        confidence=1.0, verified=True,
                        references=["https://owasp.org/www-project-secure-headers/", "https://securityheaders.com/"],
                        tags=["security-headers", "missing-header", header_name.lower().replace('-', '_')]
                    )
                    findings.append(finding)
            dangerous_headers = {
                'X-Powered-By': 'Information disclosure - reveals technology stack',
                'Server': 'Information disclosure - reveals server software',
                'X-AspNet-Version': 'Information disclosure - reveals ASP.NET version',
                'X-Generator': 'Information disclosure - reveals framework',
            }
            for header, desc in dangerous_headers.items():
                if header in headers:
                    finding = Vulnerability(
                        type=VulnType.INFO_DISCLOSURE, severity=Severity.INFO,
                        title="Information Disclosure: " + header,
                        description=desc + ". Value: " + headers[header],
                        url=url, parameter="HTTP headers", payload="",
                        evidence=header + ": " + headers[header],
                        remediation="Remove " + header + " header or configure to hide version information.",
                        cvss_score=2.3, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N",
                        cwe_id="CWE-200", confidence=1.0, verified=True,
                        references=["https://owasp.org/www-project-top-ten/2017/A6_2017-Security_Misconfiguration"],
                        tags=["info-disclosure", "headers", "reconnaissance"]
                    )
                    findings.append(finding)
        except Exception as e:
            logger.debug("Security headers scan error: " + str(e))
        return findings

# =============================================================================
# SSL/TLS VULNERABILITY SCANNER
# =============================================================================

class SSLTLSScanner:
    WEAK_CIPHERS = ['RC4', 'DES', '3DES', 'MD5', 'NULL', 'EXPORT', 'anon', 'aNULL', 'eNULL', 'LOW', 'EXP']
    VULNERABILITIES = {
        'SSLv2': {'severity': Severity.CRITICAL, 'cvss': 9.8},
        'SSLv3': {'severity': Severity.CRITICAL, 'cvss': 9.8},
        'TLSv1.0': {'severity': Severity.HIGH, 'cvss': 7.5},
        'TLSv1.1': {'severity': Severity.MEDIUM, 'cvss': 5.3},
    }

    def __init__(self, config=None):
        self.config = config or {}

    def scan(self, hostname, port=443):
        findings = []
        try:
            protocols = [
                (ssl.PROTOCOL_SSLv2, "SSLv2"), (ssl.PROTOCOL_SSLv3, "SSLv3"),
                (ssl.PROTOCOL_TLSv1, "TLSv1.0"), (ssl.PROTOCOL_TLSv1_1, "TLSv1.1"),
                (ssl.PROTOCOL_TLSv1_2, "TLSv1.2"),
            ]
            supported_protocols = []
            for proto, name in protocols:
                try:
                    context = ssl.SSLContext(proto)
                    with socket.create_connection((hostname, port), timeout=5) as sock:
                        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                            supported_protocols.append(name)
                except:
                    pass
            for proto in supported_protocols:
                if proto in self.VULNERABILITIES:
                    vuln_info = self.VULNERABILITIES[proto]
                    finding = Vulnerability(
                        type=VulnType.SSL_TLS, severity=vuln_info['severity'],
                        title="Weak SSL/TLS Protocol: " + proto,
                        description="The server supports " + proto + " which is considered weak and vulnerable to attacks.",
                        url="https://" + hostname + ":" + str(port), parameter="SSL/TLS", payload=proto,
                        evidence="Protocol " + proto + " is supported",
                        remediation="Disable " + proto + " and use TLS 1.2 or TLS 1.3 only.",
                        cvss_score=vuln_info['cvss'], cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                        cwe_id="CWE-319", confidence=1.0, verified=True,
                        references=["https://owasp.org/www-project-top-ten/2017/A6_2017-Security_Misconfiguration", "https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html"],
                        tags=["ssl", "tls", "weak-protocol", proto.lower().replace('.', '_')]
                    )
                    findings.append(finding)
            try:
                context = ssl.create_default_context()
                with socket.create_connection((hostname, port), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        cert = ssock.getpeercert()
                        cipher = ssock.cipher()
                        version = ssock.version()
                        not_after = cert.get('notAfter')
                        if not_after:
                            expiry = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                            if expiry < datetime.now():
                                finding = Vulnerability(
                                    type=VulnType.SSL_TLS, severity=Severity.HIGH,
                                    title="Expired SSL Certificate",
                                    description="The SSL certificate has expired.",
                                    url="https://" + hostname + ":" + str(port), parameter="SSL Certificate", payload="",
                                    evidence="Certificate expired on: " + not_after,
                                    remediation="Renew the SSL certificate immediately.",
                                    cvss_score=7.5, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N",
                                    cwe_id="CWE-295", confidence=1.0, verified=True,
                                    references=["https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html"],
                                    tags=["ssl", "certificate", "expired"]
                                )
                                findings.append(finding)
                        if cipher:
                            cipher_name = cipher[0]
                            for weak in self.WEAK_CIPHERS:
                                if weak.lower() in cipher_name.lower():
                                    finding = Vulnerability(
                                        type=VulnType.SSL_TLS, severity=Severity.HIGH,
                                        title="Weak Cipher Suite: " + cipher_name,
                                        description="The server uses weak cipher suite: " + cipher_name,
                                        url="https://" + hostname + ":" + str(port), parameter="SSL Cipher", payload=cipher_name,
                                        evidence="Cipher: " + cipher_name,
                                        remediation="Disable weak cipher suites. Use only strong ciphers (AES-GCM, ChaCha20-Poly1305).",
                                        cvss_score=7.5, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
                                        cwe_id="CWE-327", confidence=1.0, verified=True,
                                        references=["https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html"],
                                        tags=["ssl", "cipher", "weak-cipher"]
                                    )
                                    findings.append(finding)
                                    break
                        subject = cert.get('subject', ())
                        issuer = cert.get('issuer', ())
                        if subject == issuer:
                            finding = Vulnerability(
                                type=VulnType.SSL_TLS, severity=Severity.MEDIUM,
                                title="Self-Signed Certificate",
                                description="The server uses a self-signed certificate.",
                                url="https://" + hostname + ":" + str(port), parameter="SSL Certificate", payload="",
                                evidence="Subject matches Issuer (self-signed)",
                                remediation="Use a certificate from a trusted CA. Implement proper certificate validation.",
                                cvss_score=5.3, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N",
                                cwe_id="CWE-295", confidence=1.0, verified=True,
                                references=["https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html"],
                                tags=["ssl", "certificate", "self-signed"]
                            )
                            findings.append(finding)
            except Exception as e:
                logger.debug("SSL certificate analysis error: " + str(e))
        except Exception as e:
            logger.debug("SSL scan error: " + str(e))
        return findings

# =============================================================================
# ADVANCED PORT SCANNER
# =============================================================================

class AdvancedPortScanner:
    COMMON_PORTS = list(range(1, 1024)) + [
        1025, 1080, 1099, 1433, 1434, 1521, 1723, 2049, 2082, 2083, 2086, 2087,
        2095, 2096, 2222, 2375, 2376, 3000, 3128, 3306, 3389, 4444, 4567, 4786,
        5000, 5432, 5900, 5984, 5985, 5986, 6379, 6443, 7001, 7002, 8000, 8008,
        8080, 8081, 8443, 8888, 9000, 9043, 9090, 9200, 9300, 9418, 9999, 10000,
        11211, 27017, 27018, 27019, 28017, 50000, 50030, 50070
    ]

    SERVICES = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP",
        110: "POP3", 111: "RPC", 135: "MSRPC", 139: "NetBIOS", 143: "IMAP",
        443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S", 1433: "MSSQL",
        1723: "PPTP", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
        5900: "VNC", 6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
        27017: "MongoDB", 11211: "Memcached", 9200: "Elasticsearch",
        9300: "Elasticsearch-Transport", 9090: "WebSM", 5000: "UPnP",
        7001: "WebLogic", 7002: "WebLogic", 9043: "WebSphere",
        10000: "Webmin", 50030: "Hadoop", 50070: "Hadoop"
    }

    def __init__(self, timeout=2.0, max_workers=100, scan_type="tcp"):
        self.timeout = timeout
        self.max_workers = max_workers
        self.scan_type = scan_type
        self.lock = threading.Lock()
        self.results = []

    def _grab_banner(self, ip, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect((ip, port))
            if port in [21, 25, 110]:
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            elif port == 80:
                s.send(b"HEAD / HTTP/1.0\r\nHost: " + ip.encode() + b"\r\n\r\n")
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            elif port == 443:
                s.send(b"GET / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            else:
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            s.close()
            return banner[:300]
        except:
            return ""

    def _detect_service_version(self, banner):
        version_patterns = [
            r'([A-Za-z]+)[/\s]+([\d.]+)', r'([A-Za-z]+)[\s]+([\d.]+)',
            r'([\d.]+)', r'([A-Za-z]+)[/\s]+v?([\d.]+)',
        ]
        for pattern in version_patterns:
            match = re.search(pattern, banner)
            if match:
                return match.group(0)
        return "Unknown"

    def _tcp_scan_single(self, ip, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            result = s.connect_ex((ip, port))
            s.close()
            if result == 0:
                banner = self._grab_banner(ip, port)
                return {
                    "port": port, "service": self.SERVICES.get(port, "Unknown"),
                    "banner": banner, "state": "open",
                    "version": self._detect_service_version(banner)
                }
        except Exception as e:
            logger.debug("TCP scan error for port " + str(port) + ": " + str(e))
        return None

    def _udp_scan_single(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
            sock.sendto(b'', (ip, port))
            try:
                data, addr = sock.recvfrom(1024)
                sock.close()
                return {
                    "port": port, "service": self.SERVICES.get(port, "Unknown"),
                    "banner": data.decode('utf-8', errors='ignore')[:300],
                    "state": "open", "version": "Unknown"
                }
            except socket.timeout:
                sock.close()
                return None
        except Exception as e:
            logger.debug("UDP scan error for port " + str(port) + ": " + str(e))
        return None

    def scan(self, ip, ports=None, scan_type=None):
        if ports is None:
            ports = self.COMMON_PORTS
        if scan_type:
            self.scan_type = scan_type
        open_ports = []
        total = len(ports)
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            if self.scan_type == "udp":
                futures = {executor.submit(self._udp_scan_single, ip, port): port for port in ports}
            else:
                futures = {executor.submit(self._tcp_scan_single, ip, port): port for port in ports}
            for i, future in enumerate(as_completed(futures), 1):
                result = future.result()
                if result:
                    open_ports.append(result)
                    logger.info("Port " + str(result['port']) + " open - " + result['service'] + " - " + result['version'])
                if i % 50 == 0:
                    logger.info("Progress: " + str(i) + "/" + str(total))
        return sorted(open_ports, key=lambda x: x['port'])

# =============================================================================
# WEB CRAWLER
# =============================================================================

class WebCrawler:
    def __init__(self, session, config=None):
        self.session = session
        self.config = config or {}
        self.visited = set()
        self.urls_to_visit = []
        self.lock = threading.Lock()
        self.max_depth = self.config.get('crawl_depth', 3)
        self.max_urls = self.config.get('max_urls', 500)
        self.js_rendering = self.config.get('js_rendering', True)
        self.driver = None
        if self.js_rendering:
            try:
                options = ChromeOptions()
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--disable-extensions')
                options.add_argument('--disable-images')
                self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            except Exception as e:
                logger.warning("Could not initialize headless browser: " + str(e))
                self.js_rendering = False

    def _extract_links(self, url, html_content):
        links = set()
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            for a in soup.find_all('a', href=True):
                href = a['href']
                full_url = urljoin(url, href)
                if self._is_same_domain(url, full_url):
                    links.add(full_url)
            for script in soup.find_all('script'):
                if script.string:
                    js_urls = re.findall(r'["\']((?:https?://|/)[^"\']+)["\']', script.string)
                    for js_url in js_urls:
                        full_url = urljoin(url, js_url)
                        if self._is_same_domain(url, full_url):
                            links.add(full_url)
            for form in soup.find_all('form', action=True):
                action = form['action']
                full_url = urljoin(url, action)
                if self._is_same_domain(url, full_url):
                    links.add(full_url)
            for iframe in soup.find_all('iframe', src=True):
                src = iframe['src']
                full_url = urljoin(url, src)
                if self._is_same_domain(url, full_url):
                    links.add(full_url)
            js_files = [urljoin(url, script['src']) for script in soup.find_all('script', src=True)]
            for js_file in js_files:
                try:
                    r = self.session.get(js_file, timeout=10)
                    api_patterns = [
                        r'["\']((?:/api/|/v\d+/|/graphql)[^"\']*)["\']',
                        r'fetch\(["\']([^"\']+)["\']',
                        r'axios\.(?:get|post|put|delete)\(["\']([^"\']+)["\']',
                    ]
                    for pattern in api_patterns:
                        matches = re.findall(pattern, r.text)
                        for match in matches:
                            full_url = urljoin(url, match)
                            if self._is_same_domain(url, full_url):
                                links.add(full_url)
                except:
                    pass
        except Exception as e:
            logger.debug("Link extraction error: " + str(e))
        return links

    def _is_same_domain(self, base_url, test_url):
        try:
            base_domain = urlparse(base_url).netloc
            test_domain = urlparse(test_url).netloc
            return base_domain == test_domain and test_url not in self.visited
        except:
            return False

    def crawl(self, start_url, depth=0):
        if depth > self.max_depth or len(self.visited) >= self.max_urls:
            return
        with self.lock:
            if start_url in self.visited:
                return
            self.visited.add(start_url)
        try:
            if self.js_rendering and self.driver and depth < 2:
                self.driver.get(start_url)
                time.sleep(2)
                html_content = self.driver.page_source
            else:
                r = self.session.get(start_url, timeout=15)
                html_content = r.text
            links = self._extract_links(start_url, html_content)
            with self.lock:
                self.urls_to_visit.extend(links)
            for link in links:
                if len(self.visited) < self.max_urls:
                    self.crawl(link, depth + 1)
        except Exception as e:
            logger.debug("Crawl error for " + start_url + ": " + str(e))

    def get_results(self):
        return {'visited_urls': list(self.visited), 'total_urls': len(self.visited)}

    def close(self):
        if self.driver:
            self.driver.quit()

# =============================================================================
# SUBDOMAIN ENUMERATOR
# =============================================================================

class SubdomainEnumerator:
    COMMON_SUBDOMAINS = [
        'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
        'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'ns3', 'm', 'imap',
        'test', 'ns', 'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 'news',
        'vpn', 'ns4', 'www1', 'imap4', 'beta', 'smtp2', 'mail2', 'www3', 'api',
        'staging', 'mobile', 'search', 'wap', 'sip', 'email', 'ns5', 'exchange',
        'remote', 'webmin', 'chat', 'crm', 'support', 'help', 'wiki', 'docs',
        'portal', 'monitor', 'status', 'git', 'svn', 'cvs', 'backup', 'db',
        'sql', 'mysql', 'postgres', 'redis', 'mongo', 'elasticsearch', 'kibana',
        'grafana', 'prometheus', 'jenkins', 'gitlab', 'github', 'jira', 'confluence',
        'nagios', 'zabbix', 'splunk', 'log', 'logs', 'analytics', 'stats',
        'cdn', 'static', 'assets', 'media', 'images', 'img', 'css', 'js',
        'api-v1', 'api-v2', 'api-v3', 'rest', 'graphql', 'websocket', 'ws',
        'auth', 'login', 'sso', 'oauth', 'openid', 'saml', 'ldap', 'ad',
        'internal', 'intranet', 'extranet', 'private', 'secure', 'public',
        'demo', 'sandbox', 'playground', 'test', 'testing', 'qa', 'uat',
        'prod', 'production', 'live', 'staging', 'preprod', 'release',
        'dev', 'development', 'devel', 'build', 'ci', 'cd', 'deploy',
        'app', 'application', 'web', 'website', 'site', 'homepage',
        'shop', 'store', 'cart', 'checkout', 'payment', 'billing',
        'account', 'user', 'users', 'member', 'members', 'profile',
        'dashboard', 'panel', 'admin', 'administrator', 'root',
        'manager', 'manage', 'control', 'console', 'system', 'sys',
        'service', 'services', 'api', 'apis', 'gateway', 'proxy',
        'loadbalancer', 'lb', 'ha', 'failover', 'cluster', 'node',
        'server', 'host', 'vm', 'container', 'docker', 'kubernetes', 'k8s',
        'swarm', 'rancher', 'openshift', 'cloud', 'aws', 'azure', 'gcp',
        's3', 'bucket', 'storage', 'object', 'file', 'files', 'upload',
        'download', 'transfer', 'sync', 'mirror', 'cache', 'caching',
        'edge', 'fastly', 'cloudflare', 'akamai', 'cdn', 'distribution',
        'dns', 'nameserver', 'resolver', 'registry', 'whois', 'rdap',
        'cert', 'certificate', 'ca', 'pki', 'ssl', 'tls', 'vpn',
        'ipsec', 'wireguard', 'openvpn', 'pptp', 'l2tp', 'sstp',
        'ftp', 'sftp', 'ftps', 'scp', 'rsync', 'tftp', 'nfs',
        'cifs', 'smb', 'samba', 'afp', 'webdav', 'dav', 'caldav',
        'carddav', 'imap', 'imaps', 'pop3', 'pop3s', 'smtp', 'smtps',
        'submission', 'mx', 'mail', 'email', 'webmail', 'roundcube',
        'squirrelmail', 'horde', 'zimbra', 'exchange', 'outlook',
        'office365', 'google', 'gmail', 'yahoo', 'hotmail', 'live',
    ]

    def __init__(self, config=None):
        self.config = config or {}
        self.lock = threading.Lock()
        self.found_subdomains = []

    def enumerate(self, domain):
        found = []
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(self._check_subdomain, sub + "." + domain): sub for sub in self.COMMON_SUBDOMAINS}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    found.append(result)
                    logger.info("Found subdomain: " + result)
        return sorted(found)

    def _check_subdomain(self, subdomain):
        try:
            answers = dns.resolver.resolve(subdomain, 'A')
            if answers:
                return subdomain
        except:
            pass
        try:
            answers = dns.resolver.resolve(subdomain, 'CNAME')
            if answers:
                return subdomain
        except:
            pass
        return None

# =============================================================================
# TECHNOLOGY DETECTOR (ENHANCED)
# =============================================================================

class TechnologyDetector:
    TECH_SIGNATURES = {
        "PHP": {"headers": ["x-powered-by: php", "php"], "body": [".php", "<?php", "phpinfo()", "phpmyadmin"], "cookies": ["PHPSESSID"]},
        "ASP.NET": {"headers": ["x-aspnet-version", "x-powered-by: asp.net"], "body": ["__viewstate", "__eventvalidation", "asp.net"], "cookies": ["asp.net_sessionid", "__requestverificationtoken"]},
        "Node.js": {"headers": ["x-powered-by: express", "x-powered-by: node.js"], "body": ["node.js", "express", "npm", "package.json"], "cookies": ["connect.sid"]},
        "Python": {"headers": ["x-powered-by: python", "wsgi"], "body": ["django", "flask", "python", "wsgi", "csrfmiddlewaretoken"], "cookies": ["csrftoken", "sessionid"]},
        "Ruby": {"headers": ["x-powered-by: ruby", "x-runtime"], "body": ["ruby", "rails", "rack", "sinatra"], "cookies": ["_session_id", "_csrf_token"]},
        "Java": {"headers": ["x-powered-by: servlet", "x-powered-by: jsp"], "body": ["jsp", "servlet", "tomcat", "jetty", "spring", "struts"], "cookies": ["jsessionid", "j_session_id"]},
        "React": {"headers": [], "body": ["react", "reactjs", "__react", "react-dom", "create-react-app"], "cookies": []},
        "Vue.js": {"headers": [], "body": ["vue", "vuejs", "__vue", "v-if", "v-for", "v-model"], "cookies": []},
        "Angular": {"headers": [], "body": ["angular", "ng-app", "ng-controller", "ng-model", "ng-repeat"], "cookies": []},
        "jQuery": {"headers": [], "body": ["jquery", "jquery.min", "$.ajax", "$(document)"], "cookies": []},
        "Bootstrap": {"headers": [], "body": ["bootstrap", "bootstrap.min", "bootstrap.css", "bootstrap.js"], "cookies": []},
        "WordPress": {"headers": [], "body": ["wp-content", "wp-includes", "wordpress", "wp-json", "/wp-admin"], "cookies": ["wordpress_logged_in", "wp-settings"]},
        "Drupal": {"headers": [], "body": ["drupal", "sites/default", "drupal.js", "drupalSettings"], "cookies": ["drupal", "has_js"]},
        "Joomla": {"headers": [], "body": ["joomla", "/media/jui", "joomla.js", "com_content"], "cookies": []},
        "Laravel": {"headers": ["x-powered-by: laravel"], "body": ["laravel", "csrf-token", "laravel_session"], "cookies": ["laravel_session"]},
        "Nginx": {"headers": ["server: nginx"], "body": [], "cookies": []},
        "Apache": {"headers": ["server: apache"], "body": [], "cookies": []},
        "IIS": {"headers": ["microsoft-iis", "server: iis"], "body": [], "cookies": []},
        "Cloudflare": {"headers": ["cf-ray", "cf-cache-status", "server: cloudflare"], "body": [], "cookies": ["__cfduid", "cf_clearance"]},
        "AWS": {"headers": ["x-amzn-requestid", "x-amz-id-2"], "body": ["amazon", "aws", "s3.amazonaws", "ec2", "elb"], "cookies": []},
        "Google Cloud": {"headers": ["server: gws", "x-cloud-trace-context"], "body": ["google", "gcp", "app engine"], "cookies": []},
        "Azure": {"headers": ["x-ms-request-id", "x-ms-ratelimit"], "body": ["azure", "microsoft", "windows azure"], "cookies": []},
        "Fastly": {"headers": ["x-fastly", "fastly-io-info"], "body": [], "cookies": []},
        "Akamai": {"headers": ["x-akamai-transformed", "akamai"], "body": [], "cookies": []},
        "Docker": {"headers": [], "body": ["docker", "container", "docker-compose"], "cookies": []},
        "Kubernetes": {"headers": [], "body": ["kubernetes", "k8s", "kube", "helm"], "cookies": []},
        "MongoDB": {"headers": [], "body": ["mongodb", "mongoose", "mongo"], "cookies": []},
        "Redis": {"headers": [], "body": ["redis", "redis-cli"], "cookies": []},
        "Elasticsearch": {"headers": [], "body": ["elasticsearch", "es", "kibana", "logstash"], "cookies": []},
        "GraphQL": {"headers": [], "body": ["graphql", "apollo", "relay", "__schema", "__type"], "cookies": []},
        "WebSocket": {"headers": ["upgrade: websocket", "connection: upgrade"], "body": ["websocket", "ws://", "wss://", "socket.io"], "cookies": []},
        "Next.js": {"headers": ["x-powered-by: next.js"], "body": ["__next", "_next/static", "next.js"], "cookies": []},
        "Nuxt.js": {"headers": [], "body": ["__nuxt", "nuxt", "nuxt.js"], "cookies": []},
        "Gatsby": {"headers": [], "body": ["gatsby", "___gatsby"], "cookies": []},
        "Svelte": {"headers": [], "body": ["svelte", "sveltekit"], "cookies": []},
        "Go": {"headers": ["x-powered-by: go"], "body": ["go", "golang", "gin", "echo"], "cookies": []},
        "Rust": {"headers": [], "body": ["rust", "actix", "rocket", "axum"], "cookies": []},
    }

    def detect(self, response, url, cookies=None):
        technologies = []
        text_lower = response.text.lower()
        headers_str = str(response.headers).lower()
        cookies_str = str(cookies).lower() if cookies else ""
        for tech, signatures in self.TECH_SIGNATURES.items():
            score = 0
            for header in signatures["headers"]:
                if header.lower() in headers_str:
                    score += 2
            for body in signatures["body"]:
                if body.lower() in text_lower:
                    score += 1
            for cookie in signatures["cookies"]:
                if cookie.lower() in cookies_str:
                    score += 2
            if score >= 2:
                technologies.append(tech)
        return list(set(technologies))

# =============================================================================
# API SCANNER
# =============================================================================

class APIScanner:
    def __init__(self, session, config=None):
        self.session = session
        self.config = config or {}

    def test_endpoint(self, url, method="GET", params=None, data=None, headers=None):
        findings = []
        if method in ["POST", "PUT", "PATCH"]:
            test_data = data or {}
            test_data['id'] = '1'
            test_data['admin'] = 'true'
            test_data['role'] = 'admin'
            try:
                r = self.session.request(method, url, json=test_data, headers=headers, timeout=10)
                if r.status_code in [200, 201, 204]:
                    finding = Vulnerability(
                        type=VulnType.API_VULN, severity=Severity.HIGH,
                        title="Potential Mass Assignment Vulnerability",
                        description="API endpoint may be vulnerable to mass assignment. Sensitive fields like 'admin' or 'role' were accepted.",
                        url=url, parameter="JSON body", payload=str(test_data),
                        evidence="Status: " + str(r.status_code) + ", Response: " + r.text[:200],
                        remediation="Implement strong input validation. Use Data Transfer Objects (DTOs). Whitelist allowed fields.",
                        cvss_score=7.5, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N",
                        cwe_id="CWE-915", confidence=0.6, verified=False,
                        references=["https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html", "https://portswigger.net/web-security/api-testing"],
                        tags=["api", "mass-assignment", "input-validation"]
                    )
                    findings.append(finding)
            except Exception as e:
                logger.debug("API mass assignment test error: " + str(e))
        try:
            r = self.session.get(url, timeout=10)
            if r.status_code == 200 and 'api' in url.lower():
                sensitive_patterns = ['password', 'token', 'secret', 'key', 'credit_card', 'ssn']
                if any(p in r.text.lower() for p in sensitive_patterns):
                    finding = Vulnerability(
                        type=VulnType.API_VULN, severity=Severity.HIGH,
                        title="API Exposes Sensitive Data Without Authentication",
                        description="API endpoint returns sensitive data without proper authentication.",
                        url=url, parameter="API endpoint", payload="",
                        evidence="Sensitive data found in unauthenticated response",
                        remediation="Implement proper authentication and authorization. Use OAuth 2.0 or JWT.",
                        cvss_score=7.5, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
                        cwe_id="CWE-306", confidence=0.7, verified=False,
                        references=["https://owasp.org/www-project-api-security/", "https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html"],
                        tags=["api", "authentication", "sensitive-data"]
                    )
                    findings.append(finding)
        except Exception as e:
            logger.debug("API auth test error: " + str(e))
        return findings

# =============================================================================
# GRAPHQL SCANNER
# =============================================================================

class GraphQLScanner:
    INTROSPECTION_QUERY = (
        "query IntrospectionQuery { __schema { queryType { name } mutationType { name } "
        "subscriptionType { name } types { ...FullType } directives { name description "
        "locations args { ...InputValue } } } } fragment FullType on __Type { kind "
        "name description fields(includeDeprecated: true) { name description args { "
        "...InputValue } type { ...TypeRef } isDeprecated deprecationReason } inputFields "
        "{ ...InputValue } interfaces { ...TypeRef } enumValues(includeDeprecated: true) "
        "{ name description isDeprecated deprecationReason } possibleTypes { ...TypeRef } } "
        "fragment InputValue on __InputValue { name description type { ...TypeRef } defaultValue } "
        "fragment TypeRef on __Type { kind name ofType { kind name ofType { kind name ofType { "
        "kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name } } } } } } } }"
    )

    def __init__(self, session, config=None):
        self.session = session
        self.config = config or {}

    def test_introspection(self, url):
        findings = []
        try:
            r = self.session.post(url, json={'query': self.INTROSPECTION_QUERY}, timeout=10)
            if r.status_code == 200 and '__schema' in r.text:
                finding = Vulnerability(
                    type=VulnType.GRAPHQL, severity=Severity.HIGH,
                    title="GraphQL Introspection Enabled",
                    description="GraphQL introspection is enabled. This exposes the entire schema including queries, mutations, and types.",
                    url=url, parameter="GraphQL endpoint", payload="IntrospectionQuery",
                    evidence="Introspection query returned schema information",
                    remediation="Disable introspection in production. Use allowlists for queries. Implement query cost analysis.",
                    cvss_score=7.5, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
                    cwe_id="CWE-200", confidence=0.9, verified=True,
                    references=["https://graphql.org/learn/introspection/", "https://owasp.org/www-project-api-security/"],
                    tags=["graphql", "introspection", "information-disclosure"]
                )
                findings.append(finding)
            deep_query = '{ ' + 'a { ' * 50 + 'id ' + '} ' * 50 + '}'
            r = self.session.post(url, json={'query': deep_query}, timeout=10)
            if r.status_code == 200:
                finding = Vulnerability(
                    type=VulnType.GRAPHQL, severity=Severity.MEDIUM,
                    title="GraphQL Query Depth Limit Not Enforced",
                    description="GraphQL endpoint does not enforce query depth limits. This could lead to DoS attacks.",
                    url=url, parameter="GraphQL endpoint", payload="Deep nested query",
                    evidence="Deep query executed without error",
                    remediation="Implement query depth limiting. Use query complexity analysis. Set timeout limits.",
                    cvss_score=5.3, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L",
                    cwe_id="CWE-770", confidence=0.7, verified=False,
                    references=["https://owasp.org/www-project-api-security/", "https://graphql.org/learn/security/"],
                    tags=["graphql", "dos", "query-depth"]
                )
                findings.append(finding)
        except Exception as e:
            logger.debug("GraphQL test error: " + str(e))
        return findings

# =============================================================================
# WEBSOCKET SCANNER
# =============================================================================

class WebSocketScanner:
    def __init__(self, config=None):
        self.config = config or {}

    def test_endpoint(self, ws_url):
        findings = []
        try:
            ws = websocket.create_connection(ws_url, timeout=5)
            test_messages = [
                '{"type": "message", "content": "<script>alert(1)</script>"}',
                '{"action": "subscribe", "channel": "admin"}',
                '{"action": "join", "room": "private"}',
            ]
            for msg in test_messages:
                ws.send(msg)
                response = ws.recv()
                if '<script>' in response or 'admin' in response.lower() or 'private' in response.lower():
                    finding = Vulnerability(
                        type=VulnType.WEBSOCKET, severity=Severity.MEDIUM,
                        title="WebSocket Security Issue",
                        description="WebSocket endpoint may have security issues. Test messages returned sensitive responses.",
                        url=ws_url, parameter="WebSocket message", payload=msg,
                        evidence="Response: " + response[:200],
                        remediation="Implement authentication for WebSocket connections. Validate all messages. Use WSS (WebSocket Secure).",
                        cvss_score=5.3, cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N",
                        cwe_id="CWE-306", confidence=0.6, verified=False,
                        references=["https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client_Side_Testing/10-Testing_WebSockets", "https://portswigger.net/web-security/websockets"],
                        tags=["websocket", "authentication", "message-validation"]
                    )
                    findings.append(finding)
                    break
            ws.close()
        except Exception as e:
            logger.debug("WebSocket test error: " + str(e))
        return findings

# =============================================================================
# REPORT GENERATOR (MULTI-FORMAT)
# =============================================================================

class ReportGenerator:
    def __init__(self, results, config=None):
        self.results = results
        self.config = config or {}

    def generate_all(self, target):
        reports = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = "vampire_bite_pro_v3_report_" + timestamp
        reports['html'] = self.generate_html(target, base_name + ".html")
        reports['json'] = self.generate_json(target, base_name + ".json")
        reports['xml'] = self.generate_xml(target, base_name + ".xml")
        reports['csv'] = self.generate_csv(target, base_name + ".csv")
        reports['pdf'] = self.generate_pdf(target, base_name + ".pdf")
        return reports

    def generate_html(self, target, filename):
        vuln_by_severity = {s.value: 0 for s in Severity}
        for v in self.results.vulnerabilities:
            vuln_by_severity[v.severity.value] += 1
        severity_colors = {"Critical": "#ff0000", "High": "#ff6600", "Medium": "#ffcc00", "Low": "#00ff00", "Info": "#0099ff"}
        vuln_rows = ""
        for v in self.results.vulnerabilities:
            color = severity_colors.get(v.severity.value, "#ffffff")
            verified_badge = "<span style='color:green'>✓ Verified</span>" if v.verified else "<span style='color:orange'>⚠ Potential</span>"
            refs = "<br>".join(["<a href='" + r + "' target='_blank'>" + r[:60] + "...</a>" if len(r) > 60 else "<a href='" + r + "' target='_blank'>" + r + "</a>" for r in v.references]) if v.references else "N/A"
            vuln_rows += "<tr><td><span class=\"badge\" style=\"background:" + color + "\">" + v.severity.value + "</span></td><td>" + v.type.value + "</td><td>" + v.title + "</td><td>" + v.parameter + "</td><td><code>" + html_module.escape(v.payload[:100]) + "</code></td><td>" + str(v.cvss_score) + "</td><td>" + v.cwe_id + "</td><td>" + str(v.confidence) + "</td><td>" + verified_badge + "</td><td>" + refs + "</td></tr>"
        port_rows = ""
        for p in self.results.open_ports:
            port_rows += "<tr><td>" + str(p['port']) + "</td><td>" + p['service'] + "</td><td>" + p['state'] + "</td><td><code>" + html_module.escape(p['banner'][:100]) + "</code></td><td>" + p.get('version', 'Unknown') + "</td></tr>"
        tech_badges = " ".join(["<span class='tech-badge'>" + t + "</span>" for t in self.results.technologies])
        html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Vampire Bite Pro v3.0 - Security Report - """ + target + """</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%); color: #eee; padding: 20px; min-height: 100vh; }
.container { max-width: 1600px; margin: 0 auto; background: rgba(255,255,255,0.03); border-radius: 20px; padding: 40px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }
h1 { color: #ff0000; text-align: center; font-size: 2.5em; text-shadow: 0 0 20px rgba(255,0,0,0.5); margin-bottom: 10px; }
.subtitle { text-align: center; color: #888; font-size: 1.1em; margin-bottom: 30px; }
.header-info { background: rgba(0,0,0,0.4); border-radius: 15px; padding: 25px; margin: 20px 0; border-left: 4px solid #ff0000; }
.header-info p { margin: 8px 0; font-size: 1.05em; }
.header-info strong { color: #ff4444; display: inline-block; width: 150px; }
.stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin: 30px 0; }
.stat-card { background: linear-gradient(135deg, rgba(0,0,0,0.6) 0%, rgba(255,0,0,0.1) 100%); padding: 25px; border-radius: 15px; text-align: center; border: 1px solid rgba(255,0,0,0.2); transition: transform 0.3s; }
.stat-card:hover { transform: translateY(-5px); }
.stat-number { font-size: 2.5em; color: #ff0000; font-weight: bold; text-shadow: 0 0 10px rgba(255,0,0,0.5); }
.stat-label { color: #aaa; margin-top: 10px; font-size: 0.95em; }
table { width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 0.95em; }
th, td { border: 1px solid rgba(255,0,0,0.3); padding: 12px; text-align: left; }
th { background: linear-gradient(135deg, rgba(255,0,0,0.2) 0%, rgba(255,0,0,0.1) 100%); color: #ff4444; font-weight: bold; position: sticky; top: 0; }
tr:nth-child(even) { background: rgba(255,255,255,0.02); }
tr:hover { background: rgba(255,0,0,0.05); }
.badge { padding: 5px 12px; border-radius: 6px; font-weight: bold; font-size: 0.85em; display: inline-block; }
.tech-badge { background: rgba(0,150,255,0.2); color: #00aaff; padding: 5px 15px; border-radius: 20px; margin: 3px; display: inline-block; font-size: 0.9em; border: 1px solid rgba(0,150,255,0.3); }
.section { margin: 40px 0; padding: 25px; background: rgba(0,0,0,0.3); border-radius: 15px; border: 1px solid rgba(255,255,255,0.05); }
.section h2 { color: #ff4444; margin-bottom: 20px; font-size: 1.8em; border-bottom: 2px solid rgba(255,0,0,0.3); padding-bottom: 10px; }
.footer { text-align: center; margin-top: 40px; color: #666; padding: 20px; border-top: 1px solid rgba(255,255,255,0.1); }
.footer p { margin: 5px 0; }
code { background: rgba(0,0,0,0.5); padding: 2px 6px; border-radius: 4px; font-family: 'Courier New', monospace; font-size: 0.9em; }
@media print { body { background: white; color: black; } .container { background: white; border: 1px solid #ccc; } }
</style>
</head>
<body>
<div class="container">
<h1>🛡️ VAMPIRE BITE PRO v3.0</h1>
<p class="subtitle">Ultimate Professional Security Scanner - Comprehensive Report</p>
<div class="header-info">
<p><strong>Target:</strong> """ + target + """</p>
<p><strong>IP Address:</strong> """ + self.results.ip + """</p>
<p><strong>Scan Time:</strong> """ + self.results.scan_time + """</p>
<p><strong>Duration:</strong> """ + str(self.results.duration) + """ seconds</p>
<p><strong>WAF Detected:</strong> """ + self.results.waf_detected + """</p>
<p><strong>Web Server:</strong> """ + self.results.web_server + """</p>
<p><strong>Technologies:</strong> """ + tech_badges + """</p>
</div>
<div class="stats">
<div class="stat-card"><div class="stat-number">""" + str(len(self.results.open_ports)) + """</div><div class="stat-label">Open Ports</div></div>
<div class="stat-card"><div class="stat-number">""" + str(len(self.results.technologies)) + """</div><div class="stat-label">Technologies</div></div>
<div class="stat-card"><div class="stat-number" style="color:#ff0000">""" + str(vuln_by_severity['Critical']) + """</div><div class="stat-label">Critical</div></div>
<div class="stat-card"><div class="stat-number" style="color:#ff6600">""" + str(vuln_by_severity['High']) + """</div><div class="stat-label">High</div></div>
<div class="stat-card"><div class="stat-number" style="color:#ffcc00">""" + str(vuln_by_severity['Medium']) + """</div><div class="stat-label">Medium</div></div>
<div class="stat-card"><div class="stat-number" style="color:#00ff00">""" + str(vuln_by_severity['Low']) + """</div><div class="stat-label">Low</div></div>
<div class="stat-card"><div class="stat-number">""" + str(len(self.results.vulnerabilities)) + """</div><div class="stat-label">Total Vulns</div></div>
<div class="stat-card"><div class="stat-number">""" + str(len(self.results.subdomains)) + """</div><div class="stat-label">Subdomains</div></div>
</div>
<div class="section">
<h2>🔴 Vulnerabilities</h2>
<div style="overflow-x:auto">
<table>
<thead><tr><th>Severity</th><th>Type</th><th>Title</th><th>Parameter</th><th>Payload</th><th>CVSS</th><th>CWE</th><th>Confidence</th><th>Status</th><th>References</th></tr></thead>
<tbody>""" + vuln_rows + """</tbody>
</table>
</div>
</div>
<div class="section">
<h2>🌐 Open Ports</h2>
<div style="overflow-x:auto">
<table>
<thead><tr><th>Port</th><th>Service</th><th>State</th><th>Banner</th><th>Version</th></tr></thead>
<tbody>""" + port_rows + """</tbody>
</table>
</div>
</div>
<div class="section">
<h2>📁 Sensitive Files</h2>
<ul>""" + "".join(["<li><strong>" + f['file'] + "</strong> - " + f['url'] + " (" + str(f['size']) + " bytes)</li>" for f in self.results.sensitive_files]) + """</ul>
</div>
<div class="section">
<h2>👑 Admin Panels</h2>
<ul>""" + "".join(["<li><strong>" + a['path'] + "</strong> - " + a['url'] + "</li>" for a in self.results.admin_panels]) + """</ul>
</div>
<div class="section">
<h2>📂 Open Directories</h2>
<ul>""" + "".join(["<li><strong>" + d['path'] + "</strong> - " + d['url'] + "</li>" for d in self.results.open_directories]) + """</ul>
</div>
<div class="section">
<h2>📝 Forms</h2>
<ul>""" + "".join(["<li><strong>" + form['method'] + "</strong> " + form['action'] + " (" + str(len(form['inputs'])) + " fields)</li>" for form in self.results.forms]) + """</ul>
</div>
<div class="section">
<h2>🍪 Cookies</h2>
<ul>""" + "".join(["<li><strong>" + c['name'] + "</strong> - Secure: " + str(c['secure']) + ", HttpOnly: " + str(c['httponly']) + ", SameSite: " + c['samesite'] + "</li>" for c in self.results.cookies]) + """</ul>
</div>
<div class="section">
<h2>🔍 Subdomains</h2>
<ul>""" + "".join(["<li>" + sub + "</li>" for sub in self.results.subdomains]) + """</ul>
</div>
<div class="footer">
<p>🛡️ Vampire Bite Pro v3.0 - Ultimate Security Scanner</p>
<p>Generated: """ + datetime.now().isoformat() + """</p>
<p style="color:#666; font-size:0.9em; margin-top:10px;">This report is generated for authorized security testing purposes only. Use of this tool against systems without explicit permission is illegal.</p>
</div>
</div>
</body>
</html>"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        return filename

    def generate_json(self, target, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results.to_dict(), f, indent=2, ensure_ascii=False)
        return filename

    def generate_xml(self, target, filename):
        root = ET.Element("VampireBiteProReport")
        root.set("version", "3.0")
        root.set("target", target)
        root.set("generated", datetime.now().isoformat())
        target_info = ET.SubElement(root, "TargetInfo")
        ET.SubElement(target_info, "URL").text = target
        ET.SubElement(target_info, "IP").text = self.results.ip
        ET.SubElement(target_info, "ScanTime").text = self.results.scan_time
        ET.SubElement(target_info, "Duration").text = str(self.results.duration)
        ET.SubElement(target_info, "WAF").text = self.results.waf_detected
        ET.SubElement(target_info, "WebServer").text = self.results.web_server
        vulns = ET.SubElement(root, "Vulnerabilities")
        for v in self.results.vulnerabilities:
            vuln = ET.SubElement(vulns, "Vulnerability")
            vuln.set("severity", v.severity.value)
            vuln.set("type", v.type.value)
            ET.SubElement(vuln, "Title").text = v.title
            ET.SubElement(vuln, "Description").text = v.description
            ET.SubElement(vuln, "URL").text = v.url
            ET.SubElement(vuln, "Parameter").text = v.parameter
            ET.SubElement(vuln, "Payload").text = v.payload
            ET.SubElement(vuln, "CVSS").text = str(v.cvss_score)
            ET.SubElement(vuln, "CWE").text = v.cwe_id
            ET.SubElement(vuln, "Confidence").text = str(v.confidence)
            ET.SubElement(vuln, "Verified").text = str(v.verified)
        tree = ET.ElementTree(root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        return filename

    def generate_csv(self, target, filename):
        import csv
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Severity', 'Type', 'Title', 'URL', 'Parameter', 'Payload', 'CVSS', 'CWE', 'Confidence', 'Verified'])
            for v in self.results.vulnerabilities:
                writer.writerow([v.severity.value, v.type.value, v.title, v.url, v.parameter, v.payload, v.cvss_score, v.cwe_id, v.confidence, v.verified])
        return filename

    def generate_pdf(self, target, filename):
        doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        story = []
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#ff0000'), spaceAfter=30, alignment=1)
        story.append(Paragraph("Vampire Bite Pro v3.0", title_style))
        story.append(Paragraph("Security Assessment Report", styles['Heading2']))
        story.append(Spacer(1, 20))
        story.append(Paragraph("<b>Target:</b> " + target, styles['Normal']))
        story.append(Paragraph("<b>IP:</b> " + self.results.ip, styles['Normal']))
        story.append(Paragraph("<b>Scan Time:</b> " + self.results.scan_time, styles['Normal']))
        story.append(Paragraph("<b>Duration:</b> " + str(self.results.duration) + " seconds", styles['Normal']))
        story.append(Spacer(1, 20))
        if self.results.vulnerabilities:
            story.append(Paragraph("Vulnerabilities", styles['Heading2']))
            story.append(Spacer(1, 12))
            table_data = [['Severity', 'Type', 'Title', 'CVSS', 'CWE']]
            for v in self.results.vulnerabilities:
                table_data.append([v.severity.value, v.type.value, v.title[:50], str(v.cvss_score), v.cwe_id])
            table = Table(table_data, colWidths=[80, 100, 200, 50, 60])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff0000')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#1a1a2e')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ff0000')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ]))
            story.append(table)
            story.append(PageBreak())
        if self.results.open_ports:
            story.append(Paragraph("Open Ports", styles['Heading2']))
            story.append(Spacer(1, 12))
            port_data = [['Port', 'Service', 'State', 'Version']]
            for p in self.results.open_ports:
                port_data.append([str(p['port']), p['service'], p['state'], p.get('version', 'Unknown')])
            port_table = Table(port_data, colWidths=[80, 120, 80, 150])
            port_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff0000')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ff0000')),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#1a1a2e')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.whitesmoke),
            ]))
            story.append(port_table)
        doc.build(story)
        return filename

# =============================================================================
# MAIN VAMPIRE BITE PRO v3.0 CLASS
# =============================================================================

class VampireBitePro:
    def __init__(self, config=None):
        if config is None:
            config = {}
        self.config = config
        self.session = requests.Session()
        try:
            self.ua = UserAgent()
            self.session.headers.update({'User-Agent': self.config.get('user_agent', self.ua.random)})
        except:
            self.session.headers.update({'User-Agent': self.config.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')})
        custom_headers = self.config.get('headers', {})
        self.session.headers.update(custom_headers)
        self.session.verify = self.config.get('verify_ssl', False)
        proxy = self.config.get('proxy')
        if proxy:
            self.session.proxies = {'http': proxy, 'https': proxy}
        cookies = self.config.get('cookies', {})
        if cookies:
            self.session.cookies.update(cookies)
        self.delay = self.config.get('delay', 1.0)
        self.state_file = "scan_state_v3.json"
        self.running = True
        self.port_scanner = AdvancedPortScanner(
            timeout=self.config.get('port_timeout', 2.0),
            max_workers=self.config.get('max_workers', 100),
            scan_type=self.config.get('scan_type', 'tcp')
        )
        self.xss_scanner = XSSScanner(self.session, self.config)
        self.sqli_scanner = SQLiScanner(self.session, self.config)
        self.lfi_rfi_scanner = LFIRFIScanner(self.session, self.config)
        self.ssrf_scanner = SSRFScanner(self.session, self.config)
        self.cmd_injection_scanner = CommandInjectionScanner(self.session, self.config)
        self.xxe_scanner = XXEScanner(self.session, self.config)
        self.csrf_scanner = CSRFScanner(self.session, self.config)
        self.open_redirect_scanner = OpenRedirectScanner(self.session, self.config)
        self.idor_scanner = IDORScanner(self.session, self.config)
        self.jwt_scanner = JWTScanner(self.session, self.config)
        self.cors_scanner = CORSScanner(self.session, self.config)
        self.security_headers_scanner = SecurityHeadersScanner(self.session, self.config)
        self.ssl_scanner = SSLTLSScanner(self.config)
        self.tech_detector = TechnologyDetector()
        self.api_scanner = APIScanner(self.session, self.config)
        self.graphql_scanner = GraphQLScanner(self.session, self.config)
        self.websocket_scanner = WebSocketScanner(self.config)
        self.subdomain_enum = SubdomainEnumerator(self.config)
        self.results = ScanResult()
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        logger.info("Received shutdown signal. Saving state...")
        self.running = False
        self._save_state()
        sys.exit(0)

    def _save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.results.to_dict(), f, indent=2)
        logger.info("State saved to " + self.state_file)

    def _load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                logger.info("Previous state loaded. Resuming scan...")
                return ScanResult(**data)
            except:
                pass
        return None

    def banner(self):
        print("")
        print(Fore.CYAN + "╔══════════════════════════════════════════════════════════════════════╗")
        print("║                                                                      ║")
        print("║   ██╗   ██╗ █████╗ ███╗   ███╗██████╗ ██╗██████╗ ███████╗            ║")
        print("║   ██║   ██║██╔══██╗████╗ ████║██╔══██╗██║██╔══██╗██╔════╝            ║")
        print("║   ██║   ██║███████║██╔████╔██║██████╔╝██║██████╔╝█████╗              ║")
        print("║   ╚██╗ ██╔╝██╔══██║██║╚██╔╝██║██╔═══╝ ██║██╔══██╗██╔══╝              ║")
        print("║    ╚████╔╝ ██║  ██║██║ ╚═╝ ██║██║     ██║██║  ██║███████╗            ║")
        print("║     ╚═══╝  ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝            ║")
        print("║                                                                      ║")
        print("║  " + Fore.RED + "🛡️ VAMPIRE BITE PRO v3.0 - ULTIMATE SECURITY SCANNER" + Fore.CYAN + "           ║")
        print("║  " + Fore.GREEN + "🔥 Complete Vulnerability Detection | Professional Reports" + Fore.CYAN + "      ║")
        print("║  " + Fore.YELLOW + "⚡ XSS | SQLi | LFI | RFI | SSRF | XXE | CSRF | IDOR | CMDi" + Fore.CYAN + "       ║")
        print("║  " + Fore.MAGENTA + "🌐 SSL/TLS | API | GraphQL | WebSocket | CORS | Headers" + Fore.CYAN + "          ║")
        print("╚══════════════════════════════════════════════════════════════════════╝")
        print(Style.RESET_ALL)

    def _get_ip(self, hostname):
        try:
            return socket.gethostbyname(hostname)
        except:
            return ""

    def _is_custom_404(self, response, target):
        indicators = ['not found', '404', 'page not found', 'error', 'no such file']
        if any(i in response.text.lower() for i in indicators):
            if response.status_code == 200:
                return True
        try:
            random_path = "/" + hashlib.md5(str(random.random()).encode()).hexdigest()[:10]
            r404 = self.session.get(target + random_path, timeout=10)
            if abs(len(r404.text) - len(response.text)) < 100:
                return True
        except:
            pass
        return False

    def phase_reconnaissance(self, target, ip):
        print("")
        print(Fore.MAGENTA + "┌─────────────────────────────────────────────────────────────┐")
        print("│  PHASE 1: RECONNAISSANCE & DNS ENUMERATION                  │")
        print("└─────────────────────────────────────────────────────────────┘" + Style.RESET_ALL)
        try:
            self.results.dns_info['hostname'] = socket.getfqdn(ip)
            self.results.dns_info['ip'] = ip
            print("  " + Fore.GREEN + "✅ Hostname: " + self.results.dns_info['hostname'] + Style.RESET_ALL)
        except:
            pass
        try:
            for record_type in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']:
                try:
                    answers = dns.resolver.resolve(urlparse(target).hostname or target, record_type)
                    self.results.dns_info[record_type] = [str(rdata) for rdata in answers]
                    print("  " + Fore.GREEN + "✅ " + record_type + " Records: " + ", ".join(self.results.dns_info[record_type][:3]) + Style.RESET_ALL)
                except:
                    pass
        except:
            pass
        if target.startswith('https'):
            try:
                ssl_findings = self.ssl_scanner.scan(urlparse(target).hostname, 443)
                for finding in ssl_findings:
                    self.results.vulnerabilities.append(finding)
                    print("  " + Fore.RED + "💀 SSL/TLS: " + finding.title + Style.RESET_ALL)
            except Exception as e:
                print("  " + Fore.YELLOW + "⚠️ SSL Error: " + str(e) + Style.RESET_ALL)
        try:
            r = self.session.get(target, timeout=10)
            self.results.headers = dict(r.headers)
            waf = WAFDetector.detect(dict(r.headers), r.text, r.status_code)
            self.results.waf_detected = waf
            if waf != "None Detected":
                print("  " + Fore.YELLOW + "⚠️ WAF Detected: " + waf + Style.RESET_ALL)
            else:
                print("  " + Fore.GREEN + "✅ No WAF detected" + Style.RESET_ALL)
            techs = self.tech_detector.detect(r, target, r.cookies)
            self.results.technologies = techs
            if techs:
                print("  " + Fore.GREEN + "✅ Technologies: " + ", ".join(techs) + Style.RESET_ALL)
            server = r.headers.get('Server', 'Unknown')
            self.results.web_server = server
            print("  " + Fore.GREEN + "✅ Server: " + server + Style.RESET_ALL)
            for cookie in r.cookies:
                self.results.cookies.append({
                    'name': cookie.name,
                    'value': cookie.value[:20] + '...' if len(cookie.value) > 20 else cookie.value,
                    'secure': cookie.secure,
                    'httponly': cookie.has_nonstandard_attr('HttpOnly'),
                    'samesite': cookie.get_nonstandard_attr('SameSite', 'None')
                })
            for cookie in r.cookies:
                if len(cookie.value.split('.')) == 3:
                    jwt_findings = self.jwt_scanner.analyze_jwt(cookie.value, target)
                    for finding in jwt_findings:
                        self.results.vulnerabilities.append(finding)
                        print("  " + Fore.RED + "💀 JWT: " + finding.title + Style.RESET_ALL)
            header_findings = self.security_headers_scanner.scan_headers(target)
            for finding in header_findings:
                self.results.vulnerabilities.append(finding)
                print("  " + Fore.YELLOW + "⚠️ Header: " + finding.title + Style.RESET_ALL)
            cors_findings = self.cors_scanner.test_cors(target)
            for finding in cors_findings:
                self.results.vulnerabilities.append(finding)
                print("  " + Fore.RED + "💀 CORS: " + finding.title + Style.RESET_ALL)
        except Exception as e:
            print("  " + Fore.RED + "❌ Initial request failed: " + str(e) + Style.RESET_ALL)

    def phase_port_scan(self, ip):
        print("")
        print(Fore.MAGENTA + "┌─────────────────────────────────────────────────────────────┐")
        print("│  PHASE 2: ADVANCED PORT SCANNING                              │")
        print("└─────────────────────────────────────────────────────────────┘" + Style.RESET_ALL)
        ports = self.config.get('ports', self.port_scanner.COMMON_PORTS)
        scan_type = self.config.get('scan_type', 'tcp')
        open_ports = self.port_scanner.scan(ip, ports, scan_type)
        self.results.open_ports = open_ports
        for p in open_ports:
            print("  " + Fore.RED + "🔴 Port " + str(p['port']) + " [" + p['service'] + "] - " + p.get('version', 'Unknown') + " - " + p['banner'][:50] + Style.RESET_ALL)
        print("  " + Fore.GREEN + "✅ Found " + str(len(open_ports)) + " open ports" + Style.RESET_ALL)

    def phase_subdomain_enum(self, domain):
        print("")
        print(Fore.MAGENTA + "┌─────────────────────────────────────────────────────────────┐")
        print("│  PHASE 3: SUBDOMAIN ENUMERATION                               │")
        print("└─────────────────────────────────────────────────────────────┘" + Style.RESET_ALL)
        subdomains = self.subdomain_enum.enumerate(domain)
        self.results.subdomains = subdomains
        for sub in subdomains[:20]:
            print("  " + Fore.CYAN + "🌐 " + sub + Style.RESET_ALL)
        if len(subdomains) > 20:
            print("  " + Fore.CYAN + "... and " + str(len(subdomains) - 20) + " more" + Style.RESET_ALL)
        print("  " + Fore.GREEN + "✅ Found " + str(len(subdomains)) + " subdomains" + Style.RESET_ALL)

    def phase_content_discovery(self, target):
        print("")
        print(Fore.MAGENTA + "┌─────────────────────────────────────────────────────────────┐")
        print("│  PHASE 4: CONTENT DISCOVERY                                 │")
        print("└─────────────────────────────────────────────────────────────┘" + Style.RESET_ALL)
        sensitive_files = [
            "/robots.txt", "/.git/config", "/.env", "/phpinfo.php", "/backup.sql",
            "/.htaccess", "/config.php", "/wp-config.php.bak", "/.DS_Store",
            "/sitemap.xml", "/crossdomain.xml", "/clientaccesspolicy.xml",
            "/.svn/entries", "/.hg/hgrc", "/Dockerfile", "/docker-compose.yml",
            "/package.json", "/composer.json", "/web.config", "/.htpasswd",
            "/api/swagger.json", "/api/v1/swagger.json", "/swagger-ui.html",
            "/graphql", "/api/graphql", "/api/v1/graphql",
            "/.aws/credentials", "/.ssh/id_rsa", "/.ssh/id_rsa.pub",
            "/adminer.php", "/phpmyadmin", "/pma", "/dbadmin",
            "/.env.local", "/.env.production", "/.env.development",
            "/api-docs", "/api/docs", "/swagger", "/openapi.json",
        ]
        found_files = []
        for f in sensitive_files:
            if not self.running:
                break
            try:
                url = target.rstrip('/') + f
                r = self.session.get(url, timeout=10, allow_redirects=False)
                if r.status_code == 200 and len(r.text) > 0:
                    if not self._is_custom_404(r, target):
                        found_files.append({"file": f, "url": url, "size": len(r.text)})
                        print("  " + Fore.RED + "📁 Sensitive: " + f + " (" + str(len(r.text)) + " bytes)" + Style.RESET_ALL)
                time.sleep(self.delay)
            except:
                pass
        self.results.sensitive_files = found_files
        admin_paths = [
            "/admin", "/administrator", "/wp-admin", "/login", "/cpanel",
            "/dashboard", "/admin/login", "/backend", "/controlpanel",
            "/manage", "/admincp", "/cp", "/panel", "/moderator",
            "/api/admin", "/api/v1/admin", "/admin/api",
            "/graphql/admin", "/admin/graphql",
            "/actuator", "/actuator/health", "/actuator/env",
            "/swagger-ui.html", "/api/swagger-ui.html",
        ]
        found_admins = []
        for path in admin_paths:
            if not self.running:
                break
            try:
                url = target.rstrip('/') + path
                r = self.session.get(url, timeout=10, allow_redirects=True)
                if r.status_code == 200:
                    keywords = ['login', 'username', 'password', 'admin', 'dashboard', 'sign in', 'authentication']
                    if any(k in r.text.lower() for k in keywords):
                        found_admins.append({"path": path, "url": r.url})
                        print("  " + Fore.RED + "👑 Admin Panel: " + path + Style.RESET_ALL)
                time.sleep(self.delay)
            except:
                pass
        self.results.admin_panels = found_admins
        dirs = ["/backup", "/temp", "/tmp", "/old", "/test", "/dev", "/uploads",
                "/files", "/download", "/images", "/css", "/js", "/assets",
                "/static", "/media", "/content", "/data", "/logs", "/cache",
                "/api", "/api/v1", "/api/v2", "/api/v3", "/rest", "/graphql",
                "/ws", "/websocket", "/socket.io", "/sockjs",
                "/.well-known", "/.well-known/security.txt"]
        found_dirs = []
        for d in dirs:
            if not self.running:
                break
            try:
                url = target.rstrip('/') + d
                r = self.session.get(url, timeout=10, allow_redirects=False)
                if r.status_code == 200:
                    if 'Index of' in r.text or 'Parent Directory' in r.text or '<title>Index of' in r.text:
                        found_dirs.append({"path": d, "url": url})
                        print("  " + Fore.RED + "📂 Open Dir: " + d + Style.RESET_ALL)
                time.sleep(self.delay)
            except:
                pass
        self.results.open_directories = found_dirs

    def phase_crawl_and_form_analysis(self, target):
        print("")
        print(Fore.MAGENTA + "┌─────────────────────────────────────────────────────────────┐")
        print("│  PHASE 5: WEB CRAWLING & FORM ANALYSIS                      │")
        print("└─────────────────────────────────────────────────────────────┘" + Style.RESET_ALL)
        crawler = WebCrawler(self.session, self.config)
        crawler.crawl(target)
        crawl_results = crawler.get_results()
        self.results.crawl_data = crawl_results
        print("  " + Fore.GREEN + "✅ Crawled " + str(crawl_results['total_urls']) + " URLs" + Style.RESET_ALL)
        forms = []
        urls_to_check = [target] + list(crawl_results['visited_urls'])[:50]
        for url in urls_to_check:
            try:
                r = self.session.get(url, timeout=15)
                soup = BeautifulSoup(r.text, 'lxml')
                page_forms = soup.find_all('form')
                for form in page_forms:
                    action = form.get('action', url)
                    if action.startswith('/'):
                        action = urljoin(url, action)
                    method = form.get('method', 'GET').upper()
                    inputs = []
                    for inp in form.find_all(['input', 'textarea', 'select']):
                        inputs.append({
                            'name': inp.get('name', ''),
                            'type': inp.get('type', 'text'),
                            'required': inp.get('required', False)
                        })
                    forms.append({'action': action, 'method': method, 'inputs': inputs})
                    print("  " + Fore.CYAN + "📝 Form: " + method + " " + action + " (" + str(len(inputs)) + " fields)" + Style.RESET_ALL)
            except Exception as e:
                logger.debug("Form analysis error: " + str(e))
        self.results.forms = forms
        crawler.close()
        return forms

    def phase_vulnerability_scan(self, target, forms):
        print("")
        print(Fore.MAGENTA + "┌─────────────────────────────────────────────────────────────┐")
        print("│  PHASE 6: COMPREHENSIVE VULNERABILITY SCANNING              │")
        print("└─────────────────────────────────────────────────────────────┘" + Style.RESET_ALL)
        parsed = urlparse(target)
        if parsed.query:
            params = list(parse_qs(parsed.query).keys())
        else:
            params = ['q', 'id', 'page', 's', 'search', 'query', 'cat', 'product', 'user', 'p', 'file', 'url', 'path', 'redirect']
        for param in params:
            if not self.running:
                break
            print("  " + Fore.CYAN + "Testing parameter: " + param + Style.RESET_ALL)
            xss_findings = self.xss_scanner.test_url_parameter(target, param)
            for finding in xss_findings:
                self.results.vulnerabilities.append(finding)
                print("  " + Fore.RED + "💀 XSS Found: " + finding.title + Style.RESET_ALL)
            sqli_findings = self.sqli_scanner.test_url_parameter(target, param)
            for finding in sqli_findings:
                self.results.vulnerabilities.append(finding)
                print("  " + Fore.RED + "💀 SQLi Found: " + finding.title + Style.RESET_ALL)
            lfi_findings = self.lfi_rfi_scanner.test_url_parameter(target, param)
            for finding in lfi_findings:
                self.results.vulnerabilities.append(finding)
                print("  " + Fore.RED + "💀 LFI/RFI Found: " + finding.title + Style.RESET_ALL)
            ssrf_findings = self.ssrf_scanner.test_url_parameter(target, param)
            for finding in ssrf_findings:
                self.results.vulnerabilities.append(finding)
                print("  " + Fore.RED + "💀 SSRF Found: " + finding.title + Style.RESET_ALL)
            cmd_findings = self.cmd_injection_scanner.test_url_parameter(target, param)
            for finding in cmd_findings:
                self.results.vulnerabilities.append(finding)
                print("  " + Fore.RED + "💀 CMDi Found: " + finding.title + Style.RESET_ALL)
            redirect_findings = self.open_redirect_scanner.test_url_parameter(target, param)
            for finding in redirect_findings:
                self.results.vulnerabilities.append(finding)
                print("  " + Fore.RED + "💀 Open Redirect Found: " + finding.title + Style.RESET_ALL)
            if param in ['id', 'user_id', 'product_id', 'order_id', 'item_id']:
                idor_findings = self.idor_scanner.test_numeric_parameters(target, param)
                for finding in idor_findings:
                    self.results.vulnerabilities.append(finding)
                    print("  " + Fore.RED + "💀 IDOR Found: " + finding.title + Style.RESET_ALL)
            time.sleep(self.delay)
        for form in forms:
            if not self.running:
                break
            xss_findings = self.xss_scanner.test_form(form, target)
            for finding in xss_findings:
                self.results.vulnerabilities.append(finding)
                print("  " + Fore.RED + "💀 Form XSS Found: " + finding.title + Style.RESET_ALL)
            csrf_findings = self.csrf_scanner.test_form(form, target)
            for finding in csrf_findings:
                self.results.vulnerabilities.append(finding)
                print("  " + Fore.YELLOW + "⚠️ CSRF Found: " + finding.title + Style.RESET_ALL)
            time.sleep(self.delay)
        if self.config.get('scan_xxe', True):
            xxe_findings = self.xxe_scanner.test_endpoint(target)
            for finding in xxe_findings:
                self.results.vulnerabilities.append(finding)
                print("  " + Fore.RED + "💀 XXE Found: " + finding.title + Style.RESET_ALL)
        if self.config.get('scan_dom_xss', True):
            dom_findings = self.xss_scanner.test_dom_xss(target)
            for finding in dom_findings:
                self.results.vulnerabilities.append(finding)
                print("  " + Fore.RED + "💀 DOM XSS Found: " + finding.title + Style.RESET_ALL)
        if self.config.get('scan_api', True):
            api_paths = ['/api', '/api/v1', '/api/v2', '/rest', '/graphql', '/api/graphql']
            for api_path in api_paths:
                api_url = target.rstrip('/') + api_path
                try:
                    r = self.session.get(api_url, timeout=10)
                    if r.status_code == 200:
                        api_findings = self.api_scanner.test_endpoint(api_url)
                        for finding in api_findings:
                            self.results.vulnerabilities.append(finding)
                            print("  " + Fore.RED + "💀 API Vuln Found: " + finding.title + Style.RESET_ALL)
                        if 'graphql' in api_path.lower():
                            gql_findings = self.graphql_scanner.test_introspection(api_url)
                            for finding in gql_findings:
                                self.results.vulnerabilities.append(finding)
                                print("  " + Fore.RED + "💀 GraphQL Found: " + finding.title + Style.RESET_ALL)
                except:
                    pass
        if self.config.get('scan_websocket', True):
            ws_urls = [
                target.replace('https://', 'wss://').replace('http://', 'ws://') + '/ws',
                target.replace('https://', 'wss://').replace('http://', 'ws://') + '/websocket',
                target.replace('https://', 'wss://').replace('http://', 'ws://') + '/socket.io',
            ]
            for ws_url in ws_urls:
                try:
                    ws_findings = self.websocket_scanner.test_endpoint(ws_url)
                    for finding in ws_findings:
                        self.results.vulnerabilities.append(finding)
                        print("  " + Fore.RED + "💀 WebSocket Found: " + finding.title + Style.RESET_ALL)
                except:
                    pass

    def full_scan(self, target):
        self.start_time = time.time()
        self.results.target = target
        self.results.scan_time = datetime.now().isoformat()
        if not target.startswith(('http://', 'https://')):
            target = 'https://' + target
        parsed = urlparse(target)
        hostname = parsed.hostname or target
        ip = self._get_ip(hostname)
        self.results.ip = ip
        print(Fore.CYAN + "[TARGET] " + target + Style.RESET_ALL)
        print(Fore.CYAN + "[IP] " + ip + Style.RESET_ALL)
        self.phase_reconnaissance(target, ip)
        if self.config.get('scan_ports', True):
            self.phase_port_scan(ip)
        if self.config.get('enumerate_subdomains', True):
            self.phase_subdomain_enum(hostname)
        if self.config.get('discover_content', True):
            self.phase_content_discovery(target)
        forms = []
        if self.config.get('scan_forms', True):
            forms = self.phase_crawl_and_form_analysis(target)
        if self.config.get('scan_vulns', True):
            self.phase_vulnerability_scan(target, forms)
        self.results.duration = round(time.time() - self.start_time, 2)
        report_gen = ReportGenerator(self.results, self.config)
        reports = report_gen.generate_all(target)
        print("")
        print(Fore.CYAN + "="*60 + Style.RESET_ALL)
        print(Fore.GREEN + "📊 SCAN COMPLETE" + Style.RESET_ALL)
        print(Fore.CYAN + "="*60 + Style.RESET_ALL)
        print("  Duration: " + str(self.results.duration) + "s")
        print("  Vulnerabilities: " + str(len(self.results.vulnerabilities)))
        print("  Open Ports: " + str(len(self.results.open_ports)))
        print("  Subdomains: " + str(len(self.results.subdomains)))
        print("  Technologies: " + ", ".join(self.results.technologies))
        print("  Reports:")
        for fmt, path in reports.items():
            print("    - " + fmt.upper() + ": " + path)
        return self.results

    def run(self):
        self.banner()
        parser = argparse.ArgumentParser(description='Vampire Bite Pro v3.0 - Ultimate Security Scanner')
        parser.add_argument('target', help='Target URL or domain')
        parser.add_argument('--delay', type=float, default=1.0, help='Request delay between requests')
        parser.add_argument('--timeout', type=float, default=10.0, help='HTTP timeout')
        parser.add_argument('--port-timeout', type=float, default=2.0, help='Port scan timeout')
        parser.add_argument('--max-workers', type=int, default=100, help='Max threads')
        parser.add_argument('--ports', type=int, nargs='+', help='Custom ports to scan')
        parser.add_argument('--scan-type', choices=['syn', 'tcp', 'udp'], default='tcp', help='Port scan type')
        parser.add_argument('--no-port-scan', action='store_true', help='Skip port scan')
        parser.add_argument('--no-content', action='store_true', help='Skip content discovery')
        parser.add_argument('--no-vulns', action='store_true', help='Skip vulnerability scan')
        parser.add_argument('--no-subdomains', action='store_true', help='Skip subdomain enumeration')
        parser.add_argument('--no-forms', action='store_true', help='Skip form analysis')
        parser.add_argument('--verify-vulns', action='store_true', help='Verify vulnerabilities with headless browser')
        parser.add_argument('--waf-evasion', action='store_true', help='Enable WAF evasion techniques')
        parser.add_argument('--js-rendering', action='store_true', help='Enable JavaScript rendering for crawling')
        parser.add_argument('--crawl-depth', type=int, default=3, help='Crawl depth')
        parser.add_argument('--max-urls', type=int, default=500, help='Max URLs to crawl')
        parser.add_argument('--proxy', help='Proxy URL')
        parser.add_argument('--cookies', help='Cookies string (name=value;name2=value2)')
        parser.add_argument('--headers', help='Custom headers JSON')
        parser.add_argument('--user-agent', help='Custom User-Agent')
        parser.add_argument('--verify-ssl', action='store_true', default=False, help='Verify SSL certificates')
        parser.add_argument('--test-rfi', action='store_true', help='Test for RFI (requires external server)')
        parser.add_argument('--scan-xxe', action='store_true', default=True, help='Scan for XXE')
        parser.add_argument('--scan-dom-xss', action='store_true', default=True, help='Scan for DOM XSS')
        parser.add_argument('--scan-api', action='store_true', default=True, help='Scan API endpoints')
        parser.add_argument('--scan-websocket', action='store_true', default=True, help='Scan WebSocket endpoints')
        parser.add_argument('--output-dir', default='.', help='Output directory for reports')
        args = parser.parse_args()
        self.config.update({
            'delay': args.delay, 'timeout': args.timeout, 'port_timeout': args.port_timeout,
            'max_workers': args.max_workers, 'ports': args.ports, 'scan_type': args.scan_type,
            'scan_ports': not args.no_port_scan, 'discover_content': not args.no_content,
            'scan_vulns': not args.no_vulns, 'enumerate_subdomains': not args.no_subdomains,
            'scan_forms': not args.no_forms, 'verify_vulns': args.verify_vulns,
            'waf_evasion': args.waf_evasion, 'js_rendering': args.js_rendering,
            'crawl_depth': args.crawl_depth, 'max_urls': args.max_urls,
            'proxy': args.proxy, 'verify_ssl': args.verify_ssl, 'user_agent': args.user_agent,
            'test_rfi': args.test_rfi, 'scan_xxe': args.scan_xxe, 'scan_dom_xss': args.scan_dom_xss,
            'scan_api': args.scan_api, 'scan_websocket': args.scan_websocket, 'output_dir': args.output_dir
        })
        if args.cookies:
            cookies = {}
            for cookie in args.cookies.split(';'):
                if '=' in cookie:
                    k, v = cookie.strip().split('=', 1)
                    cookies[k] = v
            self.config['cookies'] = cookies
        if args.headers:
            import json
            self.config['headers'] = json.loads(args.headers)
        self.full_scan(args.target)

if __name__ == "__main__":
    scanner = VampireBitePro()
    scanner.run()
