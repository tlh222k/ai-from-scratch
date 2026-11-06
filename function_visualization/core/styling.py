"""Plotly figure styling shared by every graph."""

from __future__ import annotations

from typing import Any

# Shared visual constants (values are unchanged from the original figure.py).
FONT_FAMILY = "Arial, sans-serif"
BASE_FONT_SIZE = 14
TITLE_FONT_SIZE = 22
AXIS_ZERO_LINE_COLOR = "#64748b"
AXIS_ZERO_LINE_WIDTH = 2
DEFAULT_HEIGHT = 520
MARGIN = dict(l=60, r=30, t=110, b=60)
TEMPLATE = "plotly_white"


def _axis_style() -> dict[str, Any]:
    return dict(
        showgrid=True,
        zeroline=True,
        zerolinewidth=AXIS_ZERO_LINE_WIDTH,
        zerolinecolor=AXIS_ZERO_LINE_COLOR,
    )


def configure_figure(
    fig,
    title,
    xaxis_title="x",
    yaxis_title="y",
    height=DEFAULT_HEIGHT,
):
    """Apply the shared layout (title, margins, axes, legend) to ``fig``.

    Returns the same figure so calls can be chained.
    """
    fig.update_layout(
        title={
            "text": title,
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": TITLE_FONT_SIZE},
        },
        autosize=True,
        height=height,
        margin=dict(MARGIN),
        template=TEMPLATE,
        font=dict(
            family=FONT_FAMILY,
            size=BASE_FONT_SIZE,
        ),
        hovermode="closest",
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        xaxis=_axis_style(),
        yaxis=_axis_style(),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
        ),
    )

    return fig
