"""Security and input-validation regression tests."""
import pytest
from pydantic import ValidationError
from agents.base import AuditTrail, SecurityException
from agents.models import SystemTaskPayload
from agents.supervisor import SystemSupervisor


def test_changed_payload_hash_invalidates_hmac():
    audit = AuditTrail(secret_key="a" * 32)
    audit.log("supervisor", "system", "test", {"event": "checked"})
    assert audit.verify_integrity()
    audit.logs[0]["payload_hash"] = "0" * 64
    assert not audit.verify_integrity()


def test_changed_signed_metadata_invalidates_hmac():
    audit = AuditTrail(secret_key="b" * 32)
    audit.log("supervisor", "system", "test", {"event": 1})
    audit.log("supervisor", "system", "test", {"event": 2})
    audit.logs[0]["actor"] = "attacker"
    assert not audit.verify_integrity()


def test_public_logs_are_copies():
    audit = AuditTrail(secret_key="c" * 32)
    audit.log("supervisor", "system", "test", {"event": 3})
    audit.get_trail()[0]["actor"] = "tampered copy"
    assert audit.verify_integrity()


def test_nested_phi_in_attributes_is_rejected():
    supervisor = SystemSupervisor()
    payload = SystemTaskPayload(
        task_id="T01", target_identifier="SPECIMEN01", primary_metric=1.0,
        attributes={"metadata": [{"contact": "someone@hospital.org"}]},
    )
    with pytest.raises(SecurityException):
        supervisor.process_task(payload)


@pytest.mark.parametrize("metric", ["NaN", "Infinity", "-Infinity"])
def test_non_finite_numeric_metrics_rejected(metric):
    with pytest.raises(ValidationError):
        SystemTaskPayload(task_id="T01", target_identifier="SPECIMEN01", primary_metric=metric)
