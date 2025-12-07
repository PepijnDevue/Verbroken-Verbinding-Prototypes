"""
Hugging Face model handling utilities.
Contains functions for model validation, loading, and text generation.
"""

import os
import re
import json
from pathlib import Path
import streamlit as st
from transformers import pipeline
from huggingface_hub import model_info
from huggingface_hub.utils import HfHubHTTPError
from dotenv import load_dotenv

try:
    import torch
except ImportError:
    torch = None

MODEL_DEFAULT = "mistralai/Ministral-3-8B-Instruct-2512-BF16"

# Load environment variables from .env file
# This will work in development (with uv) and in Docker if .env is copied
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


def _get_token() -> str | None:
    """Return Hugging Face token from env if present."""
    return os.getenv("HF_TOKEN") or None


def _unload_model():
    """Unload the current model and free GPU memory."""
    if "pipe" not in st.session_state or st.session_state.pipe is None:
        return
    
    # Delete the pipeline
    del st.session_state.pipe
    st.session_state.pipe = None
    
    # Clear CUDA cache to free GPU memory
    if torch is not None and torch.cuda.is_available():
        torch.cuda.empty_cache()


def load_model(model_name: str = MODEL_DEFAULT, 
               accelerate: bool = True
               ) -> None:
    if not _validate_huggingface_model(model_name):
        return
    
    # Unload existing model to free memory
    _unload_model()
    
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

def extract_json_from_response(response: str, keyword: str = ">\nOUTPUT") -> dict:
    """Extract JSON from model response, handling potential markdown formatting."""
    # Remove any leading text before the keyword (incl)
    keyword_idx = response.find(keyword)
    output = response[keyword_idx + len(keyword):]

    try:
        # Try to find JSON in code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', output, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        
        # Try to find raw JSON
        json_match = re.search(r'\{.*\}', output, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
    except json.JSONDecodeError as e:
        return {"error": "json_decode_error", "details": str(e), "response": response}

    return {"error": "no_valid_json_found", "response": response}    

def generate_with_retries(prompt: str, max_retries: int = 5) -> dict:
    output = {"error": "not_processed_yet"}
    iterations = 0

    while output.get("error") is not None and iterations < max_retries:
        response = generate(prompt)
        output = extract_json_from_response(response)
        iterations += 1

    if output.get("error") is not None:
        with st.expander(output.get("error")):
            st.text(output.get("details", "No details available."))
            st.text(output.get("response", "No response captured."))
        return {}

    return output