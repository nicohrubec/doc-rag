from flask import Flask, request, render_template
import requests

app = Flask(__name__)

BACKEND_SERVER_URL = "http://127.0.0.1:5000"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']

        backend_payload = {'request': user_input}
        backend_response = requests.post(BACKEND_SERVER_URL, json=backend_payload)

        print(backend_response.text)

        if backend_response.status_code == 200:
            answer = backend_response.text
            print(answer)
            return render_template("index.html", answer=answer)
        else:
            return 'Error communicating with the backend server', 500

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, port=9000)
