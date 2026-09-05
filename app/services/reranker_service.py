from flashrank import (
    Ranker,
    RerankRequest,
)

ranker = Ranker()


def rerank(
    question: str,
    candidates: list,
    top_k: int = 10,
):

    if not candidates:

        return []

    passages = []

    for candidate in candidates:

        passages.append({

            "id":
                candidate[
                    "transaction_id"
                ],

            "text":
                candidate[
                    "content"
                ],
        })

    request = RerankRequest(

        query=question,

        passages=passages,
    )

    results = ranker.rerank(
        request
    )

    return results[:top_k]
