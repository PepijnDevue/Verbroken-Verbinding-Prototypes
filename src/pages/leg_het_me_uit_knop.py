import streamlit as st
import json

# ---------- Constants & Data ----------
with open("src/data/lhmu.json", "r", encoding="utf-8") as f:
    DATA: dict = json.load(f)

ARTICLE = DATA["article"]
DOSSIER = DATA["dossier"]

# ---------- Main Page Logic ----------
def main() -> None:
    st.title("Leg het me uit knop")

    _display_article()

def _display_article() -> None:
    st.subheader(ARTICLE["title"])
    st.write(ARTICLE["text"])

if __name__ == "__main__":
	main()