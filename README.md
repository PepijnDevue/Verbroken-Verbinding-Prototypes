# Verbroken Verbinding Prototypes

AI prototypes for the Verbroken Verbinding research project, demonstrating news analysis tools using Streamlit and Hugging Face.

## Quick Start with Docker

```bash
docker compose up -d --build
```

The Streamlit app will be available at `http://localhost`.

## Prerequisites

- Docker with GPU support ([NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html))
- (Optional) [Hugging Face token](https://huggingface.co/settings/tokens) for accessing gated models

### Hugging Face Token Setup

To access private or gated models, create a `.env` file in the project root:

```
HF_TOKEN=your_huggingface_token_here
```

## Configuration

### Caddy

Update the `Caddyfile` with your domain name and any necessary security headers.

## Local Development

### Requirements

- Python 3.12+
- [CUDA 12.6](https://developer.nvidia.com/cuda-downloads)
- [UV](https://docs.astral.sh/uv/getting-started/installation/)

### Installation

```bash
uv sync
```

### Run

```bash
uv run streamlit run streamlit_app.py
```

## License

TODO: Add license information here.
