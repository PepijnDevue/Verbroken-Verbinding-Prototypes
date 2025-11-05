"""
Main Streamlit application entry point.
Orchestrates the UI components for the VV test page.
"""

from streamlit_ui import setup_header, setup_sidebar, setup_body


def main():
    setup_header()
    setup_sidebar()
    setup_body()


if __name__ == "__main__":
    main()