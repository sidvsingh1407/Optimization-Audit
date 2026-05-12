import sqlite3
import contextlib
from typing import Dict, Any, List, Optional
from backend.config.settings import DATABASE_PATH

@contextlib.contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize the SQLite database with authoritative operational truth tables."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Audits Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                audit_date TEXT NOT NULL,
                total_score INTEGER,
                rating TEXT,
                compliance_risk_flag BOOLEAN,
                execution_id TEXT
            )
        """)

        # Dimension Scores Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS score_breakdowns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                audit_id INTEGER,
                dimension_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                FOREIGN KEY (audit_id) REFERENCES audits(id)
            )
        """)

        # Compliance Findings Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS compliance_findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                audit_id INTEGER,
                finding_reason TEXT NOT NULL,
                FOREIGN KEY (audit_id) REFERENCES audits(id)
            )
        """)

        conn.commit()

def save_audit_record(audit_data: Dict[str, Any], scores: Dict[str, Any], execution_id: str) -> int:
    """Save the deterministic audit results into the operational truth store."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        company_name = audit_data.get("metadata", {}).get("company_name", "Unknown")
        audit_date = audit_data.get("metadata", {}).get("timestamp", "1970-01-01T00:00:00")

        cursor.execute("""
            INSERT INTO audits (company_name, audit_date, total_score, rating, compliance_risk_flag, execution_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            company_name,
            audit_date,
            scores.get("total_score", 0),
            scores.get("rating", "Unknown"),
            scores.get("compliance_risk_flag", False),
            execution_id
        ))

        audit_id = cursor.lastrowid

        # Save score breakdowns
        dimensions = scores.get("dimensions", {})
        for dim, score in dimensions.items():
            cursor.execute("""
                INSERT INTO score_breakdowns (audit_id, dimension_name, score)
                VALUES (?, ?, ?)
            """, (audit_id, dim, score))

        # Save compliance findings
        reasons = scores.get("compliance_risk_reasons", [])
        for reason in reasons:
            cursor.execute("""
                INSERT INTO compliance_findings (audit_id, finding_reason)
                VALUES (?, ?)
            """, (audit_id, reason))

        conn.commit()
        return audit_id
