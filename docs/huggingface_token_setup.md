# Hugging Face Token Setup

This guide explains how to configure your Hugging Face access token for both development and Docker deployment.

## What is a Hugging Face Token?

A Hugging Face token allows you to:
- Access private models
- Bypass rate limits on model downloads
- Access gated models that require authentication

## Getting Your Token

1. Visit [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Log in to your Hugging Face account
3. Create a new token or use an existing one
4. Copy the token value

## Setup Instructions

### For Development (with uv)

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and replace `your_huggingface_token_here` with your actual token:
   ```
   HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

3. The token will be automatically loaded when you run the application with `uv run streamlit run streamlit_app.py`

### For Docker Deployment

The Docker setup supports two methods:

#### Method 1: Using .env file (Recommended)

1. Create a `.env` file in the project root with your token:
   ```
   HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

2. Build and run with docker-compose:
   ```bash
   docker-compose up -d
   ```

The `.env` file will be:
- Copied into the Docker image during build
- Used by docker-compose to set environment variables
- Loaded by the application at runtime

#### Method 2: Environment variable only

If you don't want to copy `.env` into the image, you can set the environment variable directly:

```bash
export HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
docker-compose up -d
```

Or modify `docker-compose.yml` to hardcode the token (not recommended for security):

```yaml
environment:
  - HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Security Notes

- **Never commit `.env` to git** - it's already in `.gitignore`
- The `.env.example` file is safe to commit (it contains no secrets)
- For production deployments, consider using Docker secrets or environment-specific configuration management
- Tokens should be treated as passwords and kept secure

## Verifying Setup

When the application starts, if the token is loaded successfully, you should be able to access private and gated models without issues. If there's a problem, check:

1. The `.env` file exists and contains `HF_TOKEN=...`
2. For Docker: the `.env` file was present during build
3. The token is valid (test it on [huggingface.co](https://huggingface.co))

## Troubleshooting

**Token not being recognized:**
- Ensure no extra spaces in `.env` file
- Verify the token variable name is exactly `HF_TOKEN`
- For Docker: rebuild the image after adding `.env`

**401 Unauthorized errors:**
- Your token may have expired or been revoked
- Generate a new token and update `.env`
