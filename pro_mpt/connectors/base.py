import json
import sqlite3
import uuid
from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

DB_PATH = Path.home() / ".pro-mpt" / "prompts.db"

class BaseConnector(ABC):
    """Base class for all pro-mpt data connectors"""
    
    def __init__(self, name: str, source_path: Path, cache_name: str):
        self.name = name
        self.source_path = source_path
        self.cache_path = Path.home() / ".pro-mpt" / cache_name
        self.ensure_cache()

    def ensure_cache(self):
        """Ensure cache file exists"""
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.touch(exist_ok=True)

    def get_imported_ids(self) -> set:
        """Load set of already-imported IDs from cache"""
        with open(self.cache_path) as f:
            return set(line.strip() for line in f if line.strip())

    def mark_imported(self, entry_id: str):
        """Mark an entry as imported in the cache"""
        with open(self.cache_path, "a") as f:
            f.write(f"{entry_id}\n")

    def import_to_db(self, query: str, model: str, agent: str, app: str, 
                    domain: str, timestamp: str, metadata: Dict[str, Any],
                    response: str = "", notes: str = "") -> bool:
        """Standardized method to insert into the pro-mpt database"""
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            
            # Ensure table exists with metadata column
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
                    timestamp TEXT,
                    rating INTEGER,
                    notes TEXT,
                    metadata TEXT
                )
            """)

            entry_id = str(uuid.uuid4())[:8]
            
            c.execute("""
                INSERT INTO prompts (id, query, model, agent, app, domain, version, response, timestamp, rating, notes, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry_id, query, model, agent, app, domain, "v1.0.3-refactor", 
                response, timestamp, None, notes, json.dumps(metadata)
            ))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"  ❌ Error importing to database: {e}")
            return False

    @abstractmethod
    def scan_and_import(self):
        """Main entry point for the connector"""
        pass
