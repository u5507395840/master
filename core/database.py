import sqlite3
import os
from typing import Dict, List


class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_db()

    def _ensure_db(self):
        dirpath = os.path.dirname(self.db_path)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS campaigns (
                id TEXT PRIMARY KEY,
                artist TEXT,
                track TEXT,
                genre TEXT,
                status TEXT,
                created_at TEXT
            )
            """
        )
        conn.commit()
        conn.close()

    def save_campaign(self, campaign: Dict) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute(
                "INSERT OR REPLACE INTO campaigns (id, artist, track, genre, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    campaign.get("id"),
                    campaign.get("artist"),
                    campaign.get("track"),
                    campaign.get("genre"),
                    campaign.get("status"),
                    campaign.get("created_at"),
                ),
            )
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    def get_campaign(self, campaign_id: str) -> Dict:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return dict(row)
        return None

    def get_all_campaigns(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM campaigns")
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def update_campaign_status(self, campaign_id: str, new_status: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("UPDATE campaigns SET status = ? WHERE id = ?", (new_status, campaign_id))
        updated = cur.rowcount
        conn.commit()
        conn.close()
        return updated > 0

    def get_stats(self) -> Dict:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM campaigns")
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM campaigns WHERE status = 'active' OR status = 'ACTIVE'")
        active = cur.fetchone()[0]
        conn.close()
        return {"total_campaigns": int(total), "active_campaigns": int(active)}
