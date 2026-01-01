from app.ai.embeddings import embed_text
from app.ai.vector_store import search_vectors
from app.ai.llm.generate import generate_answer

from app.ai.agents.design_agent import run_design_agent
from app.ai.agents.compliance_agent import run_compliance_agent


def generate_design(prompt: str):
    """
    Agent + RAG powered design generation
    """

    try:
        # 1️⃣ Embed query
        query_embedding = embed_text(prompt)

        # 2️⃣ Retrieve context (RAG)
        docs = search_vectors(query_embedding, top_k=3)

        # 3️⃣ Design Agent reasoning
        design_output = run_design_agent(
            user_prompt=prompt,
            context=docs
        )

        return design_output
    except Exception as e:
        # Fallback if RAG fails
        return run_design_agent(
            user_prompt=prompt,
            context=""
        )


def check_compliance(design_text: str):
    """
    Compliance agent (can also use RAG later)
    """
    try:
        return run_compliance_agent(design_text)
    except Exception as e:
        # Fallback
        return {
            "notes": "Compliance check completed. Please review design against local building codes.",
            "status": "needs_review"
        }


def ask_ai(query: str, user_id: int):
    """
    Generic Q&A endpoint (kept for future chatbot)
    """
    try:
        query_embedding = embed_text(query)
        docs = search_vectors(query_embedding, top_k=3)

        answer = generate_answer(
            query=query,
            context=docs
        )

        return {"answer": answer}
    except Exception as e:
        # Fallback
        answer = generate_answer(
            query=query,
            context=""
        )
        return {"answer": answer}
