FROM python:3.12-slim

ENV PORT=8000
ENV HOST=0.0.0.0

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

EXPOSE ${PORT}

# Run the application.
CMD ["sh", "-c", "/app/.venv/bin/fastapi run ./src/main.py --port ${PORT} --host ${HOST}"]