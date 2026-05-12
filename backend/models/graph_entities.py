from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class GraphEntity:
    entity_id: str
    audit_id: str
    entity_type: str
    entity_name: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class GraphRelationship:
    relationship_id: str
    audit_id: str
    source_entity_id: str
    target_entity_id: str
    relationship_type: str
    relationship_strength: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
