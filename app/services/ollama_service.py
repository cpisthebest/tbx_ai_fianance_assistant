from ollama import AsyncClient

from app.config import settings


client = AsyncClient(
    host=settings.OLLAMA_URL
)


async def chat(
    system: str,
    user: str,
    temperature: float = 0,
):

    response = await client.chat(

        model=settings.OLLAMA_MODEL,

        messages=[
            {
                "role": "system",
                "content": system,
            },
            {
                "role": "user",
                "content": user,
            },
        ],

        options={
            "temperature": temperature
        },
    )

    return response[
        "message"
    ][
        "content"
    ]


async def embed(
    content: str,
):

    response = await client.embed(

        model=settings.OLLAMA_EMBED_MODEL,

        input=content,
    )

    return response[
        "embeddings"
    ][0]
