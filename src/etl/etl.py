from pathlib import Path
from vectordb import Client
from docarray import DocList

from pdf_reader import extract_text_from_pdf
from src.shared.embedder import Embedder
from src.db.schema import Doc


docs_path = Path.cwd().parent.parent / 'docs'
archicad_manual_path = docs_path / 'Archicad.pdf'

embedder = Embedder()
client = Client[Doc](address=f"grpc://0.0.0.0:12345")

if __name__ == '__main__':
    print("Extracting content from pdf ...")
    pdf_content = extract_text_from_pdf(archicad_manual_path)
    print("Retrieve embeddings for content ...")
    embeddings = embedder.embed(pdf_content)
    print("Index documents ...")
    docs = [Doc(text=pdf_content[i], embedding=embeddings[i]) for i in range(len(pdf_content))]
    client.index(inputs=DocList[Doc](docs))
