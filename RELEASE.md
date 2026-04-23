# RELEASE.md - Release Process

How pro-mpt versions, ships, and maintains backwards compatibility.

---

## Versioning Scheme

**Semantic Versioning: MAJOR.MINOR.PATCH**

- **MAJOR** (0 → 1): Breaking changes
  - Data format changes
  - Command syntax changes
  - Requires user action to upgrade
  
- **MINOR** (0.1 → 0.2): New features
  - New commands
  - New connectors
  - New options (backwards compatible)
  
- **PATCH** (0.1.0 → 0.1.1): Bug fixes
  - Fixes
  - Performance improvements
  - Doc updates

### Current: 0.1.0

| Phase | Version Range | Status |
|-------|--------------|--------|
| MVP | 0.1.x | Current (breaking changes ok) |
| Stable | 0.x.x | Beta (breaking changes ok) |
| Production | 1.0+ | Strict backwards compat |

---

## Release Timeline

### Patch Releases (0.1.1, 0.1.2, etc.)
- **Frequency**: Every 1-2 weeks (as needed)
- **Changes**: Bug fixes, performance, docs
- **Testing**: Automated only
- **Migration**: None required

### Minor Releases (0.2.0, 0.3.0, etc.)
- **Frequency**: Every 3-4 weeks
- **Changes**: New features
- **Testing**: Automated + manual
- **Migration**: Documented, backwards compatible

### Major Releases (1.0.0, 2.0.0, etc.)
- **Frequency**: Rare, well-planned
- **Changes**: Breaking changes only
- **Testing**: Extensive
- **Migration**: Migration guide required

---

## Release Checklist

### 1 Week Before (Planning)

- [ ] Review merged PRs since last release
- [ ] Create GitHub milestone with target date
- [ ] Draft changelog (copy to CHANGELOG.md)
- [ ] Identify breaking changes (if any)
- [ ] Plan migration (if needed)

```markdown
# Version 0.2.0 - New Features

- Auto-capture from browser
- Search by confidence
- Better UI formatting
```

### 3 Days Before (Code Freeze)

- [ ] No new features merged
- [ ] Bug fixes only after this point
- [ ] Full test suite passes
- [ ] Type checking passes: `mypy pro_mpt.py`
- [ ] Linting passes: `ruff check pro_mpt.py`
- [ ] Coverage > 80%: `pytest --cov`

Commands:
```bash
black pro_mpt.py
ruff check pro_mpt.py --fix
mypy pro_mpt.py
pytest tests/ -v --cov=pro_mpt --cov=development
```

### Release Day (Ship It)

#### Step 1: Update Version
```python
# development/version.py (or in pro_mpt.py)
__version__ = "0.2.0"
__release_date__ = "2026-04-30"
```

Or directly in CLI:
```python
@app.command()
def version():
    """Show version"""
    print("pro-mpt 0.2.0")
```

#### Step 2: Update CHANGELOG
```bash
# Copy planned changes to CHANGELOG.md
# Update dates to today
# Mark as released (remove [Unreleased])
```

#### Step 3: Git Tag & Push
```bash
# Make sure everything is committed
git status  # Should be clean

# Create annotated tag
git tag -a v0.2.0 -m "Release version 0.2.0"

# Push to GitHub
git push origin main
git push origin v0.2.0
```

#### Step 4: GitHub Release
```bash
# Create release on GitHub
gh release create v0.2.0 \
  --title "Version 0.2.0: New Features" \
  --notes "$(cat CHANGELOG.md | grep -A 20 '## \[0.2.0\]')"

# Or manually on github.com/yourname/pro-mpt/releases
```

#### Step 5: Verify Installation
```bash
# Test that users can install
pip install pro-mpt==0.2.0

# Or if published to PyPI later
pip install --upgrade pro-mpt
```

#### Step 6: Announce
- [ ] Update README.md if needed
- [ ] Tweet/post about release
- [ ] Slack/Discord announcement
- [ ] Email to users (if applicable)

### Day After Release (Monitor)

- [ ] Watch for issue reports
- [ ] Monitor error logs (if telemetry enabled)
- [ ] Response to feedback: < 24 hours
- [ ] Patch immediately if critical bug

---

