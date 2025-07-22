FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies required by markitdown and its dependencies
RUN apt-get update && apt-get install -y \
    # For general file processing
    curl \
    wget \
    # For image processing (PIL/Pillow dependencies)
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libwebp-dev \
    # For audio processing
    ffmpeg \
    # For PDF processing
    poppler-utils \
    # For OCR capabilities
    tesseract-ocr \
    tesseract-ocr-eng \
    # Build tools for some Python packages
    gcc \
    g++ \
    # For cleaning up
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock* ./

# Install Python dependencies using uv
RUN uv sync --frozen --no-cache

# Copy application code
COPY main.py ./

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8003

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8003/health || exit 1

# Run the application
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]