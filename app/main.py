from fastapi import  FastAPI
from app.api.invoices import router as invoice_router
from app.api.health import router as health_router

app = FastAPI(
    title="invoices API",
    description="A FastAPI backend with PostgreSQL",
    version="1.0.0"
)

app.include_router(health_router)
app.include_router(invoice_router)
