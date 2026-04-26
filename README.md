# pro-mpt

**Your personal prompt archive, expertise tracker, and thinking partner.**

Track what you ask different AI models, learn from your patterns, and build a searchable library of your thinking journey.

```bash
# Log a prompt with context
$ pro-mpt log "How do I fix this UI bug?" --model claude --app myapp --domain dev --rating 5

# Search your entire history
$ pro-mpt search "UI" --app myapp --model claude

# See your expertise grow
$ pro-mpt expertise --domain dev

# Dashboard view
$ pro-mpt stats
```

---

## Why pro-mpt?

You ask AI systems hundreds of questions. But those conversations disappear.

**pro-mpt** turns them into your personal knowledge archive:
- **Find solutions you've already discovered** - "I've solved this before, what was my approach?"
- **See your growth** - Watch yourself go from asking basics to teaching others
- **Understand what works** - Which models give you the best results for different problems?
- **Version your app evolution** - Track how your prompts evolved alongside your code
- **Build your portfolio** - Prove your expertise through your actual learning journey

Works for:
- **App development** - Track prompts while building (debugging, architecture, optimization)
- **Cooking** - Save recipes and techniques you discover
- **Writing** - Keep all your creative iterations
- **Learning anything** - Document your expertise journey

---

## Features

### 📝 Archive Everything
Log any prompt with rich metadata:
```bash
pro-mpt log "query text" \
  --model claude \              # or gpt4, gemini, etc
  --app myapp \                 # optional: which project
  --domain dev \                # optional: category
  --version 1.0.2 \             # optional: app version
  --rating 5                    # optional: how well it worked
```

### 🔍 Powerful Search
Find prompts across your entire history:
```bash
pro-mpt search "authentication"           # Search by text
pro-mpt search "state" --app myapp        # Filter by app
pro-mpt search "bug" --model claude       # Filter by model
pro-mpt search "cooking" --domain cooking # Filter by domain
pro-mpt search "auth" --min-rating 4      # Show only good solutions
```

### 📊 Beautiful Dashboard
```bash
pro-mpt stats          # Quick overview
pro-mpt list --recent 20    # See recent prompts
pro-mpt morning        # Daily greeting + summary
```

### 📈 Expertise Analysis
Track your journey in any domain:
```bash
pro-mpt expertise --domain dev           # Your dev expertise
pro-mpt expertise --app myapp            # All prompts for myapp
```

See:
- Total prompts asked
- Models used
- Average rating
- Your best moments
- Growth trajectory

### 🔗 Auto-Import Claude Code Sessions
Your conversations are automatically imported from Claude Code:
```bash
python import_claude_sessions.py    # Scan and import all new sessions
```
Automatically tracks which sessions are imported to avoid duplication.

### 📄 Export to Markdown
Create beautiful markdown journals of your expertise:
```bash
pro-mpt export markdown --domain dev --output my-dev-journey.md
pro-mpt export markdown --model claude --min-rating 4
```

### 💾 Own Your Data
- **Local-first** - Everything stays on your machine
- **Portable** - Export anytime (JSON, CSV, Markdown)
- **Auto-archiving** - Claude Code sessions imported automatically
- **No lock-in** - Leave whenever you want

---

## Quick Start

### Prerequisites
- Python 3.10+
- pip

### Install

```bash
# Clone the repo
git clone https://github.com/yourusername/pro-mpt.git
cd pro-mpt

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install (in dev mode)
pip install -e .
```

### First Steps

```bash
# See all commands
pro-mpt --help

# Your first log
pro-mpt log "What's a good pattern for state management?" --model claude --domain dev

# See what you logged
pro-mpt list

# Search your archive
pro-mpt search "state"

# View stats
pro-mpt stats
```

---

## Use Cases

### 🖥️ App Developer
Track prompts while building your app:
```bash
# During development
pro-mpt log "How to handle async/await?" --app myapp --domain dev --model claude
pro-mpt log "Best pattern for error handling?" --app myapp --model gpt4

# Later, see what worked
pro-mpt expertise --app myapp --domain dev
# → Shows which models gave best answers for your app

# Version your evolution
pro-mpt log "..." --app myapp --version 1.0.0
pro-mpt log "..." --app myapp --version 1.1.0
# → Track how your questions evolved with your app
```

### 👨‍🍳 Cook & Food Enthusiast
```bash
pro-mpt log "Perfect temp for steak?" --domain cooking --model gpt4 --rating 5
pro-mpt log "Best wine pairing for salmon?" --domain cooking --model claude

pro-mpt expertise --domain cooking
# → See your culinary journey
```

### 📚 Learner
```bash
# As you learn a new topic
pro-mpt log "How does X work?" --domain machine-learning
pro-mpt log "Follow-up on Y..." --domain machine-learning

# Review your journey
pro-mpt expertise --domain machine-learning
# → Watch yourself level up
```

### 🏢 Enterprise Team (Coming Soon)
- Shared playbooks of proven solutions
- Team expertise profiles
- Compliance audit trails
- Cost optimization insights

---

## Data Structure

Everything lives in `~/.pro-mpt/prompts.db` (local SQLite):

