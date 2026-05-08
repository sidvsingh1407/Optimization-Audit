import sqlite3
import uuid
from datetime import datetime
import logging
from typing import Dict, List, Any

from backend.db.database import get_db_connection

logger = logging.getLogger(__name__)

def save_report(audit_id: str, filename: str, storage_location: str, company_name: str) -> str:
    """
    Persists report metadata.
    """
    report_id = str(uuid.uuid4())
    now_iso = datetime.utcnow().isoformat()

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reports (id, audit_id, filename, storage_location, company_name, generated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            report_id,
            audit_id,
            filename,
            storage_location,
            company_name,
            now_iso
        ))
        conn.commit()
        return report_id
    except sqlite3.Error as e:
        conn.rollback()
        logger.error(f"Failed to persist report metadata: {e}")
        raise
    finally:
        conn.close()

def get_recent_reports(limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieve recent reports."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, audit_id, filename, storage_location, company_name, generated_at
            FROM reports
            ORDER BY generated_at DESC
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
