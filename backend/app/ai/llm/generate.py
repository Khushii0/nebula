from openai import OpenAI
from app.core.config import settings

def generate_answer(query: str, context: str = "", system_prompt: str = "") -> str:

    if settings.LLM_MODE == "mock":
        return (
            "[MOCK LLM RESPONSE]\n\n"
            f"Question:\n{query}\n\n"
            f"Context:\n{context[:600]}"
        )

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    if context:
        messages.append({"role": "system", "content": f"Context:\n{context}"})

    messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model=settings.AI_MODEL,
        messages=messages,
        temperature=settings.AI_TEMPERATURE,
        max_tokens=settings.AI_MAX_TOKENS,
    )

    return response.choices[0].message.content
