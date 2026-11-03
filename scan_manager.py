"""File-level scan orchestration.

An exact SHA-256 match means byte-for-byte identity. Different hashes do not
rule out a visually or acoustically similar movie.
"""
from movie_manager import compare_candidate

def analyze_file(movie_id, filename, data):
    return compare_candidate(movie_id, filename, data)
