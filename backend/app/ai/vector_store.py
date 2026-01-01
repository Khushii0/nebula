import faiss
import numpy as np
import os
import pickle

# =========================
# CONFIG
# =========================
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")

INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")
DOCS_PATH = os.path.join(DATA_DIR, "documents.pkl")

DIM = 1536

# =========================
# INIT INDEX
# =========================
index = faiss.IndexFlatL2(DIM)
documents: list[str] = []

# =========================
# SAVE / LOAD
# =========================
def save():
    os.makedirs(DATA_DIR, exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    with open(DOCS_PATH, "wb") as f:
        pickle.dump(documents, f)


def load_index():
    if not os.path.exists(INDEX_PATH):
        raise RuntimeError("FAISS index not found. Run ingestion first.")

    return faiss.read_index(INDEX_PATH)


def load_documents():
    if not os.path.exists(DOCS_PATH):
        raise RuntimeError("Documents file not found. Run ingestion first.")

    with open(DOCS_PATH, "rb") as f:
        return pickle.load(f)

# =========================
# ADD DOCUMENTS
# =========================
def add_documents(texts: list[str], vectors: np.ndarray):
    global documents

    vectors = np.array(vectors).astype("float32")
    assert vectors.ndim == 2, "Vectors must be 2D"
    assert vectors.shape[1] == DIM, "Embedding dimension mismatch"

    index.add(vectors)
    documents.extend(texts)

    save()


# =========================
# SEARCH
# =========================
def search_vectors(query_embedding: list, top_k: int = 3) -> str:
    """
    Search for similar documents using the query embedding.
    Returns a string of concatenated document contexts.
    """
    global index, documents
    
    try:
        # Try to load existing index
        if os.path.exists(INDEX_PATH) and os.path.exists(DOCS_PATH):
            index = load_index()
            documents = load_documents()
    except Exception:
        # If loading fails, return empty context (mock mode)
        pass
    
    # If no documents exist, return empty string
    if len(documents) == 0:
        return ""
    
    # Convert query embedding to numpy array
    query_vector = np.array([query_embedding]).astype("float32")
    
    # Search
    distances, indices = index.search(query_vector, min(top_k, len(documents)))
    
    # Collect results
    results = []
    for idx in indices[0]:
        if idx != -1 and idx < len(documents):
            results.append(documents[idx])
    
    # Return concatenated context
    return "\n\n".join(results) if results else ""