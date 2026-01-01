import os
from app.ai.embeddings import embed_text
from app.ai.vector_store import add_documents

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "..", "data")


def ingest_documents():
    texts = []
    vectors = []

    for filename in os.listdir(DATA_DIR):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(DATA_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if content:
            texts.append(content)
            vectors.append(embed_text(content))

    add_documents(texts, vectors)
    print(f"Ingested {len(texts)} documents",len(vectors[0]))



if __name__ == "__main__":
    ingest_documents()
