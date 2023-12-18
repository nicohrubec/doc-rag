import pinecone
import os


def get_index():
    pinecone.init(api_key=os.environ['PINECONE_API_KEY'], environment=os.environ['PINECONE_ENV'])
    return pinecone.Index("archicad")
