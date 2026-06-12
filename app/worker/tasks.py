import logging

from app.db.repositories import InvoiceRepository
from app.schemas import TopDayResponse
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)


class Worker:

    @staticmethod
    async def reporting(repo: InvoiceRepository):
        email_service = EmailService()
        rows = await repo.get_top_days(10)
        logger.info(f"top 10 days: {rows}")
        top = [TopDayResponse(fecha=str(r.fecha), cantidad_facturas=r.cantidad_facturas, total_diario=r.total_diario) for r in rows]
        label = "<strong>Resumen de días con mayor ventas</strong><br>"
        body = label + "<br>".join(f"fecha: {r.fecha}: No. facturas: {r.cantidad_facturas}, Monto: ${r.total_diario}" for r in top)
        await email_service.send("Dias con mayor venta", body)
        return top