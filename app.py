#!/usr/bin/env python3
"""
AI Productivity Intelligence System - Web App
Streamlit-based frontend for running AI audits.

Usage:
  streamlit run app.py

Deploy:
  Push to GitHub, connect to Streamlit Cloud (free hosting)
"""

import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path

from scoring_engine import calculate_scores, format_score_report
from orchestrator import (
    analyze_tools,
    analyze_workflows,
    analyze_compliance,
    generate_analytics_report
)
from report_generator import generate_report


# Page config
st.set_page_config(
    page_title="AI Productivity Audit",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        color: white;
    }
    .score-number {
        font-size: 4rem;
        font-weight: 700;
    }
    .score-label {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    .dimension-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid #eee;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


def render_header():
    """Render the page header."""
    st.markdown('<p class="main-header">AI Productivity Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Audit your organization\'s AI maturity and identify optimization opportunities</p>', unsafe_allow_html=True)


def render_company_section():
    """Render company information section."""
    st.header("🏢 Company Information")

    col1, col2 = st.columns(2)

    with col1:
        company_name = st.text_input("Company Name *", placeholder="Acme Corp")
        industry = st.selectbox(
            "Industry *",
            [
                "Marketing/Advertising",
                "SaaS/Technology",
                "Professional Services",
                "Healthcare",
                "Finance/FinTech",
                "E-commerce/Retail",
                "Manufacturing",
                "Education",
                "Other"
            ]
        )
        contact_name = st.text_input("Contact Name *", placeholder="John Doe")

    with col2:
        employee_count = st.selectbox(
            "Number of Employees *",
            ["10-49", "50-99", "100-249", "250-499", "500+"]
        )
        contact_email = st.text_input("Contact Email *", placeholder="john@acme.com")
        benchmark_opt_in = st.checkbox(
            "Allow anonymized data for benchmarking",
            help="Your data will be anonymized and used for industry benchmarks. No company name or contact info shared."
        )

    return {
        "company_name": company_name,
        "industry": industry,
        "employee_count": employee_count,
        "contact_name": contact_name,
        "contact_email": contact_email,
        "benchmark_opt_in": benchmark_opt_in
    }


def render_score_section(section_name, questions):
    """Render a scoring section with radio questions."""
    st.subheader(section_name)
    responses = {}

    for q_id, question, options in questions:
        key = f"{q_id}_{st.session_state.get('form_key', 0)}"
        responses[q_id] = st.radio(
            question,
            options,
            key=key,
            format_func=lambda x: x.split(")")[1] if ")" in x else x  # Remove a), b), etc.
        )
        st.markdown("")  # Spacing

    return responses


def render_awareness_section():
    """Render Awareness section."""
    questions = [(q, QUESTIONS[q]["text"], QUESTIONS[q]["options"]) for q in ["q1_1", "q1_2", "q1_3"]]
    return render_score_section("Awareness", questions)


def render_adoption_section():
    """Render Adoption section."""
    questions = [(q, QUESTIONS[q]["text"], QUESTIONS[q]["options"]) for q in ["q2_1", "q2_2", "q2_3"]]
    return render_score_section("Adoption", questions)


def render_integration_section():
    """Render Integration section."""
    questions = [(q, QUESTIONS[q]["text"], QUESTIONS[q]["options"]) for q in ["q3_1", "q3_2", "q3_3"]]
    return render_score_section("Integration", questions)


def render_governance_section():
    """Render Governance section."""
    questions = [(q, QUESTIONS[q]["text"], QUESTIONS[q]["options"]) for q in ["q4_1", "q4_2", "q4_3"]]
    return render_score_section("Governance", questions)


def render_roi_section():
    """Render ROI section."""
    questions = [(q, QUESTIONS[q]["text"], QUESTIONS[q]["options"]) for q in ["q5_1", "q5_2", "q5_3"]]
    return render_score_section("ROI", questions)


def render_spend_section():
    """Render spend and tools section."""
    st.header("💰 Spend & Tools")

    monthly_spend = st.selectbox(
        "What is your total monthly AI spend (all tools combined)?",
        ["< $500", "$500-$2K", "$2K-$10K", "$10K+"]
    )

    tools_used = st.text_area(
        "List all AI tools currently in use at your company",
        placeholder="e.g., ChatGPT Enterprise, GitHub Copilot, Jasper, Midjourney, Notion AI",
        help="Comma-separated list"
    )

    spend_breakdown = st.text_area(
        "(Optional) Breakdown of spend by tool",
        placeholder="e.g., ChatGPT Enterprise: $500, Copilot: $1000, Jasper: $300",
        help="Optional: Provide per-tool spend if known"
    )

    return {
        "monthly_spend": monthly_spend,
        "tools_used": tools_used,
        "spend_breakdown": spend_breakdown
    }


def render_results(scores, audit_result, pdf_path):
    """Render the results page."""
    st.markdown("")
    st.success("✅ Audit Complete!")

    # Score display
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="score-box">
            <div class="score-number">{scores['total_score']}/100</div>
            <div class="score-label">{scores['rating']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # Dimension breakdown
    st.subheader("Dimension Breakdown")

    dimensions = scores['dimensions']
    for dim, score in dimensions.items():
        pct = score / 20 * 100
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(pct / 100)
        with col2:
            st.metric(dim.capitalize(), f"{score}/20")

    st.markdown("")

    # Compliance status
    st.subheader("Compliance Status")
    if scores['compliance_risk_flag']:
        st.error("⚠️ **Compliance Risk Detected**")
        st.write("Risk reasons:", ", ".join(scores['compliance_risk_reasons']))
    else:
        st.success("✅ No compliance risks detected")

    st.markdown("")

    # Key findings
    st.subheader("Key Findings")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Tool Analysis**")
        tool_findings = audit_result['agent_findings']['tool_evaluator']
        if tool_findings.get('redundancies'):
            st.warning(f"Found {len(tool_findings['redundancies'])} tool redundancies")
        if tool_findings.get('underutilized'):
            st.warning(f"Found {len(tool_findings['underutilized'])} underutilized tools")
        if not tool_findings.get('redundancies') and not tool_findings.get('underutilized'):
            st.info("Tool stack appears efficient")

    with col2:
        st.markdown("**Workflow Analysis**")
        workflow_findings = audit_result['agent_findings']['workflow_optimizer']
        quick_wins = workflow_findings.get('quick_wins', [])
        if quick_wins:
            st.info(f"Found {len(quick_wins)} quick win opportunities")
        else:
            st.info("Focus on integration over new tools")

    st.markdown("")

    # Recommendations
    st.subheader("Top Recommendations")
    recs = audit_result['agent_findings']['analytics_reporter']['top_5_recommendations']
    for i, rec in enumerate(recs, 1):
        with st.expander(f"{i}. {rec['action']}"):
            st.write(f"**Impact:** {rec['impact']}")
            st.write(f"**Effort:** {rec['effort']}")

    st.markdown("")

    # PDF Download
    st.subheader("Download Report")
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download PDF Report",
                data=f.read(),
                file_name=os.path.basename(pdf_path),
                mime="application/pdf"
            )
    else:
        st.warning("PDF report not available")


def main():
    """Main app."""
    render_header()

    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'form_key' not in st.session_state:
        st.session_state.form_key = 0

    # Progress bar
    if st.session_state.step == 0:
        st.progress(0)
    elif st.session_state.step == 1:
        st.progress(0.5)
    else:
        st.progress(1.0)

    # Step 0: Company + All Form Sections
    if st.session_state.step == 0:
        st.markdown("")

        # Company section
        company_data = render_company_section()

        st.markdown("")
        st.divider()

        # Scoring sections
        awareness = render_awareness_section()
        st.markdown("")
        st.divider()

        adoption = render_adoption_section()
        st.markdown("")
        st.divider()

        integration = render_integration_section()
        st.markdown("")
        st.divider()

        governance = render_governance_section()
        st.markdown("")
        st.divider()

        roi = render_roi_section()
        st.markdown("")
        st.divider()

        # Spend section
        spend_data = render_spend_section()

        st.markdown("")

        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Run AI Audit", type="primary", use_container_width=True):
                # Validate required fields
                if not all([
                    company_data['company_name'],
                    company_data['contact_name'],
                    company_data['contact_email']
                ]):
                    st.error("Please fill in all required fields (marked with *)")
                else:
                    # Combine all data
                    responses = {**awareness, **adoption, **integration, **governance, **roi}

                    audit_data = {
                        **company_data,
                        **spend_data,
                        "responses": responses
                    }

                    st.session_state.audit_data = audit_data
                    st.session_state.step = 1
                    st.rerun()

    # Step 1: Processing
    elif st.session_state.step == 1:
        st.markdown("")
        st.info("🔄 Processing your audit...")

        audit_data = st.session_state.audit_data
        responses = audit_data['responses']

        # Run scoring
        scores = calculate_scores(responses)

        # Run agent analyses
        tool_analysis = analyze_tools(responses, audit_data)
        workflow_analysis = analyze_workflows(responses, scores)
        compliance_analysis = analyze_compliance(responses, scores)
        analytics_report = generate_analytics_report(
            scores, tool_analysis, workflow_analysis, compliance_analysis, audit_data
        )

        # Generate PDF
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_name = audit_data['company_name'].replace(' ', '_').replace('/', '_')
        pdf_path = f"report_{safe_name}_{timestamp}.pdf"

        audit_result = {
            'company_name': audit_data['company_name'],
            'audit_date': datetime.now().isoformat(),
            'scores': scores,
            'agent_findings': {
                'tool_evaluator': tool_analysis,
                'workflow_optimizer': workflow_analysis,
                'compliance_auditor': compliance_analysis,
                'analytics_reporter': analytics_report,
            }
        }

        generate_report(audit_data, scores, audit_result['agent_findings'], pdf_path)

        # Show results
        render_results(scores, audit_result, pdf_path)

        # New audit button
        st.markdown("")
        if st.button("🔄 Start New Audit"):
            st.session_state.step = 0
            st.session_state.form_key += 1
            st.rerun()


if __name__ == "__main__":
    main()
