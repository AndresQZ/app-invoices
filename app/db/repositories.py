from datetime import datetime

from sqlalchemy import func, cast, Date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import Invoice


class InvoiceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, start_date: datetime | None, end_date: datetime | None, offset: int, limit: int):
        query = select(Invoice)
        if start_date:
            query = query.filter(Invoice.invoice_date >= start_date)
        if end_date:
            query = query.filter(Invoice.invoice_date <= end_date)
        total = await self.db.scalar(select(func.count()).select_from(query.subquery()))
        result = await self.db.execute(query.offset(offset).limit(limit))
        return total, result.scalars().all()

    async def get_by_id(self, invoice_id: int):
        result = await self.db.execute(select(Invoice).filter(Invoice.id == invoice_id))
        return result.scalar_one_or_none()

    async def create(self, data: dict):
        invoice = Invoice(**data)
        self.db.add(invoice)
        await self.db.commit()
        await self.db.refresh(invoice)
        return invoice

    async def delete(self, invoice_id: int):
        invoice = await self.get_by_id(invoice_id)
        if invoice:
            await self.db.delete(invoice)
            await self.db.commit()
        return invoice

    async def get_top_days(self, limit: int = 10):
        fecha_expr = cast(Invoice.invoice_date, Date)
        cantidad_col = func.count().label("cantidad_facturas")
        total_col = func.sum(Invoice.total).label("total_diario")
        query = (
            select(fecha_expr.label("fecha"), cantidad_col, total_col)
            .filter(
                Invoice.active == True,
                Invoice.invoice_date.isnot(None),
                Invoice.status.is_distinct_from("Cancelado"),
            )
            .group_by(fecha_expr)
            .order_by(total_col.desc())
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.all()
