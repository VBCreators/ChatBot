FROM python:3.14-slim

# Create non-root user
RUN useradd -m -s /bin/bash appuser

# Set working directory
WORKDIR /app

# Install curl command for performed Docker Compose Health Check
# python:3.14-slim does not have wget or curl command out of the box
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user (security best practice)
USER appuser

EXPOSE 8501

CMD ["streamlit", "run", "GUI.py", "--server.port=8501", "--server.address=0.0.0.0"]