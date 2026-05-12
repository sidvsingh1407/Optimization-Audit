import uuid
import json
import sqlite3
import networkx as nx
from typing import Dict, Any, List

from backend.db.database import get_connection
from backend.models.graph_entities import GraphEntity, GraphRelationship
from backend.config.relationship_rules import get_tool_mapping, get_governance_risk_level

def _generate_id(prefix: str, audit_id: str, name: str) -> str:
    """Generate a deterministic ID based on audit_id and entity name."""
    clean_name = name.lower().replace(' ', '_').replace('/', '_')
    return f"{audit_id}_{prefix}_{clean_name}"

def build_graph_for_audit(audit_id: str, audit_data: Dict[str, Any], scores: Dict[str, Any]) -> None:
    """
    Parses audit inputs, applies deterministic rules, generates entities/relationships,
    and persists them to SQLite.
    """
    entities: Dict[str, GraphEntity] = {}
    relationships: List[GraphRelationship] = []

    def add_entity(etype: str, name: str, meta: dict = None) -> str:
        eid = _generate_id(etype, audit_id, name)
        if eid not in entities:
            entities[eid] = GraphEntity(
                entity_id=eid,
                audit_id=audit_id,
                entity_type=etype,
                entity_name=name,
                metadata=meta or {}
            )
        return eid

    def add_relationship(src: str, tgt: str, rtype: str, meta: dict = None):
        rel_id = f"{src}_{rtype}_{tgt}"
        # Prevent duplicate relationship additions
        if not any(r.relationship_id == rel_id for r in relationships):
            relationships.append(GraphRelationship(
                relationship_id=rel_id,
                audit_id=audit_id,
                source_entity_id=src,
                target_entity_id=tgt,
                relationship_type=rtype,
                metadata=meta or {}
            ))

    # 1. Organization Entity
    company_name = audit_data.get("company_name", "Unknown Org")
    org_id = add_entity("org", company_name)

    # 2. Extract tools
    tools_str = audit_data.get("responses", {}).get("tools_used", "")
    tools = [t.strip() for t in tools_str.split(",") if t.strip()]

    # 3. Governance and Risk
    gov_score = scores.get("dimensions", {}).get("governance", 0)
    risk_level = get_governance_risk_level(gov_score)

    # Add Governance Entity
    gov_id = add_entity("governance", f"Governance_Score_{gov_score}", {"score": gov_score, "risk_level": risk_level})
    add_relationship(org_id, gov_id, "has_governance")

    # Add Overall Risk Profile
    risk_profile_id = add_entity("risk_profile", f"Risk_{risk_level.capitalize()}", {"level": risk_level})
    add_relationship(gov_id, risk_profile_id, "creates_risk")

    for tool in tools:
        tool_id = add_entity("tool", tool)
        add_relationship(org_id, tool_id, "uses_tool")

        mapping = get_tool_mapping(tool)

        # Link to Departments
        for dept in mapping.get("departments", []):
            dept_id = add_entity("department", dept)
            add_relationship(dept_id, tool_id, "operates_tool")
            add_relationship(org_id, dept_id, "has_department")

        # Link to Workflows
        for wf in mapping.get("workflows", []):
            wf_id = add_entity("workflow", wf)
            add_relationship(tool_id, wf_id, "supports_workflow")

            # Link workflow to governance risk based on overall org governance
            add_relationship(wf_id, gov_id, "governed_by")

            if risk_level in ["high", "critical"]:
                add_relationship(wf_id, risk_profile_id, "exposed_to_risk")

        # Link to Compliance Exposures
        for comp in mapping.get("compliance_linkage", []):
            comp_id = add_entity("compliance_exposure", comp)
            add_relationship(tool_id, comp_id, "creates_exposure")
            add_relationship(comp_id, gov_id, "mitigated_by")

    # Persist to SQLite
    from backend.db.database import init_db
    init_db() # ensure tables exist
    conn = get_connection()
    cursor = conn.cursor()

    # Clean existing for this audit to allow re-runs
    cursor.execute("DELETE FROM graph_relationships WHERE audit_id = ?", (audit_id,))
    cursor.execute("DELETE FROM graph_entities WHERE audit_id = ?", (audit_id,))

    for eid, ent in entities.items():
        cursor.execute(
            "INSERT INTO graph_entities (entity_id, audit_id, entity_type, entity_name, metadata_json) VALUES (?, ?, ?, ?, ?)",
            (ent.entity_id, ent.audit_id, ent.entity_type, ent.entity_name, json.dumps(ent.metadata))
        )

    for rel in relationships:
        cursor.execute(
            "INSERT INTO graph_relationships (relationship_id, audit_id, source_entity_id, target_entity_id, relationship_type, relationship_strength, metadata_json) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (rel.relationship_id, rel.audit_id, rel.source_entity_id, rel.target_entity_id, rel.relationship_type, rel.relationship_strength, json.dumps(rel.metadata))
        )

    conn.commit()
    conn.close()


def load_graph_from_db(audit_id: str) -> nx.DiGraph:
    """
    Reconstructs a NetworkX DiGraph from SQLite tables for the specified audit_id.
    """
    G = nx.DiGraph()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT entity_id, entity_type, entity_name, metadata_json FROM graph_entities WHERE audit_id = ?", (audit_id,))
    for row in cursor.fetchall():
        eid, etype, ename, meta_json = row
        meta = json.loads(meta_json) if meta_json else {}
        G.add_node(eid, type=etype, name=ename, **meta)

    cursor.execute("SELECT source_entity_id, target_entity_id, relationship_type, relationship_strength, metadata_json FROM graph_relationships WHERE audit_id = ?", (audit_id,))
    for row in cursor.fetchall():
        src, tgt, rtype, strength, meta_json = row
        meta = json.loads(meta_json) if meta_json else {}
        G.add_edge(src, tgt, type=rtype, strength=strength, **meta)

    conn.close()
    return G
