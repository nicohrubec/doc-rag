import pinecone
import os
from tqdm import tqdm

max_docs_indexed_at_once = 1000


def get_index():
    pinecone.init(api_key=os.environ['PINECONE_API_KEY'], environment=os.environ['PINECONE_ENV'])
    return pinecone.Index("doc-rag")


def index_docs(docs, namespace):
    index = get_index()

    for i in tqdm(range(len(docs) // max_docs_indexed_at_once + 1)):
        index.upsert(vectors=docs[i*max_docs_indexed_at_once:(i+1)*max_docs_indexed_at_once], namespace=namespace)
