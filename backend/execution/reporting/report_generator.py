#!/usr/bin/env python3
"""
AI Productivity Intelligence System - Report Generator
Generates PDF audit reports from scoring results and agent findings.

Usage: python report_generator.py <audit_data.json> <scores.json> <output.pdf>
"""

import json
import sys
from backend.config.settings import OUTPUTS_DIR, REPORTS_DIR, RUNTIME_DIR

from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


# Color scheme (professional, clean)
COLOR_PRIMARY = "#1a1a2e"      # Dark navy
COLOR_SECONDARY = "#16213e"    # Navy
COLOR_ACCENT = "#0f3460"       # Blue
COLOR_HIGHLIGHT = "#e94560"    # Red accent for risks
COLOR_SUCCESS = "#2ecc71"      # Green for positive
COLOR_BG_LIGHT = "#f8f9fa"     # Light gray background


def get_styles():
    """Create paragraph styles for the report."""
    styles = getSampleStyleSheet()

    # Use try/except for custom styles in case they already exist
    try:
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=24,
            textColor=colors.HexColor(COLOR_PRIMARY),
            spaceAfter=30,
            alignment=TA_CENTER,
        ))
    except KeyError:
        pass

    try:
        styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=16,
            textColor=colors.HexColor(COLOR_PRIMARY),
            spaceBefore=20,
            spaceAfter=12,
        ))
    except KeyError:
        pass

    try:
        styles.add(ParagraphStyle(
            name='SubHeading',
            parent=styles['Heading3'],
            fontName='Helvetica-Bold',
            fontSize=12,
            textColor=colors.HexColor(COLOR_SECONDARY),
            spaceBefore=12,
            spaceAfter=6,
        ))
    except KeyError:
        pass

    try:
        styles.add(ParagraphStyle(
            name='BodyText',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            leading=14,
        ))
    except KeyError:
        pass

    try:
        styles.add(ParagraphStyle(
            name='RiskBox',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            textColor=colors.white,
            backColor=colors.HexColor(COLOR_HIGHLIGHT),
            borderPadding=10,
            spaceBefore=10,
            spaceAfter=10,
        ))
    except KeyError:
        pass

    try:
        styles.add(ParagraphStyle(
            name='ScoreBox',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=colors.HexColor(COLOR_PRIMARY),
            alignment=TA_CENTER,
        ))
    except KeyError:
        pass

    return styles


def create_header_table(company_name, audit_date, report_id):
    """Create the report header table."""
    header_data = [
        [Paragraph("AI PRODUCTIVITY INTELLIGENCE", get_styles()['CustomTitle'])],
        [Paragraph("Audit Report", get_styles()['SubHeading'])],
        [Spacer(1, 20)],
        [Paragraph(f"<b>Company:</b> {company_name}", get_styles()['BodyText'])],
        [Paragraph(f"<b>Audit Date:</b> {audit_date}", get_styles()['BodyText'])],
        [Paragraph(f"<b>Report ID:</b> {report_id}", get_styles()['BodyText'])],
    ]

    header_table = Table(header_data, colWidths=[6*inch])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    return header_table


def create_score_gauge(score, rating):
    """Create a visual score representation."""
    # Determine color based on score
    if score >= 80:
        score_color = COLOR_SUCCESS
    elif score >= 60:
        score_color = "#f39c12"  # Orange
    elif score >= 40:
        score_color = "#e67e22"  # Dark orange
    else:
        score_color = COLOR_HIGHLIGHT

    score_data = [
        [Paragraph(f"AI MATURITY SCORE", get_styles()['SubHeading'])],
        [Spacer(1, 10)],
        [Paragraph(f"<b style='font-size: 36pt; color: {score_color}'>{score}/100</b>", get_styles()['ScoreBox'])],
        [Spacer(1, 10)],
        [Paragraph(f"Rating: <b>{rating}</b>", get_styles()['BodyText'])],
    ]

    score_table = Table(score_data, colWidths=[3*inch])
    score_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor(COLOR_BG_LIGHT)),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor(COLOR_PRIMARY)),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))

    return score_table


