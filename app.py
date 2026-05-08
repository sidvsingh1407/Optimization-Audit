import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

# Ensure secrets exist
secrets_path = ".streamlit/secrets.toml"
if not os.path.exists(secrets_path):
    os.makedirs(".streamlit", exist_ok=True)
    with open(secrets_path, "w") as f:
        f.write('[credentials]\n')
        f.write('usernames = { "admin" = { "email" = "admin@example.com", "name" = "Admin", "password" = "$2b$12$Nq9T.P0fG/Y1G4/uL.3WzO1h9iFhO.O0rA.2F/7T7b9lq2vE3dFqO" } }\n')

st.set_page_config(
    page_title="AI Productivity Intelligence System",
    page_icon="🧠",
    layout="wide"
)

import toml
# Load config
try:
    with open(secrets_path) as file:
        config = toml.load(file)
except Exception as e:
    config = {'credentials': {'usernames': {'admin': {'email': 'admin@example.com', 'name': 'Admin', 'password': '$2b$12$Nq9T.P0fG/Y1G4/uL.3WzO1h9iFhO.O0rA.2F/7T7b9lq2vE3dFqO'}}}}

authenticator = stauth.Authenticate(
    config['credentials'],
    'audit_system_cookie',
    'auth_key',
    cookie_expiry_days=30
)

# Render login
authenticator.login()

if st.session_state["authentication_status"]:
    st.sidebar.success(f'Welcome *{st.session_state["name"]}*')
    authenticator.logout('Logout', 'sidebar')

    st.title("🧠 AI Productivity Intelligence System")
    st.markdown("---")
    st.markdown("""
    ### Welcome to the Audit Portal

    Please select a module from the sidebar:

    - **1. Structured Audit:** The classic, form-based intake system.
    - **5. Conversational Audit:** The guided AI chat intake system.
    """)

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

