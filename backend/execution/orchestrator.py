#!/usr/bin/env python3
"""
AI Productivity Intelligence System - Orchestrator
End-to-end audit execution: load data → score → analyze → generate report

Usage:
  python orchestrator.py run <form_response.json>  # Run full audit
  python orchestrator.py score <form_response.json>  # Score only
  python orchestrator.py report <audit.json> <scores.json> <output.pdf>  # Report only
"""

import json
import sys
import os
import re
from typing import Dict, Any
from datetime import datetime
from pathlib import Path
from pydantic import ValidationError

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.config.settings import OUTPUTS_DIR, REPORTS_DIR, RUNTIME_DIR
from backend.persistence.database import init_db, save_audit_record
from backend.audit_modules.scoring.scoring_engine import calculate_scores, format_score_report, load_form_responses
from backend.utils.logger import get_logger, TraceContext
from backend.execution.context import ExecutionContext
from backend.contracts.audit import AuditInputContract, AuditScoreResult, ScoreDimensions

logger = get_logger()

# =============================================================================
# AGENT SIMULATION (MVP: Simple rule-based analysis)
# =============================================================================

def analyze_tools(responses, audit_data):
    """Rule-based tool analysis (MVP version)."""
    tools_used = audit_data.get('tools_used', '').lower()
    tool_count = len([t for t in tools_used.split(',') if t.strip()]) if tools_used else 0
    monthly_spend = audit_data.get('monthly_spend', '')

    redundancies = []
    underutilized = []
    waste_estimate = 0

    if 'chatgpt' in tools_used and 'claude' in tools_used and 'gemini' in tools_used:
        redundancies.append({
            'tools': ['ChatGPT', 'Claude', 'Gemini'],
            'overlap': 'Multiple general-purpose chatbots - consider consolidating to 1-2',
            'waste_estimate': 500
        })
        waste_estimate += 500

    if 'jasper' in tools_used and 'copy' in tools_used:
        redundancies.append({
            'tools': ['Jasper', 'Copy.ai'],
            'overlap': 'Multiple copywriting tools - pick one',
            'waste_estimate': 300
        })
        waste_estimate += 300

    adoption_score = calculate_scores(responses).get('dimensions', {}).get('adoption', 0)
    if monthly_spend in ['$2K-$10K', '$10K+'] and adoption_score < 12:
        underutilized.append({
            'tool': 'Enterprise AI tools',
            'cost': monthly_spend,
            'evidence': f'High spend ({monthly_spend}) but low adoption score ({adoption_score}/20)'
        })

    return {
        'redundancies': redundancies,
        'gaps': [],
        'underutilized': underutilized,
        'total_waste_estimate': f"${waste_estimate}/month",
        'tool_recommendations': [
            {'action': 'review', 'details': 'Consolidate overlapping tools'}
        ] if redundancies else []
    }

def analyze_workflows(responses, scores):
    """Rule-based workflow analysis (MVP version)."""
    integration_score = scores.dimensions.integration if isinstance(scores, AuditScoreResult) else scores.get('dimensions', {}).get('integration', 0)
    adoption_score = scores.dimensions.adoption if isinstance(scores, AuditScoreResult) else scores.get('dimensions', {}).get('adoption', 0)

    quick_wins = []
    automation_opportunities = []

    if integration_score < 12:
        quick_wins.append({
            'action': 'Identify top 3 manual copy/paste workflows and integrate AI directly',
            'time_to_implement': '<1 week',
            'expected_impact': 'Reduce context switching, improve adoption'
        })

    if adoption_score < 12:
        quick_wins.append({
            'action': 'Run 1-hour team training on core AI tools',
            'time_to_implement': '<1 week',
            'expected_impact': 'Increase daily active users by 20-30%'
        })

    if integration_score < 10:
        automation_opportunities.append({
            'process': 'Email drafting and summarization',
            'current_state': 'Manual',
            'ai_solution': 'Integrate AI into email client or use dedicated tool',
            'effort': 'low',
            'impact': 'medium'
        })

    return {
        'automation_opportunities': automation_opportunities,
        'integration_gaps': [],
        'quick_wins': quick_wins,
        'priority_recommendations': [
            {'rank': 1, 'recommendation': 'Focus on integration over new tools', 'rationale': 'Low integration score indicates tools exist but aren\'t embedded in workflows'}
        ]
    }

