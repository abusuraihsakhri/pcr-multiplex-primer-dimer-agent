# PCR Multiplex Primer Dimer Agent

> **Domain:** Clinical Decision Support & Biomedical Computing
> **Standards:** SantaLucia 1998 Thermodynamic Nearest-Neighbor | CAP / CLSI / ISO

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## Overview

**PCR Multiplex Primer Dimer Agent** is an analytical platform implementing pairwise primer cross-dimerization Gibbs free energy (dG kcal/mol) matrix evaluation with multi-agent consensus, cryptographic audit trails, and PHI outbound protection.

The project provides two parallel module systems:

- **`agents/`** — Enterprise Distributed Component Platform with HMAC-SHA256 audit trail, PHI guard, and FastAPI REST API
- **`multiplex_pcr/`** — SantaLucia 1998 Thermodynamic Nearest-Neighbor evaluation engine

---

## Key Features

- **Multi-Agent Consensus**: Specialized workers (InvariantQC, SafetyEscalation, ProtocolConformance) evaluate tasks with aggregated consensus
- **Zero-PHI Outbound Guard**: Active regex inspection blocking SSNs, MRNs, emails, phone numbers, and patient identifiers
- **Tamper-Evident HMAC-SHA256 Audit Trail**: Cryptographic chained logs for every evaluation
- **FastAPI REST API**: OpenAPI 3.1 endpoints with Prometheus metrics
- **CLI Interface**: Single audit, batch CSV processing, chat query, and server modes
- **Prometheus Telemetry**: Operational metrics export (`/metrics`)
- **WebSocket Telemetry**: Real-time streaming of agent reasoning steps

---

## Installation

```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/pcr-multiplex-primer-dimer-agent.git
cd pcr-multiplex-primer-dimer-agent

# Install dependencies
pip install fastapi uvicorn pydantic pytest

# Set required environment variable for audit trail
export AUDIT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
```

---

## CLI Usage

### Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### Batch CSV Processing
```bash
python cli.py batch -i sample.csv -o results.csv
```

### Chat Query
```bash
python cli.py chat "What standard is applied?"
```

### Verify Audit Integrity
```bash
python cli.py verify-audit
```

### Launch REST Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

---

## REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health and metadata check |
| `GET` | `/metrics` | Prometheus operational metrics |
| `POST` | `/api/audit` | Dispatch task across workers |
| `POST` | `/api/chat` | Supervisory conversational query |
| `GET` | `/api/audit/logs` | Retrieve HMAC audit trail |

### Example API Request
```bash
curl -X POST http://localhost:8000/api/audit \
  -H "Content-Type: application/json" \
  -d @sample_payload.json
```

---

## Testing

```bash
# Set audit key for tests
export AUDIT_SECRET_KEY="test-audit-secret-key-32chars-long-secure"

# Run full test suite
pytest -v

# Run with coverage
pytest -v --tb=short
```

### Test Coverage
- PHI guard enforcement (MRN, SSN, email, phone, patient names)
- Worker agent evaluation logic
- Supervisor consensus and audit integration
- CLI command validation
- Audit trail cryptographic integrity
- Secret key requirement enforcement

---

## Security

### Required Environment Variable
The `AUDIT_SECRET_KEY` must be set before using the audit system. Generate a secure key:
```bash
python -c "import secrets; print(secrets.token(hex(32))"
```

### PHI Protection Patterns
The system detects and blocks outbound:
- Medical Record Numbers (MRN)
- Social Security Numbers (XXX-XX-XXXX)
- Phone numbers (US format)
- Email addresses
- Date of birth references
- Patient name patterns

### Audit Trail
- HMAC-SHA256 chained integrity verification
- Each entry links to previous hash (tamper-evident)
- No fallback secret key — must be explicitly configured

---

## Docker Deployment

```bash
# Build and run with Docker Compose
export AUDIT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
docker compose up --build

# Or use Docker directly
docker build -t pcr-multiplex-primer-dimer-agent .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=$AUDIT_SECRET_KEY pcr-multiplex-primer-dimer-agent
```

---

## Project Structure

```
pcr-multiplex-primer-dimer-agent/
├── agents/                  # Enterprise agent platform
│   ├── api.py              # FastAPI REST endpoints
│   ├── base.py             # Security, PHI guard, audit trail
│   ├── models.py           # Pydantic data schemas
│   ├── supervisor.py       # Master coordinator
│   ├── workers.py          # Specialized evaluation workers
│   ├── llm_factory.py      # LLM provider abstraction
│   ├── metrics.py          # Prometheus metrics collector
│   ├── learning.py         # Bayesian calibration engine
│   └── streamer.py         # WebSocket telemetry
├── multiplex_pcr/           # SantaLucia evaluation engine
│   ├── agents.py           # Sub-agent implementations
│   ├── cli.py              # CLI interface
│   ├── engine.py           # Core algorithmic engine
│   ├── models.py           # Data models
│   └── server.py           # FastAPI server factory
├── tests/                   # Test suite
├── web/index.html           # Operations console UI
├── cli.py                   # Main CLI entry point
├── enrichment.py            # Additional enrichment engines
├── simulator.py             # Batch simulation tool
├── sample.csv               # Sample batch input
├── sample_payload.json      # Sample API payload
└── pyproject.toml           # Project configuration
```

---

## License

MIT License - see [LICENSE](LICENSE) for details.
