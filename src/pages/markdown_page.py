"""Generic markdown page renderer for Streamlit."""
import streamlit as st
from pathlib import Path


def render_markdown_page(markdown_file_path: str):
    """
    Render a markdown file as a Streamlit page.
    
    Args:
        markdown_file_path: Path to the markdown file to render
        title: Optional title to display at the top of the page
    """
    markdown_path = Path(markdown_file_path)
    
    if not markdown_path.exists():
        st.error(f"Markdown file not found: {markdown_file_path}")
        return
    
    # Read and display markdown content
    try:
        with open(markdown_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        st.markdown(markdown_content, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error reading markdown file: {e}")
