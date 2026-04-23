# 📖 Pro-MPT Usage Guide

Welcome! Pro-mpt makes it easy to track your prompts, understand your growth, and celebrate your learning journey.

---

## 🚀 Quick Start (2 minutes)

### 1. **Start Interactive Mode**
```bash
pro-go
```
You'll see a friendly prompt:
```
🚀 Ready to log? Type your prompt (or 'help')
```

### 2. **Log Your First Prompt**
```
> "How do I optimize a React component?"
```

Pro-mpt saves it with:
- ✅ The exact prompt you asked
- 🤖 Which model you're using (Claude, GPT, etc.)
- ⭐ Your rating (1-5 stars)
- 🏷️ Domain (coding, creative, analysis, etc.)

### 3. **Rate It**
```
Rating (1-5 stars)? 4
```
- 1⭐ = "Meh, wasn't helpful"
- 5⭐ = "Chef's kiss, perfect!"

### 4. **See Your Stats**
```
> stats
```
Boom! You see:
- 📊 Total prompts logged
- 🔝 Your favorite domains
- 🤖 Models you use most
- 📈 Your growth over time

---

## 🎯 All Commands

### **pro-go** (Interactive Mode)
The main experience. Ask questions, log prompts, see stats, all in one place.

```bash
pro-go

🚀 Ready to log? Type your prompt (or 'help')
> "How to structure a Python project?"

⭐ Rating (1-5)? 5
🏷️  Domain (coding, creative, analysis)? coding
💾 Saved! You've logged 42 prompts. Keep going!

> search Python
📚 Found 5 prompts about Python...
```

Commands in interactive mode:
- `log "your prompt"` - Save a prompt
- `search TERM` - Find prompts
- `stats` - View your statistics
- `recent` - See your last 10 prompts
- `domain` - See prompts by domain
- `help` - Show all commands
- `exit` - Leave interactive mode

### **pro-log** (Quick Log)
Save a prompt without entering interactive mode.

```bash
pro-log "How to deploy to AWS?"
```

### **pro-search** (Search)
Find prompts by keyword or domain.

```bash
# Search by keyword
pro-search "database optimization"

# Search by domain
pro-search --domain coding

# Search by model
pro-search --model claude

# Find highly-rated prompts
pro-search --min-rating 4
```

### **pro-dashboard** (Live Dashboard)
See your growth metrics in real-time:
- 📊 Domain expertise (progress bars)
- 🤖 Model breakdown (which AI you use most)
- ⭐ Rating distribution (are you getting better?)
- 📈 Daily activity (last 7 days)

```bash
pro-dashboard
# Updates live every 2 seconds
```

### **pro-chat** (Chat with Claude)
Discuss pro-mpt design and improvements:

```bash
pro-chat
# Have a conversation about features, architecture, improvements
```

### **pro-improve** (Suggestions)
Get AI-powered improvement suggestions:

```bash
pro-improve
# Claude analyzes your codebase and suggests next steps
```

---

## 💡 Real-World Workflows

### Workflow 1: Daily Logging
```bash
# Morning: Reflect on what you want to ask today
pro-go

> log "Best way to handle errors in async JavaScript?"
⭐ 4
🏷️ frontend

> log "How to structure large-scale data pipelines?"
⭐ 5
🏷️ backend

> stats
# See your expertise growing

> exit
```

### Workflow 2: Weekly Review
```bash
# End of week: Review your learning
pro-go

> recent
# See your last 20 prompts

> domain coding
# Focus on just coding prompts

> search "interesting challenge"
# Find specific topics you tackled

> stats
# Celebrate your growth!
```

### Workflow 3: Portfolio Building
```bash
# Building a portfolio? Export your prompts
pro-go

> export --format json
# Get all your prompts in JSON (great for portfolios)

> export --min-rating 4
# Only export your best prompts
```

---

## 🏷️ Organizing with Domains

Domains help you understand your expertise areas. Some examples:

