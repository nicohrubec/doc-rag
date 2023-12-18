from pathlib import Path

from pdf_reader import extract_text_from_pdf
from shared.embedder import Embedder
from shared import db


docs_path = Path.cwd().parent.parent / 'docs'
archicad_manual_path = docs_path / 'Archicad.pdf'

embedder = Embedder()

if __name__ == '__main__':
    print("Extracting content from pdf ...")
    pdf_content = extract_text_from_pdf(archicad_manual_path)
    print("Retrieve embeddings for content ...")
    embeddings = embedder.embed(pdf_content)
    print("Index documents ...")
    docs = [{"id": str(i), "values": embeddings[i].tolist(), "metadata": {"text": pdf_content[i]}}
            for i in range(len(pdf_content))]
    db.index_docs(docs)
