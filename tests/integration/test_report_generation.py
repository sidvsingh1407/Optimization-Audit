import pytest
import json
from pathlib import Path
import os
from report_generator import generate_report

@pytest.fixture
def sample_audit_data(tmp_path):
    audit_data = {
        'company_name': 'Report Test Corp',
        'industry': 'SaaS',
        'employee_count': '50-99'
    }

    scores = {
        'total_score': 65,
        'rating': 'AI Adopting',
        'compliance_risk_flag': True,
        'compliance_risk_reasons': ['q4_1', 'q4_3'],
        'dimensions': {
            'awareness': 15,
            'adoption': 12,
            'integration': 13,
            'governance': 10,
            'roi': 15
        }
    }

    agent_findings = {
        'tool_evaluator': {
            'redundancies': [
                {'tools': ['Jasper', 'ChatGPT'], 'overlap': 'Content generation overlap'}
            ],
            'underutilized': [
                {'tool': 'Copilot', 'cost': 1500}
            ]
        },
        'workflow_optimizer': {
            'quick_wins': [
                {'action': 'Automate meeting notes'}
            ]
        },
        'compliance_auditor': {
            'summary': 'High compliance risk due to lack of policies.'
        },
        'analytics_reporter': {
            'top_5_recommendations': [
                {'rank': 1, 'action': 'Draft policy', 'impact': 'High', 'effort': 'Low'}
            ],
            'cost_waste': {
                'monthly_estimate': '$1500',
                'annual_estimate': '$18000',
                'waste_categories': ['Unused licenses']
            }
        }
    }

    return audit_data, scores, agent_findings

def test_report_file_creation(sample_audit_data, tmp_path):
    """Test deterministic report generation outputs."""
    audit_data, scores, agent_findings = sample_audit_data

    output_pdf_path = tmp_path / "test_report.pdf"

    # Generate report
    returned_path = generate_report(audit_data, scores, agent_findings, str(output_pdf_path))

    # Verify file was created
    assert os.path.exists(output_pdf_path)
    assert str(output_pdf_path) == returned_path

    # Verify it has size > 0 bytes
    assert os.path.getsize(output_pdf_path) > 0
