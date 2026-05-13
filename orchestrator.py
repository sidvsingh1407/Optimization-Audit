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
from datetime import datetime
from pathlib import Path

from scoring_engine import calculate_scores, format_score_report, load_form_responses
from backend.execution.orchestrator import run_audit as new_run_audit

# =============================================================================
# AGENT SIMULATION (MVP: Simple rule-based analysis)
# =============================================================================
# In V2, these will call Claude API with prompts from agent_prompts.md
# For MVP, we use rule-based analysis to keep costs near zero


def analyze_tools(responses, audit_data):
    """Rule-based tool analysis (MVP version)."""
    tools_used = audit_data.get('tools_used', '').lower()
    tool_count = len([t for t in tools_used.split(',') if t.strip()]) if tools_used else 0
    monthly_spend = audit_data.get('monthly_spend', '')

    redundancies = []
    underutilized = []
    waste_estimate = 0

    # Detect common redundancies
    if 'chatgpt' in tools_used and 'claude' in tools_used and 'gemini' in tools_used:
        redundancies.append({
            'tools': ['ChatGPT', 'Claude', 'Gemini'],
            'overlap': 'Multiple general-purpose chatbots - consider consolidating to 1-2',
            'waste_estimate': 500  # Assumed waste
        })
        waste_estimate += 500

    if 'jasper' in tools_used and 'copy' in tools_used:
        redundancies.append({
            'tools': ['Jasper', 'Copy.ai'],
            'overlap': 'Multiple copywriting tools - pick one',
            'waste_estimate': 300
        })
        waste_estimate += 300

    # High spend with low adoption = underutilization
    adoption_score = calculate_scores(responses).get('dimensions', {}).get('adoption', 0)
    if monthly_spend in ['$2K-$10K', '$10K+'] and adoption_score < 12:
        underutilized.append({
            'tool': 'Enterprise AI tools',
            'cost': monthly_spend,
            'evidence': f'High spend ({monthly_spend}) but low adoption score ({adoption_score}/20)'
        })

    return {
        'redundancies': redundancies,
        'gaps': [],  # Would need industry context
        'underutilized': underutilized,
        'total_waste_estimate': f"${waste_estimate}/month",
        'tool_recommendations': [
            {'action': 'review', 'details': 'Consolidate overlapping tools'}
        ] if redundancies else []
    }


def analyze_workflows(responses, scores):
    """Rule-based workflow analysis (MVP version)."""
    integration_score = scores.get('dimensions', {}).get('integration', 0)
    adoption_score = scores.get('dimensions', {}).get('adoption', 0)

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
    governance_score = scores.get('dimensions', {}).get('governance', 0)
    q4_1 = responses.get('q4_1', 'e')
    q4_2 = responses.get('q4_2', 'e')
    q4_3 = responses.get('q4_3', 'e')

    eu_ai_risk = 'low'
    gdpr_risk = 'low'
    required_actions = []

    # EU AI Act risk
    if q4_3 in ['d', 'e']:
        eu_ai_risk = 'high'
        required_actions.append('Complete EU AI Act awareness training for leadership')
        required_actions.append('Assess if any AI uses fall under high-risk categories')

    # GDPR risk
    if q4_2 in ['d', 'e']:
        gdpr_risk = 'high'
        required_actions.append('Implement data privacy review for AI tools')
        required_actions.append('Create approved tools list with privacy vetting')

    # Governance gaps
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

    # Compliance is always priority if flagged
    if compliance_analysis.get('overall_risk') in ['critical', 'high']:
        recommendations.append({
            'rank': 1,
            'action': 'Address compliance gaps immediately (EU AI Act deadline: Aug 2026)',
            'impact': 'Avoid regulatory penalties',
            'effort': 'medium'
        })

    # Tool consolidation if redundancies found
    if tool_analysis.get('redundancies'):
        recommendations.append({
            'rank': 2,
            'action': f"Consolidate redundant tools (estimated waste: {tool_analysis.get('total_waste_estimate', 'N/A')})",
            'impact': 'Cost savings',
            'effort': 'low'
        })

    # Integration focus
    if scores.get('dimensions', {}).get('integration', 0) < 12:
        recommendations.append({
            'rank': 3,
            'action': 'Embed AI into existing workflows rather than adding new tools',
            'impact': 'Higher adoption, better ROI',
            'effort': 'medium'
        })

    # Training if adoption is low
    if scores.get('dimensions', {}).get('adoption', 0) < 12:
        recommendations.append({
            'rank': 4,
            'action': 'Implement structured AI training program for all employees',
            'impact': 'Increase productivity across organization',
            'effort': 'medium'
        })

    # Policy if missing
    if not recommendations or len(recommendations) < 5:
        recommendations.append({
            'rank': len(recommendations) + 1,
            'action': 'Establish AI governance committee and draft usage policy',
            'impact': 'Risk mitigation, consistent decision-making',
            'effort': 'low'
        })

    # Trim to top 5
    return recommendations[:5]


