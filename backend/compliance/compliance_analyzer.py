from typing import Dict, Any

def analyze_compliance(responses: Dict[str, str], scores: Dict[str, Any]) -> Dict[str, Any]:
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
