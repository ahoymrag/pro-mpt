# RECORDING.md - How to Use pro-mpt with Claude Code

Quick guide to automatically record your Claude Code sessions.

---

## 🎬 Start Recording Session

### Option A: Quick Start (Recommended)

```bash
# From pro-mpt directory
./start-with-recording.sh
```

This will:
1. ✓ Activate the pro-mpt environment
2. ✓ Show you how to log prompts
3. ✓ Launch Claude Code
4. ✓ Show session summary when done

---

## 📝 Log Prompts While Using Claude Code

While you're in your Claude Code session, open another terminal:

### Quick Log
```bash
# Activate if needed
source venv/bin/activate

# Log a prompt you just asked Claude
pro-mpt log "How do I handle state in React?" \
  --model claude \
  --app myapp \
  --domain dev \
  --rating 5
```

### Even Faster (with alias)

Add to your `.bashrc` or `.zshrc`:
```bash
alias pm='source /path/to/pro-mpt/venv/bin/activate && python /path/to/pro-mpt/pro_mpt.py'
```

Then anywhere:
```bash
pm log "your prompt" --model claude --rating 5
pm search "state"
pm stats
```

---

## 🔍 View Recorded Prompts

### During Session
```bash
# Search what you've asked
pro-mpt search "state management" --app myapp

# See your stats
pro-mpt stats

# See recent prompts
pro-mpt list --recent 10
```

### After Session
```bash
# See what you accomplished
pro-mpt morning

# Analyze your journey
pro-mpt expertise --domain dev

# Export everything
pro-mpt export --format json
```

---

## 🎯 Recording Workflow

### Typical Session

```
1. Start session:
   $ ./start-with-recording.sh
   
2. Use Claude Code (in same window or another tab)
   
3. When you ask Claude something important:
   - Keep note of it mentally
   - Or copy the prompt to a text file
   
4. After Claude responds:
   $ pm log "your prompt" --model claude --rating 5
   (takes 3 seconds)
   
5. Later, search your history:
   $ pm search "that thing I asked about"
   
6. End session:
   - Exit Claude Code
   - See session summary
   - Review: $ pm morning
```

---

## 💡 Pro Tips

### Log Immediately
Log prompts right after asking them (while fresh). Takes 10 seconds.

```bash
pm log "What's the best pattern for X?" --model claude --rating 5
```

### Rate Everything
Use --rating to mark what worked:
- 5 = Exactly what I needed
- 4 = Good, with minor issues
- 3 = Okay, needed follow-ups
- 2 = Somewhat helpful
- 1 = Not helpful

```bash
pm log "..." --rating 5    # Great answer
pm log "..." --rating 3    # Needed work
```

### Tag Your Work
Use --app and --domain to organize:
```bash
pm log "..." --app myapp --domain dev       # Work
pm log "..." --domain cooking               # Personal
pm log "..." --app portfolio --domain design # Side project
```

### Review Daily
```bash
# Every morning
pro-mpt morning

# Gives you:
# - What you asked yesterday
# - What worked well
# - Your growth trends
# - Suggestions for today
```

---

## 🔄 Integration with IDE

### VS Code

Add to `.vscode/settings.json`:
```json
{
  "terminal.integrated.shellArgs.osx": ["-i", "-l"],
  "terminal.integrated.env.osx": {
    "PROMPT_TRACKING": "true"
  }
}
```

Then in VS Code terminal:
```bash
pm log "How do I fix this type error?" --model claude --rating 4
```

### Other IDEs

Any IDE with a terminal can run:
```bash
source venv/bin/activate
pro-mpt log "your prompt" --model claude
```

---

## 📊 Viewing Your Archive

### By App
```bash
pro-mpt list --app myapp
pro-mpt expertise --app myapp
pro-mpt search "ui" --app myapp
```

### By Domain
```bash
pro-mpt expertise --domain dev
pro-mpt search "state" --domain dev
```

### By Model
```bash
pro-mpt search "pattern" --model claude
pro-mpt search "optimization" --model gpt4
```

### By Rating
```bash
pro-mpt search "anything" --min-rating 4  # Only great answers
```

---

## 🚀 Advanced: Auto-Recording

### Option 1: Shell History (Future)
Eventually: Shell integration that auto-captures Claude outputs

### Option 2: Claude Code Hooks (Coming Soon)
We'll add hooks to Claude Code to auto-log prompts

### Option 3: Browser Extension (Coming Soon)
Auto-capture from ChatGPT/Claude web interface

---

## ❓ Common Questions

**Q: Do I have to log every prompt?**
A: No. Only log the important ones. Takes 10 seconds each.

**Q: Can I batch log later?**
A: Yes, but less useful. You'll forget context. Better to log as you go.

**Q: What if I forget to log something?**
A: You can log it anytime. It's better late than never.

**Q: Can I edit a prompt after logging?**
A: Future feature. For now, delete and re-log if needed.

**Q: How do I see my growth?**
A: Use `pro-mpt expertise --domain X`. Shows your journey.

**Q: Can I share my recorded prompts?**
A: Yes. `pro-mpt export --format json` gives you a shareable file.

---

## 🎬 Recording Script (Quick Version)

Create `log.sh` in your pro-mpt directory:

```bash
#!/bin/bash
# Quick prompt logger

source venv/bin/activate 2>/dev/null || true

python pro_mpt.py log "$@"
```

Then:
```bash
chmod +x log.sh

# Use it anywhere:
./log.sh "your prompt" --model claude --rating 5

# Or with alias
alias log='/path/to/pro-mpt/log.sh'
log "prompt here" --model claude
```

---

## 📈 Viewing Reports

### Weekly Summary
```bash
# What did you build this week?
pro-mpt list --recent 50
```

### Growth Over Time
```bash
# How are you improving?
pro-mpt expertise --domain dev
# Shows: started at 45% confidence, now 85%
```

### Model Comparison
```bash
# Which model works best for you?
pro-mpt search "state" --model claude  # Results
pro-mpt search "state" --model gpt4    # Results
# Compare quality and rating
```

---

## Next: Automate More

Once you're comfortable logging manually, we'll add:
- [ ] Browser extension (auto-capture from ChatGPT/Claude)
- [ ] Shell integration (auto-capture claude outputs)
- [ ] Claude Code hooks (auto-log integration)

For now, manual logging takes 10 seconds and gives you full control.

---

**Start with `./start-with-recording.sh`, then use `pm log` while coding.**
