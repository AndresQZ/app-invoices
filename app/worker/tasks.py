import asyncio

from app.db.database import AsyncSessionLocal
from app.db.repositories import InvoiceRepository
from app.worker.celery_app import celery_app
from app.worker.worker import Worker


@celery_app.task(name="app.worker.tasks.reporting")
def reporting():
    async def run():
        async with AsyncSessionLocal() as session:
            repo = InvoiceRepository(session)
            return await Worker.reporting(repo)
    asyncio.run(run())