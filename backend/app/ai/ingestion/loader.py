from pathlib import Path
from pypdf import PdfReader


def load_documents(path: str):
    docs = []
    folder = Path(path)

    for file in folder.glob("*"):
        if file.suffix == ".pdf":
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            docs.append(text)

        elif file.suffix == ".txt":
            docs.append(file.read_text(encoding="utf-8"))

    return docs
