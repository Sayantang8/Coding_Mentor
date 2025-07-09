"""
Configuration settings for AI Coding Mentor
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Application settings
APP_TITLE = "🧠 AI Coding Mentor"
APP_VERSION = "2.0"
APP_DESCRIPTION = "Interactive Coding Problem Solver with AI Assistance"

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_BASE_URL = "https://api.openai.com/v1"

# Code Editor Settings
DEFAULT_THEME = "monokai"
DEFAULT_FONT_SIZE = 14
DEFAULT_TAB_SIZE = 4

# Supported Languages
SUPPORTED_LANGUAGES = ["python", "java", "javascript"]

# Analysis Tools Configuration
ANALYSIS_TIMEOUT = 30  # seconds
MAX_CODE_LENGTH = 10000  # characters

# UI Configuration
LAYOUT_MODE = "wide"
SIDEBAR_STATE = "auto"

# Export Settings
EXPORT_FORMAT = "json"
MAX_EXPORT_SIZE = 1024 * 1024  # 1MB

# Debug Settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

def get_config():
    """Return configuration dictionary"""
    return {
        "app": {
            "title": APP_TITLE,
            "version": APP_VERSION,
            "description": APP_DESCRIPTION
        },
        "openai": {
            "api_key": OPENAI_API_KEY,
            "org_id": OPENAI_ORG_ID,
            "model": OPENAI_MODEL
        },
        "editor": {
            "theme": DEFAULT_THEME,
            "font_size": DEFAULT_FONT_SIZE,
            "tab_size": DEFAULT_TAB_SIZE
        },
        "languages": SUPPORTED_LANGUAGES,
        "analysis": {
            "timeout": ANALYSIS_TIMEOUT,
            "max_code_length": MAX_CODE_LENGTH
        },
        "ui": {
            "layout": LAYOUT_MODE,
            "sidebar": SIDEBAR_STATE
        },
        "export": {
            "format": EXPORT_FORMAT,
            "max_size": MAX_EXPORT_SIZE
        },
        "debug": {
            "enabled": DEBUG,
            "log_level": LOG_LEVEL
        }
    }