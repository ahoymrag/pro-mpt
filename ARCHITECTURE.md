# ARCHITECTURE.md - Scaling to Market

Blueprint for evolving pro-mpt from personal tool to enterprise product.

---

## Current State (MVP)

```
pro-mpt.py (200 lines)
├── SQLite database
└── CLI interface
    ├── Log command
    ├── Search command
    ├── List command
    ├── Expertise command
    ├── Stats command
    └── Export command
```

**What it does**: Archive + search + analyze

**Data flow**:
```
User types: pro-mpt log "query" --model claude
    ↓
Save to SQLite
    ↓
User types: pro-mpt search "query"
    ↓
Read from SQLite
    ↓
Display results
```

---

## Phase 1: Foundation (Weeks 1-4) → YOU ARE HERE

**Goal**: Personal tool you use daily

**Architecture**:
```
pro_mpt.py (single file)
│
├── Database layer
│   └── SQLite: prompts.db
│
├── Commands
│   ├── log
│   ├── search
│   ├── expertise
│   └── ...
│
└── Display
    └── Rich CLI
```

**What's coming**: Nothing new, just refinement

**Technical debt**: None yet (too simple)

---

## Phase 2: Integrations (Weeks 4-8)

**Goal**: Auto-capture from multiple sources

**Architecture**:
```
development/
├── connectors/          ← NEW
│   ├── base.py
│   ├── prompt.py       # Manual logging
│   ├── github.py       # Auto-capture commits
│   ├── slack.py        # Auto-capture messages
│   ├── browser.py      # Auto-capture ChatGPT/Claude
│   └── calendar.py     # Auto-capture meetings
│
├── core/               ← EXTRACTED
│   ├── database.py
│   ├── index.py
│   └── graph.py
│
└── search/
    ├── engine.py
    └── ranker.py

pro_mpt/               ← REFACTORED
├── cli.py
├── commands/
│   ├── log.py
│   ├── search.py
│   └── ...
└── ui/
    └── formatter.py
```

**How connectors work**:
```python
class BaseConnector:
    def fetch() → List[RawData]:
        """Get data from source"""
        
    def transform(raw) → StandardizedPrompt:
        """Convert to canonical format"""

class GitHubConnector(BaseConnector):
    def fetch():
        # Call GitHub API for commits
        
    def transform(commit):
        # Convert commit → prompt

# Usage
github = GitHubConnector(token="...", repo="myapp")
prompts = github.fetch()  # Get all commits
indexed = [github.transform(p) for p in prompts]
index.ingest(indexed)
```

**New commands**:
```bash
pro-mpt setup github    # Connect GitHub account
pro-mpt ingest github   # Import history
pro-mpt sync --watch    # Live updates
```

---

## Phase 3: Intelligence (Weeks 8-12)

**Goal**: Personal agent + pattern detection

**Architecture**:
```
development/
├── connectors/ (as before)
│
├── core/
│   ├── graph.py        # Knowledge graph
│   ├── database.py
│   └── cache.py
│
├── search/ (as before)
│
├── expertise/          ← ENHANCED
│   ├── analyzer.py     # Analysis engine
│   ├── tracker.py      # Growth tracking
│   └── profiler.py     # Build profiles
│
├── ai/                 ← NEW
│   ├── agent.py        # Personal agent
│   ├── vibe.py         # Personality tracking
│   ├── suggestions.py  # Auto-feature detection
│   └── insights.py     # LLM analysis
│
└── personality/        ← NEW
    └── vibe.md         # Evolves over time
```

**Personal Agent**:
```python
class PersonalAgent:
    def __init__(self, user_archive):
        self.archive = user_archive
        self.style = self._learn_style()
        
    def suggest_solution(self, problem: str) -> Suggestion:
        # Search archive for similar problems
        similar = self.archive.search(problem)
        
        # Check what models/approaches worked
        best_approach = self._find_best_approach(similar)
        
        # Use LLM + your history to suggest
        context = f"""
        User is asking: {problem}
        Similar problems they've solved:
        {similar}
        
        Based on their history, suggest the best approach.
        Use their favorite model/style.
        """
        
        suggestion = claude.generate(context)
        return suggestion
```

**Vibe.md Evolution**:
```python
class VipeBuilder:
    def daily_update(self):
        # Analyze today's prompts
        # Update personality understanding
        # Write vibe.md
        
        # Example:
        # "They're asking about X more than usual"
        # "Their questions are more specific"
        # "Growing confidence in Y domain"
```

**New commands**:
```bash
pro-mpt suggest           # Agent suggests solutions
pro-mpt vibe              # See your personality
pro-mpt agent --chat      # Talk to your agent
pro-mpt morning           # Personalized daily
```

