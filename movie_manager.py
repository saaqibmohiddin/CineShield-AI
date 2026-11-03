from datetime import datetime
from database import connect, get_movies
from security import sha256_bytes

def register_movie(title, language, release_year, file_bytes):
    if not title.strip():
        raise ValueError("Movie title is required.")
    digest = sha256_bytes(file_bytes)
    with connect() as con:
        cur = con.execute(
            """INSERT INTO movies(title,language,release_year,reference_hash,created_at)
               VALUES(?,?,?,?,?)""",
            (title.strip(), language, str(release_year).strip(), digest,
             datetime.now().isoformat(timespec="seconds"))
        )
        return cur.lastrowid, digest

def compare_candidate(movie_id, filename, candidate_bytes):
    from datetime import datetime
    digest = sha256_bytes(candidate_bytes)
    with connect() as con:
        movie = con.execute("SELECT * FROM movies WHERE id=?", (movie_id,)).fetchone()
        if movie is None:
            raise ValueError("Selected movie was not found.")
        result = "EXACT FILE MATCH" if digest == movie["reference_hash"] else "NO EXACT FILE MATCH"
        con.execute(
            """INSERT INTO investigations(movie_title,uploaded_filename,file_hash,result,created_at)
               VALUES(?,?,?,?,?)""",
            (movie["title"], filename, digest, result,
             datetime.now().isoformat(timespec="seconds"))
        )
    return movie["title"], digest, result
