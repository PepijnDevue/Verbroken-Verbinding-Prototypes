import streamlit as st
import src.huggingface_utils as hf_utils
from src.utils import get_runtime_info

def main():
    setup_header()
    setup_sidebar()
    setup_body()


def setup_header():
    st.title("Verbroken Verbinding Test")
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

    accelerate = st.sidebar.checkbox(
        "Use Accelerate for device mapping",
        value=True,
        help="Let Hugging Face handle device mapping, instead of forcing GPU/CPU."
    )

    st.sidebar.button(
        label="Load Model",
        help="Load the specified model from Hugging Face Hub.",
        on_click=hf_utils.load_model,
        args=(model_name, accelerate)
    )
    
    with st.sidebar.expander("Runtime info", expanded=False):
        info = get_runtime_info()
        st.json(info)


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
        pipe = st.session_state.pipe
        output = hf_utils.generate(user_input, pipe)
        st.markdown(
            f"""**Output:**<br>{output}""",
            unsafe_allow_html=True)


if __name__ == "__main__":
    main()