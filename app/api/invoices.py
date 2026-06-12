from datetime import datetime
import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.repositories import InvoiceRepository
from app.schemas import InvoiceCreate, InvoiceResponse, PaginatedResponse, TopDayResponse
from app.worker.tasks import Worker

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/invoices", tags=["Invoices"])


def get_repo(db: AsyncSession = Depends(get_db)) -> InvoiceRepository:
    return InvoiceRepository(db)


@router.get("/top-days", response_model=list[TopDayResponse])
async def get_top_days(
    limit: int = Query(default=10, ge=1, le=100),
    repo: InvoiceRepository = Depends(get_repo),
):  
    return await Worker.reporting(repo)



@router.get("/", response_model=PaginatedResponse[InvoiceResponse])
async def get_invoices(
    startDate: datetime | None = Query(default=None),
    endDate: datetime | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    repo: InvoiceRepository = Depends(get_repo),
):
    logger.info(f"retrived_invoices: startDate={startDate}, endDate={endDate}, page={page}, page_size={page_size}")
    total, items = await repo.get_all(startDate, endDate, offset=(page - 1) * page_size, limit=page_size)
    return PaginatedResponse(total=total, page=page, page_size=page_size, items=items)


@router.post("/", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice(invoice_data: InvoiceCreate, repo: InvoiceRepository = Depends(get_repo)):
    logger.info(f"create_invoices: payload:{invoice_data}")
    return await repo.create(invoice_data.model_dump())


@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(invoice_id: int, repo: InvoiceRepository = Depends(get_repo)):
    logger.info(f"get_invoice: id:{invoice_id}")
    invoice = await repo.get_by_id(invoice_id)
    if not invoice:
        logger.warning(f"invoice not found: id:{invoice_id}")
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.delete("/{invoice_id}", response_model=InvoiceResponse)
async def delete_invoice(invoice_id: int, repo: InvoiceRepository = Depends(get_repo)):
    logger.info(f"delete_invoice: id:{invoice_id}")
    invoice = await repo.delete(invoice_id)
    if not invoice:
        logger.warning(f"invoice not found: id:{invoice_id}")
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice
