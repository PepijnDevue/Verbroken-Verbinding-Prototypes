"""
Hugging Face model handling utilities.
Contains functions for model validation, loading, and text generation.
"""

import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

try:
    import torch
    from transformers import pipeline
    from huggingface_hub import model_info
    from huggingface_hub.utils import HfHubHTTPError
except ImportError:
    # Handle missing dependencies gracefully
    # This repository is designed to also work on saved data without model loading
    torch = None
    pipeline = None
    model_info = None
    HfHubHTTPError = None

MODEL_DEFAULT = "mistralai/Ministral-3-8B-Instruct-2512-BF16"

# Load environment variables from .env file
# This will work in development (with uv) and in Docker if .env is copied
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


def _get_token() -> str | None:
    """Return Hugging Face token from env if present."""
    return os.getenv("HF_TOKEN") or None


def load_model(model_name: str = MODEL_DEFAULT, 
               accelerate: bool = True
               ) -> None:
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


def generate(user_input: str) -> str:
    """Generate text using the loaded model pipeline."""
    outputs = st.session_state.pipe(user_input)

    # Format outputs
    output = outputs[0]["generated_text"]

    return output

def generate_with_retries(prompt: str, 
                          reason_str: str = "BEREDENEER",
                          result_str: str = "RESULTAAT",
                          max_retries: int = 5
                          ) -> dict:
    reasoning = None
    result = None

    while (reasoning is None or result is None) and max_retries > 0:
        response = generate(prompt)

        # Search for reasoning and result sections
        reason_identifier = "\n" + reason_str
        result_identifier = "\n" + result_str
        reason_idx = response.find(reason_identifier)
        result_idx = response.find(result_identifier)

        # Try again if not found
        if reason_idx == -1 or result_idx == -1:
            max_retries -= 1
            continue

        # Extract reasoning and result
        reasoning = response[reason_idx + len(reason_identifier):result_idx].strip()
        result = response[result_idx + len(result_identifier):].strip()

        max_retries -= 1

    return {
        reason_str.lower(): reasoning, 
        result_str.lower(): result
    }