from backend.config.workflow_rules import infer_workflows
from backend.models.entities import Workflow

def map_workflows(industry: str, tools: list) -> list[Workflow]:
    workflow_data = infer_workflows(industry, tools)
    return [Workflow(**w) for w in workflow_data]