def generate_analytics_report(scores, tool_analysis, workflow_analysis, compliance_analysis, audit_data):
    """Generate the analytics reporter output."""
    total_score = scores.get('total_score', 0)
    monthly_spend = audit_data.get('monthly_spend', 'Unknown')
    waste_estimate = tool_analysis.get('total_waste_estimate', '$0')

    # Parse waste estimate
    waste_num = 0
    if '$' in waste_estimate:
        try:
            waste_num = int(''.join(filter(str.isdigit, waste_estimate)))
        except:
            pass

    # Estimate improvement potential
    governance_score = scores.get('dimensions', {}).get('governance', 0)
    if governance_score < 12:
        potential_savings = waste_num * 12  # Annual
        improvement_pct = 15  # Conservative estimate
    else:
        potential_savings = waste_num * 6
        improvement_pct = 8

    return {
        'executive_summary': f"This audit reveals an AI maturity score of {total_score}/100 ({scores.get('rating', 'Unknown')}). The organization is {'ahead of' if total_score >= 60 else 'behind'} industry benchmarks. Key opportunities identified include tool consolidation (estimated ${waste_num}/month waste), workflow integration improvements, and compliance remediation before the August 2026 EU AI Act deadline.",
        'cost_waste': {
            'monthly_estimate': waste_estimate,
            'annual_estimate': f"${waste_num * 12}/year" if waste_num else 'N/A',
            'waste_categories': ['Redundant tool subscriptions', 'Underutilized enterprise features', 'Manual processes that could be automated']
        },
        'improvement_potential': {
            'time_savings_current': f"{scores.get('dimensions', {}).get('roi', 0) * 4}% (estimated)",
            'time_savings_potential': f"{scores.get('dimensions', {}).get('roi', 0) * 4 + improvement_pct}% (with recommendations)",
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
# MAIN ORCHESTRATION
# =============================================================================


def run_audit(form_response_path):
    """Run complete audit pipeline via lightweight wrapper to backend logic."""
    print("=" * 60)
    print("AI PRODUCTIVITY INTELLIGENCE SYSTEM")
    print("Audit Pipeline (Wrapper mode)")
    print("=" * 60)

    # Delegate to the authoritative backend/execution logic
    res = new_run_audit(form_response_path)

    print()
    print("=" * 60)
    print("AUDIT COMPLETE")
    print(f"Execution ID: {res['execution_id']}")
    print("=" * 60)

    return res


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'run':
        if len(sys.argv) < 3:
            print("Usage: python orchestrator.py run <form_response.json>")
            sys.exit(1)
        run_audit(sys.argv[2])

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
        # Handled by report_generator.py
        from report_generator import main as report_main
        sys.argv = sys.argv[1:]  # Remove 'report' command
        report_main()

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