def create_dimension_breakdown(scores):
    """Create dimension score table."""
    dimensions = [
        ("Awareness", scores['dimensions']['awareness'], 20),
        ("Adoption", scores['dimensions']['adoption'], 20),
        ("Integration", scores['dimensions']['integration'], 20),
        ("Governance", scores['dimensions']['governance'], 20),
        ("ROI", scores['dimensions']['roi'], 20),
    ]

    data = [
        [
            Paragraph("<b>Dimension</b>", get_styles()['BodyText']),
            Paragraph("<b>Score</b>", get_styles()['BodyText']),
            Paragraph("<b>Rating</b>", get_styles()['BodyText']),
        ]
    ]

    for dim_name, dim_score, max_score in dimensions:
        pct = dim_score / max_score * 100
        if pct >= 75:
            rating = "Strong"
        elif pct >= 50:
            rating = "Moderate"
        else:
            rating = "Needs Work"

        data.append([
            Paragraph(dim_name, get_styles()['BodyText']),
            Paragraph(f"{dim_score}/{max_score}", get_styles()['BodyText']),
            Paragraph(rating, get_styles()['BodyText']),
        ])

    table = Table(data, colWidths=[3*inch, 1.2*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLOR_PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor(COLOR_BG_LIGHT)]),
    ]))

    return table


def create_compliance_alert(compliance_flag, compliance_reasons):
    """Create compliance risk alert box."""
    if not compliance_flag:
        return None

    alert_text = """
    <b>COMPLIANCE RISK DETECTED</b><br/><br/>
    This organization has identified compliance risks related to EU AI Act and/or GDPR requirements.
    The EU AI Act compliance deadline is <b>August 2026</b>. Immediate action is recommended
    to avoid potential penalties and ensure regulatory compliance.<br/><br/>
    <b>Identified Risks:</b> """ + ", ".join(compliance_reasons)

    alert_para = Paragraph(alert_text, get_styles()['RiskBox'])
    return alert_para


