import re
from typing import Dict, Any, Optional

def parse_spend_estimate(spend_str: str) -> Dict[str, Any]:
    """
    Parses a spend string like '$2K-$10K', '< $500', or '$10K+'
    into deterministic numeric ranges.
    """
    if not spend_str:
        return {'min': 0, 'max': 0, 'average': 0}

    spend_str = spend_str.upper().replace(' ', '')

    # Extract all numbers and optional K/M suffixes
    matches = re.findall(r'\$?(\d+)(K|M)?', spend_str)

    values = []
    for num_str, suffix in matches:
        val = int(num_str)
        if suffix == 'K':
            val *= 1000
        elif suffix == 'M':
            val *= 1000000
        values.append(val)

    if not values:
        return {'min': 0, 'max': 0, 'average': 0}

    if '<' in spend_str and len(values) == 1:
        return {'min': 0, 'max': values[0], 'average': values[0] / 2.0}
    elif '+' in spend_str and len(values) == 1:
        return {'min': values[0], 'max': None, 'average': values[0]}
    elif len(values) == 2:
        return {'min': min(values), 'max': max(values), 'average': sum(values) / 2.0}
    elif len(values) == 1:
        return {'min': values[0], 'max': values[0], 'average': float(values[0])}

    return {'min': min(values), 'max': max(values), 'average': sum(values) / len(values)}
