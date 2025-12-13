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
    dgf = st.Page(str(pages_dir / "data_geïnformeerde_feedback.py"), title="Data Geïnformeerde Feedback", icon="💬")
    lhmu = st.Page(str(pages_dir / "leg_het_me_uit_knop.py"), title="Leg Het Me Uit Knop", icon="📰")
    
    # Documentation pages
    doc_veertjes = st.Page(str(pages_dir / "docs" / "doc_veertjes.py"), title="Veertjes", icon="📄")
    doc_dgf = st.Page(str(pages_dir / "docs" / "doc_data_geïnformeerde_feedback.py"), title="Data Geïnformeerde Feedback", icon="📄")
    doc_lhmu = st.Page(str(pages_dir / "docs" / "doc_leg_het_me_uit_knop.py"), title="Leg Het Me Uit Knop", icon="📄")
    doc_vo = st.Page(str(pages_dir / "docs" / "doc_voor_ontwikkelaars.py"), title="Voor Ontwikkelaars", icon="⚙️")

    pg = st.navigation(
        pages = {
            "Paginas": [welkom],
            "Prototypes": [veertjes, dgf, lhmu],
            "Documentatie": [doc_veertjes, doc_dgf, doc_lhmu, doc_vo],
        }, 
        expanded=True)

    # # UNCOMMENT THIS CODE TO RUN WEB APP WITH MODEL LOADED
    # if not st_utils.is_model_loaded(verbose=False):
    #     hf_utils.load_model()

    pg.run()

if __name__ == "__main__":
    main()