**Technical Domains:**
- `coding` - Programming and software
- `backend` - Server-side development
- `frontend` - Web/UI development
- `databases` - Data persistence
- `devops` - Infrastructure and deployment
- `machine-learning` - AI and ML work

**Creative Domains:**
- `creative` - Art, writing, design
- `brainstorm` - Ideas and planning
- `marketing` - Business and growth

**Learning Domains:**
- `research` - Learning new topics
- `debugging` - Problem-solving
- `documentation` - Writing and explaining

**Personal Domains:**
- `career` - Job and skill development
- `cooking` - Your app use case!
- `general` - Everything else

Make up your own! Use domains that make sense for your work.

---

## ⭐ Understanding Ratings

Your ratings help you identify patterns:

| Rating | Meaning | Example |
|--------|---------|---------|
| ⭐ (1) | Not helpful | "Claude misunderstood what I asked" |
| ⭐⭐ (2) | Somewhat helpful | "Got a partial answer, had to iterate" |
| ⭐⭐⭐ (3) | Good | "Solved the problem, needed minor tweaks" |
| ⭐⭐⭐⭐ (4) | Great | "Perfect response, saved me hours" |
| ⭐⭐⭐⭐⭐ (5) | Perfect | "Exactly what I needed, no changes" |

Pro-mpt uses your ratings to show:
- Your average success rate
- Which models work best for you
- Which domains you're strongest in

---

## 🎯 Advanced Tips

### Tip 1: Use Models Parameter
Track which AI model you're using:

```bash
> log "Optimize my code" --model claude-opus --app vscode

# Now you can see which models help you most!
> search --model claude-opus
```

### Tip 2: Add Notes for Context
```bash
pro-log "How to learn Rust?"
# You can add notes/responses in interactive mode

> notes "Found great learning resource: https://..."
```

### Tip 3: Track Your Growth
```bash
# Check your expertise dashboard
pro-dashboard

# See which domains are your strength
> stats

# Review high-rated prompts to see patterns
> search --min-rating 4
```

### Tip 4: Regular Reflection
Pro-mpt works best when you use it consistently:
- Log prompts as you ask them (takes 30 seconds)
- Review your stats weekly (see your growth!)
- Refine your domains (organize better over time)

---

## ❓ FAQ

**Q: Where is my data stored?**
A: Locally on your machine at `~/.pro-mpt/prompts.db`. Your data never leaves your computer.

**Q: Can I export my data?**
A: Yes! Use `pro-export` or `pro-log --export json` to get all your prompts as JSON.

**Q: What if I want to delete a prompt?**
A: You can't accidentally delete (no built-in delete yet), but you can:
- Use the database directly: `sqlite3 ~/.pro-mpt/prompts.db`
- Or ask for the feature in GitHub Issues!

**Q: Can I back up my data?**
A: Yes! Just copy `~/.pro-mpt/prompts.db` to another location. It's a standard SQLite database.

**Q: I'm new to terminal tools. Will this be hard?**
A: Nope! Pro-mpt is designed to be friendly. Just run `pro-go` and follow the prompts. If you get stuck, type `help` in interactive mode.

**Q: Can I use this on Windows/Mac?**
A: Yes! Pro-mpt works on any system with Python and terminal access.

---

## 🚀 Troubleshooting

### "Command not found: pro-go"
Make sure pro-mpt is installed:
```bash
cd /home/alexg/Res/pro-mpt
python setup.py install
# or
bash setup.sh
```

### "Can't connect to database"
Make sure the `.pro-mpt` directory exists:
```bash
mkdir -p ~/.pro-mpt
```

### "ANTHROPIC_API_KEY not set"
Some features (auto-improve, pro-chat) need an API key:
```bash
export ANTHROPIC_API_KEY="sk-..."
```

---

## 🎉 You're Ready!

Start with `pro-go` and explore. Pro-mpt is designed to feel natural and encourage curiosity.

Questions? Check the main README or file an issue on GitHub!

**Happy prompting!** 🚀
