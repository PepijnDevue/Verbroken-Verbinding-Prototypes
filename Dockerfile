# Use NVIDIA CUDA base image with Ubuntu 22.04
# This image will use the CUDA runtime that matches the server (CUDA 12.x)
FROM nvidia/cuda:12.9.0-cudnn8-runtime-ubuntu22.04

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

# Create symlinks for python and pip
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 \
    && update-alternatives --set python3 /usr/bin/python3.12 \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && python3 -m pip install --upgrade pip setuptools wheel

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
# Install PyTorch with CUDA support from the PyTorch index
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py .
COPY pyproject.toml .
COPY README.md .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
