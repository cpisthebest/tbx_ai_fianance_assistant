from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.database import get_db
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.services.assistant_service import (
    ask_assistant,
)

app = FastAPI(

    title="Finance AI Assistant",

    description=(
        "FastAPI + PostgreSQL + pgvector "
        "+ Ollama + FlashRank"
    ),

    version="1.0.0",
)


@app.get("/health")
async def health():

    return {
        "status": "ok"
    }


@app.post(
    "/api/chat",
    response_model=ChatResponse,
)
async def chat(

    request: ChatRequest,

    db: AsyncSession = Depends(
        get_db
    ),
):

    try:

        result = await ask_assistant(

            db,

            request.question,
        )

        return ChatResponse(

            question=request.question,

            intent=result[
                "intent"
            ],

            answer=result[
                "answer"
            ],

            sql_results=result[
                "sql_results"
            ],

            semantic_results=result[
                "semantic_results"
            ],
        )

    except ValueError as e:

        raise HTTPException(

            status_code=400,

            detail=str(e),
        )

    except Exception as e:

        print(
            "ERROR:",
            str(e),
        )

        raise HTTPException(

            status_code=500,

            detail=(
                "Unable to process "
                "the finance query"
            ),
        )
