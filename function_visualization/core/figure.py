
from pathlib import Path


def configure_figure(
    fig,
    title,
    xaxis_title="x",
    yaxis_title="y",
    height=520,
):
    fig.update_layout(
        title={
            "text": title,
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 22},
        },
        autosize=True,
        height=height,
        margin=dict(l=60, r=30, t=110, b=60),
        template="plotly_white",
        font=dict(
            family="Arial, sans-serif",
            size=14,
        ),
        hovermode="closest",
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        xaxis=dict(
            showgrid=True,
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="#64748b",
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="#64748b",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
        ),
    )

    return fig


def build_caption_html(
    caption,
    title=None,
    font_size="16px",
):
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
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plot_html = fig.to_html(
        full_html=False,
        include_plotlyjs=True,
        auto_play=False,
        config={
            "responsive": True,
            "displaylogo": False,
            "scrollZoom": True,
        },
    )

    caption_html = build_caption_html(
        caption,
        caption_title,
        font_size,
    )

    title = page_title or caption_title or filename

    # ---------------------------------------------------------
    # Cấu hình slider cho từng graph
    # ---------------------------------------------------------

    config = {
        "linear_function": (
            "Hệ số góc m", -5, 5, 2, "linear"
        ),

        "quadratic_function": (
            "Hệ số a", -3, 3, 1, "quadratic"
        ),

        "limit_function": (
            "Vị trí điểm khuyết a", -2, 3, 1, "limit"
        ),

        "limit_approach_function": (
            "Điểm tiến đến a", 0, 5, 3, "approach"
        ),

        "secant_line": (
            "Điểm thứ hai x₂", 1.1, 3.5, 3, "secant"
        ),

        "secant_to_tangent": (
            "Khoảng cách h", 0.05, 2, 1, "tangent"
        ),

        # Graph cũ: J(w) = (w - 2)²
        "cost_function": (
            "Tham số mô hình w", -2, 6, 5, "cost"
        ),

        # Graph: J(w) = w²
        "quadratic_cost_function": (
            "Tham số mô hình w", -4, 4, 3, "quadratic_cost"
        ),

        # Graph: Gradient Descent trên f(x) = x²
        "gradient_descent": (
            "Vị trí hiện tại x", -4, 4, 2, "gradient_descent"
        ),
    }

    panel = ""

    if graph_id in config:
        label, low, high, default, kind = config[graph_id]

        panel = f"""
        <section class="parameter-panel">
            <h3>Điều chỉnh tham số</h3>

            <label>
                {label}:
                <b id="param-value">{default}</b>
            </label>

            <input
                id="param-slider"
                type="range"
                min="{low}"
                max="{high}"
                step="0.05"
                value="{default}"
            >

            <p id="param-caption">
                Kéo thanh trượt để quan sát sự thay đổi.
            </p>
        </section>

        <style>
            .parameter-panel {{
                padding: 18px;
                margin: 12px 0;
                background: #f8fbff;
                border: 1px solid #bfdbfe;
                border-radius: 12px;
            }}

            .parameter-panel h3 {{
                margin: 0 0 10px;
                color: #1e40af;
            }}

            .parameter-panel input {{
                width: 100%;
                accent-color: #2563eb;
                cursor: pointer;
            }}

            .parameter-panel p {{
                line-height: 1.6;
                color: #475569;
            }}
        </style>

        <script>
        (function() {{
            const g = document.querySelector(".plotly-graph-div");
            const s = document.getElementById("param-slider");

            if (!g || !s || !window.Plotly) return;

            const kind = "{kind}";

            function update() {{
                const v = Number(s.value);

                document.getElementById("param-value").textContent =
                    v.toFixed(2);

                let x = [];
                let y = [];
                let cap = "";

                // -------------------------------------------------
                // GRAPH: GRADIENT DESCENT
                // f(x) = x²
                //
                // Trace 0: Đường cong hàm số.
                // Trace 1: Điểm hiện tại.
                // Trace 2: Tiếp tuyến.
                // Trace 3: Điểm cực tiểu.
                // -------------------------------------------------

                if (kind === "gradient_descent") {{
                    const fx = v ** 2;
                    const gradient = 2 * v;
                    const learningRate = 0.2;

                    // Quy tắc cập nhật Gradient Descent
                    const nextX = v - learningRate * gradient;

                    // Cập nhật điểm hiện tại
                    Plotly.restyle(
                        g,
                        {{
                            x: [[v]],
                            y: [[fx]]
                        }},
                        [1]
                    );

                    // Tính toán tiếp tuyến:
                    // y = f(v) + f'(v)(x - v)

                    const tangentX = [];
                    const tangentY = [];

                    for (let i = 0; i < 100; i++) {{
                        const t = v - 1.2 + (2.4 * i / 99);

                        tangentX.push(t);

                        tangentY.push(
                            fx + gradient * (t - v)
                        );
                    }}

                    // Cập nhật đường tiếp tuyến
                    Plotly.restyle(
                        g,
                        {{
                            x: [tangentX],
                            y: [tangentY]
                        }},
                        [2]
                    );

                    // Cập nhật mũi tên Gradient Descent
                    // Dấu ngoặc nhọn phải được escape trong f-string.
                    Plotly.relayout(g, {{
                        annotations: [{{
                            x: nextX,
                            y: 0.55,
                            ax: v,
                            ay: 0.55,
                            xref: "x",
                            yref: "y",
                            axref: "x",
                            ayref: "y",
                            showarrow: Math.abs(gradient) > 0.01,
                            arrowhead: 3,
                            arrowsize: 1.4,
                            arrowwidth: 3,
                            arrowcolor: "#2563eb",
                            text: ""
                        }}]
                    }});

                    if (Math.abs(v) < 0.01) {{
                        cap =
                            "Bạn đang ở gần điểm cực tiểu x = 0. " +
                            "Đạo hàm gần bằng 0 nên bước cập nhật rất nhỏ.";

                    }} else if (gradient > 0) {{
                        cap =
                            "f'(x) = " + gradient.toFixed(2) +
                            " > 0. Hàm số đang tăng. " +
                            "Gradient Descent di chuyển x sang trái, " +
                            "từ " + v.toFixed(2) +
                            " đến " + nextX.toFixed(2) + ".";

                    }} else {{
                        cap =
                            "f'(x) = " + gradient.toFixed(2) +
                            " < 0. Hàm số đang giảm. " +
                            "Gradient Descent di chuyển x sang phải, " +
                            "từ " + v.toFixed(2) +
                            " đến " + nextX.toFixed(2) + ".";
                    }}

                // -------------------------------------------------
                // GRAPH: QUADRATIC COST FUNCTION
                // J(w) = w²
                // -------------------------------------------------

                }} else if (kind === "quadratic_cost") {{
                    const cost = v ** 2;

                    Plotly.restyle(
                        g,
                        {{
                            x: [[v]],
                            y: [[cost]]
                        }},
                        [1]
                    );

                    if (Math.abs(v) < 0.001) {{
                        cap =
                            "Tham số đã đạt giá trị tối ưu w* = 0. " +
                            "Hàm chi phí đạt giá trị nhỏ nhất J(w) = 0.";

                    }} else if (v < 0) {{
                        cap =
                            "Tham số hiện tại w = " + v.toFixed(2) +
                            ". Giá trị hàm chi phí J(w) = " +
                            cost.toFixed(2) +
                            ". Hãy tăng w về gần 0 để giảm chi phí.";

                    }} else {{
                        cap =
                            "Tham số hiện tại w = " + v.toFixed(2) +
                            ". Giá trị hàm chi phí J(w) = " +
                            cost.toFixed(2) +
                            ". Hãy giảm w về gần 0 để giảm chi phí.";
                    }}

                // -------------------------------------------------
                // COST FUNCTION CŨ
                // J(w) = (w - 2)²
                // -------------------------------------------------

                }} else if (kind === "cost") {{
                    const cost = (v - 2) ** 2;

                    Plotly.restyle(
                        g,
                        {{
                            x: [[v]],
                            y: [[cost]]
                        }},
                        [1]
                    );

                    if (Math.abs(v - 2) < 0.001) {{
                        cap =
                            "Tham số đã đạt giá trị tối ưu w* = 2. " +
                            "Hàm chi phí đạt giá trị nhỏ nhất J(w) = 0.";

                    }} else if (v < 2) {{
                        cap =
                            "Tham số hiện tại w = " + v.toFixed(2) +
                            ". Giá trị hàm chi phí J(w) = " +
                            cost.toFixed(2) +
                            ". Hãy tăng w về gần 2 để giảm chi phí.";

                    }} else {{
                        cap =
                            "Tham số hiện tại w = " + v.toFixed(2) +
                            ". Giá trị hàm chi phí J(w) = " +
                            cost.toFixed(2) +
                            ". Hãy giảm w về gần 2 để giảm chi phí.";
                    }}

                }} else {{

                    // -------------------------------------------------
                    // GIỮ NGUYÊN LOGIC CỦA 6 GRAPH CŨ
                    // -------------------------------------------------

                    for (let i = 0; i < 300; i++) {{
                        let t = -5 + 10 * i / 299;

                        x.push(t);

                        if (kind === "linear") {{
                            y.push(v * t + 1);

                        }} else if (kind === "quadratic") {{
                            y.push(v * t * t);

                        }} else if (kind === "limit") {{
                            y.push(
                                Math.abs(t - v) < 0.025
                                    ? null
                                    : t + v
                            );

                        }} else if (kind === "approach") {{
                            y.push(2 * t + (v - 3) * 2 + 1);

                        }} else {{
                            y.push(t * t);
                        }}
                    }}

                    Plotly.restyle(
                        g,
                        {{"x": [x], "y": [y]}},
                        [0]
                    );

                    if (kind === "linear") {{
                        cap =
                            "f(x) = " + v.toFixed(2) +
                            "x + 1. Hệ số góc m quyết định độ dốc của đường thẳng.";

                    }} else if (kind === "quadratic") {{
                        cap =
                            "g(x) = " + v.toFixed(2) +
                            "x². Dấu của a quyết định chiều mở của parabol.";

                    }} else if (kind === "limit") {{
                        cap =
                            "Điểm khuyết tại x = " + v.toFixed(2) +
                            "; giới hạn tương ứng bằng " +
                            (2 * v).toFixed(2) + ".";

                    }} else if (kind === "approach") {{
                        cap =
                            "x tiến đến a = " + v.toFixed(2) +
                            "; giới hạn của 2x+1 bằng " +
                            (2 * v + 1).toFixed(2) + ".";

                    }} else if (kind === "secant") {{
                        cap =
                            "Điều chỉnh x₂ = " + v.toFixed(2) +
                            " để khảo sát đường cát tuyến.";

                    }} else {{
                        cap =
                            "Khoảng cách h = " + v.toFixed(2) +
                            ". Khi h giảm, cát tuyến tiến gần tiếp tuyến.";
                    }}
                }}

                // Cập nhật caption động bên dưới slider
                document.getElementById("param-caption").textContent = cap;

                const captionContent = document.querySelector(
                    ".caption-content"
                );

                // Gradient Descent giữ nguyên caption bài giảng
                if (captionContent && kind !== "gradient_descent") {{
                    captionContent.textContent = cap;
                }}
            }}

            s.addEventListener("input", update);
            update();
        }})();
        </script>
        """

    # ---------------------------------------------------------
    # HTML page
    # ---------------------------------------------------------

    html = """<!DOCTYPE html>
    <html lang="vi">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>TITLE_PLACEHOLDER</title>

        <script>
            window.MathJax = {
                tex: {
                    inlineMath: [['\\\\(', '\\\\)']],
                    displayMath: [['\\\\[', '\\\\]']]
                }
            };
        </script>

        <script
            id="MathJax-script"
            async
            src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js">
        </script>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                padding: 24px;
                font-family: Arial, sans-serif;
                background: #fff;
                color: #1e293b;
            }

            .container {
                width: 100%;
                max-width: 1100px;
                margin: 0 auto;
            }

            .back-link {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                margin: 0 0 18px;
                padding: 10px 16px;
                background: #eff6ff;
                border: 1px solid #bfdbfe;
                border-radius: 9px;
                color: #1d4ed8;
                text-decoration: none;
                font-size: 14px;
                font-weight: 700;
                transition: background .15s, border-color .15s;
            }

            .back-link:hover {
                background: #dbeafe;
                border-color: #93c5fd;
            }

            .plot-container {
                width: 100%;
            }

            .note {
                margin-top: 12px;
                color: #94a3b8;
                font-size: 12px;
                text-align: center;
            }

            @media(max-width:600px) {
                body {
                    padding: 10px;
                }
            }
        </style>
    </head>

    <body>
        <main class="container">

            <a class="back-link" href="./index.html">
                ← Trang chủ
            </a>

            <section class="plot-container">
                PLOT_PLACEHOLDER
            </section>

            PANEL_PLACEHOLDER

            <section>
                CAPTION_PLACEHOLDER
            </section>

            <p class="note">
                Công thức toán được hiển thị bằng MathJax và cần kết nối
                Internet. Biểu đồ tương tác vẫn hoạt động khi ngoại tuyến.
            </p>

        </main>
    </body>

    </html>
    """

    html = (
        html
        .replace("TITLE_PLACEHOLDER", title)
        .replace("PLOT_PLACEHOLDER", plot_html)
        .replace("CAPTION_PLACEHOLDER", caption_html)
        .replace("PANEL_PLACEHOLDER", panel)
    )

    path = output_dir / filename
    path.write_text(html, encoding="utf-8")

    return path
