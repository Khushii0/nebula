import hashlib
import numpy as np
import httpx
from app.core.config import settings

DIM = 1536


def mock_embedding(text: str):
    """
    Deterministic mock embedding for development.
    """
    h = hashlib.sha256(text.encode()).digest()
    np.random.seed(int.from_bytes(h[:4], "little"))
    return np.random.rand(DIM).tolist()


def embed_text(text: str):
    # 🔥 THIS is the fix
    if settings.EMBEDDING_MODE.lower() == "mock":
        return mock_embedding(text)

    url = "https://api.openai.com/v1/embeddings"

    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "text-embedding-3-small",
        "input": text,
    }

    response = httpx.post(url, headers=headers, json=payload, timeout=30)

    if response.status_code == 429:
        # graceful fallback
        return mock_embedding(text)

    response.raise_for_status()
    return response.json()["data"][0]["embedding"]
