import streamlit as st

def init_session_state():
    """Initializes standard variables for conversational audit."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "extracted_data" not in st.session_state:
        st.session_state.extracted_data = {
            "responses": {},
            "monthly_spend": None,
            "tools_used": None,
            "company_name": "Conversational Client",
            "contact_name": "Unknown",
            "contact_email": "unknown@example.com"
        }

    if "missing_fields" not in st.session_state:
        st.session_state.missing_fields = []

    if "conversational_step" not in st.session_state:
        st.session_state.conversational_step = 0

def update_extracted_data(new_validated_data: dict):
    """Merges newly extracted data into session state."""
    # Merge responses
    current_responses = st.session_state.extracted_data.get("responses", {})
    new_responses = new_validated_data.get("responses", {})

    for k, v in new_responses.items():
        if v:
            current_responses[k] = v

    st.session_state.extracted_data["responses"] = current_responses

    # Merge other fields
    if new_validated_data.get("monthly_spend"):
        st.session_state.extracted_data["monthly_spend"] = new_validated_data["monthly_spend"]

    if new_validated_data.get("tools_used"):
        st.session_state.extracted_data["tools_used"] = new_validated_data["tools_used"]

def reset_session():
    """Clears conversational state."""
    st.session_state.messages = []
    st.session_state.extracted_data = {
        "responses": {},
        "monthly_spend": None,
        "tools_used": None,
        "company_name": "Conversational Client",
        "contact_name": "Unknown",
        "contact_email": "unknown@example.com"
    }
    st.session_state.missing_fields = []
    st.session_state.conversational_step = 0
