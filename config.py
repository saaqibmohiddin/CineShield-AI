from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "cineshield.db"
DATA_DIR = BASE_DIR / "data"
EVIDENCE_DIR = BASE_DIR / "evidence"
REPORTS_DIR = BASE_DIR / "reports"
SAMPLES_DIR = BASE_DIR / "samples"
WATERMARKS_DIR = BASE_DIR / "watermarks"

for folder in (DATA_DIR, EVIDENCE_DIR, REPORTS_DIR, SAMPLES_DIR, WATERMARKS_DIR):
    folder.mkdir(parents=True, exist_ok=True)

APP_NAME = "CINESHIELD AI"
APP_VERSION = "2.1 Modular Development Edition"
MAX_UPLOAD_MB = 200
