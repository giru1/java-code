from uuid import uuid4, UUID
from sqlalchemy import String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from database import Base
from datetime import datetime


class Wallet(Base):
    __tablename__ = "wallet"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column()
    balance: Mapped[float] = mapped_column(nullable=False, default=0.00)

    operations: Mapped[list["Operation"]] = relationship(
        "Operation",
        back_populates="wallet",
        cascade="all, delete-orphan"
    )


class Operation(Base):
    __tablename__ = "operation"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    wallet_id: Mapped[UUID] = mapped_column(ForeignKey('wallet.id'), nullable=False)
    operation_type: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    wallet: Mapped["Wallet"] = relationship(
        "Wallet",  # Добавлено имя связанной модели
        back_populates="operations"
    )



