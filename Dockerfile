FROM python:3.13-slim

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssl \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p /data/blockchain

# Expose ports
EXPOSE 7050 7051 8080 9443

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD python healthcheck.py

# Start command
CMD ["python", "main.py"]