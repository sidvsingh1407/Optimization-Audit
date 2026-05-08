# Point mapping for responses (a=20, b=15, c=10, d=5, e=0)
RESPONSE_POINTS = {
    'a': 20,
    'b': 15,
    'c': 10,
    'd': 5,
    'e': 0,
    'A': 20,
    'B': 15,
    'C': 10,
    'D': 5,
    'E': 0,
}

# Question groupings by dimension
DIMENSION_QUESTIONS = {
    'awareness': ['q1_1', 'q1_2', 'q1_3'],
    'adoption': ['q2_1', 'q2_2', 'q2_3'],
    'integration': ['q3_1', 'q3_2', 'q3_3'],
    'governance': ['q4_1', 'q4_2', 'q4_3'],
    'roi': ['q5_1', 'q5_2', 'q5_3'],
}

# Compliance risk triggers (these responses indicate risk)
COMPLIANCE_RISK_RESPONSES = {
    'q4_1': ['d', 'e'],  # No policy or informal only
    'q4_2': ['d', 'e'],  # Employee discretion or no oversight
    'q4_3': ['d', 'e'],  # Unaware or no action on EU AI Act
}
