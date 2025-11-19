import streamlit as st
import src.streamlit_utils as st_utils
import json

# ---------- Constants & Data ----------
with open("src/articles.json", "r", encoding="utf-8") as f:
    ARTICLES = json.load(f)

# ---------- Session State Keys ----------
ARTICLE_KEY = "a_selected_article"
RATING_KEY = "a_difficulty_rating"


# ---------- Main Page Logic ----------
def main() -> None:
    st.title("Ankertjes")
	
    st_utils.render_sidebar()

    _init_session_defaults()

    _render_article_selector()

    _display_selected_article()


# ---------- UI Helpers ----------
def _init_session_defaults() -> None:
	"""Initialiseer standaardkeuzes en staat voor artikel."""
	first_title = next(iter(ARTICLES))
	if ARTICLE_KEY not in st.session_state:
		st.session_state[ARTICLE_KEY] = first_title


def _display_selected_article():
    selected_article = st.session_state[ARTICLE_KEY]

    # TODO: AI
    import random
    weight = round(random.uniform(0, 5), 1)
    whole_weight = round(weight)
    empty_weight = 5 - whole_weight

    cols = st.columns([4, 1, 1])

    with cols[0]:
        st.space("small")
        st.subheader(selected_article)
    
    with cols[1]:
        st.metric(
            label="Gewicht", 
            value=f"{weight:.1f}/5",
            help="Het aantal ankertjes geeft aan hoe emotioneel beladen het artikel is."   
        )

    with cols[2]:
        badge = f"**{whole_weight*'⚓'}{empty_weight*'⚓︎'}**"

        st.space("small")
        st.badge(
            label=badge,
            color="grey"
        )
    
    st.write(ARTICLES[selected_article])


def _render_article_selector() -> None:
    options = list(ARTICLES.keys())
    
    st.pills("Kies een artikel", options=options, key=ARTICLE_KEY)

if __name__ == "__main__":
	main()