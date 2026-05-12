from backend.config.governance_rules import evaluate_governance
from backend.models.entities import GovernanceState

def map_governance(responses: dict) -> GovernanceState:
    data = evaluate_governance(responses)
    return GovernanceState(**data)
