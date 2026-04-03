import sqlite3
import threading
import time
from pathlib import Path

_SCHEMA = (Path(__file__).parent / "schema.sql").read_text()


class Vault:
    """
    Session-scoped PII mapping store backed by SQLite.

    - db_path=""  → in-memory database (default, recommended).
      Data never touches disk and is lost when the process ends.
    - db_path="/path/to/file.db" → persistent on-disk database.
      Use only when session continuity across restarts is required.
    """

    def __init__(self, db_path: str = "", ttl_seconds: int = 3600) -> None:
        self._ttl = ttl_seconds
        target = db_path if db_path else ":memory:"
        self._conn = sqlite3.connect(target, check_same_thread=False)
        self._lock = threading.Lock()
        with self._lock:
            self._conn.executescript(_SCHEMA)
            self._conn.commit()

    def store(self, session_id: str, token: str, value: str, pii_type: str) -> None:
        now = int(time.time())
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO mappings VALUES (?,?,?,?,?,?)",
                (session_id, token, value, pii_type, now, now + self._ttl),
            )
            self._conn.commit()

    def get_value(self, session_id: str, token: str) -> str | None:
        now = int(time.time())
        with self._lock:
            row = self._conn.execute(
                "SELECT value FROM mappings WHERE session_id=? AND token=? AND expires_at>?",
                (session_id, token, now),
            ).fetchone()
        return row[0] if row else None

    def get_token(self, session_id: str, value: str, pii_type: str) -> str | None:
        now = int(time.time())
        with self._lock:
            row = self._conn.execute(
                "SELECT token FROM mappings "
                "WHERE session_id=? AND value=? AND pii_type=? AND expires_at>?",
                (session_id, value, pii_type, now),
            ).fetchone()
        return row[0] if row else None

    def cleanup_expired(self) -> None:
        with self._lock:
            self._conn.execute(
                "DELETE FROM mappings WHERE expires_at<?", (int(time.time()),)
            )
            self._conn.commit()
