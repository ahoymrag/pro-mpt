# Changelog

All notable changes to pro-mpt are documented here. This file auto-updates with each release.

Format: `[VERSION] - YYYY-MM-DD`
- Features: New capabilities
- Improvements: Better or faster existing features
- Fixes: Bug fixes
- Breaking: Changes that affect existing usage

---

## [Unreleased]

### Features
- [ ] Auto-capture from browser (ChatGPT, Claude, Gemini)
- [ ] GitHub integration (commits, PRs, issues)
- [ ] Slack integration (log from Slack)
- [ ] Calendar context (meetings, decisions)
- [ ] Personal agent (learns your patterns)
- [ ] Vibe.md (emotional growth tracking)
- [ ] Cloud sync (optional, encrypted)
- [ ] Team features (shared playbooks)
- [ ] Web dashboard
- [ ] API for integrations

### In Progress
- [ ] Browser extension UI
- [ ] GitHub connector architecture
- [ ] Agent training pipeline

---

## [0.1.0] - 2026-04-23

### Features
- **Log command** - Archive prompts with metadata (model, app, domain, version, rating)
- **Search command** - Full-text search with filters (app, model, domain, rating)
- **List command** - Browse recent prompts in beautiful table
- **Expertise command** - Analyze your journey in any domain
- **Stats command** - Dashboard view of your archive
- **Morning command** - Daily greeting with summary
- **Export command** - Backup to JSON or CSV
- **Beautiful CLI** - Terminal UI with colors, animations, panels

### Technical
- Local SQLite database
- Python CLI with Typer
- Rich terminal output
- Zero external dependencies (except dev tools)

### Data Structures
- Prompts table with fields: id, query, model, agent, app, domain, version, response, timestamp, rating, notes

---

## What Each Feature Does

### Log
**Save a prompt with context**
```bash
pro-mpt log "How do I handle state?" \
  --model claude \
  --app myapp \
  --domain dev \
  --version 1.0.2 \
  --rating 5
```

**Why**: Captures the moment of learning with all context so you can search later

---

### Search
**Find prompts by text, filter by metadata**
```bash
pro-mpt search "state" --app myapp --model claude --min-rating 4
```

**Why**: You solved this before; remember how

---

### List
**See your recent prompts in a table**
```bash
pro-mpt list --recent 20 --app myapp
```

**Why**: Browse your archive, see patterns at a glance

---

### Expertise
**Analyze your journey in a domain**
```bash
pro-mpt expertise --domain dev
```

**Shows**:
- Total prompts
- Models used
- Average rating
- Your best moments
- Confidence level
- Growth trajectory

**Why**: See how far you've come, identify gaps

---

### Stats
**Dashboard of your entire archive**
```bash
pro-mpt stats
```

**Shows**:
- Total prompts
- Models used
- Apps tracked
- Domains covered
- Average rating
- Today's count

**Why**: Quick overview, high-level insight

---

### Morning
**Daily greeting + summary**
```bash
pro-mpt morning
```

**Shows**:
- Greeting with time-awareness
- Yesterday's prompts
- Stats for the session
- Recent activity

**Why**: Start your day connected to your learning

---

### Export
**Backup everything**
```bash
pro-mpt export --format json
pro-mpt export --format csv --app myapp
```

**Formats**: JSON (full fidelity), CSV (spreadsheet-friendly)

**Why**: Own your data, use it elsewhere

---

## Feature Priority Roadmap

### MVP (Now) ✓
- [x] Log prompts
- [x] Search
- [x] List
- [x] Expertise analysis
- [x] Stats
- [x] Export
- [x] Beautiful CLI

### Phase 1 (Week 2)
- [ ] Browser extension
- [ ] Auto-capture from ChatGPT/Claude
- [ ] Better search ranking
- [ ] Search templates

### Phase 2 (Week 3)
- [ ] GitHub integration
- [ ] Slack integration
- [ ] Personal agent MVP
- [ ] Confidence scoring

### Phase 3 (Week 4)
- [ ] Vibe.md personality tracking
- [ ] Feature auto-detection
- [ ] Cloud sync option
- [ ] Web dashboard

### Phase 4+ (Month 2+)
- [ ] Team features
- [ ] API
- [ ] Enterprise features
- [ ] Mobile app

---

## Delta Changes (Latest First)

### 2026-04-23 - v0.1.0 Released
**What Changed**: Everything (first release)

**Why**: MVP ready for use

**Impact**: You can now use pro-mpt to archive your prompts

**Migration**: None (first release)

**Fixes**: N/A

**Breaking Changes**: None

---

## Feature Impact Analysis

### By Use Case

#### App Developer
- ✅ Log with version tracking (app --version)
- ✅ Search by app
- ✅ Expertise per app
- ⏳ GitHub integration (coming)
- ⏳ Auto-capture from ChatGPT while coding (coming)

#### Chef/Cook
- ✅ Log by domain (--domain cooking)
- ✅ Search by domain
- ✅ Expertise tracking per domain
- ⏳ Integration with recipe tools (future)

#### Learner
- ✅ Archive everything you ask
- ✅ See your journey
- ✅ Expertise analysis
- ⏳ Personal agent tutor (coming)

#### Enterprise
- ⏳ Cloud sync (coming)
- ⏳ Team playbooks (coming)
- ⏳ Audit trails (coming)
- ⏳ Cost optimization (coming)

---

## Dependencies

### Runtime
- Python 3.10+
- sqlite3 (built-in)
- typer (CLI framework)
- rich (beautiful terminal output)

### Development
- pytest (testing)
- black (code formatting)
- ruff (linting)

### Future
- anthropic (for agent features)
- requests (for integrations)
- cryptography (for encrypted cloud sync)

---

## Known Limitations

### Current
- No cloud sync yet (local-only)
- No team features
- No browser extension
- No integrations (GitHub, Slack, etc.)
- No web UI (CLI only)

### By Design
- No AI surveillance (privacy first)
- No forced accounts (optional, future)
- No data selling (never)

---

## Compatibility

### Systems
- ✅ macOS
- ✅ Linux
- ✅ Windows (via WSL or venv)

### Python Versions
- ✅ 3.10
- ✅ 3.11
- ✅ 3.12
- ⏳ 3.13 (testing)

### Databases
- ✅ SQLite (current, all systems)
- ⏳ PostgreSQL (future, for teams)

---

## How to Read This Changelog

**For Users**: Check "Features" to see what's new, "Fixes" for what's better, "Breaking" to see if you need to change anything.

**For Developers**: Check "Technical" to see architecture changes, "Dependencies" for what you need to install.

**For Product Managers**: Check "Feature Priority Roadmap" to see what's coming, "Feature Impact Analysis" to see what users care about.

---

## Suggesting Changes

Found a bug? [Open an issue](https://github.com/yourname/pro-mpt/issues)

Want a feature? [Start a discussion](https://github.com/yourname/pro-mpt/discussions)

Want to help? See [BUILD.md](BUILD.md)

---

## Auto-Update Process

This changelog is maintained with:
- Manual updates on each release
- Automated summary generation from git commits
- Bot that detects new features and flags them

We keep this human-readable and up-to-date.
