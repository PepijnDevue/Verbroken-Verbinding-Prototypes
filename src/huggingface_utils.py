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


def load_model(model_name: str, accelerate: bool):
    if not _validate_huggingface_model(model_name):
        st.sidebar.error("Please enter a valid Hugging Face model name or path.")
        return
    
    st.session_state.pipe = _load_model(model_name=model_name, accelerate=accelerate)


def _validate_huggingface_model(model_name: str) -> bool:
    if not model_name or not model_name.strip():
        return False
    
    try:
        model_info(model_name)
        return True
    except HfHubHTTPError:
        # Handle HTTP errors (404 for not found, 401 for unauthorized, etc.)
        return False
    except Exception as e:
        # Catch other potential errors (network issues, etc.)
        st.sidebar.warning(f"Error validating model: {e}")
        return False


@st.cache_resource
def _load_model(model_name: str, accelerate: bool) -> pipeline:
    # Resolve device_map
    device_map = "auto" if accelerate else None

    # Use token if available
    token = os.getenv("HF_TOKEN")

    return pipeline(
        "text-generation",
        model=model_name,
        device_map=device_map,
        token=token,
    )


def generate(user_input: str, pipe: pipeline) -> str:
    outputs = pipe(user_input)

    # Format outputs
    output = outputs[0]["generated_text"]

    return output
