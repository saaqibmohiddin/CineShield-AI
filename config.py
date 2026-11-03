
from pathlib import Path

# =====================================
# CINESHIELD AI - CONFIGURATION
# =====================================

BASE_DIR = Path(__file__).resolve().parent

# Database
DATABASE_PATH = BASE_DIR / "cineshield.db"

# Application folders
DATA_DIR = BASE_DIR / "data"
SAMPLES_DIR = DATA_DIR / "authorized_samples"
EVIDENCE_DIR = DATA_DIR / "evidence"
REPORTS_DIR = DATA_DIR / "reports"
WATERMARKS_DIR = DATA_DIR / "watermarks"

# Supported movie formats
VIDEO_EXTENSIONS = [
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".webm"
]

# Supported audio formats
AUDIO_EXTENSIONS = [
    ".mp3",
    ".wav",
    ".aac",
    ".flac",
    ".m4a"
]

# Upload limits (in MB)
MAX_VIDEO_SIZE_MB = 2048
MAX_AUDIO_SIZE_MB = 512

# Application settings
APP_NAME = "CINESHIELD AI"
APP_VERSION = "1.0.0"
APP_ENVIRONMENT = "Development"

# Create required directories
for folder in [
    DATA_DIR,
    SAMPLES_DIR,
    EVIDENCE_DIR,
    REPORTS_DIR,
    WATERMARKS_DIR
]:
    folder.mkdir(parents=True, exist_ok=True)