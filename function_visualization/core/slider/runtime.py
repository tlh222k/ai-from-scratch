"""Builds the slider panel (HTML + CSS + JS) injected into an exported page."""

from __future__ import annotations

import json
import re
from typing import Optional

from ..assets import read_template
from .config import SliderConfig, get_slider_config

_KIND_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


def _handler_script(kind: str) -> str:
    if not _KIND_PATTERN.match(kind):
        raise ValueError(f"Invalid slider kind: {kind!r}")
    return read_template(f"handlers/{kind}.js")


def render_slider_panel(config: SliderConfig) -> str:
    """Render panel markup, its CSS, and the JS (core runtime + one handler)."""
    panel_html = (
        read_template("slider_panel.html")
        .replace("LABEL_PLACEHOLDER", str(config.label))
        .replace("MIN_PLACEHOLDER", str(config.minimum))
        .replace("MAX_PLACEHOLDER", str(config.maximum))
        .replace("STEP_PLACEHOLDER", str(config.step))
        .replace("DEFAULT_PLACEHOLDER", str(config.default))
    )
    css = read_template("slider.css")
    script = "\n".join(
        [
            "(function() {",
            read_template("slider.js"),
            _handler_script(config.kind),
            f"startSlider({json.dumps(config.kind)});",
            "})();",
        ]
    )
    return f"{panel_html}\n<style>\n{css}\n</style>\n<script>\n{script}\n</script>\n"


def build_slider_html(graph_id: Optional[str]) -> str:
    """Return the slider block for ``graph_id`` or ``""`` when it has none."""
    config = get_slider_config(graph_id)
    if config is None:
        return ""
    return render_slider_panel(config)
