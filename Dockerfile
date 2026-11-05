FROM python:3.11-slim

# Copy the uv binary from the official Astral image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory inside the container
WORKDIR /app

# Enable bytecode compilation and copy dependency manifests first
ENV UV_COMPILE_BYTECODE=1
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev --no-install-project
ENV PATH="/app/.venv/bin:$PATH"

# Copy the rest of your application code from the root directory
COPY . .

# Run your script
CMD ["python", "main.py"]
