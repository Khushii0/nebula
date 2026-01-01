from app.ai.retriever import retrieve_context
from app.ai.llm.generate import generate_answer

SYSTEM_PROMPT = (
    "You are an architectural design assistant. "
    "Answer strictly using the provided context. "
    "If the answer is not in the context, say you don't know."
)

def answer_question(question: str) -> str:
    context = retrieve_context(question)

    return generate_answer(
        query=question,
        context=context,
        system_prompt=SYSTEM_PROMPT
    )
