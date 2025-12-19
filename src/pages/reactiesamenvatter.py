import json
from pathlib import Path
import streamlit as st
import src.huggingface_utils as hf_utils
import src.streamlit_utils as st_utils


# ---------- Prompts ----------
NOTE_PROMPT = """DOEL
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
OUTPUT"""

AGGREGATION_PROMPT = """DOEL
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
5. Maak een korte, stap-voor-stap beschrijving hoe je de lijst hebt geanalyseerd en geherstructureerd. En welke onderwerpen je bent tegengekomen. Schrijf dit onder BEREDENEER.
6. Formuleer een geclusterde, geordende, en constructieve feedbackrapportage in neutrale, professionele toon. Schrijf dit onder SAMENVATTING.

ARTICLE
{{PLAATS_HIER_HET_ARTIKEL}}

INPUT
{{PLAATS_HIER_DE_RESULTATEN}}

BEREDENEER
"""


# ---------- Constants & Data ----------
with open("src/data/reactiesamenvatter.json", "r", encoding="utf-8") as f:
    ARTICLE: dict = json.load(f)

ARTICLE_TEXT = ARTICLE.get("text", "")
COMMENT_SECTION = ARTICLE.get("comment_section", {})
COMMENTS = COMMENT_SECTION.get("comments", [])

OUTPUT_FILE = Path("src/data/reactiesamenvatter_outputs.json")

PAGE_EXPLANATION = """Hier komt nog een uitleg over wat deze pagina doet en hoe het werkt. Hier komt nog een uitleg over wat deze pagina doet en hoe het werkt. Hier komt nog een uitleg over wat deze pagina doet en hoe het werkt. Hier komt nog een uitleg over wat deze pagina doet en hoe het werkt."""


# ---------- Helper Functions ----------
def process_comment_threads(comments: list[dict], article: str) -> list[dict]:
    """Process all comment threads and extract editorial feedback from each."""
    results = []
    
    for comment in comments:
        prompt = (
            NOTE_PROMPT
            .replace("{{PLAATS_HIER_DE_THREAD}}", json.dumps(comment))
            .replace("{{PLAATS_HIER_HET_ARTIKEL}}", article)
        )
        result = hf_utils.generate_with_retries(prompt)
        results.append(result)
    
    return results


def extract_feedback_strings(results: list[dict]) -> list[str]:
    """Extract non-empty feedback strings from processing results."""
    extracted_feedbacks = []
    
    for result in results:
        if not isinstance(result, dict):
            continue

        feedback = result.get("resultaat", "")

        if not feedback.strip():
            continue

        extracted_feedbacks.append(feedback)
    
    return extracted_feedbacks


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

    return hf_utils.generate_with_retries(prompt, 
                                          result_str="SAMENVATTING",
                                          max_retries=10)


def display_feedback_report() -> None:
    """Display the aggregated feedback report if available."""
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        output_data = json.load(f)

    aggregated_feedback = output_data.get("aggregated_feedback", {})

    # Main report
    st.subheader("Feedback Rapport voor de Redactie")
    st.write(aggregated_feedback.get("samenvatting", "Geen feedback beschikbaar."))

    # Extra details
    with st.expander("Wat is de gedachtengang van de AI?"):
        st.write(aggregated_feedback.get("beredeneer", "Geen gedachtengang beschikbaar."))


def process_article_feedback() -> None:
    """Process all comments to extract and aggregate editorial feedback."""
    # Stop if model not loaded
    if not st_utils.is_model_loaded(verbose=False):
        return

    # Stop if already processed
    if OUTPUT_FILE.exists() and not st.button("Analyseer reacties"):
        return

    with st.spinner("Verwerken van reacties..."):
        all_results = process_comment_threads(COMMENTS, ARTICLE_TEXT)

        extracted_feedbacks = extract_feedback_strings(all_results)

        aggregated = aggregate_feedback(extracted_feedbacks, ARTICLE_TEXT)
        
        # Save results
        output_data = {
            "individual_results": all_results,
            "aggregated_feedback": aggregated
        }
        
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)


# ---------- Main Page ----------
def main() -> None:
    st_utils.render_page_header("Reactiesamenvatter", PAGE_EXPLANATION)

    st_utils.render_article(**ARTICLE)

    process_article_feedback()
    display_feedback_report()

    st_utils.render_comment_section(title="Wat zijn de reacties?", **COMMENT_SECTION)

    st.divider()

    st_utils.render_page_link("doc_reactiesamenvatter.py")


if __name__ == "__main__":
    main()
