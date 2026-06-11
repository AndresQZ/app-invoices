from datetime import datetime
from sqlalchemy import String, Numeric, BigInteger, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    invoice_number: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    total: Mapped[float] = mapped_column(Numeric, nullable=False)
    invoice_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String, default="pending", nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)