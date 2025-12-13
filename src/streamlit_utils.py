import streamlit as st
from pathlib import Path

# ==== Render functions ====
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

def render_hyperlink(url: str,
                     owner: str = "Onbekend",
                     align_right: bool = True) -> None:
    hyperlink = f"[Bron: {owner}]({url})"

    if not align_right:
        st.write(hyperlink)
        return
    
    # Calculate column ratio based on hyperlink length
    extracted = hyperlink[hyperlink.find('[')+1:hyperlink.find(']')]
    ratio = 80//len(extracted)

    _, col = st.columns([ratio-1, 1])
    with col:
        st.write(hyperlink)
    
def render_article(title: str, 
                   text: str, 
                   url: str = "", 
                   owner: str = "Onbekend",
                   render_score: bool = False,
                   score: float = -1,
                   score_label: str = "",
                   score_help: str = "",
                   **kwargs):
    # Render within a bordered container for better visual separation
    with st.container(border=True):
        # Header with optional score metric
        if not render_score:
            # Simple title rendering
            st.subheader(title)
        else:
            # Render title with score metric
            left, right = st.columns([5, 1])
            with left:
                st.subheader(title)
            with right:
                st.space("medium")
                st.metric(
                    label=score_label, 
                    value=f"{score:.1f}/5",
                    help=score_help
                )

        st.markdown(text, unsafe_allow_html=True)

        if url:
            render_hyperlink(url, owner)
        
def _render_comment_thread(comment: dict) -> None:
    user = comment.get("user", "Onbekend")
    content = comment.get("content", "")

    with st.expander(user, icon="👤", expanded=True):
        st.write(content)

        # Render sub-replies recursively
        if replies := comment.get("replies", []):
            for reply in replies:
                _render_comment_thread(reply)

def render_comment_section(title: str,
                           comments: list[dict],
                           url: str = "",
                           owner: str = "Onbekend",
                           **kwargs) -> None:
    """
    Comment dict contains:
    - user: str
    - content: str
    - replies: list[dict] (optional)
    """
    with st.expander(title, expanded=False):
        if url:
            render_hyperlink(url, owner)

        for comment in comments:
            _render_comment_thread(comment)

def render_page_link(doc_name: str) -> None:
    path = Path(__file__).parent / "pages" / "docs" / doc_name

    if st.button("Hoe werkt de AI? 🔗", width="stretch"):
        st.switch_page(path)

def render_article_selector(options, key) -> None:    
    def format_func(option):
        max_length = 25
        if len(option) <= max_length:
            return option
        
        return option[:max_length-3] + "..."
    
    st.pills("Kies een artikel", options=options, format_func=format_func, key=key)

def render_popup_dialog(title: str,
                        text: str,
                        url: str = "",
                        owner: str = "Onbekend") -> None:
    @st.dialog(title, dismissible=True, width="medium")
    def _inner():
        st.write(text)

        if not url:
            return
        
        render_hyperlink(
            url=url,
            owner=owner
        )

    _inner()

# ==== Helper functions ====
def is_model_loaded(verbose: bool = True) -> bool:
    loaded = "pipe" in st.session_state and st.session_state.pipe is not None

    if not loaded and verbose:
        st.error("Language model not loaded. Please return to the main page to load the model.")

    return loaded