import asyncio

from sqlalchemy import select

from app.database import SessionLocal
from app.models import Transaction
from app.services.embedding_service import (
    create_transaction_embedding,
)


async def index_transactions():

    async with SessionLocal() as db:

        result = await db.execute(
            select(Transaction)
        )

        transactions = result.scalars().all()

        print(
            f"Transactions found: {len(transactions)}"
        )

        for transaction in transactions:

            print(
                "Embedding:",
                transaction.transaction_id,
            )

            await create_transaction_embedding(

                db,

                transaction,
            )


if __name__ == "__main__":

    asyncio.run(
        index_transactions()
    )
