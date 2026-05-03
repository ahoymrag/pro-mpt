import json
import uuid
from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pro_mpt.db import Database

DB_PATH = Path.home() / ".pro-mpt" / "prompts.db"

class BaseConnector(ABC):
    """Base class for all pro-mpt data connectors"""
    
    def __init__(self, name: str, source_path: Path, cache_name: str):
        self.name = name
        self.source_path = source_path
        self.cache_path = Path.home() / ".pro-mpt" / cache_name
        self.db = Database(DB_PATH)
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
            self.db.add_prompt(
                query=query,
                model=model,
                agent=agent,
                app=app,
                domain=domain,
                response=response,
                notes=notes,
                metadata=json.dumps(metadata) if isinstance(metadata, dict) else metadata
            )
            return True
        except Exception as e:
            print(f"  ❌ Error importing to database: {e}")
            return False

    @abstractmethod
    def scan_and_import(self):
        """Main entry point for the connector"""
        pass
