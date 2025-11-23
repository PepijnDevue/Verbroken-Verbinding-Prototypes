import streamlit as st
import json

# TODO AI: 
# Loop door de reacties, noteer takeaways voor de redactie.
# Verzamel takeeways in tot een stuk constructieve feedback voor de redactie. 


# ---------- Constants & Data ----------
with open("src/reactions.json", "r", encoding="utf-8") as f:
    REACTIONS = json.load(f)

# ---------- Session State Keys ----------
ARTICLE_KEY = "dgf_selected_article"


# ---------- Main Page Logic ----------
def main() -> None:
    st.title("Data Geïnformeerde Feedback")
    
    _init_session_defaults()

    _render_article_selector()

    _display_data_analysis()

    _display_comments_expander()


# ---------- UI Helpers ----------
def _init_session_defaults() -> None:
    """Initialiseer standaardkeuzes voor artikel."""
    first_title = next(iter(REACTIONS))
    if ARTICLE_KEY not in st.session_state:
        st.session_state[ARTICLE_KEY] = first_title


def _render_article_selector() -> None:
    """Render article selector pills."""
    options = list(REACTIONS.keys())
    st.pills("Kies een artikel", options=options, key=ARTICLE_KEY)


def _display_data_analysis() -> None:
    """Display simple data science analysis of the comments."""
    selected_article = st.session_state[ARTICLE_KEY]
    article_data = REACTIONS[selected_article]
    
    st.subheader(selected_article)
    
    # Extract all reactions (including replies)
    all_reactions = _get_all_reactions(article_data["reactions"])
    
    # Calculate statistics
    total_reactions = len(all_reactions)
    avg_text_length = sum(len(r["text"]) for r in all_reactions) / total_reactions if total_reactions > 0 else 0
    reactions_with_replies = sum(1 for r in article_data["reactions"] if r["replies"])
    
    # Display metrics
    cols = st.columns(3)
    with cols[0]:
        st.metric("Totaal aantal reacties", total_reactions)
    with cols[1]:
        st.metric("Gemiddelde tekstlengte", f"{avg_text_length:.0f} karakters")
    with cols[2]:
        st.metric("Reacties met antwoorden", reactions_with_replies)


def _display_comments_expander() -> None:
    """Display all comments in JSON format in an expander."""
    selected_article = st.session_state[ARTICLE_KEY]
    article_reactions = REACTIONS[selected_article]["reactions"]
    
    with st.expander("Bekijk alle reacties", expanded=False):
        st.json(article_reactions)


def _get_all_reactions(reactions: list) -> list:
    """Recursively extract all reactions including nested replies."""
    all_reactions = []
    
    for reaction in reactions:
        all_reactions.append(reaction)
        if reaction.get("replies"):
            all_reactions.extend(_get_all_reactions(reaction["replies"]))
    
    return all_reactions


if __name__ == "__main__":
    main()
