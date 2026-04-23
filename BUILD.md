# BUILD.md - Development Guide

How to work on pro-mpt: setup, coding style, testing, and iteration patterns.

## Quick Start

```bash
# Clone
git clone https://github.com/yourname/pro-mpt.git
cd pro-mpt

# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run
python pro_mpt.py --help
python pro_mpt.py morning
python pro_mpt.py log "test prompt" --model claude

# Test
pytest tests/ -v

# Check quality
black pro_mpt.py
ruff check pro_mpt.py
mypy pro_mpt.py
```

---

## Architecture (Today vs Tomorrow)

### Today (MVP)
```
pro-mpt/
├── pro_mpt.py         # Everything (200 lines)
│   ├── CLI commands
│   ├── Database ops
│   └── Output formatting
└── ~/.pro-mpt/
    └── prompts.db     # Your data
```

**Why**: Single file = easy to understand, fast to iterate

### Tomorrow (When Scaling)
```
development/           # Black box system
├── core/              # Graph engine
├── connectors/        # Data sources
├── search/            # Search logic
├── expertise/         # Analysis
└── ai/                # LLM features

pro_mpt/              # User-facing CLI
├── cli.py            # Commands
├── commands/         # Organized
└── ui/               # Output

tests/
├── unit/             # Black box tests
└── integration/      # End-to-end

data/
└── (user's database) # Sacred
```

---

## Development Workflow

### Phase 1: Quick Iteration (Weeks 1-2)

**Goal**: MVP works, you're using it daily

**Constraints**:
- Keep pro_mpt.py < 500 lines
- No external complexity
- User can understand whole thing

**Process**:
1. Add feature to pro_mpt.py
2. Test manually: `python pro_mpt.py <command>`
3. Commit when working
4. Get feedback from daily use

**Example**:
```bash
# Add search filtering
git checkout -b feature/search-by-model
# Edit pro_mpt.py
python pro_mpt.py search "state" --model claude  # Test
# Works? Commit
git add pro_mpt.py
git commit -m "feat: filter search by model"
```

### Phase 2: Architecture (Weeks 2-4)

**Goal**: Split monolith into modules, add tests

**When to do this**:
- pro_mpt.py hits 500 lines
- You want to add agents/intelligence
- Multiple people contributing

**Process**:
```
# Create black box
mkdir development/
touch development/__init__.py
touch development/core.py      # Database
touch development/search.py    # Search logic
touch development/expertise.py # Analysis

# Reorganize
mv pro_mpt.py → pro_mpt/cli.py
Create pro_mpt/commands/
Create pro_mpt/ui/

# Wire together
pro_mpt/cli.py imports development/
Tests import development/
User data stays in ~/.pro-mpt/
```

### Phase 3: Integration (Weeks 4+)

**Goal**: Connect GitHub, Slack, browser

**Architecture**:
```
development/connectors/base.py     # Base class
development/connectors/github.py   # GitHub impl
development/connectors/slack.py    # Slack impl
development/connectors/browser.py  # Browser ext impl
```

---

## Code Style

### Python
```python
# Use type hints
def search(query: str, model: Optional[str] = None) -> List[Prompt]:
    """Search prompts with optional filtering"""
    pass

# Format with Black
black pro_mpt.py

# Lint with Ruff
ruff check pro_mpt.py --fix

# Type check with Mypy
mypy pro_mpt.py
```

### Naming
- Functions: `verb_noun()` - `search_prompts()`, `log_prompt()`
- Classes: `PascalCase` - `PromptArchive`, `SearchEngine`
- Constants: `SCREAMING_SNAKE` - `DB_PATH`, `MAX_RESULTS`
- Private: `_private_function()` - `_init_db()`

### Docstrings
```python
def log_prompt(query: str, model: str) -> str:
    """Save a prompt to the archive.
    
    Args:
        query: The prompt text to save
        model: Which model (claude, gpt4, etc)
        
    Returns:
        The prompt ID
        
    Example:
        >>> log_prompt("Hello", "claude")
        "abc123"
    """
```

### Imports
```python
# Standard library
import json
from pathlib import Path
from typing import Optional, List

# Third-party
from rich.console import Console

# Local
from development.core import search_prompts
```

---

## Testing

### Unit Tests (Black Box)
Test individual functions in isolation:

