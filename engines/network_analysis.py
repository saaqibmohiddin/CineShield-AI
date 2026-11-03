"""Manual relationship records for publicly observable entities."""
from database import save_record, get_records

def add_relationship(first, second, relationship, explanation=""):
    details = f"Related entity: {second}\nRelationship: {relationship}\nObservation: {explanation}"
    return save_record("Network", first, details)

def list_relationships():
    return get_records("Network")
