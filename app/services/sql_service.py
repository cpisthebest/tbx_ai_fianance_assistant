from sqlalchemy import text

from app.services.ollama_service import chat


SCHEMA = """
TABLE bank:

bank_code VARCHAR(10)
bank_name VARCHAR(150)


TABLE account:

account_id VARCHAR(36)
entity_id VARCHAR(36)
account_number VARCHAR(20)
program_id INT
available_balance DECIMAL(15,2)
bank_code VARCHAR(10)


TABLE transactions:

transaction_id VARCHAR(36)
account_id VARCHAR(36)
transaction_date TIMESTAMP
transaction_type ENUM('credit', 'debit')
description VARCHAR(500)
transaction_amount DECIMAL(15,2)
transaction_reference_id VARCHAR(64)
utr_number VARCHAR(256)


RELATIONSHIPS:

bank.bank_code = account.bank_code

account.account_id = transactions.account_id
"""


FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE",
]


async def generate_sql(
    question: str,
    intent: str,
):

    system = f"""
You are a PostgreSQL financial query generator.

Database schema:

{SCHEMA}

Intent:

{intent}

Generate ONE SELECT statement.

Rules:

- Only SELECT.
- Never modify data.
- Never INSERT.
- Never UPDATE.
- Never DELETE.
- Never DROP.
- Never ALTER.
- Never CREATE.
- Never TRUNCATE.
- Never return full account_number.
- Never use multiple SQL statements.
- Return only SQL.
- No markdown.
"""

    sql = await chat(

        system=system,

        user=question,

        temperature=0,
    )

    sql = sql.strip()

    sql = sql.replace(
        "```sql",
        "",
    )

    sql = sql.replace(
        "```",
        "",
    )

    return sql.strip()


def validate_sql(
    sql: str,
):

    sql = sql.strip()

    if not sql.upper().startswith(
        "SELECT"
    ):

        raise ValueError(
            "Only SELECT queries are allowed"
        )

    upper_sql = sql.upper()

    for keyword in FORBIDDEN_KEYWORDS:

        if keyword in upper_sql:

            raise ValueError(
                f"Forbidden SQL keyword: {keyword}"
            )

    if ";" in sql.rstrip(";"):

        raise ValueError(
            "Multiple SQL statements are not allowed"
        )

    return sql.rstrip(";")


async def execute_sql(
    db,
    sql: str,
):

    sql = validate_sql(
        sql
    )

    result = await db.execute(
        text(sql)
    )

    rows = result.mappings().all()

    return [
        dict(row)
        for row in rows
    ]
