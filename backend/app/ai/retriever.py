import faiss
import numpy as np
from app.ai.embeddings import embed_text
from app.ai.vector_store import INDEX_PATH, load_index, load_documents

TOP_K = 3

def retrieve_context(query: str) -> list[str]:
    index = load_index()
    docs = load_documents()

    query_vector = np.array([embed_text(query)]).astype("float32")

    distances, indices = index.search(query_vector, TOP_K)

    results = []
    for idx in indices[0]:
        if idx != -1:
            results.append(docs[idx])

    return results