```python
# tests/unit/test_search.py
from development.search import search_prompts

def test_search_by_query():
    # Setup
    db = create_test_db()
    db.log_prompt("state management", "claude")
    
    # Test
    results = search_prompts(db, "state")
    
    # Assert
    assert len(results) == 1
    assert results[0]["query"] == "state management"
```

### Integration Tests
Test end-to-end user workflows:

```python
# tests/integration/test_workflow.py
from pro_mpt import cli

def test_log_and_search():
    # User logs a prompt
    runner = CliRunner()
    result = runner.invoke(cli.log, [
        "state management",
        "--model", "claude"
    ])
    assert result.exit_code == 0
    
    # User searches for it
    result = runner.invoke(cli.search, ["state"])
    assert "state management" in result.output
```

### Run Tests
```bash
# All tests
pytest tests/ -v

# Specific test
pytest tests/unit/test_search.py::test_search_by_query -v

# With coverage
pytest tests/ --cov=development --cov=pro_mpt --cov-report=html
```

### Before Commit
```bash
# Format
black pro_mpt.py

# Lint
ruff check pro_mpt.py --fix

# Type check
mypy pro_mpt.py

# Test
pytest tests/ -v

# Check for typos
codespell pro_mpt.py
```

---

## Adding a Feature

### Step 1: Design
Ask:
- What problem does this solve?
- What's the simplest way to solve it?
- Who uses it? (dev, chef, enterprise?)

**Document**:
```markdown
# Feature: Search by Model

## Problem
Users want to see which model gave them the best answer for a topic.

## Solution
Add --model flag to search command:
  pro-mpt search "state" --model claude

## Usage
Users filtering to see only Claude answers for a topic.

## Impact
Low complexity, high value for app developers.
```

### Step 2: Implement
```python
@app.command()
def search(
    query: str = typer.Argument(...),
    model_filter: Optional[str] = typer.Option(None, "--model"),
    # ... other filters
):
    """Search prompts"""
    # Filter by model if provided
    if model_filter:
        results = [r for r in results if r["model"] == model_filter]
    # Display...
```

### Step 3: Test
```python
def test_search_by_model():
    # Setup
    log_prompt("state", "claude")
    log_prompt("state", "gpt4")
    
    # Test filter
    results = search("state", model="claude")
    
    # Should have 1
    assert len(results) == 1
    assert results[0]["model"] == "claude"
```

### Step 4: Document
Update:
- `README.md` - Add to command reference
- `CHANGELOG.md` - Add to features
- Docstring - In the code
- This file - If it affects architecture

### Step 5: Commit
```bash
git add pro_mpt.py tests/ README.md CHANGELOG.md
git commit -m "feat: search by model

- Add --model flag to search command
- Filter results by specified model
- Helps users find which models work best for a topic"
```

---

## Common Tasks

### Adding a New Command
```python
@app.command()
def my_new_command(
    required: str = typer.Argument(..., help="Required param"),
    optional: Optional[str] = typer.Option(None, help="Optional param"),
):
    """One-line description of what it does"""
    
    # Get data
    conn = get_db()
    
    # Process
    # ...
    
    # Display
    console.print(Panel(...))
```

### Adding a Database Field
```python
# Update schema in init_db()
c.execute("""
    ALTER TABLE prompts ADD COLUMN new_field TEXT
""")

# Use in code
c.execute("INSERT INTO prompts (..., new_field) VALUES (..., ?)", (..., value))

# Document in CHANGELOG.md
```

### Adding a Filter to Search
```python
# In search command
if optional_filter:
    sql += " AND column = ?"
    params.append(optional_filter)

# Add to tests
def test_search_with_filter():
    # ...
```

### Improving Output Formatting
```python
# Use Rich components
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Build nice output
panel = Panel(content, border_style="cyan", padding=(1, 2))
console.print(panel)
```

---

## Performance & Optimization

### Current (MVP)
- Database: SQLite (good enough for 1000s of prompts)
- Search: Full-text scan (fine for < 100k prompts)
- Output: No caching (fine, fast anyway)

### When to Optimize
- > 10k prompts: Add search index
- > 100k prompts: Move to PostgreSQL
- Slow searches: Profile with `cProfile`
- Many users: Add caching layer

