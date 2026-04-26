#!/usr/bin/env python3
"""
Auto-import Claude Code sessions to pro-mpt
Watches ~/.claude/projects for new conversations and ingests them
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime
import uuid
import os
from typing import Optional, Dict, Any, Tuple

DB_PATH = Path.home() / ".pro-mpt" / "prompts.db"
CLAUDE_PROJECTS = Path.home() / ".claude" / "projects"
IMPORTED_CACHE = Path.home() / ".pro-mpt" / ".imported_sessions"

def ensure_imported_cache():
    """Track which sessions we've already imported"""
    IMPORTED_CACHE.parent.mkdir(parents=True, exist_ok=True)
    IMPORTED_CACHE.touch(exist_ok=True)

def get_imported_sessions() -> set:
    """Load set of already-imported session IDs"""
    if not IMPORTED_CACHE.exists():
        return set()
    with open(IMPORTED_CACHE) as f:
        return set(line.strip() for line in f if line.strip())

def mark_imported(session_id: str):
    """Mark a session as imported"""
    with open(IMPORTED_CACHE, "a") as f:
        f.write(f"{session_id}\n")

def extract_text_content(content: Any) -> str:
    """Extract text from content which can be string or list of message parts"""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        # Extract text from message parts (skip thinking, etc.)
        texts = []
        for part in content:
            if isinstance(part, dict):
                if part.get("type") == "text" and "text" in part:
                    texts.append(part["text"])
            elif isinstance(part, str):
                texts.append(part)
        return " ".join(texts)
    return str(content) if content else ""

def parse_session_file(jsonl_path: Path) -> Optional[Dict[str, Any]]:
    """Parse a Claude Code JSONL session file"""
    messages = []
    metadata = {}

    try:
        with open(jsonl_path) as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)

                # Capture metadata from first entry
                if not metadata:
                    metadata = {
                        "sessionId": entry.get("sessionId"),
                        "timestamp": entry.get("timestamp"),
                        "cwd": entry.get("cwd"),
                        "gitBranch": entry.get("gitBranch", "unknown"),
                    }

                # Collect messages
                if entry.get("type") in ("user", "assistant"):
                    content = entry.get("message", {}).get("content", "")
                    content = extract_text_content(content)
                    if content:  # Only add non-empty messages
                        messages.append({
                            "role": entry.get("type", entry.get("message", {}).get("role")),
                            "content": content,
                            "timestamp": entry.get("timestamp"),
                        })
    except Exception as e:
        print(f"  ⚠️  Error parsing {jsonl_path.name}: {e}")
        return None

    if not messages:
        return None

    return {
        "sessionId": metadata.get("sessionId"),
        "cwd": metadata.get("cwd"),
        "gitBranch": metadata.get("gitBranch"),
        "messages": messages,
        "file_mtime": jsonl_path.stat().st_mtime,
    }

def extract_app_name(cwd: str) -> str:
    """Extract app name from working directory"""
    if not cwd:
        return "unknown"
    # Get last part of path
    return Path(cwd).name or "unknown"

def import_to_pro_mpt(session_data: Dict[str, Any]) -> bool:
    """Import parsed session to pro-mpt database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Ensure table exists
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
                notes TEXT
            )
        """)

        # Extract first user message as the query
        first_user_msg = next(
            (m["content"] for m in session_data["messages"] if m["role"] == "user"),
            None
        )

        if not first_user_msg:
            return False

        # Get first assistant response
        first_assistant_msg = next(
            (m["content"] for m in session_data["messages"] if m["role"] == "assistant"),
            None
        )

        # Build notes from git branch
        notes = f"Branch: {session_data.get('gitBranch', 'unknown')}"

        # Insert
        entry_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        c.execute("""
            INSERT INTO prompts (id, query, model, agent, app, domain, version, response, timestamp, rating, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entry_id,
            first_user_msg[:500],  # Truncate to 500 chars
            "claude",
            "claude-code",
            extract_app_name(session_data.get("cwd")),
            "development",
            "claude-code",
            (first_assistant_msg[:500] if first_assistant_msg else "")[:500],
            timestamp,
            None,  # No rating yet
            notes,
        ))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"  ❌ Error importing to database: {e}")
        return False

def scan_and_import():
    """Scan Claude projects directory for new sessions"""
    ensure_imported_cache()
    imported = get_imported_sessions()

    if not CLAUDE_PROJECTS.exists():
        print("❌ ~/.claude/projects not found")
        return

    new_count = 0

    # Find all JSONL files (these are conversations)
    for jsonl_path in sorted(CLAUDE_PROJECTS.glob("**/[a-f0-9]*.jsonl")):
        session_id = jsonl_path.stem

        # Skip if already imported
        if session_id in imported:
            continue

        print(f"📥 Importing {jsonl_path.parent.name} / {jsonl_path.name}")

        # Parse and import
        session_data = parse_session_file(jsonl_path)
        if session_data and import_to_pro_mpt(session_data):
            mark_imported(session_id)
            new_count += 1
            print(f"   ✅ Imported")
        else:
            print(f"   ⏭️  Skipped (no messages)")

    if new_count > 0:
        print(f"\n✨ Imported {new_count} new session(s) to pro-mpt")
    else:
        print(f"\n✨ Already up to date ({len(imported)} total imported)")

if __name__ == "__main__":
    scan_and_import()
