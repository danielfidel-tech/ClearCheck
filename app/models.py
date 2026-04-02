import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.db import Base, engine


def generate_uuid():
    return str(uuid.uuid4())


class VerificationRequest(Base):
    __tablename__ = "verification_requests"

    request_id = Column(String, primary_key=True, default=generate_uuid)
    customer_id = Column(String, nullable=False)
    verification_type = Column(String, nullable=False)
    status = Column(String, nullable=False, default="processing")
    submitted_at = Column(DateTime, default=lambda: datetime.now())


class ApiLatencyLog(Base):
    __tablename__ = "api_latency_logs"

    api_log_id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(String, nullable=False)
    endpoint = Column(String, nullable=False)
    http_status = Column(Integer, nullable=False)
    latency_ms = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now())


class FraudFlag(Base):
    __tablename__ = "fraud_flags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now())


# Startup-safe table creation
Base.metadata.create_all(bind=engine)