### Profiling
```bash
# Profile a search
python -m cProfile -s cumtime pro_mpt.py search "query"

# Use a profiler
pip install py-spy
py-spy record -o profile.svg python pro_mpt.py search "query"
```

---

## Debugging

### Print Debugging
```python
# Quick debug output
import json
print(json.dumps(data, indent=2, default=str))

# Or use Rich for pretty output
from rich import print as rprint
rprint(data)
```

### Database Debugging
```bash
# Inspect database
sqlite3 ~/.pro-mpt/prompts.db

# In sqlite3:
sqlite> .schema prompts
sqlite> SELECT COUNT(*) FROM prompts;
sqlite> SELECT * FROM prompts LIMIT 1;
```

### Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Searching for {query}")
```

---

## Releases

See [RELEASE.md](RELEASE.md) for:
- Version numbering
- Deployment process
- Backwards compatibility
- Changelog maintenance

---

## Git Workflow

### Branch Naming
```
feature/feature-name       # New feature
fix/bug-description        # Bug fix
refactor/what-changed      # Refactoring
docs/what-docs            # Documentation
test/test-improvement     # Test improvements
```

### Commit Messages
```
feat: add --model filter to search

- Allows filtering search results by model
- Helps identify which models work best
- Closes #42

fix: handle empty query in search

- Previously crashed on empty query
- Now returns helpful error message
- Fixes #41

refactor: extract search logic to function

- Reduces duplication
- Makes testing easier
- No behavioral changes
```

### Pull Request Template
```markdown
## What
Brief description of changes

## Why
Why are these changes needed?

## How
How do the changes work?

## Tests
How did you test this?

## Checklist
- [ ] Tests pass
- [ ] Code formatted (black, ruff)
- [ ] Types check (mypy)
- [ ] Docs updated
- [ ] CHANGELOG updated
```

---

## Getting Help

**Architecture questions?** 
Open a discussion in GitHub

**Stuck on a bug?**
1. Check existing issues
2. Run tests to narrow scope
3. Use database debugging
4. Ask in discussions

**Want to pair on something?**
Ping in Discord

---

## Learning Paths

### For a New Contributor
1. Read MANIFESTO.md (understand why)
2. Read README.md (understand what)
3. Try commands: `pro-mpt log`, `pro-mpt search`
4. Read pro_mpt.py (understand how)
5. Add small feature (improve something)

### For Adding Integrations
1. Study development/connectors/base.py pattern
2. Create new connector class
3. Wire to CLI
4. Write tests
5. Document in CHANGELOG

### For Adding Intelligence
1. Learn Anthropic SDK
2. Study development/ai/ module
3. Build agent logic
4. Test with your own prompts
5. Share results

---

## Tools & Stack

### Required
- Python 3.10+
- sqlite3 (built-in)
- pip

### Development
- black (code formatter)
- ruff (linter)
- mypy (type checker)
- pytest (testing)

### Optional
- sqlite-web (visual database browser)
- pgcli (if using PostgreSQL later)

### Nice to Have
- git-delta (prettier git diff)
- fzf (fuzzy search in terminal)

---

## Project Health

### Metrics We Track
- Test coverage (aim for > 80%)
- Performance (search should be < 100ms)
- Documentation completeness
- Issue resolution time
- User feedback

### Before Major Release
- [ ] All tests passing
- [ ] 80%+ test coverage
- [ ] Performance profiled
- [ ] Docs updated
- [ ] Changelog complete
- [ ] Manual user testing
- [ ] Version bumped

---

## Looking Ahead

### Month 1 Goals
- [ ] You using it daily
- [ ] 5+ iterations based on your feedback
- [ ] Beautiful CLI polish
- [ ] Solid foundation for scale

### Month 2 Goals
- [ ] Browser extension
- [ ] Auto-capture working
- [ ] GitHub integration
- [ ] Personal agent MVP

### Month 3 Goals
- [ ] Ready for team beta
- [ ] Cloud sync option
- [ ] API for integrations
- [ ] Public demo

---

## Questions?

1. **Usage?** See README.md
2. **Why decisions?** See MANIFESTO.md
3. **How to release?** See RELEASE.md
4. **How to contribute?** See GitHub discussions
5. **Technical questions?** Open an issue

---

**Welcome to building pro-mpt. Let's make thinking visible.**
