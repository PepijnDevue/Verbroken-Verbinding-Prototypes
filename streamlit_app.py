import streamlit as st
from pathlib import Path
import src.huggingface_utils as hf_utils
import src.streamlit_utils as st_utils

def main():
    base_dir = Path(__file__).parent.resolve()
    pages_dir = base_dir / "src" / "pages"

    # Interactive pages
    welkom = st.Page(str(pages_dir / "welkom.py"), title="Welkom", icon="👋")
    ankertjes = st.Page(str(pages_dir / "ankertjes.py"), title="Ankertjes", icon="⚓")
    dif = st.Page(str(pages_dir / "data_geïnformeerde_feedback.py"), title="Data Geïnformeerde Feedback", icon="💬")
    lhmu = st.Page(str(pages_dir / "leg_het_me_uit_knop.py"), title="Leg Het Me Uit Knop", icon="📰")
    test = st.Page(str(pages_dir / "test_pagina.py"), title="Test Pagina", icon="🧪")
    
    # Documentation pages
    doc_ankertjes = st.Page(str(pages_dir / "doc_ankertjes.py"), title="Ankertjes", icon="📄")
    doc_dgf = st.Page(str(pages_dir / "doc_data_geinformeerde_feedback.py"), title="Data Geïnformeerde Feedback", icon="📄")
    doc_readme = st.Page(str(pages_dir / "doc_readme.py"), title="README", icon="📄")

    pg = st.navigation(
        pages = {
            "Paginas": [welkom],
            "Concepten": [ankertjes, dif, lhmu],
            "Test": [test],
            "Documentatie": [doc_ankertjes, doc_dgf, doc_readme]
        }, 
        expanded=True)

    # CSS to collapse the "Documentatie" section by default
    st.markdown(
        """
        <style>
        /* Target the last navigation section (Documentatie) */
        [data-testid="stSidebarNav"] ul:last-child details {
            open: false;
        }
        [data-testid="stSidebarNav"] ul:last-child details[open] {
            /* Keep it functional when user clicks */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Ensure the default model is loaded once per session
    if not st_utils.is_model_loaded(verbose=False):
        hf_utils.load_model()

    pg.run()

if __name__ == "__main__":
    main()