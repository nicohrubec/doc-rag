from flask import Flask, request
from openai import OpenAI
import json

from shared.embedder import Embedder
from shared.prompt import build_prompt_with_context, build_system_prompt_for_tool
from shared import db

app = Flask(__name__)
embedder = Embedder()
db_index = db.get_index()
num_context_prompts_used = 3
openai_client = OpenAI()


def validate_user_request(user_request):
    if 'request' not in user_request.get_json():
        return 'Request is missing', 400
    if 'tool' not in user_request.get_json():
        return 'Tool is missing', 400

    return None, None


@app.route('/', methods=['POST'])
def find_nearest():
    error_string, error_code = validate_user_request(request)

    if error_code:
        return error_string, error_code

    user_request = request.json['request']
    user_request_tool = request.json['tool']
    request_embedding = embedder.embed([user_request])

    result = db_index.query(
        namespace=user_request_tool,
        vector=request_embedding.tolist(),
        top_k=num_context_prompts_used,
        include_values=False,
        include_metadata=True,
    )

    contexts = [result.matches[i].metadata['text'] for i in range(num_context_prompts_used)]
    prompt = build_prompt_with_context(user_request, contexts)
    system_prompt = build_system_prompt_for_tool(user_request_tool)

    completion = openai_client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    response = json.loads(completion.json())['choices'][0]['message']['content']
    return response


if __name__ == '__main__':
    app.run(debug=True)
