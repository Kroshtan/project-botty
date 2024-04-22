FROM python:3.11-slim

WORKDIR /app

# We don't want poetry in here, the pre-commit ensures we have a requirements.txt file
# of just the essential requirements (no dev requirements) to install.
COPY requirements-bot.txt .

RUN apt-get update && apt install -y protobuf-compiler build-essential

RUN python -m pip install --no-cache-dir -r requirements-bot.txt

COPY services/discord_bot services/discord_bot
COPY pyproject.toml .

RUN python -m pip install .

WORKDIR /app/services/discord_bot
CMD ["python", "main.py"]
