import pytest
from pydantic import ValidationError
from backend.contracts.audit import AuditInputContract

def test_audit_input_contract_valid():
    data = {
        "company_name": "Test Company",
        "responses": {"q1_1": "a", "q2_1": "b"}
    }
    contract = AuditInputContract(**data)
    assert contract.company_name == "Test Company"
    assert contract.responses["q1_1"] == "a"

def test_audit_input_contract_invalid():
    data = {
        "industry": "Finance",
        "responses": {"q1_1": "a"}
    }
    with pytest.raises(ValidationError):
        AuditInputContract(**data) # missing company_name
