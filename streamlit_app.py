import streamlit as st
from transformers import pipeline
import torch

def main():
    setup_header()

    setup_sidebar()
    
    setup_body()


# ==== SETUP FUNCTIONS ====
def setup_header():
    st.title("Test Pagina VV")
    st.write("""
        Testing a prototype using streamlit + transformers + docker
    """)

def setup_sidebar():
    st.sidebar.title("Model Configuration")
    
    model_name = st.sidebar.text_input(
        "Model path",
        value="google/flan-t5-small",
        help="Hugging Face model name or path (e.g., google/flan-t5-small, gpt2, etc.)"
    )

    task = st.sidebar.selectbox(
        "Task",
        options=["text-generation", "text2text-generation"],
        index=0,
        help="Pick the pipeline task appropriate for your model. T5/FLAN use text2text-generation; GPT-style use text-generation."
    )

    precision = st.sidebar.selectbox(
        "Precision (dtype)",
        options=["auto", "float16", "bfloat16", "float32"],
        index=0,
        help="Use lower precision on GPU for speed/memory savings. 'auto' picks float16 on CUDA, float32 otherwise."
    )

    if not st.sidebar.button("Load Model"):
        return
    
    if (torch is None or not torch.cuda.is_available()):
        st.sidebar.warning("CUDA GPU not detected. Falling back to CPU.")

    st.session_state.pipe = load_model(
        model_name=model_name,
        task=task,
        precision=precision,
    )

    # Show a quick summary of placement/precision
    with st.sidebar.expander("Runtime details", expanded=False):
        try:
            model = st.session_state.pipe.model
            device_map = getattr(model, "hf_device_map", None)
            dtype = getattr(model, "dtype", None)
            if device_map:
                st.write("device_map detected (Accelerate):")
                st.json(device_map)
            else:
                st.write("device:", getattr(next(model.parameters()).device, "type", "unknown"))
            if dtype is not None:
                st.write("dtype:", str(dtype))
        except Exception:
            st.write("Unable to gather runtime details.")

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


# ==== MODEL FUNCTIONS ====
@st.cache_resource
def load_model(
    model_name: str,
    task: str,
    precision: str = "auto",
) -> pipeline:
    """Load a Transformers pipeline with Accelerate-aware device placement.

    - Uses device_map="auto" when GPU is preferred and available.
    - Sets dtype to selected precision. 'auto' = float16 on CUDA, float32 otherwise.
    - Avoids passing an explicit device when using device_map (per Transformers docs).
    """
    # Resolve dtype
    dtype_value = "auto"
    if precision == "auto":
        if torch is not None and torch.cuda.is_available():
            dtype_value = torch.float16
        else:
            dtype_value = "auto"  # let Transformers decide (typically float32 on CPU)
    elif precision == "float16" and torch is not None:
        dtype_value = torch.float16
    elif precision == "bfloat16" and torch is not None:
        dtype_value = torch.bfloat16
    elif precision == "float32" and torch is not None:
        dtype_value = torch.float32

    # Resolve device_map
    device_map = "auto" if (torch is not None and torch.cuda.is_available()) else None

    return pipeline(
        task,
        model=model_name,
        device_map=device_map,  # handled by Accelerate if available
        dtype=dtype_value,
    )

def generate(user_input: str) -> str:
    pipe = st.session_state.pipe

    outputs = pipe(user_input)

    # Format outputs
    output = outputs[0]["generated_text"]

    return output


if __name__ == "__main__":
    main()