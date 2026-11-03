import sqlite3
from datetime import datetime
from config import DB_PATH

def connect():
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con

def initialize_database():
    schema = """
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        language TEXT,
        release_year TEXT,
        reference_hash TEXT,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS investigations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_title TEXT NOT NULL,
        uploaded_filename TEXT NOT NULL,
        file_hash TEXT NOT NULL,
        result TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        module TEXT NOT NULL,
        title TEXT NOT NULL,
        details TEXT,
        status TEXT NOT NULL DEFAULT 'Pending',
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS evidence (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        filename TEXT NOT NULL,
        stored_path TEXT,
        file_hash TEXT NOT NULL,
        notes TEXT,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_title TEXT NOT NULL,
        movie_title TEXT NOT NULL,
        priority TEXT NOT NULL,
        status TEXT NOT NULL,
        investigator TEXT,
        created_at TEXT NOT NULL
    );
    """
    with connect() as con:
        con.executescript(schema)
        # Safe migration for databases created by the earlier single-file app.
        evidence_columns = {
            row["name"] for row in con.execute("PRAGMA table_info(evidence)").fetchall()
        }
        if "stored_path" not in evidence_columns:
            con.execute("ALTER TABLE evidence ADD COLUMN stored_path TEXT")

def save_record(module, title, details, status="Pending"):
    with connect() as con:
        cur = con.execute(
            """INSERT INTO records(module,title,details,status,created_at)
               VALUES(?,?,?,?,?)""",
            (module, title, details, status, datetime.now().isoformat(timespec="seconds"))
        )
        return cur.lastrowid

def get_records(module=None):
    with connect() as con:
        if module:
            rows = con.execute(
                "SELECT * FROM records WHERE module=? ORDER BY id DESC", (module,)
            ).fetchall()
        else:
            rows = con.execute("SELECT * FROM records ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]

def get_movies():
    with connect() as con:
        return [dict(r) for r in con.execute("SELECT * FROM movies ORDER BY id DESC")]

def get_scans():
    with connect() as con:
        return [dict(r) for r in con.execute("SELECT * FROM investigations ORDER BY id DESC")]

def get_cases():
    with connect() as con:
        return [dict(r) for r in con.execute("SELECT * FROM cases ORDER BY id DESC")]

def get_evidence():
    with connect() as con:
        return [dict(r) for r in con.execute("SELECT * FROM evidence ORDER BY id DESC")]
