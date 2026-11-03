"""Manual public-source record helper. No scraping or access-control bypass."""
from database import save_record, get_records
from security import valid_http_url

def add_public_source(movie, url, platform, notes=""):
    if not valid_http_url(url):
        raise ValueError("Enter a valid public http:// or https:// URL.")
    return save_record("Source", movie, f"URL: {url}\nPlatform: {platform}\nNotes: {notes}")

def list_sources():
    return get_records("Source")
