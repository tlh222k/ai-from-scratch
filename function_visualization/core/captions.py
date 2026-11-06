"""Caption HTML generation (MathJax-compatible: content is passed through verbatim)."""

from __future__ import annotations


def build_caption_html(
    caption,
    title=None,
    font_size="16px",
):
    """Return the caption block (HTML + scoped CSS) shown under a graph.

    ``caption`` is inserted unescaped so MathJax delimiters such as
    ``\\( ... \\)`` keep working.
    """
    title_html = (
        f'<h3 class="caption-title">{title}</h3>'
        if title
        else ""
    )

    return f"""
    <div class="visualization-caption">
        {title_html}

        <div class="caption-content">
            {caption}
        </div>
    </div>

    <style>
        .visualization-caption {{
            box-sizing: border-box;
            margin-top: 16px;
            padding: 18px 22px;
            background: #f8fafc;
            border-left: 4px solid #2563eb;
            border-radius: 8px;
            font-size: {font_size};
            line-height: 1.8;
            color: #334155;
            overflow-wrap: break-word;
        }}

        .caption-title {{
            margin: 0 0 10px;
            font-size: 20px;
            font-weight: 700;
            color: #0f172a;
        }}

        .caption-content strong {{
            color: #1d4ed8;
        }}

        @media(max-width:600px) {{
            .visualization-caption {{
                padding: 14px;
                font-size: 14px;
            }}

            .caption-title {{
                font-size: 17px;
            }}
        }}
    </style>
    """