## Types of Releases

### Hotfix Release (0.1.0 → 0.1.1)
**When**: Critical bug found in production

**Process**:
```bash
# Branch off latest release
git checkout -b hotfix/critical-bug v0.1.0

# Fix the bug
# Test thoroughly
git commit -m "fix: critical bug description"

# Tag as patch
git tag v0.1.1
git push origin main v0.1.1
```

**Changelog**:
```markdown
## [0.1.1] - 2026-04-25

### Fixes
- Critical: Fixed crash on empty query (#42)
```

### Feature Release (0.1.0 → 0.2.0)
**When**: Planned features ready (every 3-4 weeks)

**Process**:
1. Develop features on feature branches
2. PR + review + merge
3. Freeze features (code freeze)
4. Bug fixes only
5. Tag + release

### Major Release (0.9.0 → 1.0.0)
**When**: Production ready, stable API

**Process**:
1. Very careful planning
2. Extended testing
3. Migration guide (if breaking)
4. Announcement (big deal)
5. Maintain old version for transition period

---

## Data Migrations

### When Needed
- Schema changes
- Data format changes
- Breaking API changes

### Migration Strategy

**Option A: Automatic Migration (Recommended)**
```python
# development/version.py
CURRENT_SCHEMA_VERSION = 2

# On startup
if user_schema_version < CURRENT_SCHEMA_VERSION:
    print("Upgrading index...")
    migrate(user_schema_version, CURRENT_SCHEMA_VERSION)
    print("✓ Ready")
```

**Option B: Manual Migration**
```bash
# User runs
pro-mpt migrate --from 1.0.0 --to 2.0.0

# Or guided
pro-mpt migrate  # Detects version and asks
```

### Example Migration
```python
# scripts/migrate_v1_to_v2.py
def migrate():
    """Migrate from schema v1 to v2"""
    
    conn = get_db()
    c = conn.cursor()
    
    # Add new column with default
    c.execute("ALTER TABLE prompts ADD COLUMN new_field TEXT DEFAULT ''")
    
    # Backfill data if needed
    # ... (data transformation logic)
    
    # Update schema version
    c.execute("UPDATE _meta SET schema_version = 2")
    
    conn.commit()
    conn.close()
    
    print("✓ Migration complete")
```

### Backwards Compatibility

**Promise**: Older data always works

```python
# Old code still works
c.execute("SELECT * FROM prompts WHERE rating > 0")

# Old commands still work (with deprecation warning)
@app.command()
def find():  # Old name
    """Use 'search' instead (find is deprecated)"""
    logger.warning("'find' is deprecated, use 'search' instead")
    # Call search implementation
```

---

## Patch Levels Explained

### 0.1.0 (First Release)
- MVP complete
- Basic functionality working
- Core features solid
- Ready for personal use

### 0.1.1 (First Patch)
- Bug fix from 0.1.0
- No new features
- Increment patch version

### 0.1.2, 0.1.3, etc.
- Subsequent patches
- Each fixes issues in prior release
- Don't add new features

### 0.2.0 (First Minor)
- New features added
- All 0.1.x bugs fixed
- Increment minor version

### 1.0.0 (First Major)
- Production ready
- API stable
- Promises backwards compatibility

---

## Release Notes Template

Use this for GitHub releases:

```markdown
# pro-mpt v0.2.0

**Release Date**: 2026-04-30

## What's New

### Features ✨
- Auto-capture from browser (ChatGPT, Claude, Gemini)
- Search by confidence score
- Beautiful new dashboard

### Improvements 🚀
- 40% faster search on large archives
- Better error messages
- Improved terminal colors

### Fixes 🐛
- Fixed crash on empty query (#42)
- Fixed rating display glitch
- Fixed export to CSV

### Documentation 📚
- Updated README with browser extension guide
- Added troubleshooting section
- Expanded examples

## Installation

```bash
pip install --upgrade pro-mpt
```

## Migration

No migration needed. Just upgrade and enjoy!

## Contributors

- @yourname
- @contributor1
- @contributor2

## Stats

- 150 commits since v0.1.0
- 23 PRs merged
- 12 issues closed
- 2,000+ lines added

## Next Up

- Team collaboration features (v0.3.0)
- Cloud sync (v0.3.0)
- Web dashboard (v0.4.0)

## Thank You

Thanks to everyone who reported bugs, suggested features, and contributed code. This release is only possible because of community feedback.
```

