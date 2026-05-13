from fastapi import FastAPI, HTTPException
import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any

app = FastAPI(
    title="Optimization-Audit Interoperability API",
    description="Operational access interfaces for audit execution retrieval and analytics.",
    version="1.0.0"
)

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data/runtime/audit_system.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}

@app.get("/audits/{execution_id}")
def get_audit(execution_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM execution_summary WHERE execution_id = ?", (execution_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Audit not found")

    return dict(row)

@app.get("/metrics")
def get_metrics():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM execution_metrics ORDER BY start_time DESC LIMIT 50")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

@app.get("/governance/{execution_id}")
def get_governance(execution_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM event_log WHERE execution_id = ? AND event_type = ?", (execution_id, 'governance.mapped'))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Governance data not found for execution")

    event_data = json.loads(row["payload"])
    return event_data

@app.get("/relationships/{execution_id}")
def get_relationships(execution_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM event_log WHERE execution_id = ? AND event_type = ?", (execution_id, 'relationship.created'))
    rows = cursor.fetchall()
    conn.close()

    return [json.loads(row["payload"]) for row in rows]

@app.get("/traces/{execution_id}")
def get_traces(execution_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM event_log WHERE execution_id = ? AND event_type = ? ORDER BY timestamp ASC", (execution_id, 'trace.logged'))
    rows = cursor.fetchall()
    conn.close()

    return [json.loads(row["payload"]) for row in rows]
