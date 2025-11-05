import streamlit as st
from transformers import pipeline
import torch

# Modelpath validation
from huggingface_hub import model_info
from huggingface_hub.utils import HfHubHTTPError

# Gathering system info
import platform
import multiprocessing
import psutil

def main():
    setup_header()
    setup_sidebar()
    setup_body()

# ==== DISPLAY FUNCTIONS ====
def setup_header():
    st.title("Test Pagina VV")
    st.write("""
        Deze webapp wordt gebruikt om te leren hoe je eenvoudig een webapp kunt maken met Streamlit
        , een taalmodel kunt laden met Hugging Face Transformers, en dit op een server kunt hosten
        via Docker zodanig dat er optimaal gebruik wordt gemaakt van beschikbare GPU resources.
    """)

def setup_sidebar():
    st.sidebar.title("Model Configuration")
    
    model_name = st.sidebar.text_input(
        "Model path",
        value="google/flan-t5-small",
        help="Hugging Face model name or path (e.g., google/flan-t5-small, etc.)"
    )

    if st.sidebar.button("Load Model"):
        if validate_huggingface_model(model_name):
            st.session_state.pipe = load_model(model_name=model_name)
        else:
            st.sidebar.error(f"Model '{model_name}' not found on HuggingFace. Please check the model name.")
    
    display_runtime_info()

def setup_body():
    if "pipe" not in st.session_state:
        st.warning("Please load a model from the sidebar.")
        return

    user_input = st.text_area("**Input:**")

    if not st.button("Generate"):
        return
    
    if not user_input.strip():
        st.warning("Please enter some input text.")
        return
    
    with st.spinner("Generating..."):
        output = generate(user_input)
        st.markdown(
            f"""**Output:**<br>{output}""",
            unsafe_allow_html=True)

def display_runtime_info():
    with st.sidebar.expander("Runtime info", expanded=False):
        info = {"device_info": {}}
        if torch is not None and torch.cuda.is_available():
            props = torch.cuda.get_device_properties(0)
            info["device_info"]["device"] = props.name
            info["device_info"]["compute"] = f"{props.major}.{props.minor}"
            info["device_info"]["ram"] = f"{props.total_memory / 1e9:.2f}GB"
            info["device_info"]["cores"] = props.multi_processor_count
        else: # CPU fallback
            info["device_info"]["device"] = platform.processor()
            info["device_info"]["ram"] = f"{psutil.virtual_memory().total / 1e9:.2f}GB"
            info["device_info"]["cores"] = multiprocessing.cpu_count()

        if "pipe" in st.session_state:
            info["runtime_info"] = {}

            model = st.session_state.pipe.model
            device_map = getattr(model, "hf_device_map", None)
            dtype = getattr(model, "dtype", None)

            if device_map:
                info["runtime_info"]["accelerate"] = True
                info["runtime_info"]["device_map"] = device_map

            info["runtime_info"]["dtype"] = dtype or "Unknown"
            info["runtime_info"]["model_params"] = f"{model.num_parameters()/1e6:.2f}M"

        st.json(info)


# ==== MODEL FUNCTIONS ====
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
def load_model(model_name: str) -> pipeline:
    # Resolve device_map
    has_cuda = (torch is not None) and torch.cuda.is_available()
    device_map = "auto" if has_cuda else None

    return pipeline(
        "text-generation",
        model=model_name,
        device_map=device_map,  # handled by Accelerate if available
        dtype="auto",
    )

def generate(user_input: str) -> str:
    pipe = st.session_state.pipe

    outputs = pipe(user_input)

    # Format outputs
    output = outputs[0]["generated_text"]

    return output


# ==== MAIN ENTRY POINT ====

if __name__ == "__main__":
    main()