"""Parse YAML and Markdown input files into a unified data structure."""

import re
from pathlib import Path
from dataclasses import dataclass, field

import yaml


@dataclass
class Section:
    title: str = ""
    bullets: list[str] = field(default_factory=list)


@dataclass
class Card:
    title: str = ""
    period: str = ""
    company: str = ""
    summary: str = ""
    tech_tags: list[str] = field(default_factory=list)
    sections: list[Section] = field(default_factory=list)


@dataclass
class TabData:
    cards: list[Card] = field(default_factory=list)


def parse_yaml(filepath: Path) -> TabData:
    with open(filepath, "r", encoding="utf-8") as f:
        raw = yaml.load(f, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))

    if not raw or "cards" not in raw:
        return TabData()

    tab = TabData()
    for card_raw in raw["cards"]:
        card = Card(
            title=card_raw.get("title", ""),
            period=card_raw.get("period", ""),
            company=card_raw.get("company", ""),
            summary=card_raw.get("summary", ""),
            tech_tags=card_raw.get("tech_tags", []),
        )
        for sec_raw in card_raw.get("sections", []):
            card.sections.append(Section(
                title=sec_raw.get("title", ""),
                bullets=sec_raw.get("bullets", []),
            ))
        tab.cards.append(card)
    return tab


def parse_markdown(filepath: Path) -> TabData:
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    tab = TabData()
    # Split by card delimiter: "---" or multiple "# " headings
    card_blocks = re.split(r"\n---\n", text)

    for block in card_blocks:
        block = block.strip()
        if not block:
            continue
        card = _parse_md_card(block)
        if card:
            tab.cards.append(card)
    return tab


def _parse_md_card(block: str) -> Card | None:
    lines = block.split("\n")
    card = Card()
    current_section: Section | None = None

    for line in lines:
        line_stripped = line.strip()

        # H1 = card title
        if line_stripped.startswith("# ") and not line_stripped.startswith("## "):
            card.title = line_stripped[2:].strip()
            continue

        # Metadata lines (under H1, before any H2)
        if current_section is None and line_stripped.startswith("- "):
            meta = line_stripped[2:]
            if meta.startswith("period:"):
                card.period = meta.split(":", 1)[1].strip()
            elif meta.startswith("company:"):
                card.company = meta.split(":", 1)[1].strip()
            elif meta.startswith("summary:"):
                card.summary = meta.split(":", 1)[1].strip()
            elif meta.startswith("tech:"):
                tags = meta.split(":", 1)[1].strip()
                card.tech_tags = [t.strip() for t in tags.split(",")]
            continue

        # H2 = section title
        if line_stripped.startswith("## "):
            current_section = Section(title=line_stripped[3:].strip())
            card.sections.append(current_section)
            continue

        # Bullet under a section
        if current_section is not None and line_stripped.startswith("- "):
            current_section.bullets.append(line_stripped[2:].strip())

    return card if card.title else None


def parse_file(filepath: Path) -> TabData:
    suffix = filepath.suffix.lower()
    if suffix in (".yaml", ".yml"):
        return parse_yaml(filepath)
    elif suffix == ".md":
        return parse_markdown(filepath)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")
