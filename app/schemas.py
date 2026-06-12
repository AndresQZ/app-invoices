from pydantic import BaseModel
from datetime import datetime
from typing import Generic, List, TypeVar

T = TypeVar("T")

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


class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    page: int
    page_size: int
    items: List[T]

class TopDayResponse(BaseModel):
    fecha: str
    cantidad_facturas: int
    total_diario: float
