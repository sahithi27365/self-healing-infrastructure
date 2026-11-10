
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    ansible \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

RUN pip install flask

WORKDIR /app

COPY app.py .

EXPOSE 5001

CMD ["python", "app.py"]