def analyze_compliance(responses, scores):
    """Rule-based compliance analysis (MVP version)."""
    governance_score = scores.dimensions.governance if isinstance(scores, AuditScoreResult) else scores.get('dimensions', {}).get('governance', 0)
    q4_1 = responses.get('q4_1', 'e')
    q4_2 = responses.get('q4_2', 'e')
    q4_3 = responses.get('q4_3', 'e')

    eu_ai_risk = 'low'
    gdpr_risk = 'low'
    required_actions = []

    if q4_3 in ['d', 'e']:
        eu_ai_risk = 'high'
        required_actions.append('Complete EU AI Act awareness training for leadership')
        required_actions.append('Assess if any AI uses fall under high-risk categories')

    if q4_2 in ['d', 'e']:
        gdpr_risk = 'high'
        required_actions.append('Implement data privacy review for AI tools')
        required_actions.append('Create approved tools list with privacy vetting')

    governance_gaps = []
    if q4_1 in ['d', 'e']:
        governance_gaps.append({
            'gap': 'No formal AI usage policy',
            'risk': 'high',
            'fix': 'Draft and communicate AI usage policy within 30 days'
        })

    overall_risk = 'critical' if eu_ai_risk == 'high' or gdpr_risk == 'high' else 'medium' if governance_score < 12 else 'low'

    return {
        'eu_ai_act': {
            'risk_level': eu_ai_risk,
            'high_risk_uses': [],
            'compliance_deadline': 'August 2026',
            'required_actions': required_actions
        },
        'gdpr': {
            'risk_level': gdpr_risk,
            'data_concerns': [],
            'required_actions': required_actions if gdpr_risk == 'high' else []
        },
        'governance_gaps': governance_gaps,
        'remediation_timeline': [
            {'deadline': 'immediate', 'action': 'Leadership briefing on EU AI Act requirements'} if eu_ai_risk == 'high' else {},
            {'deadline': '30 days', 'action': 'Draft AI usage policy'} if q4_1 in ['d', 'e'] else {},
            {'deadline': '90 days', 'action': 'Complete compliance assessment'}
        ],
        'overall_risk': overall_risk,
        'summary': f"Compliance risk level: {overall_risk}. Governance score of {governance_score}/20 indicates {'significant gaps' if governance_score < 12 else 'moderate maturity'}. EU AI Act deadline is August 2026."
    }

def generate_recommendations(scores, tool_analysis, workflow_analysis, compliance_analysis, audit_data):
    """Generate top 5 recommendations based on all analyses."""
    recommendations = []

    overall_risk = compliance_analysis.get('overall_risk')
    if overall_risk in ['critical', 'high']:
        recommendations.append({
            'rank': 1,
            'action': 'Address compliance gaps immediately (EU AI Act deadline: Aug 2026)',
            'impact': 'Avoid regulatory penalties',
            'effort': 'medium'
        })

    if tool_analysis.get('redundancies'):
        recommendations.append({
            'rank': 2,
            'action': f"Consolidate redundant tools (estimated waste: {tool_analysis.get('total_waste_estimate', 'N/A')})",
            'impact': 'Cost savings',
            'effort': 'low'
        })

    integration_score = scores.dimensions.integration if isinstance(scores, AuditScoreResult) else scores.get('dimensions', {}).get('integration', 0)
    if integration_score < 12:
        recommendations.append({
            'rank': 3,
            'action': 'Embed AI into existing workflows rather than adding new tools',
            'impact': 'Higher adoption, better ROI',
            'effort': 'medium'
        })

    adoption_score = scores.dimensions.adoption if isinstance(scores, AuditScoreResult) else scores.get('dimensions', {}).get('adoption', 0)
    if adoption_score < 12:
        recommendations.append({
            'rank': 4,
            'action': 'Implement structured AI training program for all employees',
            'impact': 'Increase productivity across organization',
            'effort': 'medium'
        })

    if not recommendations or len(recommendations) < 5:
        recommendations.append({
            'rank': len(recommendations) + 1,
            'action': 'Establish AI governance committee and draft usage policy',
            'impact': 'Risk mitigation, consistent decision-making',
            'effort': 'low'
        })

    return recommendations[:5]

