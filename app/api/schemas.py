from pydantic import BaseModel
from datetime import datetime

class InvoiceBase(BaseModel):
    invoice_number: str
    total: float
    invoice_date: datetime
    status: str = "pending"
    active: bool = True

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceResponse(InvoiceBase):
    id: int

    model_config = {"from_attributes": True}