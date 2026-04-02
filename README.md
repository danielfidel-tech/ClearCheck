# ClearCheck
**Verification API Observability and Monitoring Platform**

ClearCheck is an end-to-end observability platform for identity and income verification APIs. It gives fintech operations teams full visibility into the verification lifecycle: from API request ingestion through provider processing, webhook delivery, and fraud signal detection.

The project was built from real operational experience working in fintech, where verification failures, missing webhooks, and latency regressions create immediate and measurable customer impact.

---

## The Problem

Fintech platforms rely on identity and income verification providers to make real-time risk decisions. These integrations are complex and failure-prone because they sit at the boundary between customer-facing workflows, third-party providers, asynchronous webhooks, and compliance requirements.

When things break, they often break silently:

- Verification requests succeed at the HTTP layer but fail downstream
- Webhooks are delayed, dropped, or misconfigured, so results never arrive
- Provider latency degrades gradually, increasing time-to-decision without a clear signal
- Fraud patterns shift in ways that look like noise until they become losses
- Operations teams have no unified view, so they rely on guesswork and ad hoc queries

The cost is real: users cannot access their money, loan applications stall, fraud exposure increases, and engineering time is consumed by manual investigation that should not require engineering at all.

---

## What ClearCheck Does

**Request lifecycle tracking.** Every verification request is logged with a correlation ID that ties it to its events, latency record, and fraud signals. When something goes wrong, the full trace is one query away.

**Provider latency monitoring.** API latency is logged per request and aggregated into average, min, and max metrics by endpoint. Regressions are detected in real time.

**Fraud anomaly detection.** Rule-based fraud signals are emitted as structured events. Monitoring queries compare current window rates against prior window rates and alert when spikes exceed expected variance.

**Failure simulation.** Three demo scenarios simulate real production failures — webhook spikes, latency degradation, and fraud surges — against a live local environment with immediate dashboard feedback.

**Operational dashboards.** Three Metabase dashboards provide platform-level health, webhook reliability metrics, and fraud signal drilldowns.

---

## Architecture
```
Fintech Client
      |
      | POST /api/v1/identity/verify
      v
FastAPI Ingestion Service
      |
      | writes
      v
PostgreSQL
  - verification_requests
  - api_latency_logs
  - fraud_flags
      |
      |---- Metabase -------> Dashboards
```

---

## Stack

| Layer | Technology |
|-------|------------|
| API | FastAPI (Python) |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy |
| Dashboards | Metabase |
| Local deployment | Docker Compose |

---

## Data Model

Three core tables connected by a shared `request_id`:

**verification_requests** — one row per verification submitted. Tracks customer ID, verification type, status, and timestamp. Outcomes are randomly distributed: approved (60%), failed (15%), timeout (15%), fraud_flagged (10%).

**api_latency_logs** — one row per API call. Tracks endpoint, HTTP status, and latency in milliseconds. Latency is distributed realistically: fast 50–150ms (70%), moderate 150–400ms (20%), spike 400–1000ms (10%).

**fraud_flags** — one row per fraud detection event. Tracks request ID, reason (velocity_risk or document_mismatch), and timestamp.

---

## Dashboards

**Platform Health.** Total request volume, status distribution, and average latency trends over time.

**Webhook Reliability.** Success vs failure split, failure rate trend, and latency SLA breach tracking.

**Risk & Fraud Signals.** Fraud flags over time, failure spikes by hour, and anomalies by customer ID.

---

## Demo Scenarios

Three failure scenarios can be simulated live against the running stack:

**Scenario 1 — Webhook Failure Spike.** Sends 20 requests to simulate increased failure volume. Failure rate jumps visibly in the Webhook Reliability dashboard.

**Scenario 2 — Latency Degradation.** Hits a dedicated slow endpoint that simulates 700–1000ms response times. SLA breach count increases in Platform Health.

**Scenario 3 — Fraud Spike.** Sends 15 requests that statistically produce elevated fraud_flagged outcomes. Fraud Flags Over Time and Anomalies by Customer ID update immediately.

---

## Local Setup

**Prerequisites:** Docker Desktop, Python 3.11+
```bash
# Clone the repository
git clone https://github.com/danielfidel-tech/ClearCheck.git
cd ClearCheck

# Start Docker services
docker compose up -d

# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the API
uvicorn app.main:app --reload
```

Once running:

| Service | URL |
|---------|-----|
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Metabase | http://localhost:3000 |
| PostgreSQL | localhost:5433 |

---

## API Endpoints

**POST /api/v1/identity/verify**

Submits a verification request. Returns a unique request ID and outcome status.
```bash
curl -X POST http://localhost:8000/api/v1/identity/verify \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "cust_001", "verification_type": "identity"}'
```

Response:
```json
{
  "request_id": "bd784724-09dd-428d-a0ee-4a3b7f5fbfc6",
  "status": "approved"
}
```

**POST /api/v1/identity/verify/slow**

Simulates a degraded provider response with 700–1000ms latency. Used for latency regression demos.

**GET /health**

Returns API health status.

---

## Project Context

ClearCheck is a portfolio project built from firsthand experience working in fintech operations, where webhook gaps, latency regressions, and fraud signal blind spots are a regular operational reality.

The problem it models is real. Platforms like Sardine, Persona, Alloy, and Unit build and maintain exactly this kind of observability layer for their fintech customers. ClearCheck is a simulation of that infrastructure, built to demonstrate what a well-instrumented verification stack looks like in practice.

---

Built by Daniel Fidel. For questions or collaboration, reach out via [LinkedIn](https://linkedin.com/in/danielfidel).