```
prompts table:
├── id (unique identifier)
├── query (what you asked)
├── model (which AI model)
├── agent (which service)
├── app (which project)
├── domain (category)
├── version (app version)
├── response (what it answered)
├── timestamp (when)
├── rating (how well it worked, 1-5)
└── notes (your thoughts)
```

---

## Commands Reference

| Command | Purpose |
|---------|---------|
| `pro-mpt log <query>` | Save a prompt |
| `pro-mpt search <term>` | Find prompts |
| `pro-mpt list` | Show recent prompts |
| `pro-mpt expertise` | See your journey |
| `pro-mpt stats` | Dashboard |
| `pro-mpt morning` | Daily greeting |
| `pro-mpt export` | Backup your data |

See all options: `pro-mpt --help`

---

## Advanced Usage

### Watch Your Growth Over Time
```bash
# Track a specific skill
pro-mpt expertise --domain async-programming
# See: started confused → now you explain it to others
```

### Model Comparison
```bash
# See which models work best for you
pro-mpt search "state management"
# Shows: Claude 4.5 (★★★★★), GPT-4 (★★★★), Sonnet (★★★)
```

### Version Tracking
```bash
# See how your app evolved
pro-mpt list --app myapp
# Shows: v0.1.0 prompts vs v1.0.0 prompts
# How did your questions change?
```

### Export & Backup
```bash
# Backup as JSON
pro-mpt export --format json

# Share your expertise portfolio
pro-mpt export --domain dev --format json > my-dev-expertise.json
```

---

## Roadmap

### Phase 1: Foundation ✓
- [x] Local archiving
- [x] Search & filtering
- [x] Expertise analysis
- [x] Beautiful CLI

### Phase 2: Integrations (Building)
- [ ] GitHub integration (see commits alongside prompts)
- [ ] Browser extension (auto-capture from ChatGPT, Claude, etc.)
- [ ] Slack integration
- [ ] Calendar context

### Phase 3: Agents & Intelligence
- [ ] Personal agent (learns your patterns)
- [ ] Smart suggestions (auto-detect repeating questions)
- [ ] Vibe.md (emotional growth tracking)
- [ ] Pattern recognition

### Phase 4: Scale
- [ ] Cloud sync (optional, encrypted)
- [ ] Team collaboration
- [ ] Web dashboard
- [ ] API for integrations
- [ ] Enterprise features

---

## Architecture

```
pro-mpt/
├── pro_mpt.py              # Main CLI (200 lines for MVP)
├── ~/.pro-mpt/
│   └── prompts.db          # Your local database
├── venv/                   # Python environment
└── docs/
    ├── README.md           # This file
    ├── MANIFESTO.md        # Why this exists
    ├── BUILD.md            # How to develop
    └── RELEASE.md          # How to ship
```

**Future:**
```
development/                # Black box system
├── core/                  # Graph engine
├── connectors/            # Data sources
├── search/                # Search engine
├── expertise/             # Analysis
└── ai/                    # LLM integration
```

---

## Development

Want to contribute? See [BUILD.md](BUILD.md) for development setup.

Want to understand the vision? See [MANIFESTO.md](MANIFESTO.md).

---

## Privacy

Your data belongs to you:
- **Local-first** - Everything runs on your machine
- **No tracking** - We don't see your prompts
- **No ads** - No business model dependent on your data
- **Encrypted backups** - Optional cloud sync is end-to-end encrypted
- **Export anytime** - Your data in JSON format

---

## Pricing

### Now
Free. Always.

### Later (When scaled)
- **Free tier** - Personal use, 100 prompts/month
- **Pro** ($10/mo) - Unlimited, integrations, cloud sync
- **Team** ($50/mo) - Team features, shared playbooks
- **Enterprise** - Custom pricing, compliance features

---

## FAQ

**Q: Does pro-mpt see my prompts?**
A: No. Everything is local. We only see aggregate stats if you opt-in.

**Q: Can I export my data?**
A: Yes. `pro-mpt export` gives you JSON. You own your data.

**Q: What if I stop using pro-mpt?**
A: Your database stays on your machine. You can export it anytime.

**Q: Can I use this with my team?**
A: Not yet, but team features are coming in Phase 4.

**Q: Will you sell my data?**
A: No. Never. Our business model doesn't depend on it.

---

## Vision

We're building the infrastructure for your thinking.

Every prompt you ask is a signal about how you think. Over time, those signals reveal:
- What you're curious about
- Where you're getting stuck
- When you're growing
- What you're really good at

**pro-mpt** makes that visible.

Then, when you're ready, it becomes your competitive advantage:
- Prove your expertise (to employers, clients, yourself)
- Learn faster (by remembering what worked)
- Make better decisions (because you have precedent)
- Teach others (by sharing your journey)

---

## Get Involved

- **Questions?** Open an issue
- **Ideas?** Discussions are open
- **Contributing?** See [BUILD.md](BUILD.md)
- **Bugs?** Report with `pro-mpt export` output

---

## License

MIT - Use it however you want.

---

## Made with ❤️

Built for people who think deeply and want to remember their journey.

```
"Your prompts are the record of how you think.
 Watch yourself get smarter."
                              — pro-mpt
```
