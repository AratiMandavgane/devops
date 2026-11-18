from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import uuid4

app = FastAPI(
    title="Payment Service",
    description="Sample payment service for the Internal Developer Platform",
    version="1.0.0"
)

payments = {}


class PaymentRequest(BaseModel):
    customer_id: str
    amount: float = Field(gt=0)
    currency: str = "INR"


@app.get("/")
def root():
    return {
        "service": "payment-service",
        "message": "Payment Service is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/payments")
def create_payment(payment: PaymentRequest):

    payment_id = str(uuid4())

    payment_record = {
        "payment_id": payment_id,
        "customer_id": payment.customer_id,
        "amount": payment.amount,
        "currency": payment.currency,
        "status": "SUCCESS"
    }

    payments[payment_id] = payment_record

    return payment_record


@app.get("/payments/{payment_id}")
def get_payment(payment_id: str):

    if payment_id not in payments:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payments[payment_id]
