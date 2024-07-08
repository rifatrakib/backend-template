FROM python:3.12-slim-bullseye

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./server /app/server

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
