import os
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(ROOT_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "codemate-development-key")
    MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "demo").strip().lower()
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
    API_KEY = os.getenv("API_KEY", "")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
    CODESEARCHNET_PATH = os.getenv(
        "CODESEARCHNET_PATH",
        str(ROOT_DIR / "datasets" / "codesearchnet"),
    )
    MBPP_SAMPLE_SIZE = int(os.getenv("MBPP_SAMPLE_SIZE", "50"))
    HUMANEVAL_PATH = os.getenv(
        "HUMANEVAL_PATH",
        str(ROOT_DIR / "datasets" / "humaneval" / "human-eval-master" / "data" / "HumanEval.jsonl.gz"),
    )
    MAX_CODE_LENGTH = int(os.getenv("MAX_CODE_LENGTH", "12000"))
    MODEL_TIMEOUT = int(os.getenv("MODEL_TIMEOUT", "60"))