---

## Phase 4: Team & Scale (Months 2+)

**Goal**: Multi-user, cloud-backed, enterprise-ready

**Architecture**:
```
Cloud Infrastructure:
├── API Server (Python/FastAPI)
│   ├── Auth (OAuth2)
│   ├── Routes (REST/GraphQL)
│   └── Rate limiting
│
├── Database (PostgreSQL)
│   ├── Users
│   ├── Prompts (encrypted)
│   ├── Teams
│   └── Domains
│
├── Cache (Redis)
│   ├── Search results
│   ├── User sessions
│   └── Aggregates
│
└── Queue (Celery/Bull)
    ├── Long-running jobs
    ├── Integrations
    └── Backups

Client:
├── CLI (local + cloud)
├── Web Dashboard
├── Mobile App
└── Browser Extension
```

**Key Design Decisions**:

1. **Local-First + Cloud-Optional**
   - User data on machine by default
   - Cloud sync is opt-in
   - Encrypted end-to-end

2. **No Data Lock-In**
   - All data exportable (JSON, CSV)
   - Open format, no proprietary
   - Users can take it anywhere

3. **API-First Internally**
   - CLI uses same API as web
   - Easy to add clients (mobile, web, IDE plugins)

4. **Privacy By Design**
   - Aggregate analytics (never raw prompts)
   - User controls what's shared
   - Clear audit log

**Team Features**:
```
Shared Playbooks:
  "Here's how we solve authentication"
  ↓ Links to solved prompts
  ↓ Shows which model worked best
  ↓ Shows iterations that led to solution

Team Expertise:
  "Team is 85% confident in distributed systems"
  ↓ Based on collective prompts
  ↓ Shows growth over time
  ↓ Identifies knowledge gaps

Decision History:
  "We decided to use Redis because..."
  ↓ Links to prompts that made the decision
  ↓ Shows conversation history
  ↓ Explains the reasoning
```

**Enterprise Features**:
```
Compliance:
  - Audit trail of all prompts
  - User/team attribution
  - Retention policies
  - Export for compliance

Cost Optimization:
  - Track AI spend per team/user
  - See which models you use most
  - Identify expensive patterns
  - Budget alerts

Security:
  - SSO/SAML
  - IP whitelisting
  - Encrypted at rest + in transit
  - SOC 2 compliance
```

---

## Technology Choices by Phase

### Phase 1-2: Python (Current)
```
Language: Python 3.10+
CLI: Typer
Output: Rich
Database: SQLite
External APIs: GitHub, Slack, Anthropic SDK
```

**Why Python**:
- Anthropic SDK is native
- Rich ecosystem for AI features
- Fast to iterate
- Easy to learn

### Phase 3: Add Anthropic SDK
```
dependencies += anthropic
```

**For Agent**:
- Prompt caching (efficient)
- Function calling (tool use)
- Streaming (real-time)

### Phase 4: Rewrite Core (Optional)
```
Option A: Keep Python, add web layer
  - FastAPI for API
  - PostgreSQL for scale
  - Redis for cache

Option B: Rewrite core in Rust (if needed)
  - Graph engine (performance)
  - Keep Python for AI/integrations
  - Hybrid architecture

Decision: Scale determines this
  - < 10k users: Python fine
  - > 100k users: Consider Rust
```

---

## Data Model Evolution

### Phase 1: Simple
```sql
CREATE TABLE prompts (
    id TEXT PRIMARY KEY,
    query TEXT,
    model TEXT,
    app TEXT,
    domain TEXT,
    version TEXT,
    timestamp DATETIME,
    rating INTEGER,
    notes TEXT
)
```

### Phase 2: Add Metadata
```sql
ALTER TABLE prompts ADD COLUMN source TEXT;  -- 'manual', 'github', 'slack'
ALTER TABLE prompts ADD COLUMN raw_data JSON; -- Original data
ALTER TABLE prompts ADD COLUMN tags TEXT[];   -- User tags
```

### Phase 3: Add Relations
```sql
CREATE TABLE prompt_relationships (
    source_id TEXT,
    target_id TEXT,
    relationship TEXT,  -- 'led_to', 'solved_by', 'similar_to'
    FOREIGN KEY (source_id, target_id) REFERENCES prompts(id)
)

CREATE TABLE user_expertise (
    user_id TEXT,
    domain TEXT,
    confidence FLOAT,
    updated_at DATETIME
)
```

### Phase 4: Multi-Tenant
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT,
    name TEXT,
    created_at DATETIME
)

CREATE TABLE teams (
    id TEXT PRIMARY KEY,
    name TEXT,
    owner_id TEXT,
    FOREIGN KEY (owner_id) REFERENCES users(id)
)

