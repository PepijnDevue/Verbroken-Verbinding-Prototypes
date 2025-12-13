"""Landing page."""
from pathlib import Path
import src.streamlit_utils as st_utils

# Get the path to the markdown file
base_dir = Path(__file__).parent.parent.parent.resolve()
markdown_file = base_dir / "docs" / "pages" / "welkom.md"


st_utils.render_markdown_page(str(markdown_file))