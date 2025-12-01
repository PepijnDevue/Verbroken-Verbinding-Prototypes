import streamlit as st
from pathlib import Path
from src.utils import get_runtime_info


def render_diagnostics():
    with st.sidebar.expander("Model & Runtime Diagnostics", expanded=False):
        st.json(get_runtime_info())


def is_model_loaded(verbose: bool = True) -> bool:
    loaded = "pipe" in st.session_state and st.session_state.pipe is not None

    if not loaded and verbose:
        st.error("Language model not loaded. Please return to the main page to load the model.")

    return loaded


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

def render_page_header(title: str, explanation: str):
    """
    Render the page header with title and explanation.
    
    Args:
        title: Title of the page
        explanation: Explanation text for the page
    """
    st.title(title)
    st.write(explanation)

def render_article(
        title: str, 
        text: str, 
        url: str = "", 
        owner: str = "Onbekend",
        **kwargs):
    # Render within a bordered container for better visual separation
    with st.container(border=True):
        st.subheader(title)
        st.markdown(text, unsafe_allow_html=True)

        if not url:
            return
        
        # Add source link
        _, col = st.columns([3, 1])
        with col:
            st.write(f"[Bron: {owner}]({url})")