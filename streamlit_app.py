import streamlit as st

def main():
    welkom = st.Page("pages/welkom.py", title="Welkom", icon="👋")
    gewichtjes = st.Page("pages/gewichtjes.py", title="Gewichtjes", icon="⚓")
    dif = st.Page("pages/data_geïnformeerde_feedback.py", title="Data Geïnformeerde Feedback", icon="💬")
    aisv = st.Page("pages/artikelen_in_simpele_versies.py", title="Artikelen in Simpele Versies", icon="📰")
    test = st.Page("pages/test_pagina.py", title="Test Pagina", icon="🧪")

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