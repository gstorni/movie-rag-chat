# Security Notes

## ⚠️ IMPORTANT: Secrets Management

**NEVER commit sensitive information to Git!**

### What NOT to commit:
- ❌ API keys (OpenAI, TMDB, etc.)
- ❌ Database passwords
- ❌ Private tokens
- ❌ `.env` files

### What IS safe to commit:
- ✅ `.env.example` (template with placeholder values)
- ✅ Code that reads from environment variables
- ✅ Configuration files without hardcoded secrets

## Setup Instructions

1. **Copy the example file:**
   ```bash
   # The .env file lives in the root directory (../../.env)
   # NOT in rag-experiment/
   cd ../..
   cp .env.example .env  # if it doesn't exist
   ```

2. **Add your API keys to `../../.env`:**
   ```bash
   POSTGRES_PASSWORD=your_actual_password
   VITE_OPENAI_API_KEY=your_actual_openai_key
   TMDB_API_KEY=your_actual_tmdb_key
   ```

3. **Verify `.env` is ignored:**
   ```bash
   git status  # should NOT show .env file
   ```

## If You Accidentally Committed Secrets

1. **Rotate the credentials immediately** - assume they are compromised
2. **Remove from Git history** using:
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch path/to/file" \
     --prune-empty --tag-name-filter cat -- --all
   ```
3. **Push the cleaned history:**
   ```bash
   git push origin --force --all
   ```

## Current Status

✅ Fixed: Removed hardcoded PostgreSQL password from `config.py` (Dec 22, 2025)
✅ Verified: `.env` files are in `.gitignore`
✅ Created: `.env.example` template for documentation
