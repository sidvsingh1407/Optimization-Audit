import sqlite3
import uuid
from datetime import datetime
import logging
from typing import Dict, List, Any

from backend.db.database import get_db_connection

logger = logging.getLogger(__name__)

def save_benchmark(audit_id: str, audit_data: Dict[str, Any], scores: Dict[str, Any]) -> str:
    """
    Persists a benchmark entry (only if opted in).
    """
    # The MVP states "Keep benchmarking INTERNAL ONLY for MVP". But since the front-end has an opt-in
    # field, we should respect it. The Streamlit checkbox defaults to False, but we want it to work.
    opt_in = audit_data.get('benchmark_opt_in')
    if opt_in is False or opt_in == "False" or opt_in == "false":
        logger.info("Benchmark opt-in is false. Skipping benchmark persistence.")
        return ""

    benchmark_id = str(uuid.uuid4())
    now_iso = datetime.utcnow().isoformat()
    dims = scores.get('dimensions', {})

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO benchmark_entries (
                id, audit_id, industry, employee_count, score_total,
                score_awareness, score_adoption, score_integration, score_governance, score_roi, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            benchmark_id,
            audit_id,
            audit_data.get('industry', 'Unknown'),
            audit_data.get('employee_count', 'Unknown'),
            scores.get('total_score', 0),
            dims.get('awareness', 0),
            dims.get('adoption', 0),
            dims.get('integration', 0),
            dims.get('governance', 0),
            dims.get('roi', 0),
            now_iso
        ))
        conn.commit()
        return benchmark_id
    except sqlite3.Error as e:
        conn.rollback()
        logger.error(f"Failed to persist benchmark: {e}")
        raise
    finally:
        conn.close()

def get_benchmark_averages_by_industry() -> List[Dict[str, Any]]:
    """Retrieve average scores grouped by industry."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT industry, COUNT(*) as count, AVG(score_total) as avg_score
            FROM benchmark_entries
            GROUP BY industry
            ORDER BY count DESC
        ''')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def get_benchmark_averages_by_size() -> List[Dict[str, Any]]:
    """Retrieve average scores grouped by company size."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT employee_count, COUNT(*) as count, AVG(score_total) as avg_score
            FROM benchmark_entries
            GROUP BY employee_count
            ORDER BY count DESC
        ''')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
