import streamlit as st
import json
import src.streamlit_utils as st_utils
import src.huggingface_utils as hf_utils

# ---------- Constants & Data ----------
with open("src/data/lhmu.json", "r", encoding="utf-8") as f:
    DATA: dict = json.load(f)

ARTICLE = DATA["article"]
DOSSIER = DATA["dossier"]

PAGE_EXPLANATION = """Hier komt nog een uitleg over wat deze pagina doet en hoe het werkt. Hier komt nog een uitleg over wat deze pagina doet en hoe het werkt. Hier komt nog een uitleg over wat deze pagina doet en hoe het werkt. Hier komt nog een uitleg over wat deze pagina doet en hoe het werkt."""

# ---------- Prompt Template ----------
PROMPT = """Je bent een expert in het uitleggen van nieuwsartikelen en de grotere context daaromheen.
Je taak is om een begrijpelijke uitleg te geven van het gegeven artikel, zodat een gemiddelde lezer de inhoud en context beter kan begrijpen.
Meestal is er een nieuw artikel toegevoegd aan een bestaand dossier. Dan vernieuw je de huidige uitleg met de nieuwe informatie.
Je verwerkt alleen de korte noddige informatie uit de artikelen, geen quotes of details. Je verwerkt alle nieuwe informatie uit het nieuwe artikel, zo is de lezer helemaal op de hoogte.

INSTRUCTIES
1. Lees eerst de HUIDIGE UITLEG goed door.
2. Lees daarna het NIEUWE ARTIKEL aandachtig.
3. Bedenk welke nieuwe informatie uit het NIEUWE ARTIKEL belangrijk is voor de lezer om te weten, beredeneer dit goed.
4. Werk de HUIDIGE UITLEG bij met deze nieuwe informatie, zodat de lezer een compleet beeld krijgt.
5. Geef je output in strikt JSON-formaat:
{\"beredeneer\": \"Korte uitleg van je aanpak en welke nieuwe informatie je hebt toegevoegd.\", \"uitleg\": \"De bijgewerkte uitleg voor de lezer.\"}

REGELS
- Gebruik een heldere, toegankelijke taal.
- Houd de uitleg beknopt en to the point.
- Vermijd jargon en ingewikkelde termen.
- Focus op de kerninformatie en context.
- BELANGRIJK: Gebruik GEEN markdown formatting (geen ###, **, -, etc.) in de JSON output, dit om de leesbaarheid en verwerkbaarheid te waarborgen.
- Gebruik gewone tekst zonder newlines of \"\\n\".
- Voor hoofdstukken: gebruik hoofdletters.
- Voor lijstjes: gebruik simpele getallen (1., 2., 3.) of schrijf het uit in lopende tekst.


HUIDIGE UITLEG
<uitleg> {{PLAATS_HIER_DE_UITLEG}} </uitleg>

NIEUWE ARTIKEL
<artikel> {{PLAATS_HIER_HET_ARTIKEL}} </artikel>

OUTPUT"""

# ---------- Main Page Logic ----------
def main() -> None:
    st_utils.render_page_header("Leg Het Me Uit Knop", PAGE_EXPLANATION)

    st_utils.render_article(**ARTICLE)

    if st.button("Leg Het Me Uit"):
        ARTICLES = DOSSIER["articles"]
        explanation_data = []
        current_explanation = "Nog geen uitleg beschikbaar."

        for article in ARTICLES[::-1] + [{"content": ARTICLE["title"] + ARTICLE["text"]}]: # Start with the oldest article
            prompt = (
                PROMPT
                .replace("{{PLAATS_HIER_DE_UITLEG}}", current_explanation)
                .replace("{{PLAATS_HIER_HET_ARTIKEL}}", article["content"])
            )
            response = hf_utils.generate_with_retries(prompt)
            with st.expander(f"Artikel: {article['content'][:30]}..."):
                st.json(response)
            current_explanation = response["uitleg"]
            explanation_data.append(response)

        # Display final explanation
        st.subheader("Uitleg van het artikel")
        st.markdown(current_explanation)

        # Save explanation data
        DATA["article"]["explanation"] = explanation_data
        with open("lhmu.json", "w", encoding="utf-8") as f:
            json.dump(DATA, f, ensure_ascii=False, indent=4)
        

    """TODO
    Onder artikel een knop "Leg Het Me Uit"
    Daarna verschijnt disclaimertje en AI uitleg
    Onderaan link naar gebruikte dossier
    """

if __name__ == "__main__":
	main()