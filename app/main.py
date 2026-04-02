from fastapi import FastAPI
from app.routes import verification
from app import models
from app.db import engine

# Create tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ClearCheck",
    description="Verification service API",
    version="0.1.0",
)

app.include_router(verification.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "ClearCheck API running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}