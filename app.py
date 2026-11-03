
import streamlit as st
import sqlite3
import hashlib
import json
from datetime import datetime
from pathlib import Path

# =========================================================
# CINESHIELD AI - SINGLE FILE APPLICATION
# =========================================================

DB = "cineshield.db"

st.set_page_config(
    page_title="CINESHIELD AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- DESIGN -----------------------------

st.markdown("""
<style>
.stApp {
    background: #080D1A;
    color: #E8EEFF;
}
[data-testid="stSidebar"] {
    background: #101A32;
    border-right: 1px solid #263B65;
}
h1, h2, h3 {
    color: #F2F5FF !important;
}
p, label, span {
    color: #D6DDF0;
}
div[data-testid="stMetric"] {
    background: #111E39;
    border: 1px solid #293F68;
    padding: 18px;
    border-radius: 12px;
}
.stButton > button {
    background: #6538D6;
    color: white;
    border-radius: 8px;
    border: none;
    min-height: 40px;
}
.stButton > button:hover {
    background: #8058F0;
    color: white;
}
section[data-testid="stFileUploader"] {
    background: #101E39;
    border-radius: 10px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- DATABASE --------------------------

def connect():
    return sqlite3.connect(DB)

def initialize_database():
    con = connect()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            language TEXT,
            release_year TEXT,
            reference_hash TEXT,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS investigations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_title TEXT,
            uploaded_filename TEXT,
            file_hash TEXT,
            result TEXT,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module TEXT NOT NULL,
            title TEXT NOT NULL,
            details TEXT,
            status TEXT,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS evidence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            filename TEXT,
            file_hash TEXT,
            notes TEXT,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_title TEXT,
            movie_title TEXT,
            priority TEXT,
            status TEXT,
            investigator TEXT,
            created_at TEXT
        )
    """)

    con.commit()
    con.close()

def save_record(module, title, details, status="Pending"):
    con = connect()
    con.execute("""
        INSERT INTO records
        (module, title, details, status, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        title,
        title,
        details,
        status,
        datetime.now().isoformat(timespec="seconds")
    ))
    con.commit()
    con.close()

def get_records(module):
    con = connect()
    rows = con.execute("""
        SELECT id, title, details, status, created_at
        FROM records
        WHERE module = ?
        ORDER BY id DESC
    """, (module,)).fetchall()
    con.close()
    return rows

def get_movies():
    con = connect()
    rows = con.execute(
        "SELECT * FROM movies ORDER BY id DESC"
    ).fetchall()
    con.close()
    return rows

def get_scans():
    con = connect()
    rows = con.execute(
        "SELECT * FROM investigations ORDER BY id DESC"
    ).fetchall()
    con.close()
    return rows

def get_cases():
    con = connect()
    rows = con.execute(
        "SELECT * FROM cases ORDER BY id DESC"
    ).fetchall()
    con.close()
    return rows

def get_evidence():
    con = connect()
    rows = con.execute(
        "SELECT * FROM evidence ORDER BY id DESC"
    ).fetchall()
    con.close()
    return rows

def sha256(data):
    return hashlib.sha256(data).hexdigest()

initialize_database()

# -------------------- NAVIGATION ------------------------

PAGES = [
    "Dashboard",
    "Movie Registry",
    "Scan Center",
    "Video Forensics",
    "Audio Forensics",
    "Watermark Center",
    "Source Discovery",
    "Uploader Intelligence",
    "Global Intelligence",
    "Network Analysis",
    "AI Investigation Assistant",
    "Risk Prediction",
    "Evidence Vault",
    "Case Management",
    "Forensic Reports",
    "Alert Center",
    "Organization Management",
    "Multilingual Intelligence",
    "Distribution Intelligence",
    "Admin Settings"
]

st.sidebar.markdown("# 🎬 CINESHIELD AI")
st.sidebar.caption("MOVIE PIRACY INTELLIGENCE PLATFORM")
st.sidebar.divider()

page = st.sidebar.radio("MAIN NAVIGATION", PAGES)

st.sidebar.divider()
st.sidebar.caption("CINESHIELD AI | Development Edition")
st.sidebar.caption("Authorized investigation use only")

# -------------------- HEADER ----------------------------

st.markdown(
    "<h1>🎬 CINESHIELD AI</h1>"
    "<p>Advanced Movie Intelligence & Digital Investigation Platform</p>",
    unsafe_allow_html=True
)

st.divider()

# =========================================================
# 1. DASHBOARD
# =========================================================

if page == "Dashboard":

    movies = get_movies()
    scans = get_scans()
    cases = get_cases()
    evidence = get_evidence()

    confirmed = sum(
        1 for scan in scans
        if scan[4] == "EXACT FILE MATCH"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Registered Movies", len(movies))
    c2.metric("Files Analyzed", len(scans))
    c3.metric("Exact File Matches", confirmed)
    c4.metric("Evidence Records", len(evidence))

    st.subheader("Intelligence Overview")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### 🎥 Movie Registry")
        st.write(f"Total movies: **{len(movies)}**")

    with c2:
        st.markdown("### 📁 Investigation Cases")
        st.write(f"Total cases: **{len(cases)}**")

    st.subheader("Recent Scans")

    if scans:
        st.dataframe(
            [{
                "Movie": x[1],
                "Filename": x[2],
                "Result": x[4],
                "Date": x[5]
            } for x in scans[:10]],
            use_container_width=True
        )
    else:
        st.info("No scans available.")

    st.info(
        "Detection metrics currently represent recorded file-hash "
        "comparisons, not verified piracy incidents."
    )

# =========================================================
# 2. MOVIE REGISTRY
# =========================================================

elif page == "Movie Registry":

    st.subheader("🎥 Movie Registry")

    with st.form("movie_registration"):

        title = st.text_input("Movie Title")

        language = st.selectbox(
            "Language",
            [
                "Telugu", "Hindi", "Tamil", "Malayalam",
                "Kannada", "Bengali", "English", "Other"
            ]
        )

        year = st.text_input("Release Year")

        file = st.file_uploader(
            "Authorized Reference Sample",
            type=["mp4", "mkv", "mov", "avi", "mp3", "wav"]
        )

        submit = st.form_submit_button("Register Movie")

        if submit:

            if not title.strip() or not file:
                st.error("Enter a movie title and upload an authorized sample.")
            else:

                file_hash = sha256(file.getvalue())

                con = connect()
                con.execute("""
                    INSERT INTO movies
                    (title, language, release_year, reference_hash, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    title.strip(),
                    language,
                    year,
                    file_hash,
                    datetime.now().isoformat(timespec="seconds")
                ))
                con.commit()
                con.close()

                st.success("Movie registered successfully!")
                st.code(file_hash)

    st.divider()
    st.subheader("Registered Movies")

    movies = get_movies()

    for movie in movies:
        with st.expander(movie[1]):
            st.write("Language:", movie[2])
            st.write("Release year:", movie[3])
            st.write("SHA-256:", movie[4])
            st.write("Created:", movie[5])

# =========================================================
# 3. SCAN CENTER
# =========================================================

elif page == "Scan Center":

    st.subheader("🔍 Movie Scan Center")

    movies = get_movies()

    if not movies:
        st.warning("Register a movie first.")
    else:

        options = {
            f"{m[1]} - {m[2]}": m for m in movies
        }

        selected = st.selectbox(
            "Select Movie",
            list(options.keys())
        )

        candidate = st.file_uploader(
            "Upload a lawfully obtained comparison sample",
            type=["mp4", "mkv", "mov", "avi", "mp3", "wav"]
        )

        if st.button("Analyze File"):

            if not candidate:
                st.error("Upload a file first.")
            else:

                movie = options[selected]
                candidate_hash = sha256(candidate.getvalue())

                if candidate_hash == movie[4]:
                    result = "EXACT FILE MATCH"
                    st.success("Exact file hash match detected.")
                else:
                    result = "NO EXACT FILE MATCH"
                    st.warning(
                        "Hashes differ. The video content may still be similar."
                    )

                con = connect()
                con.execute("""
                    INSERT INTO investigations
                    (movie_title, uploaded_filename, file_hash, result, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    movie[1],
                    candidate.name,
                    candidate_hash,
                    result,
                    datetime.now().isoformat(timespec="seconds")
                ))
                con.commit()
                con.close()

                st.write("Movie:", movie[1])
                st.write("Result:", result)
                st.write("SHA-256:", candidate_hash)

# =========================================================
# 4. VIDEO FORENSICS
# =========================================================

elif page == "Video Forensics":

    st.subheader("🎞️ Video Forensics")

    st.info(
        "Advanced frame fingerprinting and scene matching are planned "
        "for the next AI-engine integration."
    )

    video = st.file_uploader(
        "Upload an authorized video sample",
        type=["mp4", "mkv", "mov", "avi"]
    )

    if video:
        data = video.getvalue()
        st.write("Filename:", video.name)
        st.write("Size:", round(len(data) / 1024 / 1024, 2), "MB")
        st.write("SHA-256:")
        st.code(sha256(data))
        st.caption("File identity recorded. No scene similarity analysis performed.")

# =========================================================
# 5. AUDIO FORENSICS
# =========================================================

elif page == "Audio Forensics":

    st.subheader("🎧 Audio Forensics")

    st.info(
        "Audio fingerprint matching, speech recognition and soundtrack "
        "comparison require additional audio-processing engines."
    )

    audio = st.file_uploader(
        "Upload an authorized audio sample",
        type=["mp3", "wav", "ogg"]
    )

    if audio:
        data = audio.getvalue()
        st.write("Filename:", audio.name)
        st.write("Size:", round(len(data) / 1024, 2), "KB")
        st.code(sha256(data))

# =========================================================
# 6. WATERMARK CENTER
# =========================================================

elif page == "Watermark Center":

    st.subheader("💧 Digital Watermark Center")

    st.write(
        "Maintain records of watermarks assigned to authorized "
        "distribution copies."
    )

    with st.form("watermark_form"):

        movie = st.text_input("Movie Name")
        watermark_id = st.text_input("Watermark Identifier")
        recipient = st.text_input("Authorized Recipient")
        notes = st.text_area("Distribution Details")

        submit = st.form_submit_button("Save Watermark Record")

        if submit:
            if movie.strip() and watermark_id.strip():
                save_record(
                    "Watermark",
                    watermark_id,
                    f"Movie: {movie}\nRecipient: {recipient}\n{notes}"
                )
                st.success("Watermark record saved.")
            else:
                st.error("Movie and watermark ID are required.")

    for item in get_records("Watermark"):
        with st.expander(item[1]):
            st.write(item[2])

# =========================================================
# 7. SOURCE DISCOVERY
# =========================================================

elif page == "Source Discovery":

    st.subheader("🌐 Public Source Discovery")

    st.info(
        "This module records sources submitted by investigators. "
        "Automatic discovery requires permitted search or platform APIs."
    )

    with st.form("source_form"):

        movie = st.text_input("Movie Name")
        url = st.text_input("Public Source URL")
        platform = st.text_input("Platform or Website")
        notes = st.text_area("Observation Details")

        submit = st.form_submit_button("Save Source Record")

        if submit:

            if movie.strip() and url.strip():
                save_record(
                    "Source",
                    movie,
                    f"URL: {url}\nPlatform: {platform}\nNotes: {notes}"
                )
                st.success("Source record saved.")
            else:
                st.error("Movie and source URL are required.")

    for item in get_records("Source"):
        with st.expander(item[1]):
            st.write(item[2])

# =========================================================
# 8. UPLOADER INTELLIGENCE
# =========================================================

elif page == "Uploader Intelligence":

    st.subheader("👤 Public Uploader Intelligence")

    st.warning(
        "Record publicly visible account information only. "
        "Do not infer real-world identity from an account name."
    )

    with st.form("uploader_form"):

        username = st.text_input("Public Username")
        platform = st.text_input("Platform")
        profile = st.text_input("Public Profile URL")
        observation = st.text_area("Publicly Observed Activity")

        submit = st.form_submit_button("Save Observation")

        if submit:
            if username.strip():
                save_record(
                    "Uploader",
                    username,
                    f"Platform: {platform}\nProfile: {profile}\n"
                    f"Observation: {observation}"
                )
                st.success("Observation saved.")
            else:
                st.error("Enter a public username.")

    for item in get_records("Uploader"):
        with st.expander(item[1]):
            st.write(item[2])

# =========================================================
# 9. GLOBAL INTELLIGENCE
# =========================================================

elif page == "Global Intelligence":

    st.subheader("🌍 Global Intelligence")

    st.info(
        "This page currently stores investigator-submitted geographic "
        "observations. It does not track users or establish their location."
    )

    with st.form("global_form"):

        country = st.text_input("Country or Region")
        movie = st.text_input("Movie")
        language = st.text_input("Language")
        observation = st.text_area("Intelligence Observation")

        submit = st.form_submit_button("Save Intelligence")

        if submit:
            if country.strip() and movie.strip():
                save_record(
                    "Global",
                    movie,
                    f"Region: {country}\nLanguage: {language}\n"
                    f"Observation: {observation}"
                )
                st.success("Global intelligence record saved.")

    for item in get_records("Global"):
        with st.expander(item[1]):
            st.write(item[2])

# =========================================================
# 10. NETWORK ANALYSIS
# =========================================================

elif page == "Network Analysis":

    st.subheader("🔗 Distribution Network Analysis")

    st.info(
        "Store relationships between public sources, accounts and "
        "investigation records. Interactive graph visualization is a "
        "future integration."
    )

    with st.form("network_form"):

        first = st.text_input("First Public Entity")
        second = st.text_input("Related Public Entity")
        relationship = st.text_input("Observed Relationship")
        explanation = st.text_area("Supporting Observation")

        submit = st.form_submit_button("Save Relationship")

        if submit:
            if first.strip() and second.strip():
                save_record(
                    "Network",
                    first,
                    f"Related entity: {second}\n"
                    f"Relationship: {relationship}\n"
                    f"Observation: {explanation}"
                )
                st.success("Relationship saved.")

    for item in get_records("Network"):
        with st.expander(item[1]):
            st.write(item[2])

# =========================================================
# 11. AI INVESTIGATION ASSISTANT
# =========================================================

elif page == "AI Investigation Assistant":

    st.subheader("🤖 AI Investigation Assistant")

    st.info(
        "This initial assistant searches locally stored case information. "
        "It is not yet connected to an LLM."
    )

    question = st.text_input(
        "Ask about your investigation records"
    )

    if st.button("Search Records"):

        if question.strip():

            query = question.lower()

            matches = []

            for module in [
                "Watermark", "Source", "Uploader",
                "Global", "Network"
            ]:
                for record in get_records(module):
                    content = (
                        str(record[1]) + " " + str(record[2])
                    ).lower()

                    if any(
                        word in content
                        for word in query.split()
                        if len(word) > 2
                    ):
                        matches.append((module, record))

            if matches:
                st.success(f"{len(matches)} matching records found.")

                for module, record in matches:
                    st.markdown(f"**{module}: {record[1]}**")
                    st.write(record[2])
            else:
                st.info("No matching stored records found.")

# =========================================================
# 12. RISK PREDICTION
# =========================================================

elif page == "Risk Prediction":

    st.subheader("📊 Investigation Priority Analysis")

    cases = get_cases()

    high = sum(1 for c in cases if c[3] == "High")
    medium = sum(1 for c in cases if c[3] == "Medium")
    low = sum(1 for c in cases if c[3] == "Low")

    a, b, c = st.columns(3)

    a.metric("High Priority", high)
    b.metric("Medium Priority", medium)
    c.metric("Low Priority", low)

    st.info(
        "These are manually assigned investigation priorities, "
        "not machine-learning predictions."
    )

    if cases:
        st.dataframe(
            [{
                "Case": x[1],
                "Movie": x[2],
                "Priority": x[3],
                "Status": x[4]
            } for x in cases],
            use_container_width=True
        )

# =========================================================
# 13. EVIDENCE VAULT
# =========================================================

elif page == "Evidence Vault":

    st.subheader("🔐 Digital Evidence Vault")

    with st.form("evidence_form"):

        title = st.text_input("Evidence Title")

        file = st.file_uploader(
            "Upload an authorized evidence file"
        )

        notes = st.text_area("Evidence Description")

        submit = st.form_submit_button("Preserve Evidence Record")

        if submit:

            if title.strip() and file:

                file_hash = sha256(file.getvalue())

                con = connect()
                con.execute("""
                    INSERT INTO evidence
                    (title, filename, file_hash, notes, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    title,
                    file.name,
                    file_hash,
                    notes,
                    datetime.now().isoformat(timespec="seconds")
                ))
                con.commit()
                con.close()

                st.success("Evidence record created.")
                st.code(file_hash)

            else:
                st.error("Enter a title and upload a file.")

    st.divider()

    for item in get_evidence():
        with st.expander(item[1]):
            st.write("Filename:", item[2])
            st.write("SHA-256:", item[3])
            st.write("Notes:", item[4])
            st.write("Date:", item[5])

# =========================================================
# 14. CASE MANAGEMENT
# =========================================================

elif page == "Case Management":

    st.subheader("📁 Investigation Case Management")

    with st.form("case_form"):

        title = st.text_input("Case Title")
        movie = st.text_input("Movie Name")

        priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"]
        )

        status = st.selectbox(
            "Case Status",
            ["New", "Under Review", "Verified",
             "Rejected", "Closed"]
        )

        investigator = st.text_input("Investigator")

        submit = st.form_submit_button("Create Case")

        if submit:

            if title.strip() and movie.strip():

                con = connect()
                con.execute("""
                    INSERT INTO cases
                    (case_title, movie_title, priority,
                     status, investigator, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    title,
                    movie,
                    priority,
                    status,
                    investigator,
                    datetime.now().isoformat(timespec="seconds")
                ))
                con.commit()
                con.close()

                st.success("Investigation case created.")

            else:
                st.error("Case title and movie name are required.")

    st.divider()

    for case in get_cases():
        with st.expander(f"Case #{case[0]}: {case[1]}"):
            st.write("Movie:", case[2])
            st.write("Priority:", case[3])
            st.write("Status:", case[4])
            st.write("Investigator:", case[5])
            st.write("Created:", case[6])

# =========================================================
# 15. FORENSIC REPORTS
# =========================================================

elif page == "Forensic Reports":

    st.subheader("📄 Forensic Report Generator")

    movies = get_movies()
    scans = get_scans()
    evidence = get_evidence()
    cases = get_cases()

    st.write("Movies:", len(movies))
    st.write("Scans:", len(scans))
    st.write("Cases:", len(cases))
    st.write("Evidence records:", len(evidence))

    report = [
        "CINESHIELD AI - INVESTIGATION REPORT",
        "=" * 50,
        "Generated: " + datetime.now().isoformat(),
        "",
        "MOVIE REGISTRY",
        "-" * 30
    ]

    for movie in movies:
        report.append(
            f"{movie[1]} | {movie[2]} | {movie[3]}"
        )

    report += ["", "SCAN RECORDS", "-" * 30]

    for scan in scans:
        report.append(
            f"{scan[1]} | {scan[2]} | {scan[4]} | {scan[5]}"
        )

    report += ["", "INVESTIGATION CASES", "-" * 30]

    for case in cases:
        report.append(
            f"{case[1]} | {case[2]} | {case[3]} | {case[4]}"
        )

    report += ["", "EVIDENCE RECORDS", "-" * 30]

    for item in evidence:
        report.append(
            f"{item[1]} | {item[2]} | SHA256: {item[3]}"
        )

    st.download_button(
        "Download Investigation Report",
        "\n".join(report),
        file_name="cineshield_investigation_report.txt",
        mime="text/plain"
    )

# =========================================================
# 16. ALERT CENTER
# =========================================================

elif page == "Alert Center":

    st.subheader("🔔 Alert Center")

    scans = get_scans()
    cases = get_cases()

    st.write("Recent scan events")

    for scan in scans[:10]:
        st.info(
            f"{scan[1]} | {scan[4]} | {scan[5]}"
        )

    st.write("High-priority cases")

    for case in cases:
        if case[3] == "High":
            st.warning(
                f"{case[1]} | {case[2]} | {case[4]}"
            )

    st.caption(
        "These are application activity notices, not real-time web alerts."
    )

# =========================================================
# 17. ORGANIZATION MANAGEMENT
# =========================================================

elif page == "Organization Management":

    st.subheader("🏢 Organization Management")

    with st.form("organization_form"):

        name = st.text_input("Organization Name")
        organization_type = st.selectbox(
            "Organization Type",
            [
                "Film Production",
                "OTT Platform",
                "Distribution Company",
                "Copyright Investigation",
                "Other"
            ]
        )

        contact = st.text_input("Authorized Contact")
        notes = st.text_area("Organization Notes")

        submit = st.form_submit_button("Save Organization")

        if submit:
            if name.strip():
                save_record(
                    "Organization",
                    name,
                    f"Type: {organization_type}\n"
                    f"Contact: {contact}\n{notes}"
                )
                st.success("Organization saved.")

    for item in get_records("Organization"):
        with st.expander(item[1]):
            st.write(item[2])

# =========================================================
# 18. MULTILINGUAL INTELLIGENCE
# =========================================================

elif page == "Multilingual Intelligence":

    st.subheader("🌐 Multilingual Movie Intelligence")

    languages = [
        "Telugu", "Hindi", "Tamil", "Malayalam",
        "Kannada", "Bengali", "English", "Other"
    ]

    st.write("Supported movie registry languages")

    for language in languages:
        st.success(language)

    st.info(
        "Multilingual speech recognition, subtitle analysis and "
        "translation require additional AI model integration."
    )

# =========================================================
# 19. DISTRIBUTION INTELLIGENCE
# =========================================================

elif page == "Distribution Intelligence":

    st.subheader("📡 Authorized Distribution Intelligence")

    with st.form("distribution_form"):

        movie = st.text_input("Movie Name")
        distributor = st.text_input("Distributor")
        recipient = st.text_input("Authorized Recipient")
        region = st.text_input("Distribution Region")
        reference = st.text_input("Distribution Reference ID")
        notes = st.text_area("Additional Details")

        submit = st.form_submit_button("Save Distribution Record")

        if submit:

            if movie.strip() and distributor.strip():

                save_record(
                    "Distribution",
                    movie,
                    f"Distributor: {distributor}\n"
                    f"Recipient: {recipient}\n"
                    f"Region: {region}\n"
                    f"Reference: {reference}\n"
                    f"Notes: {notes}"
                )

                st.success("Distribution record saved.")

    for item in get_records("Distribution"):
        with st.expander(item[1]):
            st.write(item[2])

# =========================================================
# 20. ADMIN SETTINGS
# =========================================================

elif page == "Admin Settings":

    st.subheader("⚙️ Administration Settings")

    st.write("Application Information")
    st.write("Application: CINESHIELD AI")
    st.write("Version: 2.0 Development Edition")
    st.write("Database: SQLite")
    st.write("Storage: Local development environment")

    st.warning(
        "This development edition does not yet implement production "
        "authentication, organization isolation or encrypted file storage."
    )

    st.subheader("Database Backup")

    if st.button("Prepare Database Backup"):

        if Path(DB).exists():

            data = Path(DB).read_bytes()

            st.download_button(
                "Download Database",
                data,
                file_name="cineshield_backup.db",
                mime="application/octet-stream"
            )

    st.subheader("Application Modules")

    for item in PAGES:
        st.write("✓", item)

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "CINESHIELD AI | Movie Piracy Intelligence & Digital Forensics | "
    "Development Edition"
)

st.caption(
    "Use authorized movie samples and lawful public information. "
    "AI findings require human verification."
)