from flask import Flask, request
from vectordb import Client

from src.shared.embedder import Embedder
from src.db.schema import Doc

app = Flask(__name__)
embedder = Embedder()
client = Client[Doc](address=f"grpc://0.0.0.0:12345")


# build a separate service that does the llm inference on my mac
# it exposes an endpoint POST / that takes a prompt and returns the response
# this main app will take the user input, retrieve the context, build up a prompt (the prompt builder should be in src)
# and then send an http request to the llm service and return the response back to the user


@app.route('/')
def find_nearest():
    user_request = request.json['request']
    request_embedding = embedder.embed([user_request])
    query = Doc(text='request', embedding=request_embedding)
    result = client.search(inputs=query, limit=3)

    for idx, m in enumerate(result.matches):
        print(f"result {idx}")
        print(m.text)

    return result.matches[0].text


if __name__ == '__main__':
    app.run(debug=False)