def generate_analytics_report(scores, tool_analysis, workflow_analysis, compliance_analysis, audit_data):
    """Generate the analytics reporter output."""
    total_score = scores.total_score if isinstance(scores, AuditScoreResult) else scores.get('total_score', 0)
    rating = scores.rating if isinstance(scores, AuditScoreResult) else scores.get('rating', 'Unknown')
    monthly_spend = audit_data.get('monthly_spend', 'Unknown')
    waste_estimate = tool_analysis.get('total_waste_estimate', '$0')

    waste_num = 0
    if '$' in waste_estimate:
        try:
            waste_num = int(''.join(filter(str.isdigit, waste_estimate)))
        except:
            pass

    governance_score = scores.dimensions.governance if isinstance(scores, AuditScoreResult) else scores.get('dimensions', {}).get('governance', 0)
    roi_score = scores.dimensions.roi if isinstance(scores, AuditScoreResult) else scores.get('dimensions', {}).get('roi', 0)

    if governance_score < 12:
        potential_savings = waste_num * 12
        improvement_pct = 15
    else:
        potential_savings = waste_num * 6
        improvement_pct = 8

    return {
        'executive_summary': f"This audit reveals an AI maturity score of {total_score}/100 ({rating}). The organization is {'ahead of' if total_score >= 60 else 'behind'} industry benchmarks. Key opportunities identified include tool consolidation (estimated ${waste_num}/month waste), workflow integration improvements, and compliance remediation before the August 2026 EU AI Act deadline.",
        'cost_waste': {
            'monthly_estimate': waste_estimate,
            'annual_estimate': f"${waste_num * 12}/year" if waste_num else 'N/A',
            'waste_categories': ['Redundant tool subscriptions', 'Underutilized enterprise features', 'Manual processes that could be automated']
        },
        'improvement_potential': {
            'time_savings_current': f"{roi_score * 4}% (estimated)",
            'time_savings_potential': f"{roi_score * 4 + improvement_pct}% (with recommendations)",
            'productivity_gain_value': f"${potential_savings}/year (estimated)"
        },
        'benchmark_position': {
            'score': total_score,
            'industry_avg': 'TBD (need benchmark data)',
            'percentile': 'TBD',
            'interpretation': 'above average' if total_score >= 60 else 'below average'
        },
        'top_5_recommendations': generate_recommendations(scores, tool_analysis, workflow_analysis, compliance_analysis, audit_data),
        'urgency_flag': {
            'has_urgency': compliance_analysis.get('overall_risk') in ['critical', 'high'],
            'reason': 'compliance deadline' if compliance_analysis.get('overall_risk') == 'high' else 'cost optimization'
        }
    }


# =============================================================================
# DETERMINISTIC PIPELINE STAGES
# =============================================================================

def run_ingestion(context: ExecutionContext):
    """Load and perform raw sanity checks."""
    with TraceContext(logger, context.execution_id, "INGESTION"):
        context.transition("INGESTION")
        # Assuming raw_input is already loaded into context.raw_input by caller
        if not context.raw_input:
            raise ValueError("Input data is empty.")

        context.runtime_metadata["raw_keys"] = list(context.raw_input.keys())

