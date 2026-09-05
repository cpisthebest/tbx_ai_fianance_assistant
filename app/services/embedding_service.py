from datetime import datetime

from app.models import (
    Transaction,
    TransactionEmbedding,
)
from app.services.ollama_service import (
    embed,
)


def transaction_to_text(
    transaction: Transaction,
):

    return f"""
Transaction ID: {transaction.transaction_id}

Date: {transaction.transaction_date}

Type: {transaction.transaction_type}

Description: {transaction.description or ""}

Amount: {transaction.transaction_amount}

Reference: {
    transaction.transaction_reference_id or ""
}

UTR: {
    transaction.utr_number or ""
}
""".strip()


async def create_transaction_embedding(
    db,
    transaction: Transaction,
):

    content = transaction_to_text(
        transaction
    )

    vector = await embed(
        content
    )

    existing = await db.get(
        TransactionEmbedding,
        transaction.transaction_id,
    )

    if existing:

        existing.content = content

        existing.embedding = vector

    else:

        row = TransactionEmbedding(

            transaction_id=
                transaction.transaction_id,

            content=content,

            embedding=vector,

            created_at=datetime.utcnow(),
        )

        db.add(row)

    await db.commit()
