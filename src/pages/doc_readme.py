"""README documentation page."""
from pathlib import Path
from .markdown_page import render_markdown_page

# Get the path to the markdown file
base_dir = Path(__file__).parent.parent.parent.resolve()
markdown_file = base_dir / "README.md"

render_markdown_page(str(markdown_file))
