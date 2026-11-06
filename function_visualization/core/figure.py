"""Public facade kept for backward compatibility.

Graph modules keep importing from here::

    from function_visualization.core.figure import configure_figure, export_figure
"""

from .captions import build_caption_html
from .exporter import export_figure
from .styling import configure_figure

__all__ = [
    "configure_figure",
    "build_caption_html",
    "export_figure",
]
