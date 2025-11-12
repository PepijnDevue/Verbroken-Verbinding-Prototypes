# Server Setup Documentation

This document outlines all definitive changes made to set up the Ubuntu 22.04 GPU server for the Verbroken-Verbinding-Test Streamlit application.

## Server Specifications
- **OS**: Ubuntu 22.04 LTS
- **GPU**: NVIDIA A10
- **CUDA Version**: 12.9
- **Public IP**: 145.38.192.134

---

## 1. Docker Installation

Installed Docker Engine and Docker Compose plugin:

```bash
# Added Docker's official GPG key and repository
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Installed Docker packages
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

---

## 2. NVIDIA Container Toolkit Installation

Installed NVIDIA Container Toolkit to enable GPU access in Docker containers:

```bash
# Added NVIDIA package repository
distribution=$(. /etc/os-release; echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

# Installed nvidia-container-toolkit
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Restarted Docker to apply changes
sudo systemctl restart docker
```

**Verification**: Tested GPU access with CUDA 12.6 runtime image:
```bash
sudo docker run --rm --gpus all nvidia/cuda:12.6.2-cudnn-runtime-ubuntu22.04 nvidia-smi
```

---

## 3. Repository Deployment

Cloned the private GitHub repository to the server:

**Location**: `/home/pdevue2/Verbroken-Verbinding-Test`

**Authentication**: SSH deploy key configured for GitHub repository access.

```bash
# Generated SSH key for deploy access
ssh-keygen -t ed25519 -C "deploy-key-$(hostname)-$(date +%F)" -f ~/.ssh/github_deploy -N ""

# Added public key to GitHub repository settings (Deploy keys)
# Cloned repository
git clone git@github.com:PepijnDevue/Verbroken-Verbinding-Test.git
```

---

## 4. Docker Compose Build and Deployment

Built and started the containerized application:

```bash
cd ~/Verbroken-Verbinding-Test

# Built Docker image
docker compose build

# Started service in detached mode
docker compose up -d
```

**Container Name**: `vv-test-app`
**Exposed Port**: 8501 (Streamlit default)

---

## 5. Verification Tests Performed

### GPU Access Verification
```bash
# Inside container
docker exec -it vv-test-app nvidia-smi
```
**Result**: ✅ GPU visible and accessible

### PyTorch CUDA Verification
```bash
docker exec -it vv-test-app python -c "import torch; print('torch:', torch.__version__, 'cuda_available:', torch.cuda.is_available(), 'cuda_runtime:', torch.version.cuda)"
```
**Result**: ✅ 
- torch: 2.9.0+cu126
- cuda_available: True
- cuda_runtime: 12.6

### Streamlit Health Check
```bash
curl -f http://localhost:8501/_stcore/health
```
**Result**: ✅ Streamlit running and healthy

### Port Mapping Verification
```bash
# Check container status and port bindings
docker compose ps
```
**Result**: ✅ 
- vv-test-app: Up (healthy), internal port 8501
- vv-caddy: Up, 0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp

### Local HTTP Access
```bash
curl http://localhost:80
```
**Result**: ✅ Returns Streamlit HTML (proxied through Caddy)

---

## Quick Reference Commands

### Container Management
```bash
# View running containers
docker compose ps
docker ps

# View logs
docker compose logs -f streamlit-app

# Restart service
docker compose restart

# Stop all services
docker compose down

# Rebuild after code changes
docker compose build --no-cache
docker compose up -d
```