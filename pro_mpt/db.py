import sqlite3
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

class Database:
    """Unified database management for pro-mpt"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Core Prompts Table
        c.execute("""
            CREATE TABLE IF NOT EXISTS prompts (
                id TEXT PRIMARY KEY,
                query TEXT NOT NULL,
                model TEXT,
                agent TEXT,
                app TEXT,
                domain TEXT,
                version TEXT,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                rating INTEGER,
                notes TEXT,
                metadata TEXT
            )
        """)
        
        # Optional: FTS5 Virtual Table for Instant Search
        try:
            c.execute("CREATE VIRTUAL TABLE IF NOT EXISTS prompts_fts USING fts5(query, response, notes, content='prompts', content_rowid='rowid')")
            # Trigger to keep FTS in sync
            c.execute("""
                CREATE TRIGGER IF NOT EXISTS prompts_ai AFTER INSERT ON prompts BEGIN
                  INSERT INTO prompts_fts(rowid, query, response, notes) VALUES (new.rowid, new.query, new.response, new.notes);
                END;
            """)
        except sqlite3.OperationalError:
            # FTS5 might not be available in all sqlite3 builds
            pass

        conn.commit()
        conn.close()

    def add_prompt(self, query: str, model: str = "unknown", agent: str = "manual",
                   app: str = "personal", domain: str = "general", version: str = None,
                   response: str = None, rating: int = None, notes: str = None,
                   metadata: str = None) -> str:
        conn = self._get_conn()
        c = conn.cursor()
        prompt_id = str(uuid.uuid4())[:8]
        
        c.execute("""
            INSERT INTO prompts 
            (id, query, model, agent, app, domain, version, response, rating, notes, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (prompt_id, query, model, agent, app, domain, version, response, rating, notes, metadata))
        
        conn.commit()
        conn.close()
        return prompt_id

    def search(self, term: str, app_filter: str = None, domain_filter: str = None) -> List[Dict]:
        conn = self._get_conn()
        c = conn.cursor()
        
        # Try FTS first, fallback to LIKE
        try:
            sql = "SELECT * FROM prompts WHERE rowid IN (SELECT rowid FROM prompts_fts WHERE prompts_fts MATCH ?)"
            params = [term]
        except:
            sql = "SELECT * FROM prompts WHERE query LIKE ?"
            params = [f"%{term}%"]

        if app_filter:
            sql += " AND app = ?"
            params.append(app_filter)
        if domain_filter:
            sql += " AND domain = ?"
            params.append(domain_filter)

        sql += " ORDER BY timestamp DESC"
        c.execute(sql, params)
        results = [dict(row) for row in c.fetchall()]
        conn.close()
        return results

    def list_recent(self, limit: int = 10, app_filter: str = None) -> List[Dict]:
        conn = self._get_conn()
        c = conn.cursor()
        sql = "SELECT * FROM prompts"
        params = []
        if app_filter:
            sql += " WHERE app = ?"
            params.append(app_filter)
        sql += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        c.execute(sql, params)
        results = [dict(row) for row in c.fetchall()]
        conn.close()
        return results

    def get_stats(self) -> Dict[str, Any]:
        conn = self._get_conn()
        c = conn.cursor()
        stats = {}
        
        c.execute("SELECT COUNT(*) FROM prompts")
        stats["total"] = c.fetchone()[0]
        
        c.execute("SELECT COUNT(DISTINCT model) FROM prompts")
        stats["models"] = c.fetchone()[0]
        
        c.execute("SELECT COUNT(DISTINCT app) FROM prompts")
        stats["apps"] = c.fetchone()[0]
        
        conn.close()
        return stats
