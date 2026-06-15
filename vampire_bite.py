# Author: LORD VAMPIRE (Team Lord)

import subprocess
import sys
import os
import json
import re
import socket
import time
import random
import threading
import hashlib
import base64
import ftplib
from datetime import datetime
from urllib.parse import urlparse, urljoin, quote
from concurrent.futures import ThreadPoolExecutor, as_completed

def auto_install(pkg):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--quiet"])
        return True
    except:
        return False

def is_package_installed(package_name):
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def check_deps():
    deps = ["requests", "colorama", "bs4"]
    for d in deps:
        if d == "bs4":
            if not is_package_installed("bs4"):
                auto_install("beautifulsoup4")
        else:
            if not is_package_installed(d):
                auto_install(d)

check_deps()

import requests
from colorama import init, Fore, Back, Style
from bs4 import BeautifulSoup

init(autoreset=True)

class VampireBiteHunter:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.results = {
            "target": "", "ip": "", "scan_time": "", "duration": 0,
            "open_ports": [], "web_server": {}, "technologies": [],
            "security_headers": {}, "xss": [], "sql_injection": [],
            "sensitive_files": [], "admin_panels": [], "open_directories": [],
            "backdoors": [], "exploits_from_github": [], "exploits_from_exploitdb": [],
            "exploits_from_nvd": [], "all_exploits": []
        }
    
    def banner(self):
        print(f"""
{Fore.RED}
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                              ║
║   ██╗   ██╗ █████╗ ███╗   ███╗██████╗ ██╗██████╗ ███████╗     ██████╗ ██╗████████╗███████╗   ║
║   ██║   ██║██╔══██╗████╗ ████║██╔══██╗██║██╔══██╗██╔════╝     ██╔══██╗██║╚══██╔══╝██╔════╝   ║
║   ██║   ██║███████║██╔████╔██║██████╔╝██║██████╔╝█████╗       ██████╔╝██║   ██║   █████╗     ║
║   ╚██╗ ██╔╝██╔══██║██║╚██╔╝██║██╔═══╝ ██║██╔══██╗██╔══╝       ██╔══██╗██║   ██║   ██╔══╝     ║
║    ╚████╔╝ ██║  ██║██║ ╚═╝ ██║██║     ██║██║  ██║███████╗     ██████╔╝██║   ██║   ███████╗   ║
║     ╚═══╝  ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝     ╚═════╝ ╚═╝   ╚═╝   ╚══════╝   ║
║                                                                                              ║
║                                                                                              ║
║                                                                                              ║
║  👑 Author: LORD VAMPIRE (Team Lord Leader)                                                  ║
║  💉 One Bite. One Vulnerability. The Web Bleeds. 💉                                          ║
║  ⚡ Auto-install | GitHub Token | Fast Scan | Bloody Accurate ⚡                             ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""")
    
    def get_service_name(self, port):
        services = {21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",110:"POP3",
                   111:"RPC",135:"RPC",139:"NetBIOS",143:"IMAP",443:"HTTPS",445:"SMB",
                   993:"IMAPS",995:"POP3S",1433:"MSSQL",1723:"PPTP",3306:"MySQL",3389:"RDP",
                   5432:"PostgreSQL",5900:"VNC",6379:"Redis",8080:"HTTP-Alt",8443:"HTTPS-Alt",27017:"MongoDB"}
        return services.get(port, "Unknown")
    
    def scan_port(self, ip, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((ip, port)) == 0:
                s.close()
                return port
            s.close()
        except:
            pass
        return None
    
    def port_scan(self, ip):
        print(f"\n  {Fore.CYAN}[*] Scanning ports...{Style.RESET_ALL}")
        ports = [21,22,25,53,80,110,111,135,139,143,443,445,993,995,1433,1723,3306,3389,5432,5900,6379,8080,8443,27017]
        open_ports = []
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(self.scan_port, ip, p) for p in ports]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    open_ports.append(result)
                    print(f"      {Fore.RED}🩸 Port {result} [{self.get_service_name(result)}] OPEN{Style.RESET_ALL}")
        
        self.results["open_ports"] = open_ports
        return open_ports
    
    def detect_web_server(self, url):
        print(f"\n  {Fore.CYAN}[*] Detecting web server...{Style.RESET_ALL}")
        try:
            r = self.session.get(url, timeout=10)
            server = r.headers.get('Server', 'Unknown')
            print(f"      {Fore.RED}🩸 Server: {server}{Style.RESET_ALL}")
            self.results["web_server"] = {"name": server}
            return server
        except:
            return "Unknown"
    
    def detect_technologies(self, url):
        print(f"\n  {Fore.CYAN}[*] Detecting technologies...{Style.RESET_ALL}")
        try:
            r = self.session.get(url, timeout=10)
            text = r.text.lower()
            techs = []
            if '.php' in text:
                techs.append("PHP")
                print(f"      {Fore.GREEN}[+] PHP detected{Style.RESET_ALL}")
            if '.aspx' in text:
                techs.append("ASP.NET")
                print(f"      {Fore.GREEN}[+] ASP.NET detected{Style.RESET_ALL}")
            if 'react' in text:
                techs.append("React")
                print(f"      {Fore.GREEN}[+] React detected{Style.RESET_ALL}")
            if 'vue' in text:
                techs.append("Vue.js")
                print(f"      {Fore.GREEN}[+] Vue.js detected{Style.RESET_ALL}")
            self.results["technologies"] = techs
            return techs
        except:
            return []
    
    def check_security_headers(self, url):
        print(f"\n  {Fore.CYAN}[*] Checking security headers...{Style.RESET_ALL}")
        try:
            r = self.session.get(url, timeout=10)
            headers_list = ['X-Frame-Options', 'X-XSS-Protection', 'X-Content-Type-Options', 
                           'Strict-Transport-Security', 'Content-Security-Policy']
            for h in headers_list:
                if h in r.headers:
                    print(f"      {Fore.GREEN}✅ {h}{Style.RESET_ALL}")
                    self.results["security_headers"][h] = True
                else:
                    print(f"      {Fore.RED}❌ {h}{Style.RESET_ALL}")
                    self.results["security_headers"][h] = False
        except:
            pass
    
    def test_xss(self, url):
        print(f"\n  {Fore.CYAN}[*] Testing XSS...{Style.RESET_ALL}")
        payloads = ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>", "<svg onload=alert(1)>"]
        for p in payloads:
            try:
                test_url = f"{url}?q={quote(p)}"
                r = self.session.get(test_url, timeout=5)
                if p in r.text or p.replace('<', '&lt;') in r.text:
                    self.results["xss"].append({"payload": p, "url": test_url})
                    print(f"      {Fore.RED}[!] XSS VULNERABLE: {p[:30]}{Style.RESET_ALL}")
                    break
                time.sleep(0.1)
            except:
                pass
        if not self.results["xss"]:
            print(f"      {Fore.GREEN}[-] No XSS detected{Style.RESET_ALL}")
    
    def test_sql_injection(self, url):
        print(f"\n  {Fore.CYAN}[*] Testing SQL Injection...{Style.RESET_ALL}")
        payloads = ["'", "''", "' OR '1'='1"]
        errors = ["mysql", "sql syntax", "ora-", "postgresql", "database error"]
        for p in payloads:
            try:
                test_url = f"{url}?id={quote(p)}"
                r = self.session.get(test_url, timeout=5)
                for e in errors:
                    if e in r.text.lower():
                        self.results["sql_injection"].append({"payload": p, "evidence": e})
                        print(f"      {Fore.RED}[!] SQL INJECTION: {p}{Style.RESET_ALL}")
                        break
                time.sleep(0.1)
            except:
                pass
        if not self.results["sql_injection"]:
            print(f"      {Fore.GREEN}[-] No SQL Injection detected{Style.RESET_ALL}")
    
    def find_sensitive_files(self, url):
        print(f"\n  {Fore.CYAN}[*] Looking for sensitive files...{Style.RESET_ALL}")
        files = ["/robots.txt", "/.git/config", "/.env", "/phpinfo.php", "/backup.sql", 
                "/.htaccess", "/config.php", "/wp-config.php.bak"]
        found = []
        for f in files:
            try:
                test_url = f"{url.rstrip('/')}{f}"
                r = self.session.get(test_url, timeout=3)
                if r.status_code == 200:
                    found.append({"file": f, "url": test_url})
                    print(f"      {Fore.RED}[!] Found: {f}{Style.RESET_ALL}")
                time.sleep(0.05)
            except:
                pass
        self.results["sensitive_files"] = found
        if not found:
            print(f"      {Fore.GREEN}[-] No sensitive files found{Style.RESET_ALL}")
    
    def find_admin_panels(self, url):
        print(f"\n  {Fore.CYAN}[*] Hunting for admin panels...{Style.RESET_ALL}")
        paths = ["/admin", "/administrator", "/wp-admin", "/login", "/cpanel", "/dashboard",
                "/admin/login", "/backend", "/controlpanel", "/manage"]
        found = []
        for path in paths:
            try:
                test_url = f"{url.rstrip('/')}{path}"
                r = self.session.get(test_url, timeout=5, allow_redirects=True)
                if r.status_code == 200:
                    keywords = ['login', 'username', 'password', 'admin', 'dashboard']
                    if any(k in r.text.lower() for k in keywords):
                        found.append({"path": path, "url": r.url, "type": "Admin Panel with Login"})
                        print(f"      {Fore.RED}[✔] ADMIN PANEL: {path} → {r.url}{Style.RESET_ALL}")
                elif r.status_code in [401, 403]:
                    found.append({"path": path, "url": test_url, "type": "Authentication Required"})
                    print(f"      {Fore.RED}[!] {path} - AUTH REQUIRED (REAL ADMIN!){Style.RESET_ALL}")
                time.sleep(0.05)
            except:
                pass
        self.results["admin_panels"] = found
        if not found:
            print(f"      {Fore.GREEN}[-] No admin panels found{Style.RESET_ALL}")
    
    def find_open_directories(self, url):
        print(f"\n  {Fore.CYAN}[*] Looking for open directories...{Style.RESET_ALL}")
        dirs = ["/backup", "/temp", "/tmp", "/old", "/test", "/dev", "/uploads", "/files",
                "/download", "/images", "/css", "/js", "/assets", "/static", "/media",
                "/content", "/data", "/logs", "/cache", "/phpmyadmin", "/mysql"]
        found = []
        for d in dirs:
            try:
                test_url = f"{url.rstrip('/')}{d}"
                r = self.session.get(test_url, timeout=3, allow_redirects=False)
                if r.status_code == 200:
                    if 'Index of' in r.text or 'Parent Directory' in r.text:
                        found.append({"path": d, "url": test_url, "type": "Open Directory Listing"})
                        print(f"      {Fore.RED}[📁] OPEN DIRECTORY: {d}{Style.RESET_ALL}")
                    else:
                        found.append({"path": d, "url": test_url, "type": "Accessible Directory"})
                        print(f"      {Fore.YELLOW}[📁] Accessible: {d}{Style.RESET_ALL}")
                time.sleep(0.05)
            except:
                pass
        self.results["open_directories"] = found
        if not found:
            print(f"      {Fore.GREEN}[-] No open directories found{Style.RESET_ALL}")
    
    def find_backdoors(self, url):
        print(f"\n  {Fore.CYAN}[*] Hunting for backdoors...{Style.RESET_ALL}")
        backdoors = ["/shell.php", "/cmd.php", "/c99.php", "/r57.php", "/webshell.php", "/backdoor.php"]
        found = []
        for b in backdoors:
            try:
                test_url = f"{url.rstrip('/')}{b}"
                r = self.session.get(test_url, timeout=3)
                if r.status_code == 200:
                    found.append({"file": b, "url": test_url})
                    print(f"      {Fore.RED}[!] BACKDOOR FOUND: {b}{Style.RESET_ALL}")
                time.sleep(0.05)
            except:
                pass
        self.results["backdoors"] = found
        if not found:
            print(f"      {Fore.GREEN}[-] No backdoors found{Style.RESET_ALL}")
    
    def search_github_exploits(self, product):
        print(f"\n  {Fore.CYAN}[*] Hunting GitHub for {product} exploits...{Style.RESET_ALL}")
        exploits = []
        try:
            resp = self.session.get(
                "https://api.github.com/search/repositories",
                params={"q": f"{product} exploit CVE", "per_page": 8, "sort": "stars", "order": "desc"},
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()
                for item in data.get("items", []):
                    exploits.append({
                        "name": item.get("name", "Unknown"),
                        "url": item.get("html_url", ""),
                        "stars": item.get("stargazers_count", 0),
                        "description": item.get("description", "")[:100],
                        "language": item.get("language", "Unknown"),
                        "source": "GitHub"
                    })
                    print(f"      {Fore.RED}[!] GitHub: {item.get('name')} ⭐ {item.get('stargazers_count', 0)}{Style.RESET_ALL}")
            elif resp.status_code == 403:
                print(f"      {Fore.YELLOW}[!] GitHub API rate limit! Add GITHUB_TOKEN{Style.RESET_ALL}")
        except:
            pass
        return exploits
    
    def search_exploitdb(self, product):
        print(f"\n  {Fore.CYAN}[*] Hunting Exploit-DB for {product}...{Style.RESET_ALL}")
        exploits = []
        try:
            resp = self.session.get(
                f"https://www.exploit-db.com/search",
                params={"q": product},
                timeout=10,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            if resp.status_code == 200:
                exploit_ids = re.findall(r'/exploits/(\d+)', resp.text)
                unique_ids = list(set(exploit_ids))[:5]
                for eid in unique_ids:
                    exploits.append({
                        "id": eid,
                        "title": f"Exploit for {product}",
                        "url": f"https://www.exploit-db.com/exploits/{eid}",
                        "source": "Exploit-DB"
                    })
                    print(f"      {Fore.RED}[!] Exploit-DB: /exploits/{eid}{Style.RESET_ALL}")
        except:
            pass
        return exploits
    
    def search_nvd(self, product):
        print(f"\n  {Fore.CYAN}[*] Hunting NVD for {product} CVEs...{Style.RESET_ALL}")
        cves = []
        try:
            resp = self.session.get(
                "https://services.nvd.nist.gov/rest/json/cves/2.0",
                params={"keywordSearch": product, "resultsPerPage": 6},
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()
                for item in data.get("vulnerabilities", []):
                    cve = item["cve"]
                    cves.append({
                        "id": cve["id"],
                        "description": cve.get("descriptions", [{}])[0].get("value", "")[:100],
                        "url": f"https://nvd.nist.gov/vuln/detail/{cve['id']}",
                        "source": "NVD"
                    })
                    print(f"      {Fore.RED}[!] NVD: {cve['id']}{Style.RESET_ALL}")
        except:
            pass
        return cves
    
    def search_all_exploits(self, product):
        print(f"\n  {Fore.YELLOW}[*] Hunting exploits for: {product}{Style.RESET_ALL}")
        github = self.search_github_exploits(product)
        exploitdb = self.search_exploitdb(product)
        nvd = self.search_nvd(product)
        self.results["exploits_from_github"] = github
        self.results["exploits_from_exploitdb"] = exploitdb
        self.results["exploits_from_nvd"] = nvd
        self.results["all_exploits"] = github + exploitdb + nvd
        return self.results["all_exploits"]
    
    def full_scan(self, target):
        self.start_time = time.time()
        self.results["target"] = target
        self.results["scan_time"] = datetime.now().isoformat()
        
        if not target.startswith(('http://', 'https://')):
            target = 'https://' + target
        
        ip = urlparse(target).hostname or target
        self.results["ip"] = ip
        
        print(f"\n{Fore.CYAN}{'='*90}{Style.RESET_ALL}")
        print(f"{Fore.RED}🧛‍♂️ VAMPIRE BITE SCAN: {target}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*90}{Style.RESET_ALL}")
        
        # PHASE 1: PORT SCAN
        print(f"\n{Fore.MAGENTA}┌─────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}│  PHASE 1: PORT SCANNING                                   │{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}└─────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
        self.port_scan(ip)
        
        # PHASE 2: WEB SERVER
        print(f"\n{Fore.MAGENTA}┌─────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}│  PHASE 2: WEB SERVER & TECHNOLOGY                         │{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}└─────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
        self.detect_web_server(target)
        self.detect_technologies(target)
        
        # PHASE 3: VULNERABILITIES
        print(f"\n{Fore.MAGENTA}┌─────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}│  PHASE 3: VULNERABILITY SCANNING                          │{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}└─────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
        self.check_security_headers(target)
        self.test_xss(target)
        self.test_sql_injection(target)
        
        # PHASE 4: FILES & DIRECTORIES
        print(f"\n{Fore.MAGENTA}┌─────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}│  PHASE 4: FILES, DIRECTORIES & BACKDOORS                  │{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}└─────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
        self.find_sensitive_files(target)
        self.find_admin_panels(target)
        self.find_open_directories(target)
        self.find_backdoors(target)
        
        # PHASE 5: ONLINE EXPLOITS
        print(f"\n{Fore.MAGENTA}┌─────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}│  PHASE 5: ONLINE EXPLOIT SEARCH                           │{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}└─────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
        
        for tech in self.results["technologies"]:
            if tech:
                self.search_all_exploits(tech)
        
        if not self.results["technologies"]:
            self.search_all_exploits("web")
        
        self.results["duration"] = round(time.time() - self.start_time, 2)
        
        # SUMMARY
        print(f"\n{Fore.CYAN}{'='*90}{Style.RESET_ALL}")
        print(f"{Fore.RED}📊 VAMPIRE BITE SUMMARY{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*90}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Target: {target}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}IP: {ip}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Duration: {self.results['duration']}s{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Open Ports: {len(self.results['open_ports'])}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Web Server: {self.results['web_server'].get('name', 'Unknown')}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Technologies: {', '.join(self.results['technologies']) or 'None'}{Style.RESET_ALL}")
        print(f"  {Fore.RED}XSS: {len(self.results['xss'])} | SQLi: {len(self.results['sql_injection'])}{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}Sensitive Files: {len(self.results['sensitive_files'])}{Style.RESET_ALL}")
        print(f"  {Fore.RED}Admin Panels: {len(self.results['admin_panels'])}{Style.RESET_ALL}")
        print(f"  {Fore.RED}Open Dirs: {len(self.results['open_directories'])}{Style.RESET_ALL}")
        print(f"  {Fore.RED}Backdoors: {len(self.results['backdoors'])}{Style.RESET_ALL}")
        print(f"  {Fore.MAGENTA}GitHub: {len(self.results['exploits_from_github'])} | Exploit-DB: {len(self.results['exploits_from_exploitdb'])} | NVD: {len(self.results['exploits_from_nvd'])}{Style.RESET_ALL}")
        
        self.generate_html_report(target, ip)
        print(f"\n  {Fore.GREEN}[+] HTML Report: vampire_bite_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*90}{Style.RESET_ALL}\n")
        
        return self.results
    
    def quick_scan(self, target):
        if not target.startswith(('http://', 'https://')):
            target = 'https://' + target
        ip = urlparse(target).hostname or target
        
        print(f"\n{Fore.CYAN}{'='*90}{Style.RESET_ALL}")
        print(f"{Fore.RED}⚡ QUICK SCAN: {target}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*90}{Style.RESET_ALL}")
        
        self.port_scan(ip)
        self.detect_web_server(target)
        
        print(f"\n{Fore.GREEN}[+] Quick scan complete!{Style.RESET_ALL}")
    
    def generate_html_report(self, target, ip):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"vampire_bite_report_{ts}.html"
        
        html = f"""<!DOCTYPE html>
<html><head><title>Vampire Bite - {target}</title>
<meta charset="UTF-8">
<style>
body {{ background: #0a0a0a; color: #c00; font-family: 'Courier New', monospace; padding: 20px; }}
.container {{ max-width: 1400px; margin: auto; border: 2px solid #c00; padding: 25px; }}
h1 {{ color: #c00; text-align: center; text-shadow: 0 0 5px #c00; }}
h2 {{ color: #c00; border-bottom: 2px solid #c00; margin-top: 30px; }}
.critical {{ color: #f00; font-weight: bold; }}
.high {{ color: #ff6600; }}
table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
th, td {{ border: 1px solid #c00; padding: 8px; text-align: left; }}
th {{ background: #c00; color: #000; }}
.exploit {{ background: #111; border-left: 4px solid #c00; padding: 10px; margin: 10px 0; }}
</style>
</head>
<body>
<div class="container">
<h1>🧛‍♂️ VAMPIRE BITE - SECURITY REPORT</h1>
<div style="background:#111; padding:15px; border-left:4px solid #c00; margin:15px 0;">
<p><strong>Target:</strong> {target}</p>
<p><strong>IP:</strong> {ip}</p>
<p><strong>Scan Time:</strong> {self.results['scan_time']}</p>
<p><strong>Duration:</strong> {self.results['duration']} seconds</p>
<p><strong>Author:</strong> LORD VAMPIRE (Team Lord)</p>
</div>

<h2>🔌 OPEN PORTS ({len(self.results['open_ports'])})</h2>
<table>
<tr><th>Port</th><th>Service</th><th>Status</th></tr>
{''.join([f"<tr><td>{p}</td><td>{self.get_service_name(p)}</td><td class='critical'>OPEN</td></tr>" for p in self.results['open_ports']])}
</table>

<h2>🖥️ SYSTEM INFO</h2>
<table>
<tr><th>Component</th><th>Value</th></tr>
<tr><td>Web Server</td><td>{self.results['web_server'].get('name', 'Unknown')}</td></tr>
<tr><td>Technologies</td><td>{', '.join(self.results['technologies']) or 'None'}</td></tr>
</table>

<h2>⚠️ VULNERABILITIES</h2>
<h3>Missing Headers</h3>
<ul>{''.join([f"<li class='critical'>{h}</li>" for h, v in self.results['security_headers'].items() if not v])}</ul>
<h3>XSS ({len(self.results['xss'])})</h3>
<ul>{''.join([f"<li>{x['payload'][:50]}</li>" for x in self.results['xss']])}</ul>
<h3>SQL Injection ({len(self.results['sql_injection'])})</h3>
<ul>{''.join([f"<li>{s['payload']}</li>" for s in self.results['sql_injection']])}</ul>

<h2>📁 SENSITIVE FILES ({len(self.results['sensitive_files'])})</h2>
<ul>{''.join([f"<li><a href='{f['url']}' style='color:#ff6600;'>{f['file']}</a></li>" for f in self.results['sensitive_files']])}</ul>

<h2>👑 ADMIN PANELS ({len(self.results['admin_panels'])})</h2>
{''.join([f"<div style='background:#111; border-left:4px solid #ff6600; padding:10px; margin:10px 0;'><a href='{a['url']}' style='color:#c00;'>{a['url']}</a><br>Type: {a.get('type', 'Admin Panel')}</div>" for a in self.results['admin_panels']])}

<h2>📂 OPEN DIRECTORIES ({len(self.results['open_directories'])})</h2>
{''.join([f"<div style='background:#111; border-left:4px solid #ff6600; padding:10px; margin:10px 0;'><a href='{d['url']}' style='color:#c00;'>{d['url']}</a><br>Type: {d.get('type', 'Directory')}</div>" for d in self.results['open_directories']])}

<h2>💀 BACKDOORS ({len(self.results['backdoors'])})</h2>
<ul>{''.join([f"<li><a href='{b['url']}' style='color:#f00;'>{b['file']}</a></li>" for b in self.results['backdoors']])}</ul>

<h2>💀 ONLINE EXPLOITS ({len(self.results['all_exploits'])})</h2>
<h3>GitHub ({len(self.results['exploits_from_github'])})</h3>
{''.join([f"<div class='exploit'><a href='{e['url']}' style='color:#c00;'>{e['name']}</a><br>⭐ Stars: {e['stars']}<br>{e['description']}<br>Language: {e['language']}</div>" for e in self.results['exploits_from_github']])}
<h3>Exploit-DB ({len(self.results['exploits_from_exploitdb'])})</h3>
{''.join([f"<div class='exploit'><a href='{e['url']}' style='color:#c00;'>{e['title']}</a><br>ID: {e['id']}</div>" for e in self.results['exploits_from_exploitdb']])}
<h3>NVD CVEs ({len(self.results['exploits_from_nvd'])})</h3>
{''.join([f"<div class='exploit'><a href='{e['url']}' style='color:#c00;'>{e['id']}</a><br>{e['description']}</div>" for e in self.results['exploits_from_nvd']])}

<div style="text-align:center; margin-top:30px; padding-top:20px; border-top:1px solid #333;">
<p>🐺 CVE-HUNTER v27.0 - VAMPIRE BITE EDITION</p>
<p>⚡ Created by LORD VAMPIRE (Team Lord) ⚡</p>
<p>💉 One Bite. One Vulnerability. The Web Bleeds. 💉</p>
</div>
</div>
</body></html>"""
        
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(html)
        return fname
    
    def run(self):
        self.banner()
        while True:
            print(f"""
{Fore.RED}╔════════════════════════════════════════════════════════════════════════════════╗
║  {Fore.GREEN}[1]{Style.RESET_ALL} 🧛‍♂️ {Fore.RED}VAMPIRE{Fore.YELLOW} BITE{Style.RESET_ALL} - FULL SCAN                                              {Fore.RED}║
║  {Fore.GREEN}[2]{Style.RESET_ALL} 🔍 QUICK SCAN                                                             {Fore.RED}║
║  {Fore.GREEN}[3]{Style.RESET_ALL} 🌐 ONLINE EXPLOIT SEARCH ONLY                                             {Fore.RED}║
║  {Fore.GREEN}[0]{Style.RESET_ALL} 🚪 EXIT                                                                   {Fore.RED}║
╚════════════════════════════════════════════════════════════════════════════════╝
""")
            choice = input(f"{Fore.RED}┌─[{Fore.YELLOW}VAMPIRE{Fore.RED}]~[{Fore.GREEN}> {Style.RESET_ALL}")
            
            if choice == "1":
                target = input(f"{Fore.CYAN}Target URL (example.com): {Style.RESET_ALL}")
                self.full_scan(target)
                input(f"\n{Fore.CYAN}Press Enter...{Style.RESET_ALL}")
            elif choice == "2":
                target = input(f"{Fore.CYAN}Target URL: {Style.RESET_ALL}")
                self.quick_scan(target)
                input(f"\n{Fore.CYAN}Press Enter...{Style.RESET_ALL}")
            elif choice == "3":
                product = input(f"{Fore.CYAN}Product name (e.g., WordPress, Apache): {Style.RESET_ALL}")
                self.search_all_exploits(product)
                input(f"\n{Fore.CYAN}Press Enter...{Style.RESET_ALL}")
            elif choice == "0":
                print(f"\n{Fore.RED}🧛‍♂️ VAMPIRE BITE OUT. THE WEB BLEEDS. GOODBYE!{Style.RESET_ALL}")
                print(f"{Fore.GREEN}🐺 LORD VAMPIRE - Team Lord{Style.RESET_ALL}")
                break

if __name__ == "__main__":
    hunter = VampireBiteHunter()
    hunter.run()