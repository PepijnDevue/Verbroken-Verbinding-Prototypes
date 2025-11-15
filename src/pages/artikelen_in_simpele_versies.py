import streamlit as st
import src.streamlit_utils as st_utils


# ---------- Constants & Data ----------
ARTICLES = {
	"AI in de zorg": (
		"Kunstmatige intelligentie (AI) wordt steeds meer gebruikt in de gezondheidszorg. "
		"Het helpt artsen bij het stellen van diagnoses, het analyseren van medische beelden "
		"en het voorspellen van risico's. Toch blijven privacy, transparantie en de rol van "
		"menselijke controle belangrijke aandachtspunten."
	),
	"Klimaatverandering": (
		"Het klimaat verandert door de uitstoot van broeikasgassen. Hierdoor stijgt de temperatuur, "
		"smelten gletsjers en neemt extreem weer toe. Overheden, bedrijven en burgers werken aan "
		"oplossingen, zoals energiebesparing, hernieuwbare energie en klimaatadaptatie."
	),
	"Voeding en gezondheid": (
		"Wat we eten heeft grote invloed op onze gezondheid. Een gevarieerd dieet met veel groente, "
		"fruit, vezels en voldoende eiwitten ondersteunt een gezond lichaam. Ultra-bewerkte voeding, "
		"suikers en slechte vetten verhogen het risico op diverse ziekten."
	),
}


def main() -> None:
    st.title("Artikelen in Simpele Versies")
	
    st_utils.render_sidebar()

    _init_session_defaults()

    _render_article_selector()

    _display_selected_article()

    _render_feedback()

# ---------- Session State Keys ----------
ARTICLE_KEY = "aiv_selected_article"
ORIGINAL_TEXT_KEY = "aiv_original_text"
VIEW_TEXT_KEY = "aiv_view_text"
RATING_KEY = "aiv_difficulty_rating"


# ---------- Simplification Hook ----------
def versimpel(text: str, level: int) -> str:
	"""Placeholder die later door jou wordt geïmplementeerd.

	Contract:
	- Input: originele artikeltekst (str), niveau (int)
	- Output: vereenvoudigde tekst (str)
	- Verwachte range niveau: 1..10 (waarbij hoger simpeler is)

	Voor nu wordt de tekst ongewijzigd teruggegeven zodat de UI werkt.
	"""
	# TODO: vervang deze stub door jouw eigen implementatie.
	return text


# ---------- UI Helpers ----------
def _init_session_defaults() -> None:
	"""Initialiseer standaardkeuzes en staat voor artikel en rating."""
	first_title = next(iter(ARTICLES))
	if ARTICLE_KEY not in st.session_state:
		st.session_state[ARTICLE_KEY] = first_title
	if ORIGINAL_TEXT_KEY not in st.session_state:
		st.session_state[ORIGINAL_TEXT_KEY] = ARTICLES[st.session_state[ARTICLE_KEY]]
	if VIEW_TEXT_KEY not in st.session_state:
		st.session_state[VIEW_TEXT_KEY] = st.session_state[ORIGINAL_TEXT_KEY]
	if RATING_KEY not in st.session_state:
		st.session_state[RATING_KEY] = 5


def _display_selected_article():
    st.subheader(st.session_state[ARTICLE_KEY])
    st.write(st.session_state[VIEW_TEXT_KEY])


def _on_level_change() -> None:
	"""Aanroepen wanneer het feedbackniveau wijzigt: update de zichtbare tekst."""
	level = int(st.session_state.get(RATING_KEY, 5))
	original = st.session_state.get(ORIGINAL_TEXT_KEY, "")
	st.session_state[VIEW_TEXT_KEY] = versimpel(original, level)


def _render_article_selector() -> None:
    """Laat gebruiker een artikel kiezen via st.pills (met een veilige fallback)."""
    options = list(ARTICLES.keys())

    st.pills("Kies een artikel", options=options, key=ARTICLE_KEY)

    selected = st.session_state[ARTICLE_KEY]

    # Als de selectie is veranderd: reset tekst en niveau
    if ARTICLES[selected] != st.session_state.get(ORIGINAL_TEXT_KEY):
        st.session_state[ORIGINAL_TEXT_KEY] = ARTICLES[selected]
        st.session_state[VIEW_TEXT_KEY] = ARTICLES[selected]
        st.session_state[RATING_KEY] = 5

def _render_feedback() -> None:
    """Toon sterren-feedback op level 5 en koppel wijziging aan versimpel()."""
    st.caption("Pas het niveau aan om de tekst te vereenvoudigen.")

    st.segmented_control(
		"Gewichtjes",
		["1", "2", "3", "4", "5"],
		key=RATING_KEY,
		default="5",
        on_change=_on_level_change,
    )

if __name__ == "__main__":
	main()