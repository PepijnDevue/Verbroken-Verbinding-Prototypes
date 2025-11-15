import streamlit as st
import src.huggingface_utils as hf_utils
from src.utils import get_runtime_info


def render_sidebar() -> None:
	st.sidebar.title("Model Configuration")

	model_name = st.sidebar.text_input(
		"Model path",
		value="google/flan-t5-small",
		help="Hugging Face model name or path (e.g., google/flan-t5-small, etc.)",
	)

	accelerate = st.sidebar.checkbox(
		"Use Accelerate for device mapping",
		value=True,
		help="Let Hugging Face handle device mapping, instead of forcing GPU/CPU.",
	)

	st.sidebar.button(
		label="Load Model",
		help="Load the specified model from Hugging Face Hub.",
		on_click=hf_utils.load_model,
		args=(model_name, accelerate),
	)

	with st.sidebar.expander("Runtime info", expanded=False):
		info = get_runtime_info()
		st.json(info)
