from datetime import datetime
import logging


from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.database import get_db
from app.db.models import Invoice
from app.api.schemas import InvoiceCreate, InvoiceResponse
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.get("/", response_model=List[InvoiceResponse])
async def get_invoices(
    startDate: datetime | None = Query(default=None),
    endDate: datetime | None = Query(default=None),
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"retrived_invoices: startDate={startDate}, endDate={endDate}")
    query = select(Invoice)
    if startDate:
        query = query.filter(Invoice.invoice_date >= startDate)
    if endDate:
        query = query.filter(Invoice.invoice_date <= endDate)

    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice(invoice_data: InvoiceCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"create_invoices: payload:{invoice_data}")
    new_invoice = Invoice(**invoice_data.model_dump())
    db.add(new_invoice)
    await db.commit()
    await db.refresh(new_invoice)
    return new_invoice



@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(invoice_id: int, db: AsyncSession = Depends(get_db)):
    logger.info(f"get_invoice: id:{invoice_id}")
    result = await db.execute(select(Invoice).filter(Invoice.id == invoice_id))
    invoice = result.scalar_one_or_none()
    if not invoice:
        logger.warning(f"invoice not found: id:{invoice_id}")
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice



@router.delete("/{invoice_id}", response_model=InvoiceResponse)
async def delete_invoice(invoice_id: int, db: AsyncSession = Depends(get_db)):
        logger.info(f"delete_invoice: id:{invoice_id}")
        result = await db.execute(select(Invoice).filter(Invoice.id == invoice_id))
        invoice = result.scalar_one_or_none()
        if(invoice):
            await db.delete(invoice)
        if not invoice:
            logger.warning(f"invoice not found: id:{invoice_id}")
            raise HTTPException(status_code=404, detail="Invoice not found")
        return invoice