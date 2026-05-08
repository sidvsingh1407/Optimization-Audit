import sqlite3
import os
import logging
from pathlib import Path

# Configure basic logging
logger = logging.getLogger(__name__)

DB_DIR = Path("data")
DB_PATH = DB_DIR / "audit_system.db"

def get_db_connection():
    """Create and return a database connection."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Failed to connect to database at {DB_PATH}: {e}")
        raise

def init_db():
    """Initialize the SQLite schema."""
    DB_DIR.mkdir(parents=True, exist_ok=True)

    schema = """
    CREATE TABLE IF NOT EXISTS audits (
        id TEXT PRIMARY KEY,
        company_name TEXT NOT NULL,
        industry TEXT,
        employee_count TEXT,
        audit_date DATETIME NOT NULL,
        total_score INTEGER,
        compliance_risk_flag BOOLEAN,
        audit_type TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS score_breakdowns (
        audit_id TEXT PRIMARY KEY,
        awareness INTEGER,
        adoption INTEGER,
        integration INTEGER,
        governance INTEGER,
        roi INTEGER,
        FOREIGN KEY (audit_id) REFERENCES audits (id)
    );

    CREATE TABLE IF NOT EXISTS compliance_findings (
        id TEXT PRIMARY KEY,
        audit_id TEXT NOT NULL,
        regulation TEXT,
        article_reference TEXT,
        finding_text TEXT,
        risk_level TEXT,
        recommendation_text TEXT,
        FOREIGN KEY (audit_id) REFERENCES audits (id)
    );

    CREATE TABLE IF NOT EXISTS reports (
        id TEXT PRIMARY KEY,
        audit_id TEXT NOT NULL,
        filename TEXT NOT NULL,
        storage_location TEXT NOT NULL,
        company_name TEXT,
        generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (audit_id) REFERENCES audits (id)
    );

    CREATE TABLE IF NOT EXISTS benchmark_entries (
        id TEXT PRIMARY KEY,
        audit_id TEXT,
        industry TEXT,
        employee_count TEXT,
        score_total INTEGER,
        score_awareness INTEGER,
        score_adoption INTEGER,
        score_integration INTEGER,
        score_governance INTEGER,
        score_roi INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (audit_id) REFERENCES audits (id)
    );
    """

    conn = get_db_connection()
    try:
        conn.executescript(schema)
        conn.commit()
        logger.info("Database schema initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize database schema: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
