import streamlit as st
from pathlib import Path
import src.streamlit_utils as st_utils
import src.huggingface_utils as hf_utils

def main():
    base_dir = Path(__file__).parent.resolve()
    pages_dir = base_dir / "src" / "pages"

    # Interactive pages
    welkom = st.Page(str(pages_dir / "welkom.py"), title="Welkom", icon="👋")
    gw = st.Page(str(pages_dir / "gevoelswaarde.py"), title="Gevoelswaarde", icon="🪶")
    rs = st.Page(str(pages_dir / "reactiesamenvatter.py"), title="Reactiesamenvatter", icon="💬")
    uk = st.Page(str(pages_dir / "uitlegknop.py"), title="Uitlegknop", icon="📰")
    
    # Documentation pages
    doc_gevoelswaarde = st.Page(str(pages_dir / "docs" / "doc_gevoelswaarde.py"), title="Gevoelswaarde", icon="📄")
    doc_rs = st.Page(str(pages_dir / "docs" / "doc_reactiesamenvatter.py"), title="Reactiesamenvatter", icon="📄")
    doc_uk = st.Page(str(pages_dir / "docs" / "doc_uitlegknop.py"), title="Uitlegknop", icon="📄")
    doc_vo = st.Page(str(pages_dir / "docs" / "doc_voor_ontwikkelaars.py"), title="Voor Ontwikkelaars", icon="⚙️")

    pg = st.navigation(
        pages = {
            "Paginas": [welkom],
            "Prototypes": [gw, rs, uk],
            "Documentatie": [doc_gevoelswaarde, doc_rs, doc_uk, doc_vo],
        }, 
        expanded=True)

    # # UNCOMMENT THIS CODE TO RUN WEB APP WITH MODEL LOADED
    # if not st_utils.is_model_loaded(verbose=False):
    #     hf_utils.load_model()

    pg.run()

if __name__ == "__main__":
    main()