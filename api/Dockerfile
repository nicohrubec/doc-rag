FROM python:3.9-buster
WORKDIR /api
ENV PORT=$port
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE $port
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000"]
