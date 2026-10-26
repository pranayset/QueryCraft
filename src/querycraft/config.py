"""Environment-based configuration helpers."""
import os
from dotenv import load_dotenv

load_dotenv()

def get_setting(name: str, default: str | None = None) -> str | None:
    """Read a setting from environment variables."""
    return os.getenv(name, default)
