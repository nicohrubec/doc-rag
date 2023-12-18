from flask import Flask, request
from openai import OpenAI
import json

from shared.embedder import Embedder
from shared.prompt import build_prompt_with_context
from shared import db

app = Flask(__name__)
embedder = Embedder()
db_index = db.get_index()
num_context_prompts_used = 1
openai_client = OpenAI()


@app.route('/', methods=['POST'])
def find_nearest():
    user_request = request.json['request']
    request_embedding = embedder.embed([user_request])

    result = db_index.query(
        namespace="archicad",
        vector=request_embedding.tolist(),
        top_k=num_context_prompts_used,
        include_values=False,
        include_metadata=True,
    )

    contexts = [result.matches[i].metadata['text'] for i in range(num_context_prompts_used)]
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
