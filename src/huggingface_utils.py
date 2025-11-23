"""
Hugging Face model handling utilities.
Contains functions for model validation, loading, and text generation.
"""

import os
from pathlib import Path
import streamlit as st
from transformers import pipeline
from huggingface_hub import model_info
from huggingface_hub.utils import HfHubHTTPError
from dotenv import load_dotenv

# Load environment variables from .env file
# This will work in development (with uv) and in Docker if .env is copied
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


def _get_token() -> str | None:
    """Return Hugging Face token from env if present."""
    return os.getenv("HF_TOKEN") or None


def load_model(model_name: str, accelerate: bool):
    if not _validate_huggingface_model(model_name):
        return
    
    st.session_state.pipe = _load_model(model_name=model_name, accelerate=accelerate)


def _validate_huggingface_model(model_name: str) -> bool:
    if not model_name or not model_name.strip():
        return False

    token = _get_token()

    try:
        info = model_info(model_name, token=token)
        # If the model is private and we have no token, fail explicitly
        if getattr(info, "private", False) and not token:
            st.sidebar.error("Model is private. Add HF_TOKEN to .env.")
            return False
        return True
    except HfHubHTTPError as e:
        if e.response is not None and e.response.status_code == 401:
            st.sidebar.error("Unauthorized. Provide a valid HF_TOKEN for this private model.")
        elif e.response is not None and e.response.status_code == 404:
            st.sidebar.error("Model not found on Hugging Face.")
        else:
            st.sidebar.error(f"Hugging Face error: {e}")
        return False
    except Exception as e:
        st.sidebar.warning(f"Error validating model: {e}")
        return False


@st.cache_resource
def _load_model(model_name: str, accelerate: bool) -> pipeline:
    # Resolve device_map
    device_map = "auto" if accelerate else None

    return pipeline(
        "text-generation",
        model=model_name,
        device_map=device_map,
        token=_get_token(),
    )


def generate(user_input: str, pipe: pipeline) -> str:
    outputs = pipe(user_input)

    # Format outputs
    output = outputs[0]["generated_text"]

    return output
