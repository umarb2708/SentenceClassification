#!/usr/bin/env python
"""
Setup Verification Script
Run this to check if your environment is properly configured.
"""

import sys
from pathlib import Path

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_status(check_name, status, message=""):
    """Print a status line."""
    icon = "✅" if status else "❌"
    print(f"{icon} {check_name}")
    if message:
        print(f"   {message}")

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    is_valid = version.major == 3 and version.minor >= 8
    return is_valid, f"Python {version.major}.{version.minor}.{version.micro}"

def check_file_exists(filepath):
    """Check if a file exists."""
    return Path(filepath).exists()

def check_directory_exists(dirpath):
    """Check if a directory exists."""
    return Path(dirpath).is_dir()

def check_virtual_environment():
    """Check if running in virtual environment."""
    return hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        'flask',
        'dotenv',
        'google.generativeai',
        'gtts',
        'textblob',
        'nltk'
    ]
    
    missing = []
    installed = []
    
    for package in required_packages:
        try:
            __import__(package)
            installed.append(package)
        except ImportError:
            missing.append(package)
    
    return len(missing) == 0, installed, missing

def check_environment_variables():
    """Check if .env file is configured."""
    from dotenv import load_dotenv
    import os
    
    if not check_file_exists('.env'):
        return False, ".env file not found"
    
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        return False, "GEMINI_API_KEY not set"
    
    if api_key == 'your_gemini_api_key_here':
        return False, "GEMINI_API_KEY not configured (still contains placeholder)"
    
    return True, "API key configured"

def main():
    """Main verification function."""
    print_header("Environment Setup Verification")
    
    all_checks_passed = True
    
    # Check Python version
    print("\n📋 SYSTEM CHECKS")
    print("-" * 60)
    is_valid, version_str = check_python_version()
    print_status("Python Version", is_valid, version_str)
    if not is_valid:
        print("   ⚠️  Python 3.8 or higher is required")
        all_checks_passed = False
    
    # Check virtual environment
    in_venv = check_virtual_environment()
    print_status("Virtual Environment", in_venv, 
                 "Active" if in_venv else "Not active (run from start_app.bat)")
    if not in_venv:
        print("   ℹ️  Recommendation: Use virtual environment for better isolation")
    
    # Check project files
    print("\n📁 FILE STRUCTURE CHECKS")
    print("-" * 60)
    
    core_files = [
        ('app.py', 'Main application file'),
        ('start_app.py', 'Startup script'),
        ('requirements.txt', 'Dependencies file'),
        ('.env.example', 'Environment template')
    ]
    
    for filename, description in core_files:
        exists = check_file_exists(filename)
        print_status(f"{filename}", exists, description)
        if not exists:
            all_checks_passed = False
    
    # Check directories
    directories = [
        ('templates', 'HTML templates'),
        ('static', 'CSS and static files')
    ]
    
    for dirname, description in directories:
        exists = check_directory_exists(dirname)
        print_status(f"{dirname}/", exists, description)
        if not exists:
            all_checks_passed = False
    
    # Check template files
    template_files = [
        'templates/index.html',
        'templates/result.html'
    ]
    
    for filepath in template_files:
        exists = check_file_exists(filepath)
        print_status(f"  {filepath}", exists)
        if not exists:
            all_checks_passed = False
    
    # Check static files
    static_files = [
        'static/style.css'
    ]
    
    for filepath in static_files:
        exists = check_file_exists(filepath)
        print_status(f"  {filepath}", exists)
        if not exists:
            all_checks_passed = False
    
    # Check dependencies
    print("\n📦 DEPENDENCY CHECKS")
    print("-" * 60)
    
    deps_ok, installed, missing = check_dependencies()
    
    if deps_ok:
        print_status("All Dependencies", True, f"{len(installed)} packages installed")
        if '--verbose' in sys.argv or '-v' in sys.argv:
            for pkg in installed:
                print(f"   ✓ {pkg}")
    else:
        print_status("Dependencies", False, f"{len(missing)} packages missing")
        for pkg in missing:
            print(f"   ✗ {pkg}")
        print("\n   ℹ️  Run 'pip install -r requirements.txt' to install missing packages")
        all_checks_passed = False
    
    # Check environment configuration
    print("\n⚙️  CONFIGURATION CHECKS")
    print("-" * 60)
    
    try:
        env_ok, env_msg = check_environment_variables()
        print_status("Environment Configuration", env_ok, env_msg)
        if not env_ok:
            print("   ℹ️  Steps to configure:")
            print("   1. Copy .env.example to .env")
            print("   2. Get API key from: https://makersuite.google.com/app/apikey")
            print("   3. Edit .env and add your API key")
            all_checks_passed = False
    except Exception as e:
        print_status("Environment Configuration", False, str(e))
        all_checks_passed = False
    
    # Final summary
    print_header("VERIFICATION SUMMARY")
    
    if all_checks_passed:
        print("\n🎉 All checks passed! Your environment is properly configured.")
        print("\n✨ You're ready to start the application!")
        print("\n   Run: python start_app.py")
        print("   Or:  start_app.bat")
        print("\n   Then open: http://localhost:5000")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\n   If you need help:")
        print("   1. Read the README.md file")
        print("   2. Check QUICKSTART.md for common issues")
        print("   3. Run setup.bat to reconfigure")
    
    print("\n" + "=" * 60 + "\n")
    
    return 0 if all_checks_passed else 1

if __name__ == '__main__':
    sys.exit(main())
