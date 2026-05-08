import json
from typing import Dict, Any

def load_form_responses(filepath: str) -> Dict[str, Any]:
    """Load form responses from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)
