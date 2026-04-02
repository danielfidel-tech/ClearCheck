import uuid
import random
import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import VerificationRequest, ApiLatencyLog, FraudFlag
from app.schemas import VerificationRequestSchema, VerificationResponseSchema

router = APIRouter()


def assign_outcome():
    roll = random.random()
    if roll < 0.60:
        return "approved"
    elif roll < 0.75:
        return "failed"
    elif roll < 0.90:
        return "timeout"
    else:
        return "fraud_flagged"


def simulate_latency():
    roll = random.random()
    if roll < 0.70:
        return random.randint(50, 150)
    elif roll < 0.90:
        return random.randint(150, 400)
    else:
        return random.randint(400, 1000)


@router.post("/identity/verify", response_model=VerificationResponseSchema)
def verify_identity(payload: VerificationRequestSchema, db: Session = Depends(get_db)):
    request_id = str(uuid.uuid4())
    status = assign_outcome()
    latency = simulate_latency()

    verification = VerificationRequest(
        request_id=request_id,
        customer_id=payload.customer_id,
        verification_type=payload.verification_type,
        status=status,
    )
    db.add(verification)

    log = ApiLatencyLog(
        request_id=request_id,
        endpoint="/identity/verify",
        http_status=200,
        latency_ms=latency,
    )
    db.add(log)

    if status == "fraud_flagged":
        fraud_reason = random.choice(["velocity_risk", "document_mismatch"])
        flag = FraudFlag(
            request_id=request_id,
            reason=fraud_reason,
        )
        db.add(flag)

    db.commit()
    db.refresh(verification)

    return VerificationResponseSchema(
        request_id=str(verification.request_id),
        status=str(verification.status),
    )


@router.post("/identity/verify/slow")
def verify_identity_slow(payload: VerificationRequestSchema, db: Session = Depends(get_db)):
    request_id = str(uuid.uuid4())
    latency = random.randint(700, 1000)
    time.sleep(latency / 1000)

    verification = VerificationRequest(
        request_id=request_id,
        customer_id=payload.customer_id,
        verification_type=payload.verification_type,
        status="timeout",
    )
    db.add(verification)

    log = ApiLatencyLog(
        request_id=request_id,
        endpoint="/identity/verify/slow",
        http_status=200,
        latency_ms=latency,
    )
    db.add(log)
    db.commit()

    return {"request_id": request_id, "status": "timeout"}