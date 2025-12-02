import streamlit as st

TEXT = """Welkom bij de conceptversies van de Verbroken Verbinding app. Welkom bij de conceptversies van de Verbroken Verbinding app. Welkom bij de conceptversies van de Verbroken Verbinding app. Welkom bij de conceptversies van de Verbroken Verbinding app. Welkom bij de conceptversies van de Verbroken Verbinding app.

## Navigatie
In de zijbalk kunt u navigeren naar de verschillende pagina's die de conceptversies tonen. In de zijbalk kunt u navigeren naar de verschillende pagina's die de conceptversies tonen. In de zijbalk kunt u navigeren naar de verschillende pagina's die de conceptversies tonen. In de zijbalk kunt u navigeren naar de verschillende pagina's die de conceptversies tonen.

## Prototypes
#### Veertjes
Uitleg over veertjes komt hier. Uitleg over veertjes komt hier. Uitleg over veertjes komt hier. Uitleg over veertjes komt hier. Uitleg over veertjes komt hier. Uitleg over veertjes komt hier. Uitleg over veertjes komt hier.

#### Data Geïnformeerde Feedback
Uitleg over data geïnformeerde feedback hier. Uitleg over data geïnformeerde feedback hier. Uitleg over data geïnformeerde feedback hier. Uitleg over data geïnformeerde feedback hier. Uitleg over data geïnformeerde feedback hier.

#### Leg Het Me Uit Knop
Uitleg over de 'Leg Het Me Uit' knop komt hier. Uitleg over de 'Leg Het Me Uit' knop komt hier. Uitleg over de 'Leg Het Me Uit' knop komt hier. Uitleg over de 'Leg Het Me Uit' knop komt hier. Uitleg over de 'Leg Het Me Uit' knop komt hier.

## Links en Doorverwijzingen
Eventueel?"""


def main():
    st.set_page_config(
        page_title="Verbroken Verbinding Prototypes",
        page_icon="⛓️‍💥"
    )

    st.title("Verbroken Verbinding - Prototypes")
    st.markdown(TEXT)

if __name__ == "__main__":
    main()