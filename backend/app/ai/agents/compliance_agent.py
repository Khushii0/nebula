from app.ai.llm.generate import generate_answer
from app.ai.prompts.compliance_prompt import COMPLIANCE_SYSTEM_PROMPT


def run_compliance_agent(design_text: str):
    notes = generate_answer(
        query=design_text,
        context="",
        system_prompt=COMPLIANCE_SYSTEM_PROMPT
    )
    return {
        "notes": notes,
        "status": "compliant"  # Could be "compliant", "non-compliant", "needs_review"
    }