def run_validation(context: ExecutionContext):
    """Strictly validate input using Pydantic contracts."""
    with TraceContext(logger, context.execution_id, "VALIDATION"):
        context.transition("VALIDATION")
        try:
            # Map raw input to the contract structure
            contract_data = context.raw_input.copy()
            # If responses are at the root, nest them for validation
            if 'responses' not in contract_data:
                contract_data = {
                    'company_name': contract_data.get('company_name', 'Unknown'),
                    'industry': contract_data.get('industry', 'Unknown'),
                    'employee_count': contract_data.get('employee_count', 'Unknown'),
                    'contact_name': contract_data.get('contact_name', 'Unknown'),
                    'contact_email': contract_data.get('contact_email', 'Unknown'),
                    'benchmark_opt_in': contract_data.get('benchmark_opt_in', False),
                    'responses': contract_data
                }

            context.contract = AuditInputContract(**contract_data)
            context.validation_state["status"] = "success"
        except ValidationError as e:
            context.validation_state["status"] = "failed"
            context.validation_state["errors"] = e.errors()
            raise ValueError(f"Strict validation failed: {e}")

def run_normalization(context: ExecutionContext):
    """Ensure data is uniformly formatted for processing."""
    with TraceContext(logger, context.execution_id, "NORMALIZATION"):
        context.transition("NORMALIZATION")
        # In MVP, our Pydantic model implicitly normalizes most fields
        # Just update the raw input to match the validated, normalized structure
        context.raw_input = context.contract.model_dump()
        context.entity_count += 1 # Base company entity

def run_risk_scoring(context: ExecutionContext):
    """Deterministic score calculation."""
    with TraceContext(logger, context.execution_id, "RISK_SCORING"):
        context.transition("RISK_SCORING")
        raw_scores = calculate_scores(context.contract.responses)

        # Enforce contract on scores
        context.scores = AuditScoreResult(
            dimensions=ScoreDimensions(**raw_scores.get('dimensions', {})),
            total_score=raw_scores.get('total_score', 0),
            rating=raw_scores.get('rating', 'Unknown'),
            compliance_risk_flag=raw_scores.get('compliance_risk_flag', False),
            compliance_risk_reasons=raw_scores.get('compliance_risk_reasons', [])
        )
        if context.scores.compliance_risk_flag:
            context.governance_flags += 1

def run_entity_mapping(context: ExecutionContext):
    """Extract operational intelligence via rule-based agents."""
    with TraceContext(logger, context.execution_id, "ENTITY_MAPPING"):
        context.transition("ENTITY_MAPPING")

        audit_data = context.contract.responses
        context.agent_findings['tool_evaluator'] = analyze_tools(audit_data, context.raw_input)
        context.agent_findings['workflow_optimizer'] = analyze_workflows(audit_data, context.scores)
        context.agent_findings['compliance_auditor'] = analyze_compliance(audit_data, context.scores)
        context.agent_findings['analytics_reporter'] = generate_analytics_report(
            context.scores,
            context.agent_findings['tool_evaluator'],
            context.agent_findings['workflow_optimizer'],
            context.agent_findings['compliance_auditor'],
            context.raw_input
        )

        # Track simulated entities found
        context.entity_count += len(context.agent_findings['tool_evaluator'].get('redundancies', []))
        context.entity_count += len(context.agent_findings['tool_evaluator'].get('underutilized', []))

def run_report_generation(context: ExecutionContext):
    """Generate final artifacts (JSON, PDF)."""
    with TraceContext(logger, context.execution_id, "REPORT_GENERATION"):
        context.transition("REPORT_GENERATION")
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        company_clean = re.sub(r'[^a-zA-Z0-9_\-]', '_', context.contract.company_name)

        # Save JSON output
        audit_result = {
            'execution_id': context.execution_id,
            'company_name': context.contract.company_name,
            'audit_date': datetime.now().isoformat(),
            'scores': context.scores.model_dump(),
            'agent_findings': context.agent_findings
        }

        audit_path = OUTPUTS_DIR / f"audit_{timestamp}.json"
        with open(audit_path, 'w') as f:
            json.dump(audit_result, f, indent=2)

        scores_path = OUTPUTS_DIR / f"scores_{timestamp}.json"
        with open(scores_path, 'w') as f:
            json.dump(context.scores.model_dump(), f, indent=2)

        context.runtime_metadata["audit_json_path"] = str(audit_path)
        context.runtime_metadata["scores_json_path"] = str(scores_path)

        # PDF Report
        try:
            from backend.execution.reporting.report_generator import generate_report
            pdf_path = REPORTS_DIR / f"report_{company_clean}_{timestamp}.pdf"
            # report_generator expects raw dictionaries
            generate_report(context.raw_input, context.scores.model_dump(), context.agent_findings, str(pdf_path))
            context.report_path = str(pdf_path)
            context.runtime_metadata["report_pdf_path"] = str(pdf_path)
        except ImportError as e:
            logger.warning(f"Report generator not available: {e}", extra={"execution_id": context.execution_id})

