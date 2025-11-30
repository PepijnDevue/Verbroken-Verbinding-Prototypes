import json
import re
from pathlib import Path
import streamlit as st
import src.huggingface_utils as hf_utils
import src.streamlit_utils as st_utils

# TODO AI:
# Loop door de reacties, noteer takeaways voor de redactie.
# Verzamel takeeways in tot een stuk constructieve feedback voor de redactie.

# ---------- Constants & Data ----------
with open("src/dgf_venlo.json", "r", encoding="utf-8") as f:
    ARTICLE_DATA: dict = json.load(f)

OUTPUT_FILE = Path("src/dgf_outputs.json")

NOTE_PROMPT = """
DOEL
Je analyseert één thread onder een nieuwsartikel (één hoofdcomment + alle replies). Identificeer of er bruikbare, redactie-gerichte lezersfeedback in de thread staat. Alleen expliciet gegeven feedback moet worden vastgelegd; neem impliciete opmerkingen alleen mee als ze duidelijk en direct als suggestie/klacht aan de redactie zijn geformuleerd.
BELANGRIJK — richtlijnen
- Gebruik de artikeltekst als context; negeer alles wat niet direct relevant is (lange discussies, algemene meningen, off-topic).
- Sla alleen feedback op die de gebruiker expliciet aan de redactie richt (bv. “de titel is misleidend”, “controleer deze bron”, “meer uitleg over X graag”, “fout in regel Y”).
- Impliciete signalen: neem die alleen op als ze eenduidig actiegericht en concreet zijn (bv. “dit klopt niet” gevolgd door een concreet punt). Vermijd inferenties over intentie of sentiment.
- Focus op concrete, redactie-bruikbare punten: fouten, onnauwkeurigheden, ontbrekende bronnen, onduidelijkheid, gewenste verdieping, toon/titels, feitelijke correcties, navraag naar bronnen.
WERKWIJZE
1. Lees eerst de artikeltekst.
2. Lees daarna de volledige thread.
3. Bepaal of er expliciete redactie-feedback aanwezig is. (Als je alleen vage meningen of discussie ziet: geen feedback.)
4. Als er feedback is: formuleer één korte, feitelijke en constructieve samenvatting.
5. Als er geen redactie-relevante feedback is: geef een lege string.
6. Geef een kort beslissingsoverzicht (max. 2 zinnen) waarin je feitelijk beschrijft welke signalen je als feedback hebt gezien en waarom je ze wel/niet meeneemt. Geen interne redenering of chain-of-thought.
OUTPUT — strikt JSON
Geef alleen de volgende JSON-structuur (én niets anders):
{
"beredeneer": "Kort beslissingsoverzicht (max. 2 zinnen). Geen interne chain-of-thought.",
"resultaat": "Constructieve samenvatting van de expliciete redactie-feedback, of: "" (lege string) als er geen concrete feedback is."
}
ARTICLE
<article> {{PLAATS_HIER_HET_ARTIKEL}} </article>
INPUT
Hieronder staat één thread:
<thread>
{{PLAATS_HIER_DE_THREAD}}
</thread>
OUTPUT
"""

AGGREGATION_PROMPT = """
DOEL
Je ontvangt een lijst met JSON-objecten die per thread samengevatte feedback bevatten.
Je taak is om alle aanwezige feedbackpunten te combineren tot één samenhangend, constructief en professioneel redactierapport.
INHOUDSRICHTLIJNEN
- Lees de artikeltekst als context voor interpretatie.
- Gebruik alle feedback die niet leeg is.
- Cluster gelijkaardige punten (bijv. titelproblemen, feitencontrole, ontbrekende context, bronnen, toon).
- Vermijd herhaling en bundel dubbele signalen.
- Formuleer neutraal, professioneel en agressieloos.
- Geen namen, geen quotes, geen verzonnen punten.
WERKWIJZE
1. Lees eerst de artikeltekst.
2. Lees alle JSON-items.
3. Extraheer alle niet-lege 'resultaat'-velden.
4. Groepeer en synthetiseer alle feedback in logische categorieën.
5. Formuleer een geordende, constructieve eindrapportage.
6. Denk eerst stap voor stap in een 'beredeneer'-sectie.
7. Geef daarna alleen de JSON-output.
OUTPUT
Geef uitsluitend dit JSON-schema:
{
    "beredeneer": "Korte, stap-voor-stap beschrijving hoe je de lijst hebt geanalyseerd en geherstructureerd. En welke onderwerpen je bent tegengekomen.",
    "samenvatting": "Geclusterde en geordende feedback in neutrale, professionele toon."
}
ARTICLE
<article>
{{PLAATS_HIER_HET_ARTIKEL}}
</article>
INPUT
Hieronder staat de lijst met JSON-resultaten:
<results>
{{PLAATS_HIER_DE_RESULTATEN}}
</results>
OUTPUT
"""


