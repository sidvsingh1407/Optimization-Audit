import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, Optional

DEFAULT_DB_PATH = Path("data/audit_system.db")

def get_connection(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: Path = DEFAULT_DB_PATH):
    """Initializes the SQLite schema."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS audits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        audit_date TEXT NOT NULL,
        total_score INTEGER,
        compliance_risk_flag BOOLEAN,
        report_path TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS score_breakdowns (
        audit_id INTEGER,
        awareness INTEGER,
        adoption INTEGER,
        integration INTEGER,
        governance INTEGER,
        roi INTEGER,
        FOREIGN KEY(audit_id) REFERENCES audits(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS benchmark_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        industry TEXT,
        employee_count TEXT,
        total_score INTEGER
    )
    ''')

    conn.commit()
    conn.close()

def save_audit(audit_data: Dict[str, Any], scores: Dict[str, Any], report_path: str = None, db_path: Path = DEFAULT_DB_PATH) -> int:
    """Saves an audit record and its associated data to the database."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    company_name = audit_data.get('company_name', 'Unknown')
    audit_date = audit_data.get('audit_date', 'Unknown')
    total_score = scores.get('total_score', 0)
    compliance_risk = scores.get('compliance_risk_flag', False)

    cursor.execute('''
        INSERT INTO audits (company_name, audit_date, total_score, compliance_risk_flag, report_path)
        VALUES (?, ?, ?, ?, ?)
    ''', (company_name, audit_date, total_score, compliance_risk, report_path))

    audit_id = cursor.lastrowid

    dims = scores.get('dimensions', {})
    cursor.execute('''
        INSERT INTO score_breakdowns (audit_id, awareness, adoption, integration, governance, roi)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (audit_id, dims.get('awareness', 0), dims.get('adoption', 0),
          dims.get('integration', 0), dims.get('governance', 0), dims.get('roi', 0)))

    if audit_data.get('benchmark_opt_in', False):
        cursor.execute('''
            INSERT INTO benchmark_entries (industry, employee_count, total_score)
            VALUES (?, ?, ?)
        ''', (audit_data.get('industry', ''), audit_data.get('employee_count', ''), total_score))

    conn.commit()
    conn.close()
    return audit_id

def get_audit(audit_id: int, db_path: Path = DEFAULT_DB_PATH) -> Optional[Dict[str, Any]]:
    """Retrieves an audit record by its ID."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM audits WHERE id = ?', (audit_id,))
    audit_row = cursor.fetchone()

    if not audit_row:
        conn.close()
        return None

    cursor.execute('SELECT * FROM score_breakdowns WHERE audit_id = ?', (audit_id,))
    score_row = cursor.fetchone()

    conn.close()

    return {
        'audit': dict(audit_row),
        'scores': dict(score_row) if score_row else None
    }
