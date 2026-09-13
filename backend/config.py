import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "codemate-development-key")
    MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "demo").strip().lower()
    MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5-coder:7b")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    API_KEY = os.getenv("API_KEY", "")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
    MAX_CODE_LENGTH = int(os.getenv("MAX_CODE_LENGTH", "12000"))
    MODEL_TIMEOUT = int(os.getenv("MODEL_TIMEOUT", "60"))
