import os
import streamlit as st

class Settings:
    @staticmethod
    def get_config(key: str, default: str = None) -> str:
        """
        Safe configuration loader that checks multiple sources:
        1. Streamlit Secrets (st.secrets)
        2. Environment Variables (os.environ)
        3. Default fallback
        """
        # Try Streamlit Secrets First
        try:
            if key in st.secrets:
                return st.secrets[key]
        except Exception:
            # Not running in Streamlit or secrets not configured
            pass

        # Try Environment Variables
        env_value = os.environ.get(key)
        if env_value is not None:
            return env_value

        return default

    @property
    def gemini_api_key(self) -> str:
        return self.get_config("GEMINI_API_KEY", "")

    @property
    def environment(self) -> str:
        return self.get_config("ENVIRONMENT", "production")

    @property
    def db_path(self) -> str:
        return self.get_config("DB_PATH", "data/audit_system.db")

    @property
    def auth_credentials(self) -> dict:
        """Returns auth configuration for streamlit-authenticator"""
        try:
            if "credentials" in st.secrets:
                return dict(st.secrets["credentials"])
        except Exception:
            pass
        return {}

    @property
    def cookie_config(self) -> dict:
        try:
            if "cookie" in st.secrets:
                return dict(st.secrets["cookie"])
        except Exception:
            pass
        return {
            "expiry_days": 30,
            "key": "some_signature_key",
            "name": "some_cookie_name"
        }

settings = Settings()