def create_recommendations_table(recommendations):
    """Create prioritized recommendations table."""
    data = [
        [
            Paragraph("<b>#</b>", get_styles()['BodyText']),
            Paragraph("<b>Recommendation</b>", get_styles()['BodyText']),
            Paragraph("<b>Impact</b>", get_styles()['BodyText']),
            Paragraph("<b>Effort</b>", get_styles()['BodyText']),
        ]
    ]

    for rec in recommendations[:5]:  # Top 5
        data.append([
            Paragraph(str(rec.get('rank', '')), get_styles()['BodyText']),
            Paragraph(rec.get('action', ''), get_styles()['BodyText']),
            Paragraph(rec.get('impact', ''), get_styles()['BodyText']),
            Paragraph(rec.get('effort', ''), get_styles()['BodyText']),
        ])

    table = Table(data, colWidths=[0.5*inch, 3*inch, 1.2*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLOR_PRIMARY)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    return table


def generate_report(audit_data, scores, agent_findings, output_path):
    """Generate the full PDF report."""

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
    )

    story = []
    styles = get_styles()

    # === PAGE 1: Executive Summary ===

    # Header
    company_name = audit_data.get('company_name', 'Unknown')
    audit_date = datetime.now().strftime("%Y-%m-%d")
    report_id = f"AUDIT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    story.append(create_header_table(company_name, audit_date, report_id))
    story.append(Spacer(1, 30))

    # Score gauge
    story.append(create_score_gauge(scores['total_score'], scores['rating']))
    story.append(Spacer(1, 20))

    # Dimension breakdown
    story.append(Paragraph("Dimension Breakdown", styles['SectionHeading']))
    story.append(create_dimension_breakdown(scores))
    story.append(Spacer(1, 20))

    # Compliance alert (if applicable)
    if scores['compliance_risk_flag']:
        story.append(Paragraph("Compliance Alert", styles['SectionHeading']))
        alert = create_compliance_alert(
            scores['compliance_risk_flag'],
            scores['compliance_risk_reasons']
        )
        if alert:
            story.append(alert)

    story.append(PageBreak())

    # === PAGE 2: Findings ===

    story.append(Paragraph("Key Findings", styles['SectionHeading']))

    # Tool findings
    if agent_findings.get('tool_evaluator'):
        story.append(Paragraph("Tool Stack Analysis", styles['SubHeading']))
        tool_findings = agent_findings['tool_evaluator']

        redundancies = tool_findings.get('redundancies', [])
        if redundancies:
            story.append(Paragraph("<b>Redundancies identified:</b>", styles['BodyText']))
            for r in redundancies:
                tools = r.get('tools', [])
                overlap = r.get('overlap', '')
                story.append(Paragraph(f"  - {', '.join(tools)}: {overlap}", styles['BodyText']))
            story.append(Spacer(1, 10))

        underutilized = tool_findings.get('underutilized', [])
        if underutilized:
            story.append(Paragraph("<b>Underutilized tools:</b>", styles['BodyText']))
            for u in underutilized:
                tool = u.get('tool', '')
                cost = u.get('cost', '')
                story.append(Paragraph(f"  - {tool}: ${cost}/month", styles['BodyText']))
            story.append(Spacer(1, 10))

        story.append(Spacer(1, 15))

    # Workflow findings
    if agent_findings.get('workflow_optimizer'):
        story.append(Paragraph("Workflow Analysis", styles['SubHeading']))
        workflow_findings = agent_findings['workflow_optimizer']
        quick_wins = workflow_findings.get('quick_wins', [])
        if quick_wins:
            story.append(Paragraph("<b>Quick Wins (implement within 1 week):</b>", styles['BodyText']))
            for win in quick_wins[:3]:
                story.append(Paragraph(f"  - {win.get('action', '')}", styles['BodyText']))
        story.append(Spacer(1, 15))

    # Compliance findings
    if agent_findings.get('compliance_auditor'):
        story.append(Paragraph("Compliance Assessment", styles['SubHeading']))
        compliance = agent_findings['compliance_auditor']
        summary = compliance.get('summary', 'No compliance summary available.')
        story.append(Paragraph(summary, styles['BodyText']))
        story.append(Spacer(1, 15))

    story.append(PageBreak())

    # === PAGE 3: Recommendations ===

    story.append(Paragraph("Top 5 Recommendations", styles['SectionHeading']))

    if agent_findings.get('analytics_reporter'):
        recommendations = agent_findings['analytics_reporter'].get('top_5_recommendations', [])
        story.append(create_recommendations_table(recommendations))
        story.append(Spacer(1, 30))

        # Cost waste summary
        cost_data = agent_findings['analytics_reporter'].get('cost_waste', {})
        if cost_data:
            story.append(Paragraph("Cost Waste Estimate", styles['SectionHeading']))
            waste_text = f"""
            <b>Monthly Waste:</b> {cost_data.get('monthly_estimate', 'N/A')}<br/>
            <b>Annual Waste:</b> {cost_data.get('annual_estimate', 'N/A')}<br/><br/>
            <b>Categories:</b><br/>
            """
            for cat in cost_data.get('waste_categories', []):
                waste_text += f"  - {cat}<br/>"
            story.append(Paragraph(waste_text, styles['BodyText']))

    # Footer
    story.append(Spacer(1, 50))
    footer = Paragraph(
        "<i>Generated by AI Productivity Intelligence System | Confidential</i>",
        styles['BodyText']
    )
    story.append(footer)

    # Build PDF
    doc.build(story)
    return output_path


def main():
    if len(sys.argv) < 4:
        print("Usage: python report_generator.py <audit_data.json> <scores.json> <output.pdf>")
        sys.exit(1)

    audit_file = sys.argv[1]
    scores_file = sys.argv[2]
    output_file = sys.argv[3]

    try:
        with open(audit_file, 'r') as f:
            audit_data = json.load(f)

        with open(scores_file, 'r') as f:
            scores = json.load(f)

        # Placeholder for agent findings (would come from agent execution)
        agent_findings = {
            'tool_evaluator': {
                'redundancies': [],
                'underutilized': [],
            },
            'workflow_optimizer': {
                'quick_wins': [],
            },
            'compliance_auditor': {},
            'analytics_reporter': {
                'top_5_recommendations': [],
                'cost_waste': {},
            }
        }

        generate_report(audit_data, scores, agent_findings, output_file)
        print(f"Report generated: {output_file}")

    except FileNotFoundError as e:
        print(f"Error: File not found: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
