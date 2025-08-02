"""
Database utility script for the Loan Origination System
Provides functions to initialize, reset, and manage the database
"""

import os
import sys
from sqlalchemy import create_engine, text
from database import Base, engine, DATABASE_URL
from seed_data import create_seed_data

def create_database():
    """Create all database tables"""
    try:
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        return False

def drop_database():
    """Drop all database tables"""
    try:
        print("Dropping database tables...")
        Base.metadata.drop_all(bind=engine)
        print("✅ Database tables dropped successfully!")
        return True
    except Exception as e:
        print(f"❌ Error dropping database tables: {e}")
        return False

def reset_database():
    """Drop and recreate all database tables"""
    if drop_database() and create_database():
        print("✅ Database reset successfully!")
        return True
    return False

def check_database_connection():
    """Test database connection"""
    try:
        with engine.connect() as conn:
            # Use a query that works with both PostgreSQL and SQLite
            if 'sqlite' in DATABASE_URL.lower():
                result = conn.execute(text("SELECT sqlite_version()"))
                version = result.fetchone()[0]
                print(f"✅ Database connection successful!")
                print(f"SQLite version: {version}")
            else:
                result = conn.execute(text("SELECT version()"))
                version = result.fetchone()[0]
                print(f"✅ Database connection successful!")
                print(f"PostgreSQL version: {version}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def show_table_info():
    """Show information about database tables"""
    try:
        with engine.connect() as conn:
            # Get table names
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = result.fetchall()
            
            if not tables:
                print("No tables found in the database.")
                return
                
            print(f"\n📊 Database Tables ({len(tables)} total):")
            print("=" * 50)
            
            for table in tables:
                table_name = table[0]
                
                # Get row count
                count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                row_count = count_result.fetchone()[0]
                
                print(f"• {table_name}: {row_count} rows")
                
    except Exception as e:
        print(f"❌ Error getting table information: {e}")

def initialize_database():
    """Initialize database with tables and seed data"""
    print("🏦 Loan Origination System - Database Initialization")
    print("=" * 60)
    
    if not check_database_connection():
        return False
        
    if create_database():
        print("\n🌱 Creating seed data...")
        try:
            create_seed_data()
            print("✅ Database initialization completed successfully!")
            print("\n📋 Next steps:")
            print("1. Update your .env file with the correct DATABASE_URL")
            print("2. Start your FastAPI server: python fastapi_app.py")
            print("3. Access API docs at: http://localhost:8000/docs")
            return True
        except Exception as e:
            print(f"❌ Error creating seed data: {e}")
            return False
    return False

def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("🏦 Loan Origination System - Database Manager")
        print("=" * 50)
        print("Usage: python db_utils.py <command>")
        print("\nAvailable commands:")
        print("  init     - Initialize database with tables and seed data")
        print("  create   - Create database tables")
        print("  drop     - Drop all database tables")
        print("  reset    - Drop and recreate all tables")
        print("  test     - Test database connection")
        print("  info     - Show database table information")
        print("  seed     - Create seed data only")
        return
    
    command = sys.argv[1].lower()
    
    if command == "init":
        initialize_database()
    elif command == "create":
        create_database()
    elif command == "drop":
        if input("⚠️  Are you sure you want to drop all tables? (yes/no): ").lower() == "yes":
            drop_database()
        else:
            print("Operation cancelled.")
    elif command == "reset":
        if input("⚠️  Are you sure you want to reset the database? (yes/no): ").lower() == "yes":
            reset_database()
        else:
            print("Operation cancelled.")
    elif command == "test":
        check_database_connection()
    elif command == "info":
        show_table_info()
    elif command == "seed":
        create_seed_data()
    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'python db_utils.py' for usage information.")

if __name__ == "__main__":
    main()
