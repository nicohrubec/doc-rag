from flask import Flask, request
from vectordb import Client
from openai import OpenAI
import json

from src.shared.embedder import Embedder
from src.db.schema import Doc
from src.shared.prompt import build_prompt_with_context

app = Flask(__name__)
embedder = Embedder()
db_client = Client[Doc](address=f"grpc://0.0.0.0:12345")
num_context_prompts_used = 3
openai_client = OpenAI()


# TODO: should be a POST request
@app.route('/')
def find_nearest():
    user_request = request.json['request']
    request_embedding = embedder.embed([user_request])
    query = Doc(text=user_request, embedding=request_embedding)
    result = db_client.search(inputs=query, limit=num_context_prompts_used)
    contexts = [result.matches[i].text for i in range(num_context_prompts_used)]

    prompt = build_prompt_with_context(user_request, contexts)

    completion = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant, skilled in explaining complex Archicad problems in simple terms."},
            {"role": "user", "content": prompt}
        ]
    )

    response = json.loads(completion.json())['choices'][0]['message']['content']
    return response


if __name__ == '__main__':
    app.run(debug=False)
