import streamlit as st
import src.huggingface_utils as hf_utils
import src.streamlit_utils as st_utils

def main():
    setup_header()
    st_utils.render_diagnostics()
    setup_body()


def setup_header():
    st.title("Verbroken Verbinding Test")
    st.write("""
        Deze webapp wordt gebruikt om te leren hoe je eenvoudig een webapp kunt maken met Streamlit
        , een taalmodel kunt laden met Hugging Face Transformers, en dit op een server kunt hosten
        via Docker zodanig dat er optimaal gebruik wordt gemaakt van beschikbare GPU resources.
    """)

def setup_body():
    user_input = st.text_area("**Input:**")

    if not st.button("Generate"):
        return

    if not user_input.strip():
        st.warning("Please enter some input text.")
        return

    if not st_utils.is_model_loaded():
        return

    with st.spinner("Genereren..."):
        output = hf_utils.generate(user_input)
        st.markdown(f"""**Output:**<br>{output}""", unsafe_allow_html=True)


if __name__ == "__main__":
    main()