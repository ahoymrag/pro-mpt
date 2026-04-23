# 🔧 Troubleshooting Guide

Got stuck? You're not alone. Here are solutions to common issues.

---

## Installation Issues

### "Command not found: pro-go"

**Problem:** You installed pro-mpt but the commands don't work.

**Solution:**
```bash
# Navigate to pro-mpt directory
cd /home/alexg/Res/pro-mpt

# Run setup to install command wrappers
bash setup.sh

# Verify installation
pro-go --help
```

If it still doesn't work:
```bash
# Check if ~/.local/bin is in your PATH
echo $PATH | grep ".local/bin"

# If not, add it to your shell config
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## Database Issues

### "Database is locked"

**Problem:** You see `database is locked` error.

**Solution:**
```bash
# Make sure no other pro-mpt instance is running
ps aux | grep pro-mpt

# Try again (usually resolves itself)
pro-go
```

If persistent:
```bash
# Backup your database
pro-export backup

# Delete the lock file (if it exists)
rm ~/.pro-mpt/prompts.db-wal
rm ~/.pro-mpt/prompts.db-shm

# Try again
pro-go
```

### "No database found" / Empty database

**Problem:** Pro-mpt says there's no database or it's empty.

**Solution:**
```bash
# Check if ~/.pro-mpt directory exists
ls -la ~/.pro-mpt/

# If it doesn't exist, create it
mkdir -p ~/.pro-mpt

# Run pro-go to create the database
pro-go

# Log your first prompt
# Then you should see data
```

---

## API Key Issues

### "ANTHROPIC_API_KEY not set"

**Problem:** Pro-chat, pro-improve, or agent features fail with this error.

**Solution:**

1. **Get your API key:**
   - Go to https://console.anthropic.com/account/keys
   - Click "Create Key"
   - Copy the key (looks like `sk-...`)

2. **Set it in your environment:**
   ```bash
   export ANTHROPIC_API_KEY="sk-your-actual-key"
   ```

3. **Make it permanent:**
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   echo 'export ANTHROPIC_API_KEY="sk-your-actual-key"' >> ~/.bashrc
   source ~/.bashrc
   ```

4. **Verify it works:**
   ```bash
   pro-chat    # Should start without API key error
   ```

---

## Data Issues

### "My prompts disappeared!"

**Don't panic!** Your data isn't lost. SQLite databases are very stable.

**Possible causes:**
1. You're looking at a different database file
2. You filtered the view and forgot about it

**Solutions:**
```bash
# Check the database file exists
ls -lh ~/.pro-mpt/prompts.db

# Make sure you're in interactive mode, not filtered
pro-go
> recent    # Shows all recent, no filter

# Check if you filtered by domain
> domain    # Shows all domains
> recent    # Shows all again

# As a last resort, check backups
pro-export backup  # Look in ./backups/ folder
```

### "I accidentally deleted/modified data"

**Solution:**
```bash
# Restore from backup if you have one
cp backups/prompts_backup_2024-04-23_19-30-45.db ~/.pro-mpt/prompts.db

# If no backup exists, unfortunately the data can't be recovered
# But you can start fresh:
pro-go
```

---

## Performance Issues

### "Pro-mpt is slow / commands are laggy"

**Problem:** Interactive mode feels sluggish or commands take forever.

**Solution:**
```bash
# Check database file size
ls -lh ~/.pro-mpt/prompts.db

# If it's very large (>100MB), optimize it
sqlite3 ~/.pro-mpt/prompts.db "VACUUM;"

# Or create a fresh database and export old prompts
pro-export json > old_prompts.json
rm ~/.pro-mpt/prompts.db
pro-go
```

### "Dashboard updates are slow"

**Solution:**
```bash
# The dashboard queries the database frequently
# Large databases can be slow

# Option 1: Optimize database
sqlite3 ~/.pro-mpt/prompts.db "VACUUM;"

# Option 2: Archive old prompts
pro-export json --min-rating 4 > high_rated.json
pro-export backup
rm ~/.pro-mpt/prompts.db
```

---

## Display Issues

### "Text is cut off / weird characters appearing"

**Problem:** Terminal display looks broken.

**Solution:**
```bash
# Clear and restart
clear
pro-go

# If still broken, your terminal might not support colors
# Try disabling colors
export TERM=xterm
pro-go
```

### "Colors look wrong"

**Solution:**
```bash
# Check terminal type
echo $TERM

# Try a different terminal:
# - iTerm2 (Mac)
# - Windows Terminal
# - GNOME Terminal
# - Konsole (KDE)

# Or export with plain text
pro-export json > data.json
cat data.json
```

---

## Feature-Specific Issues

### "pro-chat doesn't work"

**Problem:** Chat feature fails or hangs.

**Solution:**
```bash
# Make sure API key is set
echo $ANTHROPIC_API_KEY

# If empty, set it:
export ANTHROPIC_API_KEY="sk-..."

# Check internet connection
ping api.anthropic.com

# Try again
pro-chat
```

### "pro-improve doesn't suggest anything"

**Problem:** Improvement suggestions are empty.

**Solution:**
```bash
# Make sure code files exist in pro-mpt directory
ls *.py

# Check API key is set
echo $ANTHROPIC_API_KEY

# Try manually:
pro-improve

# If nothing appears, the AI might be failing silently
# Check if API usage is maxed out:
# https://console.anthropic.com/account/usage
```

### "pro-export says 'No prompts found'"

**Problem:** Export finds zero prompts even though you know you logged some.

**Solution:**
```bash
# Make sure you logged prompts
pro-go
> recent

# If recent shows data but export doesn't, there's a filter
pro-export json                  # No filters
pro-export json --min-rating 1   # Allow all ratings
pro-export json --domain general # Check the default domain
```

---

## Getting Help

### If the above doesn't fix it:

1. **Gather diagnostic info:**
   ```bash
   # Database info
   ls -lh ~/.pro-mpt/prompts.db
   sqlite3 ~/.pro-mpt/prompts.db "SELECT COUNT(*) FROM prompts;"
   
   # System info
   python --version
   echo $SHELL
   ```

2. **File a GitHub issue:** https://github.com/ahoymrag/pro-mpt/issues
   - Describe what you did
   - Include the error message
   - Include your OS and Python version

3. **Check existing issues** for similar problems

---

## Advanced Recovery

### Nuclear Option: Complete Fresh Start

⚠️ **WARNING: This deletes all local data. Restore from backup first!**

```bash
# 1. Backup everything
pro-export json > all_prompts.json
pro-export backup

# 2. Delete everything
rm -rf ~/.pro-mpt
rm -rf ~/.config/pro-mpt  # if it exists

# 3. Start fresh
pro-go

# 4. Data is clean now
```

---

## Prevention Tips

✅ **Back up regularly:**
```bash
# Monthly
pro-export backup

# Copy backups to cloud/external drive
cp backups/*.db ~/Dropbox/  # or Google Drive, etc
```

✅ **Export high-value data:**
```bash
# Keep exported copies of important prompts
pro-export json --min-rating 4 > my_best_work.json
```

✅ **Use version control for backups:**
```bash
git add ~/.pro-mpt/prompts.db
git commit -m "Monthly backup"
```

---

Still stuck? We're here to help! Open an issue or reach out. 🤝
