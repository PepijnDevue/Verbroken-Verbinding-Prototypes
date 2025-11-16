import streamlit as st
from pathlib import Path

def main():
    base_dir = Path(__file__).parent.resolve()
    pages_dir = base_dir / "src" / "pages"

    welkom = st.Page(str(pages_dir / "welkom.py"), title="Welkom", icon="👋")
    ankertjes = st.Page(str(pages_dir / "ankertjes.py"), title="Ankertjes", icon="⚓")
    dif = st.Page(str(pages_dir / "data_geïnformeerde_feedback.py"), title="Data Geïnformeerde Feedback", icon="💬")
    aisv = st.Page(str(pages_dir / "artikelen_in_simpele_versies.py"), title="Artikelen in Simpele Versies", icon="📰")
    test = st.Page(str(pages_dir / "test_pagina.py"), title="Test Pagina", icon="🧪")

    pg = st.navigation(
        pages = {
            "Paginas": [welkom],
            "Concepten": [ankertjes, dif, aisv],
            "Test": [test]
        }, 
        expanded=True)

    pg.run()

if __name__ == "__main__":
    main()