ALTER TABLE prompts ADD COLUMN user_id TEXT;
ALTER TABLE prompts ADD COLUMN team_id TEXT;
-- Data stays encrypted at rest
```

---

## Migration Path

### Personal → Team
```
User's archive → Sync to server
    ↓
User invites teammate
    ↓
Teammate sees shared prompts
    ↓
Team builds collective playbooks
```

### Team → Enterprise
```
Teams collaborate → Organization layer
    ↓
Admin oversight → Compliance features
    ↓
Cost visibility → Budget controls
    ↓
Knowledge management → Search across org
```

---

## Performance Targets

| Phase | Dataset | Latency | Throughput |
|-------|---------|---------|-----------|
| 1 | 1k prompts | < 100ms | NA |
| 2 | 10k prompts | < 200ms | 10 ops/sec |
| 3 | 100k prompts | < 500ms | 100 ops/sec |
| 4 | 1M prompts | < 1s | 1000 ops/sec |

### Optimization Timeline
- Phase 1: No optimization needed (too fast)
- Phase 2: Add search index if slow
- Phase 3: Switch to PostgreSQL
- Phase 4: Add cache layer (Redis)

---

## Testing Strategy

### Unit Tests (Development/)
```python
# Test search engine
def test_search_query():
    engine = SearchEngine(test_db)
    results = engine.search("state")
    assert len(results) > 0

# Test connectors
def test_github_transform():
    connector = GitHubConnector()
    commit = {"message": "fix bug", ...}
    prompt = connector.transform(commit)
    assert prompt["query"] == "fix bug"
```

### Integration Tests (End-to-End)
```python
# Test whole workflow
def test_log_and_search():
    cli = CLI()
    cli.log("test", model="claude")
    results = cli.search("test")
    assert len(results) == 1
```

### Performance Tests
```python
# Test with large dataset
def test_search_1m_prompts():
    db = create_large_test_db(1_000_000)
    start = time.time()
    results = search(db, "test")
    elapsed = time.time() - start
    assert elapsed < 1.0  # Must be sub-second
```

### User Testing
- **Phase 1-2**: You using it daily
- **Phase 3**: 5-10 friends using it
- **Phase 4**: Beta group (100+ users)

---

## Open Questions → Decisions Needed

### 1. **Team Features Timing**
- Option A: Phase 4 (months away)
- Option B: Early Phase 3 (speed to market)
- Option C: Wait for demand (user-driven)

### 2. **Enterprise Market**
- Go for it immediately?
- Focus on individuals first?
- Both (different products)?

### 3. **Business Model**
- Freemium (free personal, paid team)?
- Open source (donations)?
- Licensing?

### 4. **Rewrite Timeline**
- Keep Python as long as possible?
- Rewrite to Rust when?
- Hybrid (Python + Rust)?

---

## Success Metrics by Phase

### Phase 1
- ✓ You use daily
- ✓ 50+ prompts archived
- ✓ Search works fast

### Phase 2
- ✓ 5+ friends trying it
- ✓ Auto-capture working
- ✓ GitHub integration live

### Phase 3
- ✓ Agent suggests solutions
- ✓ Vibe.md evolves daily
- ✓ 50 users on beta

### Phase 4
- ✓ 1000+ users
- ✓ Teams collaborating
- ✓ Enterprise interest

---

## Risk Mitigation

### Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| User data leak | End-to-end encryption, audits |
| Performance issues at scale | Load testing, profiling, optimization |
| People don't want it | User research, iterate based on feedback |
| Competitors | Moat: user data control, privacy, openness |
| Burn out from building | Public roadmap, community help, fundraising |

---

## What You Need to Do

### Immediate (Next Week)
- [ ] Use pro-mpt daily for 5+ days
- [ ] File issues/suggestions
- [ ] Refine proto based on real usage

### Short-term (Weeks 2-3)
- [ ] Implement Phase 2 (connectors)
- [ ] GitHub integration
- [ ] Browser extension start

### Medium-term (Weeks 4-8)
- [ ] Implement Phase 3 (agent)
- [ ] Vibe.md personality
- [ ] Invite 5-10 friends

### Long-term (Months 2+)
- [ ] Decide on business model
- [ ] Decide on team timing
- [ ] Plan rewrite if needed

---

## Conclusion

**pro-mpt starts as a personal tool. It becomes infrastructure.**

- Week 1-4: Your thinking archive
- Week 4-8: Your agent
- Month 2: Your team's playbook
- Month 3+: Enterprise knowledge layer

Each phase builds on the last. No backtracking.

Your competitive advantage: **You built it for yourself first.**

That's the best way to build something people want.

---

**Build it. Use it. Scale it. Own it.**
