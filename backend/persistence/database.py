import sqlite3
import json
from typing import Dict, Any, List
from pathlib import Path
from backend.contracts.events import BaseEvent

DB_DIR = Path(__file__).resolve().parent.parent.parent / "data/runtime"
DB_PATH = DB_DIR / "audit_system.db"

def init_db():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Execution metrics for durations and general run stats
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS execution_metrics (
            execution_id TEXT PRIMARY KEY,
            status TEXT,
            start_time TEXT,
            end_time TEXT,
            duration_ms REAL,
            warning_counts INTEGER DEFAULT 0,
            error_counts INTEGER DEFAULT 0,
            governance_flags INTEGER DEFAULT 0,
            relationship_counts INTEGER DEFAULT 0
        )
    """)

    # Event log for tracking specific deterministically extracted state events
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS event_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            execution_id TEXT,
            event_type TEXT,
            timestamp TEXT,
            schema_version TEXT,
            event_version TEXT,
            payload TEXT
        )
    """)

    # Summary data linked to execution run
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS execution_summary (
            execution_id TEXT PRIMARY KEY,
            company_name TEXT,
            total_score INTEGER,
            compliance_risk_flag INTEGER,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()

def log_event(event: BaseEvent):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO event_log (execution_id, event_type, timestamp, schema_version, event_version, payload) VALUES (?, ?, ?, ?, ?, ?)",
        (event.execution_id, event.event_type, event.timestamp, event.schema_version, event.event_version, event.model_dump_json())
    )
    conn.commit()
    conn.close()

def init_execution_metrics(execution_id: str, start_time: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO execution_metrics (execution_id, status, start_time) VALUES (?, 'running', ?)",
        (execution_id, start_time)
    )
    conn.commit()
    conn.close()

def update_execution_metrics(execution_id: str, updates: Dict[str, Any]):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
    values = list(updates.values())
    values.append(execution_id)
    cursor.execute(
        f"UPDATE execution_metrics SET {set_clause} WHERE execution_id = ?",
        values
    )
    conn.commit()
    conn.close()

def save_execution_summary(execution_id: str, company_name: str, total_score: int, compliance_risk_flag: bool, created_at: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO execution_summary (execution_id, company_name, total_score, compliance_risk_flag, created_at) VALUES (?, ?, ?, ?, ?)",
        (execution_id, company_name, total_score, int(compliance_risk_flag), created_at)
    )
    conn.commit()
    conn.close()
