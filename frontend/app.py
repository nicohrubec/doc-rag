from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

# check if we are running from docker
if 'DOCKER_NETWORK' in os.environ and os.environ['DOCKER_NETWORK'] == 'true':
    BACKEND_SERVER_URL = "http://backend-service:8000"
else:
    BACKEND_SERVER_URL = "http://127.0.0.1:8000"


@app.route('/<tool>', methods=['GET', 'POST'])
def chatbot(tool):
    if tool not in ['archicad', 'rfem']:
        return render_template("404.html")

    if request.method == 'POST':
        user_input = request.form['user_input']

        backend_payload = {'request': user_input, 'tool': tool}
        backend_response = requests.post(BACKEND_SERVER_URL, json=backend_payload)

        if backend_response.status_code == 200:
            answer = backend_response.text
            return render_template("chatbot.html", answer=answer, tool=tool)
        else:
            return 'Error communicating with the backend server', 500

    return render_template("chatbot.html", tool=tool)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=False, port=9000)
