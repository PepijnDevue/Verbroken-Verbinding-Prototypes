"""Leg Het Me Uit Knop documentation page."""
from pathlib import Path
import streamlit as st
import src.streamlit_utils as st_utils

# Get the path to the markdown file
base_dir = Path(__file__).parent.parent.parent.parent.resolve()
markdown_file = base_dir / "docs" / "pages" / "leg_het_me_uit_knop.md"

with st.container(border=True):
    st_utils.render_markdown_page(str(markdown_file))
