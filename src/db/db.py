from vectordb import InMemoryExactNNVectorDB

from schema import Doc

PORT = '12345'


def run_db():
    db = InMemoryExactNNVectorDB[Doc](workspace='./workspace_path')

    with db.serve(protocol='grpc', port=PORT, replicas=1, shards=1) as service:
        service.block()


if __name__ == '__main__':
    run_db()
