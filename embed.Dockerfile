FROM python:3.11-slim

WORKDIR /app

# We don't want poetry in here, the pre-commit ensures we have a requirements.txt file
# of just the essential requirements (no dev requirements) to install.
COPY requirements-embed-service.txt .

RUN python -m pip install --no-cache-dir -r requirements-embed-service.txt
RUN python -m pip install torch==2.2.2+cpu -f https://download.pytorch.org/whl/torch_stable.html

COPY services/embed_service services/embed_service
COPY pyproject.toml .

RUN python -m pip install .
RUN python -m pip install gunicorn

EXPOSE 8080

WORKDIR /app/services/embed_service/server
CMD ["gunicorn", "--timeout", "300", "--bind", "0.0.0.0:8080", "wsgi:app"]
