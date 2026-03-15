"""Generate the bilingual HTML page using pre-compiled Jinja2 template."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from parser import TabData

# Pre-compile template at import time (once per process)
_env = Environment(
    loader=FileSystemLoader(Path(__file__).parent / "templates"),
    autoescape=True,
)
_template = _env.get_template("page.html")


def generate_html(
    title: str,
    tabs: list[dict],
    data: dict[str, dict[str, TabData | None]],
) -> str:
    return _template.render(title=title, tabs=tabs, data=data)
