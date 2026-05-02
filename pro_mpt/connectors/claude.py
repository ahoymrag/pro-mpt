import json
from pathlib import Path
from .base import BaseConnector
from typing import Optional, Dict, Any

class ClaudeConnector(BaseConnector):
    def __init__(self):
        super().__init__(
            name="claude-code",
            source_path=Path.home() / ".claude" / "projects",
            cache_name=".imported_sessions"
        )

    def extract_text(self, content: Any) -> str:
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            texts = []
            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    texts.append(part.get("text", ""))
                elif isinstance(part, str):
                    texts.append(part)
            return " ".join(texts)
        return str(content)

    def scan_and_import(self):
        if not self.source_path.exists():
            return

        imported = self.get_imported_ids()
        new_count = 0

        for jsonl_path in self.source_path.glob("**/[a-f0-9]*.jsonl"):
            session_id = jsonl_path.stem
            if session_id in imported:
                continue

            messages = []
            metadata_ctx = {}
            try:
                with open(jsonl_path) as f:
                    for line in f:
                        if not line.strip(): continue
                        entry = json.loads(line)
                        if not metadata_ctx:
                            metadata_ctx = {
                                "cwd": entry.get("cwd"),
                                "gitBranch": entry.get("gitBranch", "unknown")
                            }
                        if entry.get("type") in ("user", "assistant"):
                            content = self.extract_text(entry.get("message", {}).get("content", ""))
                            if content:
                                messages.append({
                                    "role": entry.get("type"),
                                    "content": content,
                                    "timestamp": entry.get("timestamp")
                                })
                
                if not messages: continue

                # Use first user message as primary query
                first_user = next((m for m in messages if m["role"] == "user"), None)
                first_assistant = next((m for m in messages if m["role"] == "assistant"), None)
                
                if not first_user: continue

                metadata = {
                    "session_id": session_id,
                    "connector": "claude-code",
                    "git_branch": metadata_ctx.get("gitBranch"),
                    "full_session": True
                }

                cwd = metadata_ctx.get("cwd") or "unknown"
                app_name = Path(cwd).name or "unknown"

                if self.import_to_db(
                    query=first_user["content"],
                    model="claude",
                    agent="claude-code",
                    app=app_name,
                    domain="development",
                    timestamp=first_user["timestamp"],
                    metadata=metadata,
                    response=first_assistant["content"] if first_assistant else "",
                    notes=f"Branch: {metadata_ctx.get('gitBranch')}"
                ):
                    self.mark_imported(session_id)
                    new_count += 1
            except Exception as e:
                print(f"  ⚠️ Error processing {jsonl_path}: {e}")

        if new_count > 0:
            print(f"✨ [Claude] Imported {new_count} new sessions")
        return new_count
