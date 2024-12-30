
FROM python:3.9-slim-buster


WORKDIR  app
COPY . /app
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8800

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8800"]

