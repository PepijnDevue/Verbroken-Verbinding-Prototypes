import streamlit as st
from src.utils import get_runtime_info


def render_diagnostics():
    with st.sidebar.expander("Model & Runtime Diagnostics", expanded=False):
        st.json(get_runtime_info())

def is_model_loaded(verbose: bool = True) -> bool:
    loaded = "pipe" in st.session_state and st.session_state.pipe is not None

    if not loaded and verbose:
        st.error("Language model not loaded. Please return to the main page to load the model.")

    return loaded