import streamlit as st
from src.utils import get_runtime_info


def render_diagnostics():
    with st.sidebar.expander("Model & Runtime Diagnostics", expanded=False):
        st.json(get_runtime_info())