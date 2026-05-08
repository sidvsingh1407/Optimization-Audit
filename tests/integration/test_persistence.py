import pytest
from pathlib import Path
from db_persistence import init_db, save_audit, get_audit

@pytest.fixture
def temp_db(tmp_path):
    """Provides a temporary DB path for testing persistence."""
    db_path = tmp_path / "test_audit_system.db"
    init_db(db_path)
    return db_path

def test_sqlite_schema_init_and_insert(temp_db):
    """Test full insert and retrieval flow."""
    audit_data = {
        'company_name': 'Integration Test Corp',
        'audit_date': '2026-04-05',
        'industry': 'SaaS',
        'employee_count': '50-99',
        'benchmark_opt_in': True
    }

    scores = {
        'total_score': 72,
        'compliance_risk_flag': False,
        'dimensions': {
            'awareness': 15,
            'adoption': 14,
            'integration': 12,
            'governance': 16,
            'roi': 15
        }
    }

    report_path = "/fake/path/to/report.pdf"

    # Save the audit
    audit_id = save_audit(audit_data, scores, report_path, temp_db)

    assert audit_id > 0

    # Retrieve the audit
    retrieved = get_audit(audit_id, temp_db)

    assert retrieved is not None
    assert retrieved['audit']['company_name'] == 'Integration Test Corp'
    assert retrieved['audit']['total_score'] == 72
    assert retrieved['audit']['compliance_risk_flag'] == 0 # SQLite stores boolean as 0/1
    assert retrieved['audit']['report_path'] == report_path

    assert retrieved['scores']['awareness'] == 15
    assert retrieved['scores']['roi'] == 15

def test_get_nonexistent_audit(temp_db):
    """Test retrieval logic gracefully handles nonexistent entries."""
    retrieved = get_audit(999, temp_db)
    assert retrieved is None

def test_repository_retrieval_logic(temp_db):
    """Test repository retrieval logic to ensure previous audits can be loaded."""
    # Insert a few records
    for idx in range(3):
        save_audit({
            'company_name': f'Repo Test Corp {idx}',
            'audit_date': f'2026-04-0{idx+1}'
        }, {
            'total_score': 60 + idx,
            'compliance_risk_flag': False,
            'dimensions': {}
        }, f'/report_{idx}.pdf', temp_db)

    import sqlite3
    conn = sqlite3.connect(temp_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT id, company_name FROM audits ORDER BY id ASC')
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()

    assert len(results) >= 3
    assert results[0]['company_name'] == 'Repo Test Corp 0'
    assert results[-1]['company_name'] == 'Repo Test Corp 2'
