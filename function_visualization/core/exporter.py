"""HTML export: combines Plotly output, caption, slider and the page template."""

from __future__ import annotations

from pathlib import Path

from .assets import read_template
from .captions import build_caption_html
from .slider.runtime import build_slider_html

PLOTLY_CONFIG = {
    "responsive": True,
    "displaylogo": False,
    "scrollZoom": True,
}


def render_page(title, plot_html, caption_html, panel_html) -> str:
    """Fill the shared page template (pure function, no I/O besides assets)."""
    return (
        read_template("page.html")
        .replace("TITLE_PLACEHOLDER", title)
        .replace("STYLES_PLACEHOLDER", read_template("styles.css"))
        .replace("PLOT_PLACEHOLDER", plot_html)
        .replace("CAPTION_PLACEHOLDER", caption_html)
        .replace("PANEL_PLACEHOLDER", panel_html)
    )


def export_figure(
    fig,
    output_dir,
    filename,
    caption,
    caption_title=None,
    page_title=None,
    font_size="16px",
    graph_id=None,
):
    """Write ``fig`` as a standalone HTML page and return its ``Path``."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plot_html = fig.to_html(
        full_html=False,
        include_plotlyjs=True,
        auto_play=False,
        config=dict(PLOTLY_CONFIG),
    )
    caption_html = build_caption_html(caption, caption_title, font_size)
    panel_html = build_slider_html(graph_id)
    title = page_title or caption_title or filename

    path = output_dir / filename
    path.write_text(
        render_page(title, plot_html, caption_html, panel_html),
        encoding="utf-8",
    )
    return path
