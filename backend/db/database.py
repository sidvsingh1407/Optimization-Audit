import sqlite3
import json
from pathlib import Path

DB_PATH = Path("data/audit_system.db")

def get_db_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        industry TEXT,
        employee_count TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS audits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER,
        audit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        raw_responses TEXT,
        total_score INTEGER,
        FOREIGN KEY (company_id) REFERENCES companies (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS operational_states (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        audit_id INTEGER UNIQUE,
        tools TEXT,
        workflows TEXT,
        governance TEXT,
        compliance TEXT,
        risks TEXT,
        FOREIGN KEY (audit_id) REFERENCES audits (id)
    )
    ''')

    conn.commit()
    conn.close()

def save_audit_state(company_data: dict, responses: dict, total_score: int, org_model):
    """Saves the audit state and operational intelligence into SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO companies (name, industry, employee_count) VALUES (?, ?, ?)",
        (company_data.get("company_name"), company_data.get("industry"), company_data.get("employee_count"))
    )

    cursor.execute("SELECT id FROM companies WHERE name = ?", (company_data.get("company_name"),))
    company_id = cursor.fetchone()["id"]

    cursor.execute(
        "INSERT INTO audits (company_id, raw_responses, total_score) VALUES (?, ?, ?)",
        (company_id, json.dumps(responses), total_score)
    )
    audit_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO operational_states
        (audit_id, tools, workflows, governance, compliance, risks)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            audit_id,
            json.dumps([t.model_dump() for t in org_model.tools]),
            json.dumps([w.model_dump() for w in org_model.workflows]),
            json.dumps(org_model.governance.model_dump()),
            json.dumps(org_model.compliance.model_dump()),
            json.dumps([r.model_dump() for r in org_model.risks]),
        )
    )

    conn.commit()
    conn.close()

    return audit_id

def get_latest_operational_state(company_name: str):
    """Retrieves the latest operational state for a company."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT os.tools, os.workflows, os.governance, os.compliance, os.risks
        FROM operational_states os
        JOIN audits a ON os.audit_id = a.id
        JOIN companies c ON a.company_id = c.id
        WHERE c.name = ?
        ORDER BY a.audit_date DESC LIMIT 1
    ''', (company_name,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "tools": json.loads(row["tools"]),
            "workflows": json.loads(row["workflows"]),
            "governance": json.loads(row["governance"]),
            "compliance": json.loads(row["compliance"]),
            "risks": json.loads(row["risks"])
        }
    return None

def get_all_operational_states():
    """Retrieve all states for the dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT c.name as company_name, os.tools, os.workflows, os.governance, os.compliance, os.risks, a.audit_date
        FROM operational_states os
        JOIN audits a ON os.audit_id = a.id
        JOIN companies c ON a.company_id = c.id
        ORDER BY a.audit_date DESC
    ''')

    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "company_name": row["company_name"],
            "audit_date": row["audit_date"],
            "tools": json.loads(row["tools"]),
            "workflows": json.loads(row["workflows"]),
            "governance": json.loads(row["governance"]),
            "compliance": json.loads(row["compliance"]),
            "risks": json.loads(row["risks"])
        })
    return results
