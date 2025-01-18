FROM python:3.8.9-slim

WORKDIR /api/
COPY Pipfile /api/Pipfile
COPY Pipfile.lock /api/Pipfile.lock
COPY ./api/ /api/

CMD ["uvicorn", "--port", "8001", "--host", "0.0.0.0","--log-level", "error", "app:APP"]
