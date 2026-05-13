import sqlite3
import contextlib
import json
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
    """Initialize the SQLite database with authoritative operational truth tables derived from Pydantic Contracts."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Audits Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                industry TEXT,
                employee_count TEXT,
                audit_date TEXT NOT NULL,
                total_score INTEGER,
                rating TEXT,
                compliance_risk_flag BOOLEAN,
                execution_id TEXT UNIQUE
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

        # Reports Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                audit_id INTEGER,
                pdf_path TEXT NOT NULL,
                generated_at TEXT NOT NULL,
                executive_summary TEXT,
                FOREIGN KEY (audit_id) REFERENCES audits(id)
            )
        """)

        # Benchmark Entries Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS benchmark_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                audit_id INTEGER,
                company_name TEXT,
                industry TEXT,
                total_score INTEGER,
                opt_in_date TEXT,
                FOREIGN KEY (audit_id) REFERENCES audits(id)
            )
        """)

        # Trace Logs Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trace_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                execution_id TEXT NOT NULL,
                audit_id INTEGER,
                stage TEXT NOT NULL,
                status TEXT NOT NULL,
                duration_ms INTEGER,
                validation_outcomes TEXT,
                governance_flags INTEGER,
                relationships_created INTEGER,
                entity_count INTEGER,
                timestamp TEXT NOT NULL
            )
        """)

        conn.commit()

def save_audit_record(audit_data: Dict[str, Any], scores: Dict[str, Any], execution_id: str, context_trace_logs: List[Any] = None) -> int:
    """Save the deterministic audit results and execution lineage into the operational truth store."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        company_name = audit_data.get("metadata", {}).get("company_name", "Unknown")
        industry = audit_data.get("metadata", {}).get("industry", "Unknown")
        employee_count = audit_data.get("metadata", {}).get("employee_count", "Unknown")
        audit_date = audit_data.get("metadata", {}).get("timestamp", "1970-01-01T00:00:00")
        opt_in = audit_data.get("metadata", {}).get("benchmark_opt_in", False)

        cursor.execute("""
            INSERT INTO audits (company_name, industry, employee_count, audit_date, total_score, rating, compliance_risk_flag, execution_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            company_name,
            industry,
            employee_count,
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

        # Optional: benchmark opt-in
        if opt_in:
             cursor.execute("""
                INSERT INTO benchmark_entries (audit_id, company_name, industry, total_score, opt_in_date)
                VALUES (?, ?, ?, ?, ?)
            """, (audit_id, company_name, industry, scores.get("total_score", 0), audit_date))

        # Save trace logs
        if context_trace_logs:
            for trace in context_trace_logs:
                cursor.execute("""
                    INSERT INTO trace_logs (execution_id, audit_id, stage, status, duration_ms, validation_outcomes, governance_flags, relationships_created, entity_count, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    trace.execution_id,
                    audit_id,
                    trace.stage,
                    trace.status,
                    trace.duration_ms,
                    json.dumps(trace.validation_outcomes),
                    trace.governance_flags,
                    trace.relationships_created,
                    trace.entity_count,
                    trace.timestamp
                ))

        conn.commit()
        return audit_id
