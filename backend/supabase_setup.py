#!/usr/bin/env python3
"""
Supabase Database Setup Script
Helps configure and test the Supabase database connection
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

def get_supabase_credentials():
    """Guide user through getting Supabase credentials"""
    print("🗄️  Supabase Database Setup")
    print("=" * 50)
    print()
    print("To complete setup, you need your Supabase database password.")
    print("Here's how to get it:")
    print()
    print("1. Go to: https://kjbiltokwmrelyyvrnmu.supabase.co")
    print("2. Sign in to your Supabase account")
    print("3. Navigate to Settings → Database")
    print("4. Under 'Connection string', find your password")
    print("5. Copy the password (it looks like: postgres://postgres:[PASSWORD]@...)")
    print()
    
    password = input("Enter your Supabase database password: ").strip()
    
    if not password:
        print("❌ Password cannot be empty!")
        return None
        
    return password

def update_env_file(password):
    """Update the .env file with the correct database URL"""
    env_file = ".env"
    
    # Create the database URL
    database_url = f"postgresql://postgres:{password}@db.kjbiltokwmrelyyvrnmu.supabase.co:5432/postgres"
    
    # Read current .env file
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Update the DATABASE_URL line
    with open(env_file, 'w') as f:
        for line in lines:
            if line.startswith('DATABASE_URL='):
                f.write(f'DATABASE_URL={database_url}\n')
            else:
                f.write(line)
    
    print(f"✅ Updated {env_file} with Supabase credentials")
    return database_url

def test_connection(database_url):
    """Test the database connection"""
    try:
        print("\n🔗 Testing database connection...")
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Connection successful!")
            print(f"PostgreSQL version: {version[:50]}...")
            return True
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check your password is correct")
        print("2. Ensure your Supabase project is active")
        print("3. Check your internet connection")
        return False

def initialize_database():
    """Initialize the database with tables and seed data"""
    print("\n🏗️  Initializing database...")
    
    try:
        from db_utils import initialize_database
        return initialize_database()
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def main():
    print("🏦 Loan Origination System - Supabase Setup")
    print("=" * 60)
    print()
    
    # Load environment variables
    load_dotenv()
    
    # Check if DATABASE_URL is already configured
    current_url = os.getenv('DATABASE_URL', '')
    if 'kjbiltokwmrelyyvrnmu.supabase.co' in current_url and '[YOUR_PASSWORD]' not in current_url:
        print("✅ Database URL already configured")
        database_url = current_url
    else:
        # Get credentials from user
        password = get_supabase_credentials()
        if not password:
            return
        
        # Update .env file
        database_url = update_env_file(password)
    
    # Test connection
    if not test_connection(database_url):
        return
    
    # Ask if user wants to initialize database
    print()
    init_db = input("Would you like to initialize the database with tables and seed data? (y/n): ").lower().strip()
    
    if init_db in ['y', 'yes']:
        if initialize_database():
            print("\n🎉 Database setup completed successfully!")
            print()
            print("📋 Next steps:")
            print("1. Start your FastAPI server: python fastapi_app.py")
            print("2. Access API docs at: http://localhost:8000/docs")
            print("3. Test with frontend: npm run dev (in frontend directory)")
            print()
            print("👥 Default test users created:")
            print("   admin@loanorigination.com / admin123")
            print("   underwriter@loanorigination.com / underwriter123")
            print("   john.doe@email.com / applicant123")
        else:
            print("❌ Database initialization failed")
    else:
        print("Database connection tested successfully. You can initialize later with:")
        print("python db_utils.py init")

if __name__ == "__main__":
    main()
