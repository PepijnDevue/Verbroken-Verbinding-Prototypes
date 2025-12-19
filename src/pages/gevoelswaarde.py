import json
import streamlit as st
import src.streamlit_utils as st_utils
import src.huggingface_utils as hf_utils

# ---------- Prompts ----------
PROMPT = """DOEL
Je bent een expert in het scoren van nieuwsartikelen op emotionele zwaarte op een schaal van 0 tot 5.
Je taak is om nieuwsartikelen te analyseren en een score toe te kennen op basis van hun emotionele impact vanuit een Nederlands perspectief.

INSTRUCTIES
Lees het volledige artikel en analyseer de emotionele impact.
Geef een uitleg van je analyse en score, dek alle aspecten kort. Schrijf dit onder BEREDENEER.
Geef daarna alleen de score als een getal tussen 0 en 5 onder SCORE.

SCHAAL
0-0.5: POSITIEF - Vreugde, trots, inspiratie. Emotionele woorden, succesverhalen, menselijke veerkracht.
1.0: NEUTRAAL - Zakelijk, feitelijk, geen emotie. Geen persoonlijke verhalen of betrokkenheid.
2.0: LICHT NEGATIEF - Beperkte zorgen, zakelijke toon, weinig details, lage nabijheid.
3.0: MATIG ZWAAR - Duidelijk menselijk leed, persoonlijke verhalen, emotionele quotes, identificeerbare slachtoffers.
4.0: ZWAAR - Ernstige tragedies, schokkende details, sterke emotionele taal, impact op gemeenschappen.
5.0: EXTREEM - Extreme wreedheid/massa slachtoffers, overweldigend leed, traumatische details.

FACTOREN
Inhoud: Objectieve ernst (slachtoffers, schade, maatschappelijke impact).
Type gebeurtenis: Zwaarder (kinderen, geweld tegen groepen, misbruik, massa ongelukken, moord, systemisch falen). Lichter (politiek, economie, verkeersongelukken, natuurrampen zonder leed).
Presentatie: Emotionele woorden, persoonlijke details, quotes betrokkenen, visualiseerbare beschrijvingen = zwaarder.
Nabijheid: Nederland/Nederlanders/herkenbaar = zwaarder. Ver weg/vreemd = lichter (tenzij extreem).

REGELS
Emotionele presentatie weegt het zwaarst, ook bij mindere ernst.
Acute crisis is zwaarder dan chronisch probleem.
Kinderen altijd +0.5 tot +1 zwaarder.
Gebruik halve punten voor nuance.

ARTIKEL
{{PLAATS_HIER_DE_TITEL}}
{{PLAATS_HIER_HET_ARTIKEL}}

BEREDENEER
"""


# ---------- Constants & Data ----------
with open("src/data/gevoelswaarde.json", "r", encoding="utf-8") as f:
    ARTICLES = json.load(f)

ARTICLE_KEY = "selected_article"
TITLES = [article.get("title", "Onbekend") for article in ARTICLES]

PAGE_EXPLANATION = """Hier komt nog een uitleg over veertjes. Hier komt nog een uitleg over veertjes. Hier komt nog een uitleg over veertjes. Hier komt nog een uitleg over veertjes. Hier komt nog een uitleg over veertjes."""


# ---------- Helper Functions ----------
def _init_session_defaults() -> None:
	"""Initialiseer standaardkeuzes en staat voor artikel."""
	first_title = ARTICLES[0].get("title", "Onbekend")
	if ARTICLE_KEY not in st.session_state:
		st.session_state[ARTICLE_KEY] = first_title


def rate_articles() -> None:
    if not st_utils.is_model_loaded(verbose=False):
        return
    
    if not st.button("Beoordeel artikelen op gevoelswaarde"):
        return

    with st.spinner("AI aan het denken..."):
        for article in ARTICLES:
            title = article.get("title", "Onbekend")
            text = article.get("text", "")
            
            prompt_filled = PROMPT.replace("{{PLAATS_HIER_DE_TITEL}}", title)
            prompt_filled = prompt_filled.replace("{{PLAATS_HIER_HET_ARTIKEL}}", text)

            analysis = hf_utils.generate_with_retries(prompt_filled, result_str="SCORE")

            article.update({"analysis": analysis})

        # write back to file
        with open("src/data/gevoelswaarde.json", "w", encoding="utf-8") as f:
            json.dump(ARTICLES, f, ensure_ascii=False, indent=4)


# ---------- Main Page Logic ----------
def main() -> None:
    _init_session_defaults()

    st_utils.render_page_header("Gevoelswaarde", PAGE_EXPLANATION)

    st_utils.render_article_selector(TITLES, ARTICLE_KEY)

    chosen_title = st.session_state[ARTICLE_KEY]
    ARTICLE = ARTICLES[TITLES.index(chosen_title)]
    
    rate_articles()

    st_utils.render_article(
		**ARTICLE,
        render_score=True,
        score=ARTICLE.get("analysis", {}).get("score", -1234),
        score_label="Beladenheid",
        score_help="De score geeft aan hoe emotioneel beladen het artikel is."
	)

    with st.expander("Hoe heeft de AI deze score bepaald?"):
        analysis = ARTICLE.get("analysis", {})

        for header, content in analysis.get("beredeneer", {}).items():
            st.markdown(f"**{header.replace('_', ' ').title()}**:")
            st.write(content)

    st.divider()
	
    st_utils.render_page_link("doc_gevoelswaarde.py")


if __name__ == "__main__":
	main()