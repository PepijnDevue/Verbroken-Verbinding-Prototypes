import streamlit as st
from pathlib import Path
import src.streamlit_utils as st_utils
import src.huggingface_utils as hf_utils

def main():
    base_dir = Path(__file__).parent.resolve()
    pages_dir = base_dir / "src" / "pages"

    # Interactive pages
    welkom = st.Page(str(pages_dir / "welkom.py"), title="Welkom", icon="👋")
    veertjes = st.Page(str(pages_dir / "veertjes.py"), title="Veertjes", icon="🪶")
    dif = st.Page(str(pages_dir / "data_geïnformeerde_feedback.py"), title="Data Geïnformeerde Feedback", icon="💬")
    lhmu = st.Page(str(pages_dir / "leg_het_me_uit_knop.py"), title="Leg Het Me Uit Knop", icon="📰")
    test = st.Page(str(pages_dir / "test_pagina.py"), title="Test Pagina", icon="🧪")
    
    # Documentation pages
    doc_veertjes = st.Page(str(pages_dir / "docs" / "doc_veertjes.py"), title="Veertjes", icon="📄")
    doc_dgf = st.Page(str(pages_dir / "docs" / "doc_data_geïnformeerde_feedback.py"), title="Data Geïnformeerde Feedback", icon="📄")
    doc_readme = st.Page(str(pages_dir / "docs" / "doc_readme.py"), title="README", icon="📄")

    pg = st.navigation(
        pages = {
            "Paginas": [welkom],
            "Prototypes": [veertjes, dif, lhmu],
            "Test": [test],
            "Documentatie": [doc_veertjes, doc_dgf, doc_readme]
        }, 
        expanded=True)

    # # UNCOMMENT THIS CODE TO RUN WEB APP WITH MODEL LOADED
    if not st_utils.is_model_loaded(verbose=False):
        hf_utils.load_model()

    pg.run()

if __name__ == "__main__":
    main()