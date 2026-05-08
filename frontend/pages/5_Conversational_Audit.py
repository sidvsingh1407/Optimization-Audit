import streamlit as st
import os
import json
from datetime import datetime
import sys
from pathlib import Path

# Setup paths
sys.path.append(str(Path(__file__).parent.parent.parent))

from backend.conversation.session_manager import init_session_state, update_extracted_data, reset_session
from backend.conversation.extractor import extract_structured_data
from backend.conversation.validators import validate_extraction, get_missing_fields
from backend.config.question_mapping import get_question_by_id
from scoring_engine import calculate_scores
from orchestrator import (
    analyze_tools,
    analyze_workflows,
    analyze_compliance,
    generate_analytics_report,
    run_audit
)
from report_generator import generate_report

# Page Config
st.set_page_config(page_title="Conversational Audit", page_icon="💬", layout="wide")

# Check Auth
if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
    st.error("Please login from the main app page.")
    st.stop()

# Init State
init_session_state()

# Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.title("💬 Conversational AI Audit")

    # Check for Gemini API Key
    if not os.environ.get("GEMINI_API_KEY"):
        st.warning("⚠️ GEMINI_API_KEY not found. Conversational AI extraction is disabled. Please proceed directly to the manual form below.")
        st.session_state.conversational_step = 1
    else:
        # Chat Interface
        if st.session_state.conversational_step == 0:
            st.markdown("Describe your company's AI usage. Mention the tools you use, your policies, and the challenges you face.")

            # Display chat messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Chat input
            if prompt := st.chat_input("Tell me about your AI stack..."):
                # Add user message
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Run Extraction
                with st.spinner("Extracting insights..."):
                    raw_data = extract_structured_data(st.session_state.messages)
                    if raw_data:
                        valid_data = validate_extraction(raw_data)
                        update_extracted_data(valid_data)
                        st.session_state.missing_fields = get_missing_fields(st.session_state.extracted_data)

                # Simple bot acknowledgment
                bot_msg = "Thanks! I've updated the scorecard on the right. Please continue describing your AI workflows, or click 'Proceed to Finalize' if you're done."
                st.session_state.messages.append({"role": "assistant", "content": bot_msg})
                with st.chat_message("assistant"):
                    st.markdown(bot_msg)

            # Action buttons
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🔄 Reset Conversation"):
                    reset_session()
                    st.rerun()
            with col_b:
                if st.button("➡️ Proceed to Finalize", type="primary"):
                    st.session_state.missing_fields = get_missing_fields(st.session_state.extracted_data)
                    st.session_state.conversational_step = 1
                    st.rerun()

    # Fallback / Finalization Form
    if st.session_state.conversational_step == 1:
        st.subheader("📝 Finalize Audit Data")
        st.markdown("Please fill in any remaining missing fields before submitting.")

        # Calculate current missing
        missing = get_missing_fields(st.session_state.extracted_data)

        if not missing:
            st.success("All required fields are complete!")

        with st.form("finalize_form"):
            # Company Details (always required manually for now)
            st.markdown("#### Company Details")
            c_name = st.text_input("Company Name*", value=st.session_state.extracted_data.get("company_name", ""))
            c_contact = st.text_input("Contact Name*", value=st.session_state.extracted_data.get("contact_name", ""))
            c_email = st.text_input("Contact Email*", value=st.session_state.extracted_data.get("contact_email", ""))

            # Missing Fields
            if missing:
                st.markdown("#### Missing Information")
                for m in missing:
                    if m == "monthly_spend":
                        val = st.selectbox(
                            "What is your total monthly AI spend?",
                            ["< $500", "$500-$2K", "$2K-$10K", "$10K+"],
                            key="fb_spend"
                        )
                    elif m == "tools_used":
                        val = st.text_area(
                            "List all AI tools currently in use",
                            placeholder="e.g., ChatGPT, Copilot...",
                            key="fb_tools"
                        )
                    else:
                        q_data = get_question_by_id(m)
                        if q_data:
                            val = st.selectbox(
                                q_data["label"],
                                q_data["options"],
                                key=f"fb_{m}"
                            )

            submit_btn = st.form_submit_button("🚀 Generate Audit Report", type="primary")

            if submit_btn:
                # Update data from form
                st.session_state.extracted_data["company_name"] = c_name
                st.session_state.extracted_data["contact_name"] = c_contact
                st.session_state.extracted_data["contact_email"] = c_email

                for m in missing:
                    if m == "monthly_spend":
                        st.session_state.extracted_data["monthly_spend"] = st.session_state.fb_spend
                    elif m == "tools_used":
                        st.session_state.extracted_data["tools_used"] = st.session_state.fb_tools
                    else:
                        st.session_state.extracted_data["responses"][m] = st.session_state[f"fb_{m}"].split(")")[0]

                st.session_state.conversational_step = 2
                st.rerun()

    # Processing & Results
    if st.session_state.conversational_step == 2:
        st.info("🔄 Processing your audit...")

        audit_data = st.session_state.extracted_data
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

        # Output Dirs
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        outputs_dir = Path("data/generated_outputs")
        reports_dir = Path("data/generated_reports")
        outputs_dir.mkdir(parents=True, exist_ok=True)
        reports_dir.mkdir(parents=True, exist_ok=True)

        import re
        safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', audit_data['company_name'])

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

        # Save JSON
        audit_path = outputs_dir / f"audit_{timestamp}.json"
        with open(audit_path, 'w') as f:
            json.dump(audit_result, f, indent=2)

        # Save PDF
        pdf_path = reports_dir / f"report_{safe_name}_{timestamp}.pdf"
        generate_report(audit_data, scores, audit_result['agent_findings'], str(pdf_path))

        st.success("✅ Audit Complete!")

        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Download PDF Report",
                    data=f.read(),
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf"
                )

        if st.button("🔄 Start New Audit"):
            reset_session()
            st.rerun()

with col2:
    st.subheader("📊 Live Scorecard Preview")

    # Calculate live score
    current_responses = st.session_state.extracted_data.get("responses", {})
    if current_responses:
        live_scores = calculate_scores(current_responses)

        st.markdown(f"**Current Score:** {live_scores['total_score']}/100")

        if live_scores['compliance_risk_flag']:
            st.error("⚠️ **Compliance Risk Detected**")
        else:
            st.success("✅ No immediate compliance risks detected")

        st.progress(live_scores['total_score'] / 100.0)
    else:
        st.info("Awaiting input...")

    st.markdown("---")
    st.markdown("#### Fields Extracted:")
    st.write(f"Questions: {len(current_responses)}/15")
    st.write(f"Spend: {'✅' if st.session_state.extracted_data.get('monthly_spend') else '❌'}")
    st.write(f"Tools: {'✅' if st.session_state.extracted_data.get('tools_used') else '❌'}")
