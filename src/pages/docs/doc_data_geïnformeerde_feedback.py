"""Data Geïnformeerde Feedback documentation page."""
from pathlib import Path
import streamlit as st
import src.streamlit_utils as st_utils

# Get the path to the markdown file
base_dir = Path(__file__).parent.parent.parent.parent.resolve()
markdown_file = base_dir / "docs" / "pages" / "data_geïnformeerde_feedback.md"

with st.container(border=True):
    st_utils.render_markdown_page(str(markdown_file))
