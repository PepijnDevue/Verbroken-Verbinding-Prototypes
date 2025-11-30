"""Ankertjes documentation page."""
from pathlib import Path
import streamlit as st
import src.streamlit_utils as st_utils

# Get the path to the markdown file
current_file = Path(__file__).resolve()
base_dir = current_file.parent.parent.parent.parent.resolve()

# Debug: Show path resolution
st.write("DEBUG: Current file:", current_file)
st.write("DEBUG: Base dir (4 levels up):", base_dir)
st.write("DEBUG: Base dir exists?", base_dir.exists())
st.write("DEBUG: Base dir contents:", list(base_dir.iterdir()) if base_dir.exists() else "N/A")

# Check /app directory
app_dir = Path("/app")
if app_dir.exists():
    st.write("DEBUG: /app exists")
    st.write("DEBUG: /app contents:", list(app_dir.iterdir()))
    docs_dir = app_dir / "docs"
    if docs_dir.exists():
        st.write("DEBUG: /app/docs exists")
        st.write("DEBUG: /app/docs contents:", list(docs_dir.iterdir()))

markdown_file = base_dir / "docs" / "ankertjes.md"
st.write("DEBUG: Looking for markdown at:", markdown_file)
st.write("DEBUG: Markdown file exists?", markdown_file.exists())

st_utils.render_markdown_page(str(markdown_file))
