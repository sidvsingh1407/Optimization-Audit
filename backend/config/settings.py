import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Subdirectories
RUNTIME_DIR = DATA_DIR / "runtime"
OUTPUTS_DIR = DATA_DIR / "generated_outputs"
REPORTS_DIR = DATA_DIR / "generated_reports"
TEST_INPUTS_DIR = DATA_DIR / "test_inputs"

# Ensure directories exist
RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Database
DATABASE_PATH = RUNTIME_DIR / "audit_system.db"

# Settings
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
