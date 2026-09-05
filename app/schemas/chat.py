from pydantic import BaseModel


class ChatRequest(BaseModel):

    question: str


class ChatResponse(BaseModel):

    question: str

    intent: str

    answer: str

    sql_results: list

    semantic_results: list
