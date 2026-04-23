# ⚡ Pro-MPT Quick Reference

## Start Here
```bash
pro-go              # Interactive mode - recommended for new users
pro-log "prompt"    # Quick log from command line
```

## Main Commands
```bash
pro-go              # Interactive mode with all features
pro-log             # Quick command-line logging
pro-search          # Find prompts by keyword
pro-dashboard       # Live metrics dashboard
pro-chat            # Chat with Claude about features
pro-improve         # AI improvement suggestions
pro-export          # Export your archive
```

## In Interactive Mode (pro-go)
```
log "your prompt"       → Log a new prompt
search TERM            → Find prompts
recent                 → Show last 10 prompts
stats                  → View your statistics
domain DOMAIN          → Filter by domain
model MODEL            → Filter by model
help                   → Show all commands
exit                   → Leave interactive mode
```

## Export Commands
```bash
pro-export json                    # All prompts as JSON
pro-export json -r 4               # Only 4-5 star prompts
pro-export csv --domain coding     # CSV by domain
pro-export backup                  # Full database backup
pro-export stats                   # Statistics as JSON
```

## Search Filters
```bash
pro-search "keyword"               # Search by text
pro-search --domain coding         # Filter by domain
pro-search --model claude          # Filter by model
pro-search --min-rating 4          # Only high-rated
```

## Ratings Guide
```
1⭐ = Meh, not helpful
2⭐ = Somewhat helpful
3⭐ = Good, solved it
4⭐ = Great, perfect mostly
5⭐ = Chef's kiss, exactly right
```

## Common Domains
- `coding` - Programming
- `frontend` / `backend` - Web development
- `devops` - Infrastructure
- `creative` - Writing, design, art
- `research` - Learning
- `cooking` - Recipes (your use case!)
- `career` - Job & growth

## Database Location
```
~/.pro-mpt/prompts.db     # Your local database
```

## Backup Your Data
```bash
pro-export backup              # Automated backup
cp ~/.pro-mpt/prompts.db ~backup  # Manual copy
```

## Troubleshooting
```bash
# Command not found?
bash setup.sh                  # Reinstall command wrappers

# API key needed?
export ANTHROPIC_API_KEY="sk-..."

# Reset everything?
rm ~/.pro-mpt/prompts.db      # Delete database
pro-go                         # Start fresh
```

## Pro Tips
1. **Consistency** - Log prompts as you ask them (30 sec each)
2. **Review** - Check `pro-dashboard` weekly
3. **Export** - Back up your data monthly
4. **Share** - Export high-rated prompts as portfolio
5. **Reflect** - Use `pro-go stats` to see patterns

---

For full details, see USAGE.md or run `pro-go` and type `help`
