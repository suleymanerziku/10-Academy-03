FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
COPY . .

RUN pip install --upgrade pip \
    && pip install pytest

CMD ["pytest"]
