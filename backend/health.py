#!/usr/bin/env python3
"""
Simple health check script to verify deployment
"""
import sys
import os

print("=== Render Deployment Health Check ===")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in current directory:")
for f in sorted(os.listdir('.')):
    print(f"  - {f}")

print("\n=== Checking for app_wsgi.py ===")
if os.path.exists('app_wsgi.py'):
    print("✅ app_wsgi.py found")
    try:
        import app_wsgi
        print("✅ app_wsgi.py imports successfully")
        if hasattr(app_wsgi, 'application'):
            print("✅ application function found")
        else:
            print("❌ application function not found")
    except Exception as e:
        print(f"❌ Error importing app_wsgi: {e}")
else:
    print("❌ app_wsgi.py not found")

print("\n=== Checking requirements ===")
if os.path.exists('requirements-wsgi.txt'):
    print("✅ requirements-wsgi.txt found")
    with open('requirements-wsgi.txt', 'r') as f:
        print("Contents:", f.read().strip())
else:
    print("❌ requirements-wsgi.txt not found")
