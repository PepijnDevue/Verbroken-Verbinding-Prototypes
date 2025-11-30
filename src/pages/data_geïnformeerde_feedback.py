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
with open("src/data/dgf.json", "r", encoding="utf-8") as f:
    ARTICLE_DATA: dict = json.load(f)

OUTPUT_FILE = Path("src/data/dgf_outputs_chatgpt.json")

NOTE_PROMPT = """
DOEL
Je analyseert één thread onder een nieuwsartikel (één hoofdcomment + alle replies). Je taak is uitsluitend te bepalen of er expliciete feedback aan de redactie over het artikel in staat.
HARDERE REGELS
- Alleen feedback opnemen die duidelijk gericht is op het artikel of de redactie.
- Reacties die een probleem beschrijven zonder het artikel te benoemen zijn geen feedback.
- Alleen als een gebruiker expliciet verwijst naar het artikel of iets dat de redactie heeft gedaan/nagelaten (titel, feit, bron, uitleg, fout, gemis) mag het meetellen.
- Geen interpretaties, geen afleidingen, geen pogingen intenties te raden.
- Als er geen expliciete verwijzing is naar het artikel of redactionele keuzes -> resultaat = "".
WERKWIJZE
1. Lees het artikel.
2. Lees de volledige thread.
3. Beantwoord alleen deze vraag:
Is er een reactie die expliciet de redactie aanspreekt?
4. Zo ja: vat dat kort en feitelijk samen.
5. Zo nee: geef een lege string.
OUTPUT (strikte JSON)
{
"beredeneer": "Korte uitleg waarom er wel/geen expliciete verwijzing naar het artikel of redactie is.",
"resultaat": "Samenvatting van de expliciete feedback, of ""."
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
        return {"error": "json_decode_error", "details": str(e), "response": response}

    return {"error": "no_valid_json_found", "response": response}    

def generate_with_retries(prompt: str, max_retries: int = 5) -> dict:
    output = {"error": "not_processed_yet"}
    iterations = 0

    while output.get("error") is not None and iterations < max_retries:
        response = hf_utils.generate(prompt)
        output = extract_json_from_response(response)
        iterations += 1

    if output.get("error") is not None:
        with st.expander(output.get("error")):
            st.text(output.get("details", "No details available."))
            st.text(output.get("response", "No response captured."))
        return {}

    return output

def process_comment_thread(comment: dict, article: str) -> dict:
    """Process a single comment thread and extract editorial feedback."""
    prompt = (
        NOTE_PROMPT
        .replace("{{PLAATS_HIER_DE_THREAD}}", json.dumps(comment))
        .replace("{{PLAATS_HIER_HET_ARTIKEL}}", article)
    )
    
    return generate_with_retries(prompt)


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

    return generate_with_retries(prompt, max_retries=10)

def display_feedback_report() -> None:
    # Read file
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        output_data = json.load(f)

    # Main report
    st.subheader("Feedback Rapport voor de Redactie")
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

    # Process comments
    if no_file: # or col2.button("Genereer"):
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

    display_feedback_report()

    # # Download file
    # with open(OUTPUT_FILE, "rb") as f:
    #     st.download_button(
    #         label="Download Resultaten",
    #         data=f,
    #         file_name=OUTPUT_FILE.name,
    #         mime="application/json"
    #     )
        

if __name__ == "__main__":
    main()
