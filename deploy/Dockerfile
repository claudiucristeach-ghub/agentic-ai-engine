FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml ./
COPY app ./app

RUN pip install --upgrade pip && pip install .

EXPOSE 8080

CMD ["uvicorn", "app.api.fastapi_app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8080"]