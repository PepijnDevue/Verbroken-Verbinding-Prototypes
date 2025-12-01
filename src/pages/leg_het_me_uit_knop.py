import streamlit as st
import json
import src.streamlit_utils as st_utils

# ---------- Constants & Data ----------
with open("src/data/lhmu.json", "r", encoding="utf-8") as f:
    DATA: dict = json.load(f)

ARTICLE = DATA["article"]
DOSSIER = DATA["dossier"]

PAGE_EXPLANATION = """Hier komt nog een uitleg over wat deze pagina doet en hoe het werkt. Hier komt nog een uitleg over wat deze pagina doet en hoe het werkt. Hier komt nog een uitleg over wat deze pagina doet en hoe het werkt. Hier komt nog een uitleg over wat deze pagina doet en hoe het werkt."""

# ---------- Main Page Logic ----------
def main() -> None:
    st_utils.render_page_header("Leg Het Me Uit Knop", PAGE_EXPLANATION)

    st_utils.render_article(**ARTICLE)

if __name__ == "__main__":
	main()