import streamlit as st
from transformers import pipeline

def main():
    setup_header()

    setup_sidebar()

    if "pipe" not in st.session_state:
        st.warning("Please load a model from the sidebar.")
        return
    
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
        value="google/flan-t5-small"
    )

    if st.sidebar.button("Load Model"):
        st.session_state.pipe = load_model(model_name)
        st.sidebar.success(f"Model '{model_name}' loaded successfully!")

def setup_body():
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
def load_model(model_name: str) -> pipeline:
    return pipeline(
        "text2text-generation",
        model=model_name,
        device=0
    )

def generate(user_input: str) -> str:
    pipe = st.session_state.pipe

    outputs = pipe(user_input)

    # Format outputs
    output = outputs[0]["generated_text"]

    return output


if __name__ == "__main__":
    main()