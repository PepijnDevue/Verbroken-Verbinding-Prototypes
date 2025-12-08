import json
import streamlit as st
import src.streamlit_utils as st_utils
import src.huggingface_utils as hf_utils

# ---------- Prompts ----------
TITLE_PROMPT = """DOEL
Je bent een expert in sentimentanalyse van nieuwskoppen. Je taak is om de emotionele toon van een nieuwskop te beoordelen.
INSTRUCTIES
Beoordeel de volgende nieuwskop op sentiment:
- Score -1 voor negatief sentiment (slecht nieuws, negatieve emoties, problemen, conflicten)
- Score 0 voor neutraal sentiment (feitelijk, objectief, geen duidelijke emotionele lading)
- Score 1 voor positief sentiment (goed nieuws, positieve emoties, vooruitgang, successen)
WERKWIJZE
1. Lees de nieuwskop zorgvuldig.
2. Analyseer de gebruikte woorden, zinsstructuur en context.
3. Beredeneer welke emoties of toon de kop overbrengt.
4. Kies de score die het beste past bij de algehele toon van de kop.
5. Geef alleen de JSON terug met je beredenering en het resultaat, geen extra tekst.
OUTPUT_FORMAT
Geef je antwoord als JSON in exact dit formaat:
{
"beredeneer": "leg hier uit welke aspecten van de kop je hebt geanalyseerd en waarom je tot deze score komt",
"resultaat": 0
}
TITEL
<title> {{PLAATS_HIER_DE_TITEL}} </title>
OUTPUT"""

TEXT_PROMPT = """DOEL
Je bent een expert in sentimentanalyse van nieuwsartikelen. Je taak is om de emotionele toon van de volledige artikeltekst te beoordelen.
INSTRUCTIES
Beoordeel de volgende artikeltekst op sentiment:
- Score -1 voor negatief sentiment (slecht nieuws, negatieve emoties, problemen, conflicten, zorgen)
- Score 0 voor neutraal sentiment (feitelijk, objectief, balanced reporting, geen duidelijke emotionele lading)
- Score 1 voor positief sentiment (goed nieuws, positieve emoties, vooruitgang, successen, oplossingen)
WERKWIJZE
1. Lees de volledige artikeltekst zorgvuldig.
2. Analyseer de gebruikte woorden, toon, framing en context door het hele artikel.
3. Let op de balans tussen positieve en negatieve elementen in het artikel.
4. Beredeneer welke emoties of toon de tekst als geheel overbrengt.
5. Kies de score die het beste past bij het overheersende sentiment van het artikel.
6. Geef alleen de JSON terug met je beredenering en het resultaat, geen extra tekst.
OUTPUT_FORMAT
Geef je antwoord als JSON in exact dit formaat:
{
"beredeneer": "Werk je gedachtegang uit: wat valt je op in de tekst en hoe kom je tot je conclusie",
"resultaat": 0
}
BELANGRIJK: Schrijf je beredenering als doorlopende tekst zonder markdown opmaak. Gebruik gewone zinnen gescheiden door spaties. Dit waarborgt de JSON-integriteit en voorkomt parsing-fouten.
TEKST
<text> {{PLAATS_HIER_DE_TEKST}} </text>
OUTPUT"""

VALENCE_PROMPT = """DOEL
Je bent een expert in het analyseren van emotionele intensiteit (valentie) in nieuwsartikelen. Je taak is om te beoordelen of een artikel hoge valentie bevat op basis van twee specifieke criteria. Valentie meet de emotionele intensiteit, ongeacht of deze positief of negatief is.
INSTRUCTIES
Beoordeel of de artikeltekst hoge valentie bevat:
- Score 0 voor lage valentie (neutraal, weinig emotioneel geladen inhoud)
- Score 1 voor hoge valentie (sterk emotioneel geladen inhoud, zowel positief als negatief)

BELANGRIJK: Hoge valentie kan zowel positieve als negatieve emoties betreffen. Het gaat om de intensiteit en levendigheid van de beschrijving, niet om de richting (positief/negatief).

Valentie wordt bepaald door de aanwezigheid van minimaal één van deze twee elementen:

CRITERIUM 1: Gedetailleerde beschrijving met emotionele inhoud
- Worden er specifieke, gedetailleerde beschrijvingen gegeven van gebeurtenissen?
- Maken deze details het mogelijk voor de lezer om zich levendig in te beelden wat er gebeurde?
- Voorbeelden NEGATIEF: grafische details over geweld, nauwkeurige beschrijvingen van traumatische momenten, visuele details die angst of verdriet oproepen
- Voorbeelden POSITIEF: levendige beschrijvingen van vreugdevolle momenten, gedetailleerde weergave van emotionele herenigingen, visuele details die blijdschap of trots oproepen

CRITERIUM 2: Expressie van affect
- Worden er directe affectieve uitspraken gedaan door bronnen of betrokkenen?
- Worden emotionele toestanden expliciet beschreven?
- Voorbeelden NEGATIEF: "Ik dacht dat ik doodging", "Ik was doodsbang", "Het was verschrikkelijk"
- Voorbeelden POSITIEF: "Ik was zo ontzettend blij", "Het mooiste moment van mijn leven", "Ik voelde me overweldigd van geluk"

WERKWIJZE
1. Lees de volledige artikeltekst zorgvuldig.
2. Identificeer passages die voldoen aan criterium 1 (gedetailleerde beschrijvingen met emotionele lading, positief OF negatief).
3. Identificeer passages die voldoen aan criterium 2 (directe expressie van affect, positief OF negatief).
4. Beredeneer of minimaal één criterium duidelijk aanwezig is.
5. Score 1 als er sprake is van hoge valentie (één of beide criteria zijn aanwezig met sterke emotionele intensiteit), score 0 als beide criteria afwezig zijn.
6. Geef alleen de JSON terug met je beredenering en het resultaat, geen extra tekst.
OUTPUT_FORMAT
Geef je antwoord als JSON in exact dit formaat:
{
"beredeneer": "Werk je gedachtegang uit: wat valt je op in de tekst en hoe kom je tot je conclusie",
"resultaat": 0
}
BELANGRIJK: Schrijf je beredenering als doorlopende tekst zonder markdown opmaak. Gebruik gewone zinnen gescheiden door spaties. Dit waarborgt de JSON-integriteit en voorkomt parsing-fouten.
TEKST
<text> {{PLAATS_HIER_DE_TEKST}} </text>
OUTPUT"""

