from pathlib import Path
import argparse

from pdf_reader import extract_text_from_pdf
from shared.embedder import Embedder
from shared import db


docs_path = Path.cwd().parent.parent / 'docs'
parser = argparse.ArgumentParser()

embedder = Embedder()

if __name__ == '__main__':
    parser.add_argument('filename')
    parser.add_argument('tool')
    args = parser.parse_args()

    manual_path = docs_path / args.filename

    print("Extracting content from pdf ...")
    pdf_content = extract_text_from_pdf(manual_path)
    print("Retrieve embeddings for content ...")
    embeddings = embedder.embed(pdf_content)
    print("Index documents ...")
    docs = [db.get_document(str(i), embeddings[i].tolist(), pdf_content[i]) for i in range(len(pdf_content))]
    db.index_docs(docs, namespace=args.tool)
