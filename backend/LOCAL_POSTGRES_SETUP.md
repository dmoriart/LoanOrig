# Local PostgreSQL Setup Alternative

If you want to use a local PostgreSQL database for development:

## Install PostgreSQL (macOS)
```bash
# Using Homebrew
brew install postgresql
brew services start postgresql

# Create database
createdb loan_origination
```

## Update .env file
```bash
DATABASE_URL=postgresql://postgres@localhost:5432/loan_origination
```

## Initialize database
```bash
python db_utils.py init
```

This will work locally while you resolve the Supabase connection issues.
