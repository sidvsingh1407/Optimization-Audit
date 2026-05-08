#!/usr/bin/env python3
"""
AI Productivity Intelligence System - Scoring Engine
Calculates AI maturity scores from form responses.

Usage: python scoring_engine.py <form_response.json>
Output: Prints score breakdown and sets compliance flags
"""

import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import sys
from typing import Dict, Any, Tuple, Optional

from backend.config.constants import RESPONSE_POINTS, DIMENSION_QUESTIONS, COMPLIANCE_RISK_RESPONSES

def response_to_points(response: str) -> int:
    """Convert a single response to points."""
    return RESPONSE_POINTS.get(response, 0)


def calculate_dimension_score(responses: Dict[str, str], dimension: str) -> Tuple[int, bool]:
    """
    Calculate score for a single dimension.

    Returns:
        Tuple of (score, has_missing_data)
    """
    questions = DIMENSION_QUESTIONS[dimension]
    points = []
    missing = False

    for q in questions:
        response = responses.get(q)
        if response is None or response.strip() == '':
            missing = True
        else:
            points.append(response_to_points(response))

    # Handle missing data
    if len(points) == 0:
        # All questions missing
        return 0, True
    elif len(points) == 1:
        # 2 questions missing: average the 1, multiply by 1.5
        return round(points[0] * 1.5), True
    elif len(points) == 2:
        # 1 question missing: average the 2, multiply by 1.5
        return round(sum(points) / 2 * 1.5), True
    else:
        # All 3 questions present
        return round(sum(points) / 3), False


def check_compliance_risk(responses: Dict[str, str]) -> Tuple[bool, list]:
    """
    Check if compliance risk flag should be set.

    Returns:
        Tuple of (has_risk, list of risk reasons)
    """
    risk_reasons = []

    for question, risky_responses in COMPLIANCE_RISK_RESPONSES.items():
        response = responses.get(question)
        if response in risky_responses:
            risk_reasons.append(question)

    return len(risk_reasons) > 0, risk_reasons


def detect_contradictions(responses: Dict[str, str]) -> list:
    """
    Detect contradictory responses that need manual review.

    Returns:
        List of contradiction descriptions
    """
    contradictions = []

    # Contradiction 1: High adoption but low frequency
    adoption_rate = responses.get('q2_1', 'e')
    frequency = responses.get('q2_3', 'e')

    if adoption_rate in ['a', 'b'] and frequency in ['d', 'e']:
        contradictions.append(
            f"High adoption ({adoption_rate}) contradicts low frequency ({frequency})"
        )

    # Contradiction 2: Deep integration but no tools
    integration = responses.get('q3_1', 'e')
    tool_count = responses.get('q2_2', 'e')

    if integration == 'a' and tool_count in ['d', 'e']:
        contradictions.append(
            f"Deep integration ({integration}) contradicts low tool count ({tool_count})"
        )

    return contradictions


def get_score_rating(total_score: int) -> str:
    """Get rating label for total score."""
    if total_score >= 80:
        return "AI Mature"
    elif total_score >= 60:
        return "AI Adopting"
    elif total_score >= 40:
        return "AI Emerging"
    elif total_score >= 20:
        return "AI Initial"
    else:
        return "AI Nascent"


def calculate_scores(responses: Dict[str, str]) -> Dict[str, Any]:
    """
    Calculate all scores from form responses.

    Args:
        responses: Dictionary of question_id -> response

    Returns:
        Dictionary with all scores, flags, and metadata
    """
    result = {
        'dimensions': {},
        'total_score': 0,
        'rating': '',
        'compliance_risk_flag': False,
        'compliance_risk_reasons': [],
        'contradictions': [],
        'missing_data_flags': [],
    }

    # Calculate each dimension
    for dimension in DIMENSION_QUESTIONS.keys():
        score, has_missing = calculate_dimension_score(responses, dimension)
        result['dimensions'][dimension] = score
        if has_missing:
            result['missing_data_flags'].append(dimension)

    # Calculate total
    result['total_score'] = sum(result['dimensions'].values())
    result['rating'] = get_score_rating(result['total_score'])

    # Check compliance risk
    has_risk, risk_reasons = check_compliance_risk(responses)
    result['compliance_risk_flag'] = has_risk
    result['compliance_risk_reasons'] = risk_reasons

    # Detect contradictions
    result['contradictions'] = detect_contradictions(responses)

    return result


def format_score_report(scores: Dict[str, Any], company_name: str = "") -> str:
    """Format scores as human-readable report."""
    lines = [
        "=" * 50,
        f"AI MATURITY SCORE REPORT",
        f"Company: {company_name or 'Unknown'}",
        "=" * 50,
        "",
        f"TOTAL SCORE: {scores['total_score']}/100",
        f"RATING: {scores['rating']}",
        "",
        "DIMENSION BREAKDOWN:",
        f"  Awareness:   {scores['dimensions']['awareness']}/20",
        f"  Adoption:    {scores['dimensions']['adoption']}/20",
        f"  Integration: {scores['dimensions']['integration']}/20",
        f"  Governance:  {scores['dimensions']['governance']}/20",
        f"  ROI:         {scores['dimensions']['roi']}/20",
        "",
    ]

    if scores['compliance_risk_flag']:
        lines.extend([
            "[!] COMPLIANCE RISK FLAG: TRUE",
            f"    Risk reasons: {', '.join(scores['compliance_risk_reasons'])}",
            "",
        ])

    if scores['contradictions']:
        lines.extend([
            "[!] CONTRADICTIONS DETECTED (Manual Review Needed):",
        ])
        for contradiction in scores['contradictions']:
            lines.append(f"    - {contradiction}")
        lines.append("")

    if scores['missing_data_flags']:
        lines.extend([
            "[!] MISSING DATA IN DIMENSIONS:",
        ])
        for dim in scores['missing_data_flags']:
            lines.append(f"    - {dim}")
        lines.append("")

    lines.append("=" * 50)

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scoring_engine.py <form_response.json>")
        sys.exit(1)

    filepath = sys.argv[1]

    from backend.utils.data_loader import load_form_responses

    try:
        data = load_form_responses(filepath)
        responses = data.get('responses', data)  # Handle both formats
        company_name = data.get('company_name', data.get('responses', {}).get('company_name', ''))

        scores = calculate_scores(responses)
        report = format_score_report(scores, company_name)
        print(report)

        # Output JSON for programmatic use
        print("\n\nJSON OUTPUT:")
        print(json.dumps(scores, indent=2))

    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
