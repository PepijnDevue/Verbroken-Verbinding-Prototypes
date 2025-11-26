import json
import re
from pathlib import Path
import streamlit as st
import src.huggingface_utils as hf_utils

# TODO AI:
# Loop door de reacties, noteer takeaways voor de redactie.
# Verzamel takeeways in tot een stuk constructieve feedback voor de redactie.

# ---------- Constants & Data ----------
with open("src/dgf_venlo.json", "r", encoding="utf-8") as f:
    ARTICLE_DATA: dict = json.load(f)

OUTPUT_FILE = Path("src/dgf_outputs.json")

NOTE_PROMPT = """
DOEL
Je analyseert één thread uit de reacties onder een nieuwsbericht. Een thread bestaat uit:
- één hoofdcomment
- alle reacties daaronder
Je taak: identificeer of er bruikbare lezersfeedback voor de redactie in deze thread staat. Zo ja: vat dit kort, feitelijk en constructief samen.
BELANGRIJK
- Negeer alle andere inhoud (discussies, meningen, politiek, off-topic).
- Focus alleen op concrete signalen die waardevol zijn voor een redactie (bijv. onduidelijkheden, fouten, gewenste verdieping, ontbrekende bronnen, toon, misleidende titels, etc.).
- Als er geen redactie-relevante feedback in de volledige thread staat, rapporteer een lege string.
WERKWIJZE
1. Lees de volledige thread.
2. Bepaal of er expliciet of impliciet feedback voor de redactie in voorkomt.
3. Als feedback aanwezig is: bundel het tot een kernachtige, constructieve samenvatting.
4. Als er geen feedback is: geef dat aan.
5. Denk eerst stap voor stap in een interne beredeneer-sectie.
6. Geef daarna alleen de JSON-output.
OUTPUT-FORMAT
Geef uitsluitend de volgende JSON-structuur:
{
    "beredeneer": "Korte, stap-voor-stap uitleg van je interne gedachten over hoe je tot het resultaat kwam.",
    "resultaat": "Constructieve samenvatting van de feedback, of: '' (lege string) als er geen feedback is."
}
INPUT
Hieronder staat één thread:
<thread>{{PLAATS_HIER_DE_THREAD}}</thread>
OUTPUT
"""

AGGREGATION_PROMPT = """
DOEL
Je ontvangt een lijst met individuele rauwe stukken feedback voor de nieuwsredactie.
Je taak is om alle aanwezige feedbackpunten te combineren tot één samenhangend, constructief redactierapport.
INHOUDSRICHTLIJNEN
Cluster gelijkaardige punten (bijv. titelproblemen, feitencontrole, ontbrekende context, toon, bronvermelding).
Vat dubbelingen samen.
Formuleer neutraal, professioneel, respectvol en zonder verwijtende toon.
Geef alleen punten die daadwerkelijk relevant zijn.
Geef geen namen, quotes of individuele commenters weer.
Geen verzinsels: alleen aggregatie van wat aanwezig is.
WERKWIJZE
Lees alle stukken feedback aandachtig door.
Groepeer en synthetiseer de feedback in hoofdcategorieën.
Formuleer de uiteindelijke samenvatting: helder, gestructureerd en kort.
Denk eerst stap-voor-stap in een beredeneer-sectie.
Geef daarna enkel de JSON-output.
OUTPUT-FORMAT
Geef uitsluitend dit JSON-schema:
{
    "beredeneer": "Korte, stap-voor-stap beschrijving hoe je de lijst hebt geanalyseerd en geherstructureerd.",
    "categorieën": "Lijst van de hoofdcategorieën van feedback die je hebt geïdentificeerd.",
    "feedback_rapport": "De uiteindelijke, geaggregeerde feedbacksamenvatting voor de redactie."
}
INPUT
Hieronder staat de lijst met JSON-resultaten:
<results>{{PLAATS_HIER_DE_RESULTATEN}}</results>
OUTPUT
"""


# ---------- Helper Functions ----------
def extract_json_from_response(response: str) -> dict:
    """Extract JSON from model response, handling potential markdown formatting."""
    # Try to find JSON in code blocks
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(1))
    
    # Try to find raw JSON
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(0))
    
    raise ValueError("No valid JSON found in response")


def process_comment_thread(comment: dict, pipe) -> dict:
    """Process a single comment thread and extract editorial feedback."""
    prompt = NOTE_PROMPT.replace("{{PLAATS_HIER_DE_THREAD}}", comment)
    
    response = hf_utils.generate(prompt, pipe)
    return extract_json_from_response(response)


def aggregate_feedback(results: list[dict], pipe) -> dict:
    """Aggregate all feedback results into a final report."""
    # Filter out empty results
    feedback_items = [r["resultaat"] for r in results if r.get("resultaat", "").strip()]
    
    if not feedback_items:
        return {
            "beredeneer": "Geen redactie-relevante feedback gevonden in de reacties.",
            "categorieën": [],
            "feedback_rapport": "Er is geen constructieve feedback voor de redactie geïdentificeerd in de reacties."
        }
    
    results_json = json.dumps(results, ensure_ascii=False, indent=2)
    prompt = AGGREGATION_PROMPT.replace("{{PLAATS_HIER_DE_RESULTATEN}}", results_json)
    
    response = hf_utils.generate(prompt, pipe)
    return extract_json_from_response(response)


# ---------- Main Page ----------
def main() -> None:
    title: str = ARTICLE_DATA.get("title", "Artikel")
    article_text: str = ARTICLE_DATA.get("text", "")
    comments: list[dict] = ARTICLE_DATA.get("comments", [])

    st.title("Data-geïnformeerde Feedback")
    st.header(title)
    st.markdown(article_text)

    with st.expander("Bekijk alle reacties", expanded=False):
        st.json(comments)

    st.divider()
    
    # Check if model is loaded
    if "pipe" not in st.session_state or st.session_state.pipe is None:
        st.error("Language model not loaded. Please return to the main page to load the model.")
        return
    
    # Process comments
    with st.spinner("Verwerken van reacties..."):
        try:
            # Process each comment thread
            all_results = []
            progress_bar = st.progress(0)
            
            for idx, comment in enumerate(comments):
                st.text(f"Verwerken van reactie {idx + 1}/{len(comments)}...")
                result = process_comment_thread(comment, st.session_state.pipe)
                all_results.append(result)
                progress_bar.progress((idx + 1) / len(comments))
            
            # Aggregate feedback
            st.text("Aggregeren van feedback...")
            aggregated = aggregate_feedback(all_results, st.session_state.pipe)
            
            # Save results
            output_data = {
                "individual_results": all_results,
                "aggregated_feedback": aggregated
            }
            
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            st.success(f"Analyse voltooid! Resultaten opgeslagen in {OUTPUT_FILE}")
            
            # Display aggregated feedback
            st.subheader("Feedback Rapport voor de Redactie")
            st.markdown(aggregated.get("feedback_rapport", "Geen feedback beschikbaar."))
            
            with st.expander("Geïdentificeerde categorieën"):
                st.write(aggregated.get("categorieën", []))
            
            with st.expander("Redenering"):
                st.write(aggregated.get("beredeneer", ""))
            
            with st.expander("Alle individuele resultaten"):
                st.json(all_results)
                
        except Exception as e:
            st.error(f"Fout bij verwerken: {str(e)}")
            st.exception(e)
    
    # todo : load file if exists, otherwise process and save


if __name__ == "__main__":
    main()
