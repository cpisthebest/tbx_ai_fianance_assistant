import json

from app.services.ollama_service import chat


INTENTS = """
BALANCE

Use for:
- current balance
- total balance
- account balance
- how much money do I have
- available balance


TRANSACTION_SUMMARY

Use for:
- total spending
- total debit
- total credit
- spending this month
- spending last month
- number of transactions
- highest transaction
- average transaction
- transaction statistics


EXACT_TRANSACTION

Use for:
- transaction ID
- UTR number
- transaction reference
- exact transaction lookup
- find transaction TXN-001
- find UTR123456


SEMANTIC_TRANSACTION_SEARCH

Use for:
- food expenses
- travel expenses
- shopping
- entertainment
- hotel payments
- restaurant payments
- transactions related to Amazon
- transactions related to a concept/category
- natural language transaction search


BANK_INFO

Use for:
- list banks
- which banks do I have
- bank names
- accounts by bank


ACCOUNT_INFO

Use for:
- list accounts
- account information
- how many accounts
- account details


GENERAL

Use when the question does not fit the above.
"""


async def classify_intent(
    question: str,
):

    system = f"""
You are an intent classifier for a financial AI assistant.

Available intents:

{INTENTS}

Return ONLY valid JSON.

Format:

{{
    "intent": "BALANCE",
    "search_query": null
}}

For semantic transaction searches:

{{
    "intent": "SEMANTIC_TRANSACTION_SEARCH",
    "search_query": "food related transactions"
}}

Do not include markdown.
Do not include explanations.
"""

    result = await chat(

        system=system,

        user=question,

        temperature=0,
    )

    result = result.strip()

    result = result.replace(
        "```json",
        "",
    )

    result = result.replace(
        "```",
        "",
    )

    result = result.strip()

    try:

        parsed = json.loads(result)

    except json.JSONDecodeError:

        return {
            "intent": "GENERAL",
            "search_query": None,
        }

    return parsed
