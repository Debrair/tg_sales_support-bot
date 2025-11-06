FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY bot.py .

# Expose port for health checks
EXPOSE 8000

# Create non-root user for security
RUN useradd -m -r botuser && \
    chown -R botuser:botuser /app
USER botuser

CMD ["python", "bot.py"]
