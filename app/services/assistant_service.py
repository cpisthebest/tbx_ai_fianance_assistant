from app.services.intent_service import (
    classify_intent,
)

from app.services.sql_service import (
    generate_sql,
    execute_sql,
)

from app.services.ollama_service import (
    embed,
    chat,
)

from app.services.vector_service import (
    vector_search,
)

from app.services.reranker_service import (
    rerank,
)


async def ask_assistant(
    db,
    question: str,
):

    # =================================================
    # STEP 1
    # INTENT CLASSIFICATION
    # =================================================

    intent_result = await classify_intent(
        question
    )

    intent = intent_result.get(
        "intent",
        "GENERAL",
    )

    search_query = (
        intent_result.get(
            "search_query"
        )
        or question
    )

    print(
        "Intent:",
        intent,
    )

    # =================================================
    # STEP 2
    # VECTOR SEARCH
    # =================================================

    semantic_results = []

    if intent == (
        "SEMANTIC_TRANSACTION_SEARCH"
    ):

        query_embedding = await embed(
            search_query
        )

        candidates = await vector_search(

            db,

            query_embedding,

            limit=4,
        )
        print("candidates ->",candidates)
        semantic_results = rerank(

            search_query,

            candidates,

            top_k=2,
        )

    # =================================================
    # STEP 3
    # SQL SEARCH
    # =================================================

    sql_results = []

    sql = None

    sql_intents = [
        "BALANCE",
        "TRANSACTION_SUMMARY",
        "EXACT_TRANSACTION",
        "BANK_INFO",
        "ACCOUNT_INFO",
    ]

    if intent in sql_intents:

        sql = await generate_sql(

            question,

            intent,
        )

        sql_results = await execute_sql(

            db,

            sql,
        )

    # =================================================
    # STEP 4
    # GENERAL
    # =================================================

    if intent == "GENERAL":

        sql_results = []

    # =================================================
    # STEP 5
    # BUILD CONTEXT
    # =================================================

    context = {

        "intent":
            intent,

        "sql_results":
            sql_results,

        "semantic_results":
            semantic_results,
    }

    # =================================================
    # STEP 6
    # FINAL OLLAMA RESPONSE
    # =================================================

    system = """
You are a financial AI assistant.

Answer the user's question using ONLY
the supplied database context.

Rules:

1. Never invent financial information.

2. Never invent transactions.

3. Never expose full account numbers.

4. Use the database results as the source
   of truth.

5. If no matching data exists, say so.

6. Format money with two decimal places.

7. Keep the response concise.

8. Do not mention internal SQL,
   embeddings, pgvector or FlashRank
   unless the user specifically asks.
"""

    answer = await chat(

        system=system,

        user=f"""
User question:

{question}

Detected intent:

{intent}

Database context:

{context}

Give the final answer.
""",

        temperature=0.1,
    )

    return {

        "intent":
            intent,

        "answer":
            answer,

        "sql":
            sql,

        "sql_results":
            sql_results,

        "semantic_results":
            semantic_results,
    }
