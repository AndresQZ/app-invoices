from datetime import datetime
import logging


from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.database import get_db
from app.db.models import Invoice
from app.api.schemas import InvoiceCreate, InvoiceResponse, PaginatedResponse
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.get("/", response_model=PaginatedResponse[InvoiceResponse])
async def get_invoices(
    startDate: datetime | None = Query(default=None),
    endDate: datetime | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"retrived_invoices: startDate={startDate}, endDate={endDate}, page={page}, page_size={page_size}")
    query = select(Invoice)
    if startDate:
        query = query.filter(Invoice.invoice_date >= startDate)
    if endDate:
        query = query.filter(Invoice.invoice_date <= endDate)

    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    result = await db.execute(query.offset((page - 1) * page_size).limit(page_size))

    return PaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=result.scalars().all()
    )

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