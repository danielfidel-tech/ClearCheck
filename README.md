# ClearCheck

A FastAPI-based identity verification service backed by PostgreSQL.

---

## Requirements

- Python 3.11+
- Docker Desktop

---

## Setup & Run

### 1. Start Docker
Open Docker Desktop, then start the containers:
```bash
docker compose up -d
```

### 2. Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the API
```bash
uvicorn app.main:app --reload
```

### 4. Test the Endpoint
```bash
curl -X POST http://localhost:8000/api/v1/identity/verify \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "cust_001", "verification_type": "identity"}'
```

Expected response:
```json
{
  "request_id": "some-uuid",
  "status": "processing"
}
```

---

## Services

| Service   | URL                          |
|-----------|------------------------------|
| API       | http://localhost:8000        |
| API Docs  | http://localhost:8000/docs   |
| Metabase  | http://localhost:3000        |
| PostgreSQL| localhost:5433               |
