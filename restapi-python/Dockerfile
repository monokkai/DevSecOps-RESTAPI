FROM python:3.11-slim

WORKDIR /api

COPY . /api

RUN pip install --no-cache-dir "fastapi[standard]"

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