PROMPT = """DOEL
Je bent een expert in het scoren van nieuwsartikelen op emotionele zwaarte op een schaal van 0 tot 5.
Je taak is om nieuwsartikelen te analyseren en een score toe te kennen op basis van hun emotionele impact vanuit een Nederlands perspectief.

INSTRUCTIES
Lees het volledige artikel en analyseer de emotionele impact.
Geef je output in strikt JSON-formaat:
{\"beredeneer\": \"Uitleg van je analyse en score, dek alle aspecten kort\", \"resultaat\": score}

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
<title> {{PLAATS_HIER_DE_TITEL}} </title>
<text> {{PLAATS_HIER_HET_ARTIKEL}} </text>

OUTPUT"""

# ---------- Constants & Data ----------
with open("src/data/veertjes.json", "r", encoding="utf-8") as f:
    ARTICLES = json.load(f)

# ---------- Session State Keys ----------
ARTICLE_KEY = "a_selected_article"

# ---------- Page Explanation ----------
PAGE_EXPLANATION = """Hier komt nog een uitleg over veertjes. Hier komt nog een uitleg over veertjes. Hier komt nog een uitleg over veertjes. Hier komt nog een uitleg over veertjes. Hier komt nog een uitleg over veertjes."""

# ---
def rate_articles() -> None:
    with st.spinner("AI aan het denken..."):
        for article in ARTICLES:
            title = article.get("title", "Onbekend")
            text = article.get("text", "")
            
            # title_prompt_filled = TITLE_PROMPT.replace("{{PLAATS_HIER_DE_TITEL}}", title)
            # text_prompt_filled = TEXT_PROMPT.replace("{{PLAATS_HIER_DE_TEKST}}", text)
            # valence_prompt_filled = VALENCE_PROMPT.replace("{{PLAATS_HIER_DE_TEKST}}", text)

            # title_sentiment = hf_utils.generate_with_retries(title_prompt_filled)
            # text_sentiment = hf_utils.generate_with_retries(text_prompt_filled)
            # text_valence = hf_utils.generate_with_retries(valence_prompt_filled)

            # title_sentiment_score = title_sentiment.get("resultaat", -1000)
            # text_sentiment_score = text_sentiment.get("resultaat", -1000)
            # text_valence_score = text_valence.get("resultaat", -1000)
            # title_multiplier = 0.5
            # text_multiplier = 2

            # title_score = title_multiplier * title_sentiment_score
            # text_score = (1 - text_valence_score + text_multiplier * text_valence_score) * text_sentiment_score

            # score = -1 * (title_score + text_score) + 2.5

            # article.update({
            #     "analysis": {
            #         "title_sentiment": title_sentiment,
            #         "text_sentiment": text_sentiment,
            #         "valence": text_valence,
            #         "score": score
            #     }
            # })
            prompt_filled = PROMPT.replace("{{PLAATS_HIER_DE_TITEL}}", title).replace("{{PLAATS_HIER_HET_ARTIKEL}}", text)

            analysis = hf_utils.generate_with_retries(prompt_filled)

            article.update({"analysis": analysis})

        # write back to file
        with open("src/data/veertjes.json", "w", encoding="utf-8") as f:
            json.dump(ARTICLES, f, ensure_ascii=False, indent=4)

# ---------- Main Page Logic ----------
def main() -> None:
    TITLES = [article.get("title", "Onbekend") for article in ARTICLES]

    _init_session_defaults()

    st_utils.render_page_header("Veertjes", PAGE_EXPLANATION)

    st_utils.render_article_selector(TITLES, ARTICLE_KEY)

    chosen_title = st.session_state[ARTICLE_KEY]
    ARTICLE = ARTICLES[TITLES.index(chosen_title)]
    
    st_utils.render_article(
		**ARTICLE,
        render_score=True,
        score=ARTICLE.get("analysis", {}).get("score", -1234),
        score_label="Beladenheid",
        score_help="Het aantal veertjes geeft aan hoe emotioneel beladen het artikel is."
	)
	
    # UNCOMMENT THIS CODE TO ENABLE AI RATING BUTTON
    # if st.button("Beoordeel met AI"):
    #     rate_articles()

    with st.expander("Hoe heeft de AI deze score bepaald?"):
        analysis = ARTICLE.get("analysis", {})

        for header, content in analysis.get("beredeneer", {}).items():
            st.markdown(f"**{header.replace('_', ' ').title()}**:")
            st.write(content)

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