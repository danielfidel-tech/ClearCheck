from pydantic import BaseModel


class VerificationRequestSchema(BaseModel):
    customer_id: str
    verification_type: str


class VerificationResponseSchema(BaseModel):
    request_id: str
    status: str

    class Config:
        from_attributes = True
