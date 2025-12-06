import json
import streamlit as st
import src.streamlit_utils as st_utils
import src.huggingface_utils as hf_utils

# ---------- Constants & Data ----------
with open("src/data/veertjes.json", "r", encoding="utf-8") as f:
    ARTICLES = json.load(f)

# ---------- Session State Keys ----------
ARTICLE_KEY = "a_selected_article"

# ---------- Page Explanation ----------
PAGE_EXPLANATION = """Hier komt nog een uitleg over veertjes. Hier komt nog een uitleg over veertjes. Hier komt nog een uitleg over veertjes. Hier komt nog een uitleg over veertjes. Hier komt nog een uitleg over veertjes."""

# ---------- Main Page Logic ----------
def main() -> None:
    TITLES = [article.get("title", "Onbekend") for article in ARTICLES]

    _init_session_defaults()

    st_utils.render_page_header("Veertjes", PAGE_EXPLANATION)

    st_utils.render_article_selector(TITLES, ARTICLE_KEY)

    chosen_title = st.session_state[ARTICLE_KEY]
    ARTICLE = ARTICLES[TITLES.index(chosen_title)]

    # TODO: AI deel:
	# - Definieer de valencie van de tekst (0,1)
	# - Beoordeel de sentiment van titel en tekst afzonderlijk [-1,0,1]
    # - Onder het artikel expander met AI gedachten 
    # - Hoe heeft AI deze score bepaald?
    import random
    score = round(random.uniform(0, 5), 1)

    st_utils.render_article(
		**ARTICLE,
        render_score=True,
        score=score,
        score_label="Beladenheid",
        score_help="Het aantal veertjes geeft aan hoe emotioneel beladen het artikel is."
	)
	
    st.divider()
	
    st_utils.render_page_link("doc_veertjes.py")
	
# ---------- UI Helpers ----------
def _init_session_defaults() -> None:
	"""Initialiseer standaardkeuzes en staat voor artikel."""
	first_title = ARTICLES[0].get("title", "Onbekend")
	if ARTICLE_KEY not in st.session_state:
		st.session_state[ARTICLE_KEY] = first_title


if __name__ == "__main__":
	main()