import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Service configurations"""
    APP_VERSION = os.environ.get("VERSION", "0.0.0")
    APP_TITLE = os.environ.get("APP_TITLE", "FastAPI template")
    APP_DESCRIPTION = os.environ.get("APP_DESCRIPTION", "A template for FastAPI.")

    DB_URL = os.environ.get("DB_URL", "")
    LINE_TOKEN = os.environ.get("LINE_TOKEN", "")  # LINE token for chatbot 
    API_KEY = os.environ.get("API_KEY", "secret")
    # This flag is used during development for local debug
    MOCK_RESPONSE = os.environ.get("MOCK_RESPONSE", "false").lower() == "true"