---

## Release Cadence

### Weeks 1-2: MVP Phase
- Daily iterations (multiple "releases" for personal use)
- No official versions yet
- Feedback from your own usage

### Week 3: 0.1.0 Release
- Official first release
- Git tag v0.1.0
- Ready for others to use

### Weeks 4-6: Stability Phase
- Patch releases as needed (0.1.1, 0.1.2)
- Focus on reliability
- Gather feedback

### Weeks 7+: Feature Releases
- 0.2.0 (browser extension)
- 0.3.0 (GitHub integration)
- 0.4.0 (web dashboard)
- 1.0.0 (production ready)

---

## Long-term Maintenance

### After 1.0.0
- **Support current + 1 major version** (1.0 and 2.0)
- **Security patches**: Always
- **Bug fixes**: Current version only
- **Features**: Only in new major version

### Deprecation Policy
- Announce: 1 release in advance
- Warn: For 2 releases
- Remove: In next major version

Example:
```python
# v1.0.0: Announce
logger.warning("Command 'find' is deprecated. Use 'search' instead. "
               "It will be removed in v2.0.0")

# v1.1.0, v1.2.0: Keep warning
# v2.0.0: Remove entirely
```

---

## Rolling Back

### If Critical Bug in Release

```bash
# Tag as broken
git tag v0.2.0-broken

# Remove bad release
gh release delete v0.2.0

# Revert commits
git revert <commit-hash>
git push origin main

# Tag as fixed
git tag v0.2.1
git push origin v0.2.1

# Update release notes
# Announce: "Pulled 0.2.0, use 0.2.1"
```

### If Data Corruption

```bash
# Create emergency patch
git checkout -b hotfix/data-corruption
# Fix the issue
git commit -m "fix: prevent data corruption in search"
git tag v0.1.2
git push origin main v0.1.2

# Announce immediately
# "Use 0.1.2 immediately if using 0.1.1"
```

---

## Publishing (Future)

### To PyPI
```bash
# Install tools
pip install build twine

# Build distribution
python -m build

# Upload
twine upload dist/*

# Verify
pip install pro-mpt==0.2.0
```

### To Homebrew (macOS)
```bash
# Create formula
# Submit to homebrew-core

# Users can then
brew install pro-mpt
```

### Binary Distribution (Rust Era)
```bash
# Once rewritten in Rust
# Single binary: pro-mpt-v0.2.0-macos
# Users download, run directly
```

---

## Monitoring Releases

### Health Checks
- [ ] Installation works
- [ ] All commands functional
- [ ] No crashes reported in 24 hours
- [ ] Performance acceptable

### Metrics
- Downloads (if on PyPI)
- Reported issues (GitHub)
- User feedback (discussions)
- Error reports (if telemetry)

---

## Communication

### Before Release
- PR in changelog
- Announce in discussions
- Estimated date

### During Release
- Tag on GitHub
- Release notes posted
- Tweet/socials (if applicable)

### After Release
- Monitor for issues
- Respond to feedback
- Plan next release

---

## Questions & Edge Cases

**Q: How often should we release?**
A: Patches when urgent (as needed), features every 3-4 weeks, majors rarely.

**Q: What if I need to skip a version number?**
A: You don't. Skip minor versions (1.0 → 1.2 if 1.1 had issues). Skip patch versions if needed.

**Q: Can I release two versions on the same day?**
A: Yes, if one is a hotfix. Example: 0.1.0 release, then immediate 0.1.1 hotfix.

**Q: How long to support old versions?**
A: Current + 1 major. So if at 2.0, support 1.0 with security patches, 2.0 with everything.

---

## Tools

### Required
- Git
- GitHub account

### Optional
- GitHub CLI (`gh`)
- Twine (for PyPI)
- Python build (`python -m build`)

---

## Next Steps

1. **First release**: When you want others to use it
2. **PyPI**: When it's stable (1.0+)
3. **Binary distribution**: If popularity demands it

---

**Happy releasing! Ship fast, iterate faster.**
