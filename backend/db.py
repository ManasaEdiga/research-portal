import sqlite3

conn = sqlite3.connect("documents.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    doc_type TEXT,
    upload_date TEXT
)
""")

conn.commit()
