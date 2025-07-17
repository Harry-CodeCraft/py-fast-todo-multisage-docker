# -------- Stage 1: Build Dependencies --------
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies only needed during pip install
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies into a local directory
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# -------- Stage 2: Final Slim Image --------
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies from builder stage
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy app code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
