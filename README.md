# Verbroken Verbinding Test

A testing and development environment for combining Hugging Face, Streamlit, and Docker an ubuntu base with GPU support. And developing simple prototypes for Verbroken Verbinding.

## Quick Start with Docker

Running the following command will build and start the Docker container. Caddy will serve the Streamlit app on port 80, the default HTTP port.

```bash
# Build and run the Docker container (detached mode)
docker compose up -d --build
```

The Streamlit app is now accessible at `http://localhost` or `http://<your-server-ip>`.

## Prerequisites

- **Github Repository**: Have access to [this repository](https://github.com/PepijnDevue/Verbroken-Verbinding-Prototypes).
- **Server with GPU**: An Ubuntu server with an NVIDIA GPU.
- **Hugging Face Account**: (Optional) For accessing private models or gated models. Get your token from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).

## Configuration

### Server Setup

Read [server_setup.md](docs/server_setup.md) for detailed server setup instructions, including CUDA and Docker installation.

### Hugging Face Token Setup

To access private models or avoid rate limits, configure your Hugging Face token:

1. Create an environment file:
   ```bash
   touch .env
   ```

2. Add your Hugging Face token to `.env`:
   ```
   HF_TOKEN=your_huggingface_token_here
   ```

### Repository Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/PepijnDevue/Verbroken-Verbinding-Prototypes.git
   git checkout main
   cd Verbroken-Verbinding-Prototypes
   ```

2. Caddy Configuration:

   - Update the `Caddyfile` with your domain name and any necessary security headers.


## Development Setup (Without Docker)

### Requirements

- Python 3.12+
- [CUDA 13.0](https://developer.nvidia.com/cuda-downloads)
- [UV](https://docs.astral.sh/uv/getting-started/installation/#installation-methods)

### Installation

```bash
# Install with UV
uv sync
```

### Run Locally

```bash
# Run with UV
uv run streamlit run
```

```bash
# Or run using .venv
streamlit run
```

## License

TODO: Add license information here.