def run_persistence(context: ExecutionContext):
    """Persist structured state to SQLite."""
    with TraceContext(logger, context.execution_id, "PERSISTENCE"):
        context.transition("PERSISTENCE")
        # Convert Pydantic model to dictionary structure expected by DB
        audit_data_dict = {
            "metadata": {
                "company_name": context.contract.company_name,
                "industry": context.contract.industry,
                "employee_count": context.contract.employee_count,
                "benchmark_opt_in": context.contract.benchmark_opt_in,
                "timestamp": datetime.now().isoformat()
            }
        }
        scores_dict = context.scores.model_dump()
        audit_id = save_audit_record(audit_data_dict, scores_dict, context.execution_id, context.trace_logs)
        context.audit_id = audit_id

def run_trace_logging(context: ExecutionContext):
    """Finalize lineage tracing."""
    with TraceContext(logger, context.execution_id, "TRACE_LOGGING"):
        context.transition("TRACE_LOGGING")
        summary = context.generate_trace_summary()
        logger.info("Pipeline execution completed successfully", extra={
            "execution_id": context.execution_id,
            "trace_summary": summary
        })

# =============================================================================
# MAIN ORCHESTRATION PIPELINE
# =============================================================================

def execute_audit_pipeline(form_response_path: str) -> Dict[str, Any]:
    """Execute the structured audit lifecycle."""
    raw_data = load_form_responses(form_response_path)
    context = ExecutionContext(raw_input=raw_data)

    try:
        run_ingestion(context)
        run_validation(context)
        run_normalization(context)
        run_risk_scoring(context)
        run_entity_mapping(context)
        run_report_generation(context)
        run_persistence(context)
        run_trace_logging(context)
    except Exception as e:
        logger.error(f"Execution failed at stage {context.current_stage}: {str(e)}", extra={
            "execution_id": context.execution_id,
            "stage": context.current_stage
        })
        raise e

    return {
        "execution_id": context.execution_id,
        "audit_id": context.audit_id,
        "scores_path": context.runtime_metadata.get("scores_json_path"),
        "audit_path": context.runtime_metadata.get("audit_json_path"),
        "pdf_path": context.report_path,
        "scores": context.scores.model_dump()
    }


def main():
    init_db()
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'run':
        if len(sys.argv) < 3:
            print("Usage: python orchestrator.py run <form_response.json>")
            sys.exit(1)
        result = execute_audit_pipeline(sys.argv[2])
        print(f"\nExecution ID: {result['execution_id']}")
        print(f"Scores saved to: {result['scores_path']}")
        if result['pdf_path']:
            print(f"Report saved to: {result['pdf_path']}")

    elif command == 'score':
        if len(sys.argv) < 3:
            print("Usage: python orchestrator.py score <form_response.json>")
            sys.exit(1)
        data = load_form_responses(sys.argv[2])
        responses = data.get('responses', data)
        scores = calculate_scores(responses)
        print(format_score_report(scores, responses.get('company_name', '')))

    elif command == 'report':
        if len(sys.argv) < 5:
            print("Usage: python orchestrator.py report <audit.json> <scores.json> <output.pdf>")
            sys.exit(1)
        from backend.execution.reporting.report_generator import main as report_main
        sys.argv = sys.argv[1:]
        report_main()

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
