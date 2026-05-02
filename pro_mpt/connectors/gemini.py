import json
from pathlib import Path
from .base import BaseConnector
from typing import Optional, Dict, Any

class GeminiConnector(BaseConnector):
    def __init__(self):
        super().__init__(
            name="gemini-cli",
            source_path=Path.home() / ".gemini" / "tmp",
            cache_name=".imported_gemini_messages"
        )

    def extract_intent(self, query: str) -> str:
        """Heuristic intent extraction"""
        if "?" in query:
            return "question"
        elif any(word in query.lower() for word in ["buy", "call", "do", "fix", "defrost"]):
            return "task"
        elif any(word in query.lower() for word in ["film", "story", "character", "scene"]):
            return "creative"
        return "unknown"

    def scan_and_import(self):
        if not self.source_path.exists():
            return

        imported = self.get_imported_ids()
        new_count = 0

        for logs_path in self.source_path.glob("**/logs.json"):
            app_name = logs_path.parent.parent.name or "unknown"
            try:
                with open(logs_path) as f:
                    messages = json.load(f)
                    for msg in messages:
                        if msg.get("type") != "user":
                            continue
                        
                        session_id = msg.get("sessionId")
                        message_id = msg.get("messageId")
                        tracking_id = f"{session_id}:{message_id}"

                        if tracking_id in imported:
                            continue

                        query = msg.get("message", "")
                        intent = self.extract_intent(query)
                        metadata = {
                            "intent": intent,
                            "session_id": session_id,
                            "connector": "gemini-cli",
                            "agent_interpretation": f"This looks like a {intent}."
                        }

                        if self.import_to_db(
                            query=query,
                            model="gemini",
                            agent="gemini-cli",
                            app=app_name,
                            domain="ambient",
                            timestamp=msg.get("timestamp"),
                            metadata=metadata,
                            notes=f"Ambient capture from {app_name}"
                        ):
                            self.mark_imported(tracking_id)
                            new_count += 1
            except Exception as e:
                print(f"  ⚠️ Error processing {logs_path}: {e}")

        if new_count > 0:
            print(f"✨ [Gemini] Imported {new_count} new prompts")
        return new_count
