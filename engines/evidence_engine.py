from datetime import datetime
from pathlib import Path
from database import connect, get_evidence
from config import EVIDENCE_DIR
from security import sha256_bytes, safe_filename

def preserve_evidence(title, filename, data, notes=""):
    digest = sha256_bytes(data)
    stored_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}_{safe_filename(filename)}"
    destination = EVIDENCE_DIR / stored_name
    destination.write_bytes(data)
    with connect() as con:
        cur = con.execute(
            """INSERT INTO evidence(title,filename,stored_path,file_hash,notes,created_at)
               VALUES(?,?,?,?,?,?)""",
            (title, filename, str(destination), digest, notes,
             datetime.now().isoformat(timespec="seconds"))
        )
        return cur.lastrowid, digest

def list_evidence():
    return get_evidence()
