# Pro-MPT Commands Reference

All commands work from anywhere after setup. Just type the command name!

## Installation (One-time)

```bash
cd /home/alexg/Res/pro-mpt
bash setup.sh
source ~/.bashrc  # or ~/.zshrc
```

---

## Commands

### 💬 **pro-chat** - Talk to Claude (NEW!)
Chat with Claude about pro-mpt. Ask questions, get suggestions, improve features:

```bash
pro-chat
```

Inside the chat:
```
You: I want to add real-time collaboration
Claude: Great idea! Let me ask a few questions...
  - How many users per session?
  - Self-hosted or cloud?
  - What data should sync?

You: For now just 2-3 people, self-hosted
Claude: Perfect. Here's what I'd suggest...
```

**Requires**: Set `ANTHROPIC_API_KEY` environment variable

```bash
export ANTHROPIC_API_KEY='sk-...'
pro-chat
```

---

### 📊 **pro-dashboard** - Terminal Dashboard (NEW!)
Real-time overlay dashboard like `btop`:

```bash
pro-dashboard
```

Shows:
- 📈 Expertise by domain (progress bars 0-100%)
- 🤖 Model usage breakdown
- ⭐ Rating distribution
- 📅 Last 7 days activity
- Overall stats

Updates live. Press `Ctrl+C` to exit.

---

### 🚀 **pro-go** - Interactive Mode
Start the interactive prompt archive:

```bash
pro-go
```

Inside you can type:
- `log "question" --model claude --rating 5`
- `search "topic"`
- `list`, `stats`, `morning`, `expertise`
- `export --format json`
- `help`, `exit`

---

### 🌱 **pro-grow** - Automated Growth Routine
Daily growth routine with insights:

```bash
pro-grow
```

Shows:
- ✅ Morning summary (recent prompts, stats)
- 📊 Growth stats (total, average rating, models used)
- 📈 Expertise by domain
- 💡 Auto-generated insights & suggestions

**Suggested**: Run every morning with `pro-grow`

---

### 📝 **pro-log** - Quick Logging
Log a prompt without entering interactive mode:

```bash
pro-log "How do I handle state?" --model claude --rating 5
pro-log "Test question" --app myapp --domain dev --rating 4
```

Flags:
- `--model` - Which model (claude, gpt4, etc)
- `--rating` - Rate 1-5 (5=perfect, 1=unhelpful)
- `--app` - Which app/project
- `--domain` - Topic (dev, cooking, design, etc)

---

### 🎙️ **pro-record** - Recording Session
Start a recording session with Claude Code:

```bash
pro-record
```

Then in another terminal, log prompts as you go:
```bash
pro-log "code question" --rating 5
```

---

### 📋 **pro-review** - Morning Summary
Quick morning summary with recent prompts:

```bash
pro-review
```

Shows your progress from yesterday + recent work.

---

### 🔍 **pro-search** - Quick Search
Search your archive without interactive mode:

```bash
pro-search "state management"
pro-search "react" --app myapp
pro-search "tips" --domain cooking
```

---

### 💾 **pro-export** - Export Data
Export your entire archive:

```bash
pro-export --format json   # Creates pro-mpt-export-TIMESTAMP.json
pro-export --format csv    # Creates pro-mpt-export-TIMESTAMP.csv
```

---

## Usage Patterns

### Daily Workflow

```bash
# Start your day
pro-grow

# Log prompts as you work
pro-log "Question for Claude" --rating 5

# Search old prompts
pro-search "solution I found before"

# End day: interactive review
pro-go
> morning
> expertise --domain dev
> exit
```

### Weekly Review

```bash
# Full growth analysis
pro-grow

# Export for backup
pro-export --format json
```

### Quick Logging (During Coding)

```bash
# While coding, keep a terminal for quick logs
pro-log "Fix this bug" --app myapp --domain dev --rating 4
pro-log "Design question" --domain design --rating 3
pro-log "Best practice found!" --rating 5
```

---

## Examples

### Log with all metadata
```bash
pro-log "How do I handle async/await in Python?" \
  --model claude \
  --app data-pipeline \
  --domain backend \
  --rating 5
```

### Search by domain
```bash
pro-search "best practices" --domain dev
```

### Find what worked well
```bash
pro-search "solution" --app myapp --rating 5  # Only great answers
```

### Interactive session
```bash
pro-go
> log "test" --rating 5
> search "python"
> stats
> export --format json
> exit
```

---

## Data Storage

All data is stored locally in:
```
~/.pro-mpt/prompts.db  (SQLite database)
```

You own your data. Export anytime:
```bash
pro-export --format json  # Portable format
```

---

## Workflow Tips

1. **Log immediately** - Best right after asking Claude
2. **Always rate** - Helps track what worked
3. **Use domains** - dev, cooking, design, writing, etc
4. **Run pro-grow daily** - See patterns & get insights
5. **Search before asking** - Save time finding past solutions
6. **Export weekly** - Backup your archive

---

## Coming Soon (Phase 2)

- Auto-sync to cloud
- Browser extension (auto-capture)
- Team collaboration
- Advanced analytics
- Custom insights

For now: **Pro-MPT is your personal archive, 100% private, fully portable.**
