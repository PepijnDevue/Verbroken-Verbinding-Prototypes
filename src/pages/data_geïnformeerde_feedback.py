import streamlit as st
import src.streamlit_utils as st_utils
import json

# TODO AI:
# Categoriseer reacties op verschillende soorten feedback en non-feedback.
# """
# Je bent een professionele en nauwkeurige assistent die één comment-thread (één hoofdreactie + alle bijbehorende replies) één voor één beoordeelt. Schrijf in het Nederlands. Volg strikt de instructies hieronder — de uitvoer moet Machine-parsebaar en eenduidig zijn.
# Doel
# Voor elke aangeleverde thread:
# Lees alleen de tekst van die thread (de hoofdreactie en alle directe replies).
# Beoordeel of de thread redactionele feedback bevat (feedback gericht op de redactie, journalistieke keuzes, kop, framing, bronnen, formulering, etc.).
# Als het redactionele feedback is: wijs exact één categorie toe uit de vaste lijst:
# titel, bias, onvolledig, bronkeuze, formulering, feitelijke fout, overig
# (kies de beste match; als meerdere van toepassing lijken, kies de meest dominante en licht kort toe waarom).
# Als het géén redactionele feedback is: antwoord met exact de string "geen-feedback" als categorie.
# Begin met een korte, neutrale samenvatting van de thread (1-3 zinnen).
# Geef daarna een korte beredenering waarin je concreet uitlegt welk(e) signaal/zin/argument in de thread leidde tot de categoriekeuze.
# Vereiste uitvoerformat (verplicht; géén extra tekst)
# Retourneer enkel geldige JSON met precies deze velden:
# {
#   "summary": "<korte samenvatting in het Nederlands>",
#   "reasoning": "<korte, feitelijke toelichting waarom die categorie gekozen is — citeer (kort) tekstfragmenten uit de thread als bewijs>",
#   "category": "<één van: titel | bias | onvolledig | bronkeuze | formulering | feitelijke fout | overig | geen-feedback>",
# }
# summary: max 2-3 zinnen, neutraal, geen oordeel.
# reasoning: 1-4 korte zinnen; zet exacte citaten tussen aanhalingstekens (max 25 woorden per citaat). Verbind de citaten met de gekozen categorie.
# category: één van de voorgeschreven labels of "geen-feedback".
# Klassificatieregels:
# titel: expliciete klachten over de kop of vergelijking in de kop.
# bias: aantijging van partijdigheid, politieke gekleurdheid, bevooroordeeldheid of onevenwichtige weergave van actoren.
# onvolledig: lezers noemen expliciet ontbrekende context, oorzaken of relevante feiten (“u vermeldt niet…”, “waar is …?”).
# bronkeuze: kritiek op gebruikte bronnen of gebrek aan bronnen.
# formulering: kritiek op taalgebruik, toon, leesbaarheid, te technisch of misleidende zinsbouw.
# feitelijke fout: lezer wijst op concrete onjuiste cijfers of aantoonbare fouten in feiten in het artikel (niet opinie).
# overig: redactionele feedback die niet in bovenstaande categorieën past maar duidelijk op de redactie gericht is.
# geen-feedback: discussie over inhoud, meningen, persoonlijke verhalen, kosten of beleid zonder verwijzing naar de redactie, kop, bronnen of journalistieke keuzes.
# Extra instructies:
# Als een thread zowel klachten over de kop als over onvolledigheid bevat: kies de meest expliciet aanwezige klacht (noem dit in reasoning).
# Gebruik alleen informatie uit de thread; maak geen aannames buiten de tekst.
# Wees bondig en feitelijk; vermijd retoriek en longform uitleg.
# Geef geen extra velden en geen extra tekst buiten het gevraagde JSON.
# Begin nu — behandel de aangeleverde thread en produceer alleen de gevraagde JSON.
# """
# Verzamel alle reacties per categorie, display ze, en schrijf een samenvatting die emotieneel neutraal is en de feedback concreet beschrijft.



# ---------- Constants & Data ----------
with open("src/reactions.json", "r", encoding="utf-8") as f:
    REACTIONS = json.load(f)

# ---------- Session State Keys ----------
ARTICLE_KEY = "dgf_selected_article"


# ---------- Main Page Logic ----------
def main() -> None:
    st.title("Data Geïnformeerde Feedback")
    
    st_utils.render_sidebar()

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
