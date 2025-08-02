#!/usr/bin/env python3
"""
Simple script to update Supabase password in .env file
"""

import os
import re

def update_database_password():
    print("🔑 Supabase Password Update")
    print("=" * 40)
    print()
    print("To get your password:")
    print("1. Go to: https://kjbiltokwmrelyyvrnmu.supabase.co")
    print("2. Navigate to: Settings → Database")
    print("3. Find 'Connection parameters' or 'Connection string'")
    print("4. Copy the password from the connection string")
    print()
    
    password = input("Enter your Supabase database password: ").strip()
    
    if not password:
        print("❌ Password cannot be empty!")
        return False
    
    # Read .env file
    env_file = ".env"
    try:
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Replace the placeholder with actual password
        new_content = content.replace('[YOUR-PASSWORD]', password)
        
        # Write back to file
        with open(env_file, 'w') as f:
            f.write(new_content)
        
        print("✅ Password updated in .env file!")
        
        # Test the connection
        return test_connection()
        
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")
        return False

def test_connection():
    """Test the database connection"""
    print("\n🔗 Testing database connection...")
    
    try:
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        database_url = os.getenv('DATABASE_URL')
        
        if '[YOUR-PASSWORD]' in database_url:
            print("❌ Password still not updated in DATABASE_URL")
            return False
        
        # Try importing and testing
        from sqlalchemy import create_engine, text
        
        engine = create_engine(database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Connection successful!")
            print(f"PostgreSQL: {version[:60]}...")
            
            # Test if tables exist
            result = conn.execute(text("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'"))
            table_count = result.fetchone()[0]
            
            if table_count == 0:
                print(f"\n📋 Database is empty ({table_count} tables found)")
                print("Next step: Initialize database with tables")
                print("Run: python db_utils.py init")
            else:
                print(f"\n📊 Database has {table_count} tables")
                print("✅ Database appears to be set up!")
            
            return True
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Try: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Double-check your password")
        print("2. Ensure your Supabase project is active")
        print("3. Check your internet connection")
        return False

if __name__ == "__main__":
    if update_database_password():
        print("\n🎉 Database connection set up successfully!")
        print("\n📋 Next steps:")
        print("1. Initialize database: python db_utils.py init")
        print("2. Start FastAPI server: python fastapi_app.py")
        print("3. Test at: http://localhost:8000/docs")
    else:
        print("\n❌ Setup incomplete. Please try again.")