# ---------- Helper Functions ----------
def extract_json_from_response(response: str, keyword: str = ">\nOUTPUT") -> dict:
    """Extract JSON from model response, handling potential markdown formatting."""
    # Remove any leading text before the keyword (incl)
    keyword_idx = response.find(keyword)
    output = response[keyword_idx + len(keyword):]

    try:
        # Try to find JSON in code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', output, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        
        # Try to find raw JSON
        json_match = re.search(r'\{.*\}', output, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
    except json.JSONDecodeError as e:
        with st.expander("JSON Decode Error Details"):
            st.write(f"Fout bij het decoderen van JSON: {e}")
            st.write("Volledige response:")
            st.write(response)
        return {}
    
    with st.expander("Geen geldige JSON gevonden"):
        st.write("Volledige response:")
        st.write(response)
        return {}

def process_comment_thread(comment: dict, article: str) -> dict:
    """Process a single comment thread and extract editorial feedback."""
    prompt = (
        NOTE_PROMPT
        .replace("{{PLAATS_HIER_DE_THREAD}}", json.dumps(comment))
        .replace("{{PLAATS_HIER_HET_ARTIKEL}}", article)
    )
    
    response = hf_utils.generate(prompt)

    return extract_json_from_response(response)


def aggregate_feedback(results: list[str], article: str) -> dict:
    """Aggregate all feedback results into a final report."""
    if not results:
        return {
            "beredeneer": "Geen redactie-relevante feedback gevonden in de reacties.",
            "categorieën": [],
            "feedback_rapport": "Er is geen constructieve feedback voor de redactie geïdentificeerd in de reacties."
        }
    
    prompt = (
        AGGREGATION_PROMPT
        .replace("{{PLAATS_HIER_DE_RESULTATEN}}", json.dumps(results))
        .replace("{{PLAATS_HIER_HET_ARTIKEL}}", article)
    )
    
    response = hf_utils.generate(prompt)
    return extract_json_from_response(response)

def display_feedback_report(col1) -> None:
    # Read file
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        output_data = json.load(f)

    # Main report
    col1.subheader("Feedback Rapport voor de Redactie")
    st.text(output_data.get("aggregated_feedback", {}).get("samenvatting", "Geen feedback beschikbaar."))

    # Extra details
    with st.expander("Geänalyseerde Reacties"):
        st.json(output_data.get("individual_results", []))


# ---------- Main Page ----------
def main() -> None:
    title: str = ARTICLE_DATA.get("title", "Artikel")
    article_text: str = ARTICLE_DATA.get("text", "")
    comments: list[dict] = ARTICLE_DATA.get("comments", [])

    st.title("Data-geïnformeerde Feedback")
    st.subheader(title)
    st.write(article_text)

    with st.expander("Bekijk alle reacties", expanded=False):
        st.json(comments)

    st.divider()
    
    # Check if model is loaded
    if not st_utils.is_model_loaded():
        return
    
    no_file = not OUTPUT_FILE.exists()

    col1, col2 = st.columns([5, 1])

    # Process comments button
    if no_file or col2.button("Genereer"):
        with st.spinner("Verwerken van reacties..."):
            # Process each comment thread
            all_results = []
            progress_bar = st.progress(0)
            
            for idx, comment in enumerate(comments):
                result = process_comment_thread(comment, article_text)
                all_results.append(result)
                progress_bar.progress((idx + 1) / len(comments))
            
            extracted_feedbacks = [r.get("resultaat", "") for r in all_results if isinstance(r, dict) and r.get("resultaat", "").strip()]

            # Aggregate feedback
            st.text("Aggregeren van feedback...")
            aggregated = aggregate_feedback(extracted_feedbacks, article_text)
            
            # Save results
            output_data = {
                "individual_results": all_results,
                "aggregated_feedback": aggregated
            }
            
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            st.success(f"Analyse voltooid! Resultaten opgeslagen in {OUTPUT_FILE}")

    display_feedback_report(col1)

    # Download file
    with open(OUTPUT_FILE, "rb") as f:
        st.download_button(
            label="Download Resultaten",
            data=f,
            file_name=OUTPUT_FILE.name,
            mime="application/json"
        )
        

if __name__ == "__main__":
    main()
