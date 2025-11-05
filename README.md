# Verbroken Verbinding Test

A Streamlit web application for testing Hugging Face language models with GPU acceleration.

## Features

- 🤖 Load and test Hugging Face language models
- ⚡ GPU acceleration with CUDA support
- 🎨 Clean, intuitive Streamlit interface
- 🐳 Fully containerized with Docker
- 📊 Runtime information display (GPU/CPU, model details)

## Prerequisites

### For Docker Deployment (Recommended)

- Docker Engine 20.10+ with Docker Compose
- NVIDIA GPU with compute capability 3.5+
- NVIDIA Driver 525.60.13+ (for CUDA 13.0)
- NVIDIA Container Toolkit

### Installing NVIDIA Container Toolkit on Linux

```bash
# Configure the production repository
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Update package list
sudo apt-get update

# Install NVIDIA Container Toolkit
sudo apt-get install -y nvidia-container-toolkit

# Configure Docker to use NVIDIA runtime
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Test GPU access in Docker
docker run --rm --gpus all nvidia/cuda:13.0.0-base-ubuntu22.04 nvidia-smi
```

## Quick Start with Docker

### 1. Build the Docker Image

```bash
docker-compose build
```

### 2. Run the Container

```bash
docker-compose up -d
```

### 3. Access the Application

Open your browser and navigate to:
```
http://localhost:8501
```

### 4. Stop the Container

```bash
docker-compose down
```

## Docker Commands Reference

### View Logs

```bash
# Follow logs in real-time
docker-compose logs -f

# View last 100 lines
docker-compose logs --tail=100
```

### Restart Container

```bash
docker-compose restart
```

### Rebuild After Code Changes

```bash
docker-compose up -d --build
```

### Access Container Shell

```bash
docker exec -it vv-test-app /bin/bash
```

### Remove Everything (including volumes)

```bash
docker-compose down -v
```

## Configuration

### Environment Variables

Create a `.env` file in the project root to configure optional settings:

```env
# Optional: Hugging Face token for private models
HUGGINGFACE_TOKEN=your_token_here
```

### GPU Configuration

The `docker-compose.yml` is configured to use all available GPUs. To limit GPU usage:

```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          device_ids: ['0']  # Use only first GPU
          capabilities: [gpu]
```

## Development Setup (Without Docker)

### Requirements

- Python 3.12+
- CUDA 13.0
- UV or pip

### Installation

```bash
# Install with UV
uv pip install -r requirements.txt

# Or with pip
pip install -r requirements.txt
```

### Run Locally

```bash
streamlit run streamlit_app.py
```

## Project Structure

```
.
├── streamlit_app.py       # Main application entry point
├── streamlit_ui.py        # UI components and layout
├── huggingface_utils.py   # Model loading and generation
├── utils.py               # System information utilities
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
├── Dockerfile             # Container image definition
├── docker-compose.yml     # Docker orchestration
└── .dockerignore          # Docker build exclusions
```

## Troubleshooting

### GPU Not Detected

1. Verify NVIDIA driver installation:
   ```bash
   nvidia-smi
   ```

2. Check NVIDIA Container Toolkit:
   ```bash
   docker run --rm --gpus all nvidia/cuda:13.0.0-base-ubuntu22.04 nvidia-smi
   ```

3. Verify Docker GPU access:
   ```bash
   docker exec -it vv-test-app nvidia-smi
   ```

### Container Won't Start

1. Check logs:
   ```bash
   docker-compose logs
   ```

2. Verify port 8501 is available:
   ```bash
   # Linux
   sudo lsof -i :8501
   
   # Or use netstat
   netstat -an | grep 8501
   ```

3. Check disk space and memory:
   ```bash
   df -h
   free -h
   ```

### Out of Memory Errors

Increase shared memory in `docker-compose.yml`:

```yaml
shm_size: '4gb'  # Increase from 2gb
```

## License

MIT

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.