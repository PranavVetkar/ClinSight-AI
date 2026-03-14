"""
Local SQLite database replacing Firebase/Firestore.
Data is stored in backend/local_data/app.db
Three tables: users, documents, queries — each storing rows as JSON blobs.
"""
import json
import sqlite3
import os
from typing import Optional, List, Dict, Any

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "local_data")
DB_PATH = os.path.join(DB_DIR, "app.db")


def _get_conn() -> sqlite3.Connection:
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables if they don't exist. Called at app startup."""
    with _get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                uid     TEXT PRIMARY KEY,
                email   TEXT UNIQUE NOT NULL,
                data    TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS documents (
                doc_id  TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                data    TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_documents_user_id ON documents(user_id);

            CREATE TABLE IF NOT EXISTS queries (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                doc_id  TEXT NOT NULL,
                data    TEXT NOT NULL
            );
        """)


# ── Users ──────────────────────────────────────────────────────────────────────

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT data FROM users WHERE email = ?", (email,)
        ).fetchone()
    return json.loads(row["data"]) if row else None


def create_user(user: Dict[str, Any]) -> None:
    with _get_conn() as conn:
        conn.execute(
            "INSERT INTO users (uid, email, data) VALUES (?, ?, ?)",
            (user["uid"], user["email"], json.dumps(user)),
        )


# ── Documents ─────────────────────────────────────────────────────────────────

def create_document(doc: Dict[str, Any]) -> None:
    with _get_conn() as conn:
        conn.execute(
            "INSERT INTO documents (doc_id, user_id, data) VALUES (?, ?, ?)",
            (doc["doc_id"], doc["user_id"], json.dumps(doc)),
        )


def get_document(doc_id: str) -> Optional[Dict[str, Any]]:
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT data FROM documents WHERE doc_id = ?", (doc_id,)
        ).fetchone()
    return json.loads(row["data"]) if row else None


def list_user_documents(user_id: str) -> List[Dict[str, Any]]:
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT data FROM documents WHERE user_id = ? ORDER BY rowid DESC",
            (user_id,),
        ).fetchall()
    return [json.loads(r["data"]) for r in rows]


def delete_document(doc_id: str) -> None:
    with _get_conn() as conn:
        conn.execute("DELETE FROM documents WHERE doc_id = ?", (doc_id,))


# ── Queries ───────────────────────────────────────────────────────────────────

def create_query(query: Dict[str, Any]) -> None:
    with _get_conn() as conn:
        conn.execute(
            "INSERT INTO queries (user_id, doc_id, data) VALUES (?, ?, ?)",
            (query["user_id"], query["doc_id"], json.dumps(query)),
        )
