#!/usr/bin/env python3
"""
Auto-import Gemini CLI sessions to pro-mpt
Watches ~/.gemini/tmp/ for active conversations and ingests them
Supports continuous/ambient capture by tracking individual messages.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime
import uuid
import os
from typing import Optional, Dict, Any, List

DB_PATH = Path.home() / ".pro-mpt" / "prompts.db"
GEMINI_TMP = Path.home() / ".gemini" / "tmp"
IMPORTED_CACHE = Path.home() / ".pro-mpt" / ".imported_gemini_messages"

def ensure_imported_cache():
    """Track which specific messages we've already imported"""
    IMPORTED_CACHE.parent.mkdir(parents=True, exist_ok=True)
    IMPORTED_CACHE.touch(exist_ok=True)

def get_imported_messages() -> set:
    """Load set of already-imported message IDs (format: sessionId:messageId)"""
    if not IMPORTED_CACHE.exists():
        return set()
    with open(IMPORTED_CACHE) as f:
        return set(line.strip() for line in f if line.strip())

def mark_imported(session_id: str, message_id: int):
    """Mark a message as imported"""
    with open(IMPORTED_CACHE, "a") as f:
        f.write(f"{session_id}:{message_id}\n")

def parse_logs_file(json_path: Path) -> List[Dict[str, Any]]:
    """Parse a Gemini CLI logs.json file"""
    try:
        with open(json_path) as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception as e:
        print(f"  ⚠️  Error parsing {json_path}: {e}")
    return []

def extract_app_name(dir_path: Path) -> str:
    """Extract app name from directory"""
    return dir_path.parent.name or "unknown"

def import_to_pro_mpt(message: Dict[str, Any], app_name: str) -> bool:
    """Import a single user prompt to pro-mpt database"""
    if message.get("type") != "user" or not message.get("message"):
        return False
        
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Ensure table exists with metadata
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

        query = message.get("message", "")
        timestamp = message.get("timestamp", datetime.now().isoformat())
        session_id = message.get("sessionId", "unknown")
        
        # Identity Preservation: No truncation (or very large limit)
        # Agent Understanding: basic intent extraction
        intent = "unknown"
        if "?" in query:
            intent = "question"
        elif any(word in query.lower() for word in ["buy", "call", "do", "fix", "defrost"]):
            intent = "task"
        elif any(word in query.lower() for word in ["film", "story", "character", "scene"]):
            intent = "creative"
        
        metadata_obj = {
            "intent": intent,
            "session_id": session_id,
            "captured_ambiently": True,
            "agent_interpretation": f"This looks like a {intent}."
        }
        
        # Insert
        entry_id = str(uuid.uuid4())[:8]

        c.execute("""
            INSERT INTO prompts (id, query, model, agent, app, domain, version, response, timestamp, rating, notes, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entry_id,
            query, # PRESERVE IDENTITY: NO TRUNCATION
            "gemini",
            "gemini-cli",
            app_name,
            "ambient",
            "v1.0.3-alpha",
            "",
            timestamp,
            None,
            f"Ambient capture from {app_name}",
            json.dumps(metadata_obj)
        ))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"  ❌ Error importing to database: {e}")
        return False

def scan_and_import():
    """Scan Gemini tmp directory for new messages"""
    ensure_imported_cache()
    imported = get_imported_messages()

    if not GEMINI_TMP.exists():
        print("❌ ~/.gemini/tmp not found")
        return

    new_count = 0

    # Find all logs.json files
    for logs_path in GEMINI_TMP.glob("**/logs.json"):
        app_name = extract_app_name(logs_path)
        messages = parse_logs_file(logs_path)
        
        for msg in messages:
            if msg.get("type") != "user":
                continue
                
            session_id = msg.get("sessionId")
            message_id = msg.get("messageId")
            
            if session_id is None or message_id is None:
                continue
                
            tracking_id = f"{session_id}:{message_id}"
            
            # Skip if already imported
            if tracking_id in imported:
                continue

            print(f"📥 Importing prompt from {app_name}...")
            
            if import_to_pro_mpt(msg, app_name):
                mark_imported(session_id, message_id)
                new_count += 1

    if new_count > 0:
        print(f"\n✨ Imported {new_count} new prompt(s) from Gemini CLI to pro-mpt")
    else:
        print(f"\n✨ Already up to date (Monitoring ambiently)")

if __name__ == "__main__":
    scan_and_import()
