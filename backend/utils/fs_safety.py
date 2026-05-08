import os
import re
from pathlib import Path
from backend.utils.logger import app_logger

def sanitize_filename(name: str) -> str:
    """
    Sanitizes strings to be safe for filenames.
    Replaces non-alphanumeric chars (excluding _ and -) with underscores.
    """
    if not name:
        return "Unknown"
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', str(name))

def ensure_directory(path_str: str) -> bool:
    """
    Safely creates a directory if it doesn't exist.
    Returns True if successful/exists, False otherwise.
    """
    try:
        os.makedirs(path_str, exist_ok=True)
        return True
    except Exception as e:
        app_logger.error(f"Failed to create directory {path_str}: {e}")
        return False

def get_safe_output_dir(base_dir: str = "data/generated_outputs") -> Path:
    """Gets a safe path for generic outputs, creating it if necessary."""
    ensure_directory(base_dir)
    return Path(base_dir)

def get_safe_report_dir(base_dir: str = "data/generated_reports") -> Path:
    """Gets a safe path for reports, creating it if necessary."""
    ensure_directory(base_dir)
    return Path(base_dir)
