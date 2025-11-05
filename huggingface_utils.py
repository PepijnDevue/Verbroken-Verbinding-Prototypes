"""
Hugging Face model handling utilities.
Contains functions for model validation, loading, and text generation.
"""

import streamlit as st
from transformers import pipeline
from huggingface_hub import model_info
from huggingface_hub.utils import HfHubHTTPError


def validate_huggingface_model(model_name: str) -> bool:
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
def load_model(model_name: str, accelerate: bool) -> pipeline:
    # Resolve device_map
    device_map = "auto" if accelerate else None

    return pipeline(
        "text-generation",
        model=model_name,
        device_map=device_map,
    )


def generate(user_input: str, pipe: pipeline) -> str:
    outputs = pipe(user_input)

    # Format outputs
    output = outputs[0]["generated_text"]

    return output
