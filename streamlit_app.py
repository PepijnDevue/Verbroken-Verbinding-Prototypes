import streamlit as st

def main():
    welkom = st.Page("src/pages/welkom.py", title="Welkom", icon="👋")
    gewichtjes = st.Page("src/pages/gewichtjes.py", title="Gewichtjes", icon="⚓")
    dif = st.Page("src/pages/data_geïnformeerde_feedback.py", title="Data Geïnformeerde Feedback", icon="💬")
    aisv = st.Page("src/pages/artikelen_in_simpele_versies.py", title="Artikelen in Simpele Versies", icon="📰")
    test = st.Page("src/pages/test_pagina.py", title="Test Pagina", icon="🧪")

    pg = st.navigation(
        pages = {
            "Paginas": [welkom],
            "Concepten": [gewichtjes, dif, aisv],
            "Test": [test]
        }, 
        expanded=True)

    pg.run()

if __name__ == "__main__":
    main()