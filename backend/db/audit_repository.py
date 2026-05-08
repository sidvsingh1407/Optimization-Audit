import sqlite3
import uuid
from datetime import datetime
import logging
from typing import Dict, List, Any, Optional

from backend.db.database import get_db_connection

logger = logging.getLogger(__name__)

def save_audit(audit_data: Dict[str, Any], scores: Dict[str, Any], compliance_data: List[Dict[str, Any]], audit_type: str = "structured") -> str:
    """
    Persists an audit and its related score breakdown and compliance findings.
    Validations are assumed to have passed before calling this.
    """
    audit_id = str(uuid.uuid4())
    now_iso = datetime.utcnow().isoformat()

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # 1. Insert Audit
        cursor.execute('''
            INSERT INTO audits (id, company_name, industry, employee_count, audit_date, total_score, compliance_risk_flag, audit_type, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            audit_id,
            audit_data.get('company_name', 'Unknown'),
            audit_data.get('industry', 'Unknown'),
            audit_data.get('employee_count', 'Unknown'),
            audit_data.get('audit_date', now_iso),
            scores.get('total_score', 0),
            bool(scores.get('compliance_risk_flag', False)),
            audit_type,
            now_iso
        ))

        # 2. Insert Score Breakdown
        dims = scores.get('dimensions', {})
        cursor.execute('''
            INSERT INTO score_breakdowns (audit_id, awareness, adoption, integration, governance, roi)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            audit_id,
            dims.get('awareness', 0),
            dims.get('adoption', 0),
            dims.get('integration', 0),
            dims.get('governance', 0),
            dims.get('roi', 0)
        ))

        # 3. Insert Compliance Findings
        for finding in compliance_data:
            finding_id = str(uuid.uuid4())
            cursor.execute('''
                INSERT INTO compliance_findings (id, audit_id, regulation, article_reference, finding_text, risk_level, recommendation_text)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                finding_id,
                audit_id,
                finding.get('regulation', 'Unknown'),
                finding.get('article_reference', ''),
                finding.get('finding_text', ''),
                finding.get('risk_level', 'Unknown'),
                finding.get('recommendation_text', '')
            ))

        conn.commit()
        logger.info(f"Successfully persisted audit {audit_id} for company {audit_data.get('company_name')}")
        return audit_id
    except sqlite3.Error as e:
        conn.rollback()
        logger.error(f"Failed to persist audit: {e}")
        raise
    finally:
        conn.close()

def get_recent_audits(limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieve the most recent audits."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, a.company_name, a.industry, a.audit_date, a.total_score, a.compliance_risk_flag,
                   b.awareness, b.adoption, b.integration, b.governance, b.roi
            FROM audits a
            LEFT JOIN score_breakdowns b ON a.id = b.audit_id
            ORDER BY a.created_at DESC
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def get_audit_history_by_company(company_name: str) -> List[Dict[str, Any]]:
    """Retrieve audit history for a specific company."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, audit_date, total_score, compliance_risk_flag
            FROM audits
            WHERE company_name = ?
            ORDER BY audit_date DESC
        ''', (company_name,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def get_total_audits_count() -> int:
    """Retrieve total number of audits."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as cnt FROM audits')
        row = cursor.fetchone()
        return row['cnt'] if row else 0
    finally:
        conn.close()

def get_compliance_risk_count() -> int:
    """Retrieve total number of audits with a compliance risk."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as cnt FROM audits WHERE compliance_risk_flag = 1')
        row = cursor.fetchone()
        return row['cnt'] if row else 0
    finally:
        conn.close()

def get_average_score() -> float:
    """Retrieve average maturity score across all audits."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT AVG(total_score) as avg_score FROM audits')
        row = cursor.fetchone()
        return round(row['avg_score'], 1) if row and row['avg_score'] is not None else 0.0
    finally:
        conn.close()
