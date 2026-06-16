#!/usr/bin/env python3
"""
Vampire Bite Pro - Dependency Installer
======================================
این فایل تمام پیش‌نیازهای برنامه Vampire Bite Pro را نصب می‌کند.

نحوه استفاده:
    python install_deps.py
    python install_deps.py --verbose
    python install_deps.py -v

پیش‌نیازها:
    - Python 3.8+
    - pip

پکیج‌های نصب شده:
    requests, colorama, beautifulsoup4, lxml, tldextract,
    dnspython, cryptography, pyOpenSSL, selenium, webdriver-manager,
    websocket-client, reportlab, Jinja2, fake-useragent
"""

import subprocess
import sys
import os


# لیست تمام پیش‌نیازها
# نام ماژول: نام پکیج pip
DEPENDENCIES = {
    "requests": "requests",
    "colorama": "colorama",
    "bs4": "beautifulsoup4",
    "lxml": "lxml",
    "tldextract": "tldextract",
    "dns": "dnspython",
    "cryptography": "cryptography",
    "OpenSSL": "pyOpenSSL",
    "selenium": "selenium",
    "webdriver_manager": "webdriver-manager",
    "websocket": "websocket-client",
    "reportlab": "reportlab",
    "jinja2": "Jinja2",
    "fake_useragent": "fake-useragent",
}


def print_banner():
    """نمایش بنر"""
    banner = """
+============================================================+
|                                                            |
|     VAMPIRE BITE PRO - DEPENDENCY INSTALLER                |
|                                                            |
|     نصب‌کننده پیش‌نیازهای برنامه اسکنر امنیتی              |
|                                                            |
+============================================================+
"""
    print(banner)


def check_python_version():
    """بررسی نسخه Python"""
    print("[INFO] بررسی نسخه Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("[ERROR] نیاز به Python 3.8 یا بالاتر دارید!")
        print("[ERROR] نسخه فعلی: {}.{}.{}".format(version.major, version.minor, version.micro))
        return False
    print("[OK] Python {}.{}.{} ✅".format(version.major, version.minor, version.micro))
    return True


def check_pip():
    """بررسی نصب pip"""
    print("[INFO] بررسی pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"],
                      capture_output=True, check=True)
        print("[OK] pip نصب است ✅")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[ERROR] pip نصب نیست!")
        print("[INFO] برای نصب pip:")
        print("       python -m ensurepip --upgrade")
        print("       یا:")
        print("       apt install python3-pip  (Linux)")
        print("       brew install python3     (Mac)")
        return False


def is_installed(module_name):
    """بررسی نصب بودن یک ماژول"""
    try:
        __import__(module_name.replace("-", "_"))
        return True
    except ImportError:
        return False


def install_package(package_name, verbose=False):
    """نصب یک پکیج با pip"""
    print("[INFO] در حال نصب {}...".format(package_name))

    cmd = [sys.executable, "-m", "pip", "install", package_name, "--upgrade"]

    if not verbose:
        cmd.append("--quiet")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] {} نصب شد ✅".format(package_name))
            return True
        else:
            print("[ERROR] خطا در نصب {}".format(package_name))
            if verbose and result.stderr:
                print("[DEBUG] {}".format(result.stderr[:200]))
            return False
    except Exception as e:
        print("[ERROR] خطا: {}".format(e))
        return False


def create_requirements_file():
    """ساخت فایل requirements.txt"""
    print("[INFO] ساخت فایل requirements.txt...")

    req_content = """# Vampire Bite Pro - Dependencies
# نصب با: pip install -r requirements.txt

requests>=2.28.0
colorama>=0.4.4
beautifulsoup4>=4.11.0
lxml>=4.9.0
tldextract>=3.4.0
dnspython>=2.3.0
cryptography>=39.0.0
pyOpenSSL>=23.0.0
selenium>=4.8.0
webdriver-manager>=3.8.0
websocket-client>=1.5.0
reportlab>=3.6.0
Jinja2>=3.1.0
fake-useragent>=1.1.0
"""

    req_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
    with open(req_file, "w", encoding="utf-8") as f:
        f.write(req_content)

    print("[OK] requirements.txt ساخته شد: {}".format(req_file))


def main():
    """تابع اصلی"""
    # بررسی پارامترها
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    print_banner()

    # بررسی‌های اولیه
    if not check_python_version():
        sys.exit(1)

    if not check_pip():
        sys.exit(1)

    print("\n" + "="*60)
    print("[INFO] بررسی پیش‌نیازهای نصب شده...")
    print("="*60 + "\n")

    # بررسی و نصب هر پیش‌نیاز
    installed = []
    failed = []
    already_installed = []

    for module_name, package_name in DEPENDENCIES.items():
        if is_installed(module_name):
            print("[OK] {} قبلاً نصب است ✅".format(package_name))
            already_installed.append(package_name)
        else:
            if install_package(package_name, verbose):
                installed.append(package_name)
            else:
                failed.append(package_name)

    # نتایج
    print("\n" + "="*60)
    print("📊 نتایج نصب:")
    print("="*60)

    if already_installed:
        print("\n✅ قبلاً نصب شده ({}):".format(len(already_installed)))
        for pkg in already_installed:
            print("   • {}".format(pkg))

    if installed:
        print("\n✅ تازه نصب شده ({}):".format(len(installed)))
        for pkg in installed:
            print("   • {}".format(pkg))

    if failed:
        print("\n❌ خطا در نصب ({}):".format(len(failed)))
        for pkg in failed:
            print("   • {}".format(pkg))
        print("\n[INFO] برای نصب دستی:")
        print("       python -m pip install {}".format(" ".join(failed)))

    # ساخت requirements.txt
    print("\n" + "="*60)
    create_requirements_file()

    # پیام نهایی
    print("\n" + "="*60)
    if not failed:
        print("🎉 تمام پیش‌نیازها نصب شدند!")
        print("\n[INFO] حالا می‌توانید Vampire Bite Pro را اجرا کنید:")
        print("       python vampire_bite_fixed.py https://target.com")
    else:
        print("⚠️ برخی پیش‌نیازها نصب نشدند.")
        print("[INFO] لطفاً خطاها را بررسی و دوباره تلاش کنید.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
