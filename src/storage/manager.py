"""
Storage manager - handles saving and loading interview sessions
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

from src.config import Config


class StorageManager:
    """Handles storing, loading, and summarizing interview sessions."""

    def __init__(self):
        # Ensure directories exist
        os.makedirs(Config.INTERVIEWS_DIR, exist_ok=True)

    # ------------------------------------------------------------
    # Save Interview
    # ------------------------------------------------------------
    def save_interview(self, session_data: Dict) -> str:
        """
        Save interview session to a JSON file.
        """

        session_id = session_data.get(
            "session_id",
            datetime.now().strftime("%Y%m%d_%H%M%S")
        )
        role = session_data.get("role", "unknown")

        filename = f"{session_id}_{role}.json"
        filepath = os.path.join(Config.INTERVIEWS_DIR, filename)

        session_data["saved_at"] = datetime.now().isoformat()

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)

            return filepath

        except Exception as e:
            print(f"[StorageManager] Error saving session: {e}")
            return ""

    # ------------------------------------------------------------
    # Load Interview by Session ID
    # ------------------------------------------------------------
    def load_interview(self, session_id: str) -> Optional[Dict]:
        """
        Load a saved interview session using its session_id.
        """

        try:
            for filename in os.listdir(Config.INTERVIEWS_DIR):
                if filename.startswith(session_id) and filename.endswith(".json"):
                    filepath = os.path.join(Config.INTERVIEWS_DIR, filename)
                    with open(filepath, "r", encoding="utf-8") as f:
                        return json.load(f)
        except Exception as e:
            print(f"[StorageManager] Error loading session: {e}")

        return None

    # ------------------------------------------------------------
    # List Interview Summaries
    # ------------------------------------------------------------
    def list_interviews(self, limit: int = 50) -> List[Dict]:
        """
        Return list of interview summaries (newest first).
        """

        summaries = []

        try:
            files = [
                f for f in os.listdir(Config.INTERVIEWS_DIR)
                if f.endswith(".json")
            ]

            # Sort by last modified time (descending)
            files.sort(
                key=lambda x: os.path.getmtime(
                    os.path.join(Config.INTERVIEWS_DIR, x)
                ),
                reverse=True
            )

            for filename in files[:limit]:
                filepath = os.path.join(Config.INTERVIEWS_DIR, filename)

                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    summary = {
                        "session_id": data.get("session_id", "unknown"),
                        "role": data.get("role", "unknown"),
                        "persona": data.get("persona", "normal"),
                        "timestamp": data.get("timestamp_start", ""),
                        "duration_seconds": data.get("duration_seconds", 0),
                        "overall_score": data.get("feedback", {}).get("overall_score", 0),
                        "question_count": len([
                            m for m in data.get("messages", [])
                            if m.get("role") == "interviewer"
                        ]),
                        "filename": filename,
                    }

                    summaries.append(summary)

                except Exception as e:
                    print(f"[StorageManager] Error reading file {filename}: {e}")
                    continue

        except Exception as e:
            print(f"[StorageManager] Error listing sessions: {e}")

        return summaries

    # ------------------------------------------------------------
    # Delete a saved interview
    # ------------------------------------------------------------
    def delete_interview(self, session_id: str) -> bool:
        """
        Delete interview session by its session ID.
        """

        for filename in os.listdir(Config.INTERVIEWS_DIR):
            if filename.startswith(session_id) and filename.endswith(".json"):
                try:
                    os.remove(
                        os.path.join(Config.INTERVIEWS_DIR, filename)
                    )
                    return True
                except Exception as e:
                    print(f"[StorageManager] Error deleting session: {e}")
                    return False

        return False

    # ------------------------------------------------------------
    # Generate Stats for Sidebar
    # ------------------------------------------------------------
    def get_stats(self) -> Dict:
        """
        Return high-level statistics about interview history.
        """

        sessions = self.list_interviews(limit=500)

        if not sessions:
            return {
                "total_interviews": 0,
                "average_score": 0,
                "roles_distribution": {},
                "latest_interview": None
            }

        total = len(sessions)

        avg_score = sum(
            s.get("overall_score", 0) for s in sessions
        ) / total

        # Role distribution
        roles = {}
        for s in sessions:
            role = s.get("role", "unknown")
            roles[role] = roles.get(role, 0) + 1

        return {
            "total_interviews": total,
            "average_score": round(avg_score, 2),
            "roles_distribution": roles,
            "latest_interview": sessions[0]
        }
