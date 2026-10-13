# PCR Multiplex Primer Dimer Agent

A local, sequence-based screening tool for potential primer–primer complementarity in multiplex PCR panels. The repository also retains the earlier generic metric-audit CLI/API for compatibility.

## Browser application

Open `web/index.html` in a modern browser (or serve the repository root and open `/web/`). Enter one `name,sequence` record per line, or upload a CSV file with these columns. Select **Screen primers** to view a symmetric pairwise matrix, flagged primer pairs, and a downloadable pairwise CSV. Self-dimers are included.

The browser calculation uses JavaScript; no Python runtime, backend, login, or network service is required. Primer sequences and CSV uploads remain in the browser. No persistent storage is used.

### How to interpret the result

For each pair, the application enumerates ungapped antiparallel alignments and reports:

- **Longest contiguous match (nt):** largest complementary stretch across all offsets.
- **3′-anchored match (nt):** largest complementary stretch touching the 3′ end of either primer.
- **Heuristic flag:** moderate if 3′ ≥4 nt or longest ≥7 nt; high if 3′ ≥5 nt or longest ≥9 nt.

These thresholds are screening rules **only**. Scores do **not** calculate Gibbs free energy (ΔG), melting temperature, hairpin stability, PCR efficiency, off-target amplification, or assay specificity. They have not been validated as experimental risk probabilities. Assess candidates using established thermodynamic and target-specific analysis tools and laboratory validation before experimental or clinical use.

The screen supports 1–100 uniquely named primers of 4–80 unambiguous A/C/G/T bases each. IUPAC ambiguity codes are rejected rather than silently reinterpreted.

## Python installation

Python 3.10+ is tested in CI.

```bash
python -m pip install -e ".[server,test]"
python -m pytest -q
```

To run the sequence-screening CLI:

```bash
python cli.py screen-primers -i primers.csv -o pairwise.json
```

The input file must have `name,sequence` headers. Omit `-o` to print structured JSON. This command uses the same complementarity rules as the browser implementation.

## Legacy metric audit

The existing metric-audit workflows remain in `cli.py`, `agents/`, and `multiplex_pcr/`. Their numeric thresholds are legacy software rules, **not primer thermodynamics**. Set a private random signing key before invoking the audit:

```bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
python cli.py audit --task-id T01 --primary 28 --secondary 14
python cli.py batch -i sample.csv -o results.csv
python cli.py verify-audit
python cli.py serve --host 127.0.0.1 --port 8000
```

The optional FastAPI service provides `GET /health`, `GET /metrics` (JSON), `POST /api/audit`, `POST /api/chat`, `GET /api/audit/logs`, and generated API documentation at `/docs`. These endpoints serve the **legacy metric audit**, not the new primer screen.

The audit ledger is HMAC-SHA256 chained and held **in process memory only**; it is not a durable or independent audit record. The input identifier filter is regex-based, is not comprehensive PHI detection, and does not establish HIPAA compliance. Do not send protected health information. There is no user authentication: keep the API on a trusted localhost interface rather than exposing it to the public internet.

## Docker

```bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
docker compose up --build
```

Docker Compose binds the legacy API to `127.0.0.1:8000` by default. A signing key is required; the repository does not provide a production default.

## Technology and testing

- Browser: standalone HTML, CSS, and modern JavaScript (File and Blob APIs).
- Python: standard-library sequence screening; Pydantic v2 models and optional FastAPI/Uvicorn server.
- GitHub Actions: Python 3.10–3.12 tests, compilation/package checks, and a dependency-free Node.js browser script smoke test.
- Browser compatibility: current Chromium, Firefox, and Safari with modern JavaScript support.
- License: MIT; see [LICENSE](LICENSE).

No third-party frontend scripts or fonts are loaded by the browser application.
