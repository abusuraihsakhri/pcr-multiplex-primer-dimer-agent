"""
Test configuration for pcr-multiplex-primer-dimer-agent.
Sets required environment variables for secure test execution.
"""
import os

# Ensure tests have a valid audit secret key for cryptographic operations
os.environ.setdefault("AUDIT_SECRET_KEY", "test-audit-secret-key-32chars-long-secure")
