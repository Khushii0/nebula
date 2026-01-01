from app.ai.llm.generate import generate_answer
from app.ai.prompts.design_prompt import DESIGN_SYSTEM_PROMPT


def run_design_agent(user_prompt: str, context: str):
    narrative = generate_answer(
        query=user_prompt,
        context=context,
        system_prompt=DESIGN_SYSTEM_PROMPT
    )
    return {
        "narrative": narrative,
        "model_url": "/static/mock_model.glb"  # Placeholder for 3D model
    }
