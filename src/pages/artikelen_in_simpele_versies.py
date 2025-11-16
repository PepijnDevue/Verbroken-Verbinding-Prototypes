import streamlit as st
import src.streamlit_utils as st_utils
import json

# ---------- Constants & Data ----------
with open("src/articles.json", "r", encoding="utf-8") as f:
    ARTICLES = json.load(f)

# ---------- Session State Keys ----------
ARTICLE_KEY = "aiv_selected_article"
RATING_KEY = "aiv_difficulty_rating"


# ---------- Main Page Logic ----------
def main() -> None:
    st.title("Artikelen in Simpele Versies")
	
    st_utils.render_sidebar()

    _init_session_defaults()

    _render_input_bar()

    _display_selected_article()


# ---------- UI Helpers ----------
def _init_session_defaults() -> None:
	"""Initialiseer standaardkeuzes en staat voor artikel en rating."""
	first_title = next(iter(ARTICLES))
	if ARTICLE_KEY not in st.session_state:
		st.session_state[ARTICLE_KEY] = first_title
	if RATING_KEY not in st.session_state:
		st.session_state[RATING_KEY] = 5


def _display_selected_article():
    selected_article = st.session_state[ARTICLE_KEY]

    # TODO: AI
    st.subheader(selected_article)
    st.write(ARTICLES[selected_article])


def _render_input_bar() -> None:
    cols = st.columns([2, 1])
	
    # Article selector
    with cols[0]:
        options = list(ARTICLES.keys())
		
        st.pills("Kies een artikel", options=options, key=ARTICLE_KEY)
			
    # Difficulty selector
    with cols[1]:
        st.segmented_control(
            "Complexiteit",
            [1, 2, 3, 4, 5],
            key=RATING_KEY,
            default=5,
			help="Kies hoe complex de tekst mag zijn (1 = Meest versimpeld, 5 = Origineel)"
        )

if __name__ == "__main__":
	main()