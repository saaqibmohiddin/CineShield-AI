"""Watermark assignment registry helper.

This records a watermark ID and its authorized recipient. It does not embed
or extract a watermark from video files.
"""
from database import save_record, get_records

def register_watermark(movie, watermark_id, recipient, notes=""):
    details = f"Movie: {movie}\nRecipient: {recipient}\nNotes: {notes}"
    return save_record("Watermark", watermark_id, details)

def list_watermarks():
    return get_records("Watermark")
