#!/usr/bin/env python3
"""
Simple database connection test without importing database.py
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_connection_simple():
    """Test database connection using a simple approach"""
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    print(f"🔗 Testing connection to Supabase...")
    print(f"URL: {database_url.replace(database_url.split('@')[0].split(':')[-1], '*****')}")
    
    try:
        import psycopg2
        
        # Parse the URL manually to avoid SQLAlchemy issues
        if database_url.startswith('postgresql://'):
            url_parts = database_url.replace('postgresql://', '').split('@')
            user_pass = url_parts[0].split(':')
            host_port_db = url_parts[1].split('/')
            host_port = host_port_db[0].split(':')
            
            connection_params = {
                'host': host_port[0],
                'port': int(host_port[1]),
                'database': host_port_db[1],
                'user': user_pass[0],
                'password': user_pass[1]
            }
            
            conn = psycopg2.connect(**connection_params)
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            
            print(f"✅ Connection successful!")
            print(f"PostgreSQL version: {version[:80]}...")
            return True
            
    except ImportError:
        print("❌ psycopg2 not available, trying alternative method...")
        return test_with_urllib()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check your password is correct")
        print("2. Ensure your Supabase project is active")
        print("3. Verify your internet connection")
        return False

def test_with_urllib():
    """Test connection using urllib as fallback"""
    try:
        import urllib.request
        import json
        
        # Test if we can reach the Supabase endpoint
        supabase_url = os.getenv('SUPABASE_URL', 'https://kjbiltokwmrelyyvrnmu.supabase.co')
        test_url = f"{supabase_url}/rest/v1/"
        
        req = urllib.request.Request(test_url)
        req.add_header('User-Agent', 'LoanOriginationSystem/1.0')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 401:  # Expected - no API key provided
                print("✅ Supabase endpoint is reachable!")
                print("❌ But PostgreSQL driver is not working on this system")
                print("\n🔧 Workaround: Use the raw SQL script method")
                return True
            
    except Exception as e:
        print(f"❌ Network test failed: {e}")
        return False

if __name__ == "__main__":
    print("🏦 Database Connection Test")
    print("=" * 40)
    test_connection_simple()
