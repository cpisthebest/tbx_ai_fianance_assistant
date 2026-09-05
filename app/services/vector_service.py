from sqlalchemy import select

from app.models import (
    TransactionEmbedding,
)


async def vector_search(
    db,
    query_embedding,
    limit: int = 30,
):

    distance = (
        TransactionEmbedding.embedding
        .cosine_distance(
            query_embedding
        )
    )

    query = (

        select(

            TransactionEmbedding.transaction_id,

            TransactionEmbedding.content,

            distance.label(
                "distance"
            ),
        )

        .order_by(distance)

        .limit(limit)
    )

    result = await db.execute(
        query
    )

    return result.mappings().all()
