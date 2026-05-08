import os

class Settings:
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    DATABASE_URL = os.environ.get("DATABASE_URL", "")
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

settings = Settings()
