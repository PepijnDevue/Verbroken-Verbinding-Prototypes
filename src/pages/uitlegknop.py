import streamlit as st
import json
import src.streamlit_utils as st_utils
import src.huggingface_utils as hf_utils


# ---------- Prompt ----------
PROMPT = """Je bent een expert in het uitleggen van nieuwsartikelen en de grotere context daaromheen.
Je taak is om een begrijpelijke uitleg te geven van het gegeven artikel, zodat een gemiddelde lezer de inhoud en context beter kan begrijpen.
Meestal is er een nieuw artikel toegevoegd aan een bestaand dossier. Dan vernieuw je de huidige uitleg met de nieuwe informatie.
Je verwerkt alleen de korte noddige informatie uit de artikelen, geen quotes of details. Je verwerkt alle nieuwe informatie uit het nieuwe artikel, zo is de lezer helemaal op de hoogte.

INSTRUCTIES
1. Lees eerst de HUIDIGE UITLEG goed door.
2. Lees daarna het NIEUWE ARTIKEL aandachtig.
3. Bedenk welke nieuwe informatie uit het NIEUWE ARTIKEL belangrijk is voor de lezer om te weten, beredeneer dit goed en schrijf het onder BEREDENEER.
4. Werk de HUIDIGE UITLEG bij met deze nieuwe informatie, zodat de lezer een compleet beeld krijgt, schrijf dit onder UITLEG.

REGELS
- Gebruik een heldere, toegankelijke taal.
- Houd de uitleg super beknopt en to the point, maximaal 150 woorden.
- Vermijd jargon en ingewikkelde termen.
- Focus op de kerninformatie en context.

HUIDIGE UITLEG
{{PLAATS_HIER_DE_UITLEG}}

NIEUWE ARTIKEL
{{PLAATS_HIER_HET_ARTIKEL}}

BEREDENEER
"""


# ---------- Constants & Data ----------
with open("src/data/uitlegknop.json", "r", encoding="utf-8") as f:
    DATA: dict = json.load(f)

ARTICLE = DATA["article"]
DOSSIER = DATA["dossier"]

PAGE_EXPLANATION = """Hier komt nog een uitleg over wat deze pagina doet en hoe het werkt. Hier komt nog een uitleg over wat deze pagina doet en hoe het werkt. Hier komt nog een uitleg over wat deze pagina doet en hoe het werkt. Hier komt nog een uitleg over wat deze pagina doet en hoe het werkt."""


# ---------- Helper Functions ----------
def process_article_explanation() -> None:
    if not st_utils.is_model_loaded(verbose=False):
        return
    
    if not st.button("Leg Het Me Uit"):
        return

    ARTICLES = DOSSIER["articles"]

    # Add the main article at the end of the list
    all_articles = ARTICLES + [{"content": ARTICLE["title"] + ARTICLE["text"]}]

    explanation_data = []
    current_explanation = "Nog geen uitleg beschikbaar."
    for article in all_articles:
        prompt = (
            PROMPT
            .replace("{{PLAATS_HIER_DE_UITLEG}}", current_explanation)
            .replace("{{PLAATS_HIER_HET_ARTIKEL}}", article["content"])
        )
        response = hf_utils.generate_with_retries(prompt)
        current_explanation = response["uitleg"]
        explanation_data.append(response)

    # Save explanation data
    DATA["article"]["explanation"] = explanation_data
    with open("src/data/uitlegknop.json", "w", encoding="utf-8") as f:
        json.dump(DATA, f, ensure_ascii=False, indent=4)


def display_explanation() -> None:
    if st.button("Leg Het Me Uit"):
        with open("src/data/uitlegknop.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            explanations = data.get("article", {}).get("explanation", [{}])

        text = explanations[-1].get("uitleg", "Geen uitleg gevonden.")
        url = DOSSIER.get("url", None)
        owner = ARTICLE.get("owner", "Onbekend")

        st_utils.render_popup_dialog(
            title="Hoe zit het nou?",
            text=text,
            url=url,
            owner=owner
        )


# ---------- Main Page Logic ----------
def main() -> None:
    st_utils.render_page_header("Uitlegknop", PAGE_EXPLANATION)

    st_utils.render_article(**ARTICLE)

    process_article_explanation()

    display_explanation()

    st.divider()

    st_utils.render_page_link("doc_uitlegknop.py")


if __name__ == "__main__":
	main()