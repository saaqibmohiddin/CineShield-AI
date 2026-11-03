from datetime import datetime
from database import get_movies, get_scans, get_cases, get_evidence

def build_report():
    lines = [
        "CINESHIELD AI - INVESTIGATION REPORT",
        "=" * 52,
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "NOTICE: Records are investigative leads and require human review.",
        "An exact SHA-256 match indicates identical file bytes only.",
        "",
        "MOVIES", "-" * 30
    ]
    for m in get_movies():
        lines.append(f'#{m["id"]} | {m["title"]} | {m["language"]} | {m["release_year"]} | {m["reference_hash"]}')
    lines += ["", "SCANS", "-" * 30]
    for s in get_scans():
        lines.append(f'#{s["id"]} | {s["movie_title"]} | {s["uploaded_filename"]} | {s["result"]} | {s["created_at"]}')
    lines += ["", "CASES", "-" * 30]
    for c in get_cases():
        lines.append(f'#{c["id"]} | {c["case_title"]} | {c["movie_title"]} | {c["priority"]} | {c["status"]}')
    lines += ["", "EVIDENCE", "-" * 30]
    for e in get_evidence():
        lines.append(f'#{e["id"]} | {e["title"]} | {e["filename"]} | SHA256={e["file_hash"]}')
    return "\n".join(lines)
