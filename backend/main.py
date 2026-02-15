from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from datetime import datetime
from pypdf import PdfReader

from db import cursor, conn
from ai_summary import generate_summary

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
SUMMARY_DIR = "summaries"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(SUMMARY_DIR, exist_ok=True)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    cursor.execute(
        "INSERT INTO documents (filename, doc_type, upload_date) VALUES (?, ?, ?)",
        (file.filename, "concall", datetime.now().isoformat())
    )
    conn.commit()

    return {"status": "uploaded"}

@app.get("/documents")
def list_documents():
    rows = cursor.execute("SELECT * FROM documents").fetchall()
    return [
        {"id": r[0], "filename": r[1], "doc_type": r[2], "upload_date": r[3]}
        for r in rows
    ]


@app.post("/ai-summary/{doc_id}")
def run_ai_summary(doc_id: int):
    row = cursor.execute(
        "SELECT filename FROM documents WHERE id = ?", (doc_id,)
    ).fetchone()

    filename = row[0]
    path = f"{UPLOAD_DIR}/{filename}"

    text = ""

    if path.lower().endswith(".pdf"):
        reader = PdfReader(path)
        for page in reader.pages:
            text += page.extract_text() or ""
    else:
        with open(path, "r", errors="ignore") as f:
            text = f.read()

    summary = generate_summary(text)

    summary_path = f"{SUMMARY_DIR}/{doc_id}.txt"
    with open(summary_path, "w") as f:
        f.write(summary)

    return {"summary": summary}


@app.get("/summary/{doc_id}")
def get_summary(doc_id: int):
    path = f"{SUMMARY_DIR}/{doc_id}.txt"
    if not os.path.exists(path):
        return {"summary": None}

    with open(path) as f:
        return {"summary": f.read()}
