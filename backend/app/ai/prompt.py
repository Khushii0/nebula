SYSTEM_PROMPT = """
You are an Architectural Design Assistant.
Use ONLY the provided context.
If the answer is not in the context, say "I don’t know".
"""

def build_prompt(context_chunks: list[str], question: str) -> str:
    context = "\n\n".join(context_chunks)

    return f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}

Answer:
"""
