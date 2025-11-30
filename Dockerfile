# Use NVIDIA CUDA 12.6 base image with Ubuntu 22.04
FROM nvidia/cuda:12.6.2-cudnn-runtime-ubuntu22.04

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    PATH="/root/.local/bin:$PATH"

# Install Python 3.12 and system dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.12 \
    python3.12-dev \
    python3.12-venv \
    python3-pip \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up pip for Python 3.12 and symlinks
# Note: Use ensurepip with Python 3.12 to avoid Debian's system pip (which may rely on distutils)
RUN python3.12 -m ensurepip --upgrade \
    && python3.12 -m pip install --upgrade pip setuptools wheel \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && python3 -m pip --version \
    && python3.12 -m venv /opt/venv \
    && /opt/venv/bin/python -m pip install --upgrade pip setuptools wheel

# Use isolated virtual environment for Python packages
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies inside the virtual environment
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py .
COPY src ./src
COPY docs ./docs
COPY pyproject.toml .
COPY README.md .

# Copy .env file if it exists (optional, can also use environment variables from docker-compose)
COPY .env* ./
RUN if [ ! -f .env ]; then echo "Warning: .env file not found. HF_TOKEN will need to be set via environment variables." && touch .env; fi

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
