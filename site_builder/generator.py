from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from string import Template
from typing import Iterable


TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "base.html"


@dataclass(frozen=True)
class Section:
    heading: str
    content: str


@dataclass(frozen=True)
class SiteSpec:
    title: str
    tagline: str
    sections: tuple[Section, ...]


class SpecError(ValueError):
    pass


def load_spec(path: Path) -> SiteSpec:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SpecError(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise SpecError("Spec must be a JSON object.")

    title = _require_str(raw, "title")
    tagline = _require_str(raw, "tagline")
    sections_raw = raw.get("sections", [])
    if not isinstance(sections_raw, list):
        raise SpecError("'sections' must be a list.")

    sections: list[Section] = []
    for idx, item in enumerate(sections_raw, start=1):
        if not isinstance(item, dict):
            raise SpecError(f"Section {idx} must be an object.")
        heading = _require_str(item, "heading", context=f"Section {idx}")
        content = _require_str(item, "content", context=f"Section {idx}")
        sections.append(Section(heading=heading, content=content))

    return SiteSpec(title=title, tagline=tagline, sections=tuple(sections))


def generate_site(spec: SiteSpec, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    template = Template(TEMPLATE_PATH.read_text(encoding="utf-8"))
    section_markup = _render_sections(spec.sections)
    html = template.substitute(
        title=spec.title,
        tagline=spec.tagline,
        sections=section_markup,
    )
    output_path = output_dir / "index.html"
    output_path.write_text(html, encoding="utf-8")
    return output_path


def _render_sections(sections: Iterable[Section]) -> str:
    if not sections:
        return "<section class=\"section\"><p>Add your first section in the JSON spec.</p></section>"

    rendered = []
    for section in sections:
        rendered.append(
            "\n".join(
                [
                    "<section class=\"section\">",
                    f"  <h2>{section.heading}</h2>",
                    f"  <p>{section.content}</p>",
                    "</section>",
                ]
            )
        )
    return "\n".join(rendered)


def _require_str(data: dict, key: str, *, context: str | None = None) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        label = f"{context} '{key}'" if context else f"'{key}'"
        raise SpecError(f"{label} must be a non-empty string.")
    return value.strip()
