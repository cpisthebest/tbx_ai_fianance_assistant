from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    String,
    Integer,
    Numeric,
    DateTime,
    Text,
    ForeignKey,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)

from pgvector.sqlalchemy import Vector


class Base(DeclarativeBase):
    pass


class Bank(Base):

    __tablename__ = "bank"

    bank_code: Mapped[str] = mapped_column(
        String(10),
        primary_key=True,
    )

    bank_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )


class Account(Base):

    __tablename__ = "account"

    account_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    entity_id: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
    )

    account_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    program_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    available_balance: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    bank_code: Mapped[str] = mapped_column(
        ForeignKey("bank.bank_code"),
        nullable=False,
    )


class Transaction(Base):

    __tablename__ = "transaction"

    transaction_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    account_id: Mapped[str] = mapped_column(
        ForeignKey("account.account_id"),
        nullable=False,
    )

    transaction_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    transaction_type: Mapped[str] = mapped_column(
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(500)
    )

    transaction_amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    transaction_reference_id: Mapped[str | None] = mapped_column(
        String(64)
    )

    utr_number: Mapped[str | None] = mapped_column(
        String(256)
    )


class TransactionEmbedding(Base):

    __tablename__ = "transaction_embedding"

    transaction_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(768),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
