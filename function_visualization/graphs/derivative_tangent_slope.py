
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from function_visualization.core.figure import configure_figure
from function_visualization.core.captions import build_caption_html
from function_visualization.core.exporter import (
    PLOTLY_CONFIG,
    render_page,
)


# ============================================================
# 1. GRAPH CONFIGURATION
# ============================================================

GRAPH_ID = "derivative_tangent_slope"
OUTPUT_FILENAME = "derivative_tangent_slope.html"

TITLE = "Derivative: Understanding Tangent Slopes"


# ============================================================
# 2. MATHEMATICAL FUNCTIONS
# ============================================================

def function(x):
    """
    f(x) = x² - 2x + 3
    """
    return x**2 - 2*x + 3


def derivative(x):
    """
    f'(x) = 2x - 2
    """
    return 2*x - 2


def tangent_function(x, x0):
    """
    Tangent line at x = x0:

    y = f(x0) + f'(x0)(x - x0)
    """
    y0 = function(x0)
    slope = derivative(x0)

    return y0 + slope * (x - x0)


# ============================================================
# 3. BUILD GRAPH
# ============================================================

def build(output_dir: Path):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # Domain
    # --------------------------------------------------------

    x_values = np.linspace(-2, 4, 500)
    y_values = function(x_values)

    tangent_x = np.linspace(-2, 4, 200)

    # Three important points
    reference_points = [
        {
            "x": -1,
            "color": "#ef4444",
            "name": "x = -1",
            "slope": -4,
        },
        {
            "x": 1,
            "color": "#eab308",
            "name": "x = 1",
            "slope": 0,
        },
        {
            "x": 3,
            "color": "#16a34a",
            "name": "x = 3",
            "slope": 4,
        },
    ]

    # --------------------------------------------------------
    # Figure
    # --------------------------------------------------------

    fig = go.Figure()

    # Trace 0: Original function
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines",
            name="f(x) = x² - 2x + 3",
            line=dict(
                color="#2563eb",
                width=3,
            ),
            hovertemplate=(
                "x = %{x:.2f}<br>"
                "f(x) = %{y:.2f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 1, 2, 3: Three tangent lines
    tangent_colors = [
        "#ef4444",
        "#eab308",
        "#16a34a",
    ]

    for point in reference_points:

        x0 = point["x"]

        fig.add_trace(
            go.Scatter(
                x=tangent_x,
                y=tangent_function(tangent_x, x0),
                mode="lines",
                name=(
                    f"Tangent at x = {x0} "
                    f"(slope = {point['slope']})"
                ),
                line=dict(
                    color=point["color"],
                    width=2.5,
                    dash="dash",
                ),
                hovertemplate=(
                    f"Tangent at x = {x0}<br>"
                    f"Slope = {point['slope']}<br>"
                    "x = %{x:.2f}<br>"
                    "y = %{y:.2f}"
                    "<extra></extra>"
                ),
            )
        )

    # Trace 4: Three points on the original curve
    point_x = [-1, 1, 3]
    point_y = [function(x) for x in point_x]

    fig.add_trace(
        go.Scatter(
            x=point_x,
            y=point_y,
            mode="markers+text",
            name="Reference Points",
            text=["A (-1, 6)", "B (1, 2)", "C (3, 6)"],
            textposition=[
                "top left",
                "bottom right",
                "top right",
            ],
            textfont=dict(
                size=12,
                color="#334155",
            ),
            marker=dict(
                size=11,
                color=tangent_colors,
                line=dict(
                    color="white",
                    width=2,
                ),
            ),
            hovertemplate=(
                "x = %{x}<br>"
                "f(x) = %{y}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 5: Dynamic tangent
    initial_x = 0.0

    fig.add_trace(
        go.Scatter(
            x=tangent_x,
            y=tangent_function(tangent_x, initial_x),
            mode="lines",
            name="Tangent at selected x",
            line=dict(
                color="#9333ea",
                width=2.5,
                dash="dot",
            ),
            hovertemplate=(
                "Selected tangent<br>"
                "x = %{x:.2f}<br>"
                "y = %{y:.2f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 6: Dynamic point
    fig.add_trace(
        go.Scatter(
            x=[initial_x],
            y=[function(initial_x)],
            mode="markers",
            name="Selected Point",
            marker=dict(
                size=13,
                color="#9333ea",
                line=dict(
                    color="white",
                    width=2,
                ),
            ),
            hovertemplate=(
                "Selected Point<br>"
                "x = %{x:.2f}<br>"
                "f(x) = %{y:.2f}"
                "<extra></extra>"
            ),
        )
    )

    # --------------------------------------------------------
    # Layout
    # --------------------------------------------------------

    configure_figure(
        fig,
        title=TITLE,
        xaxis_title="x",
        yaxis_title="f(x)",
        height=600,
    )

    fig.update_layout(
        template="plotly_white",
        hovermode="closest",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
        ),
        margin=dict(
            l=65,
            r=35,
            t=110,
            b=65,
        ),
    )

    fig.update_xaxes(
        range=[-2.3, 4.3],
        zeroline=True,
        zerolinewidth=1.5,
        zerolinecolor="#64748b",
        gridcolor="#e2e8f0",
    )

    fig.update_yaxes(
        range=[-1, 14],
        zeroline=True,
        zerolinewidth=1.5,
        zerolinecolor="#64748b",
        gridcolor="#e2e8f0",
    )

    # --------------------------------------------------------
    # Control panel
    # --------------------------------------------------------

    panel_html = """
    <div class="derivative-panel">

        <div class="panel-heading">
            <h3>Khảo sát độ dốc tiếp tuyến</h3>
            <p>
                Di chuyển thanh trượt x để quan sát tiếp tuyến
                và đạo hàm tại từng vị trí trên đồ thị.
            </p>
        </div>

        <div class="control-group">

            <div class="control-label">
                <label for="derivative-x">
                    Vị trí khảo sát (x)
                </label>

                <strong id="derivative-x-value">0.00</strong>
            </div>

            <input
                id="derivative-x"
                type="range"
                min="-2"
                max="4"
                step="0.05"
                value="0"
            />

            <div class="range-labels">
                <span>-2</span>
                <span>0</span>
                <span>2</span>
                <span>4</span>
            </div>

        </div>

        <div class="metrics-grid">

            <div class="metric-card">
                <span>Giá trị hàm số f(x)</span>
                <strong id="derivative-fx">3.000</strong>
            </div>

            <div class="metric-card">
                <span>Đạo hàm f'(x)</span>
                <strong id="derivative-slope">-2.000</strong>
            </div>

        </div>

        <div id="derivative-status" class="derivative-status">
            Đạo hàm âm: hàm số đang giảm tại vị trí khảo sát.
        </div>

        <div class="formula-box">

            <strong>Công thức đạo hàm</strong>

            <div class="formula">
                f'(x) = 2x - 2
            </div>

            <div class="formula-note">
                Đạo hàm chính là độ dốc của đường tiếp tuyến
                tại điểm đang xét.
            </div>

        </div>

    </div>

    <style>

        .derivative-panel {
            width: 100%;
            max-width: 900px;
            margin: 20px auto;
            padding: 22px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            box-sizing: border-box;
            color: #1e293b;
        }

        .panel-heading h3 {
            margin: 0 0 6px;
            font-size: 20px;
        }

        .panel-heading p {
            margin: 0 0 22px;
            color: #64748b;
            font-size: 14px;
            line-height: 1.6;
        }

        .control-group {
            margin-bottom: 20px;
        }

        .control-label {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            font-size: 14px;
            font-weight: 600;
        }

        .control-label strong {
            color: #9333ea;
            font-variant-numeric: tabular-nums;
        }

        .control-group input[type="range"] {
            width: 100%;
            accent-color: #9333ea;
            cursor: pointer;
        }

        .range-labels {
            display: flex;
            justify-content: space-between;
            color: #64748b;
            font-size: 12px;
            margin-top: 5px;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin: 20px 0;
        }

        .metric-card {
            display: flex;
            flex-direction: column;
            gap: 8px;
            padding: 15px;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
        }

        .metric-card span {
            color: #64748b;
            font-size: 13px;
        }

        .metric-card strong {
            font-size: 22px;
            font-variant-numeric: tabular-nums;
        }

        .derivative-status {
            padding: 14px;
            background: #f3e8ff;
            border-radius: 8px;
            color: #6b21a8;
            font-size: 14px;
            line-height: 1.6;
        }

        .formula-box {
            margin-top: 18px;
            padding: 16px;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
        }

        .formula {
            margin: 12px 0;
            font-size: 22px;
            font-weight: 600;
            text-align: center;
        }

        .formula-note {
            color: #64748b;
            font-size: 13px;
            text-align: center;
            line-height: 1.5;
        }

        @media (max-width: 600px) {
            .metrics-grid {
                grid-template-columns: 1fr;
            }
        }

    </style>
    """

    # --------------------------------------------------------
    # JavaScript: Dynamic tangent and derivative
    # --------------------------------------------------------

    post_script = r"""
    (function () {

        const get = (id) => document.getElementById(id);

        function f(x) {
            return x * x - 2 * x + 3;
        }

        function derivative(x) {
            return 2 * x - 2;
        }

        function initialize(attempt = 0) {

            const plot = document.querySelector(".js-plotly-plot");

            const xInput = get("derivative-x");
            const xValue = get("derivative-x-value");

            const fxValue = get("derivative-fx");
            const slopeValue = get("derivative-slope");

            const status = get("derivative-status");

            const required = [
                plot,
                xInput,
                xValue,
                fxValue,
                slopeValue,
                status
            ];

            if (required.some(element => element === null)) {

                if (attempt < 120) {
                    setTimeout(
                        () => initialize(attempt + 1),
                        50
                    );
                } else {
                    console.error(
                        "Derivative controls could not be initialized."
                    );
                }

                return;
            }

            // ------------------------------------------------
            // Update dynamic tangent
            // ------------------------------------------------

            function updateGraph() {

                const x = parseFloat(xInput.value);

                const y = f(x);
                const slope = derivative(x);

                const tangentX = [];
                const tangentY = [];

                // Tangent equation:
                // y = f(x0) + f'(x0)(x - x0)

                for (let i = 0; i <= 100; i++) {

                    const pointX = -2 + (6 * i / 100);

                    const pointY =
                        y + slope * (pointX - x);

                    tangentX.push(pointX);
                    tangentY.push(pointY);
                }

                // Trace 5: Dynamic tangent
                Plotly.restyle(
                    plot,
                    {
                        x: [tangentX],
                        y: [tangentY]
                    },
                    [5]
                );

                // Trace 6: Dynamic point
                Plotly.restyle(
                    plot,
                    {
                        x: [[x]],
                        y: [[y]]
                    },
                    [6]
                );

                // Update numerical values
                xValue.textContent = x.toFixed(2);
                fxValue.textContent = y.toFixed(3);
                slopeValue.textContent = slope.toFixed(3);

                // Interpret derivative sign
                if (Math.abs(slope) < 0.000001) {

                    status.textContent =
                        "Đạo hàm bằng 0: tiếp tuyến nằm ngang. " +
                        "Đây là điểm cực tiểu của hàm số.";

                } else if (slope < 0) {

                    status.textContent =
                        "Đạo hàm âm: tiếp tuyến hướng xuống " +
                        "khi x tăng. Hàm số đang giảm.";

                } else {

                    status.textContent =
                        "Đạo hàm dương: tiếp tuyến hướng lên " +
                        "khi x tăng. Hàm số đang tăng.";

                }
            }

            // ------------------------------------------------
            // Slider event
            // ------------------------------------------------

            xInput.addEventListener(
                "input",
                updateGraph
            );

            updateGraph();
        }

        initialize();

    })();
    """

    # --------------------------------------------------------
    # 4. VIETNAMESE CAPTION
    # --------------------------------------------------------

    caption = """
    <p>
        Xét hàm số:
        <strong>f(x) = x² − 2x + 3</strong>.
        Đạo hàm của hàm số là
        <strong>f'(x) = 2x − 2</strong>.
    </p>

    <p>
        Đạo hàm tại một điểm cho biết độ dốc của đường tiếp tuyến
        với đồ thị tại điểm đó. Dựa vào dấu của đạo hàm,
        chúng ta có thể xác định chiều biến thiên của hàm số.
    </p>

    <p>
        <strong>Tại x = −1:</strong>
        Đạo hàm bằng −4. Tiếp tuyến có độ dốc âm,
        hướng xuống khi x tăng. Vì vậy, hàm số đang giảm.
    </p>

    <p>
        <strong>Tại x = 1:</strong>
        Đạo hàm bằng 0. Tiếp tuyến nằm ngang.
        Đây là điểm cực tiểu của hàm số, tại đó f(1) = 2.
    </p>

    <p>
        <strong>Tại x = 3:</strong>
        Đạo hàm bằng 4. Tiếp tuyến có độ dốc dương,
        hướng lên khi x tăng. Vì vậy, hàm số đang tăng.
    </p>

    <p>
        Hãy sử dụng thanh trượt để thay đổi vị trí khảo sát.
        Quan sát cách đường tiếp tuyến thay đổi độ dốc,
        đồng thời theo dõi giá trị đạo hàm tương ứng.
    </p>

    <p>
        <strong>Kết luận:</strong>
        Đạo hàm âm cho biết hàm số đang giảm;
        đạo hàm bằng 0 cho biết tiếp tuyến nằm ngang;
        đạo hàm dương cho biết hàm số đang tăng.
    </p>
    """

    caption_html = build_caption_html(
        caption,
        TITLE,
        "16px",
    )

    # --------------------------------------------------------
    # 5. EXPORT HTML
    # --------------------------------------------------------

    plot_html = fig.to_html(
        full_html=False,
        include_plotlyjs=True,
        config=PLOTLY_CONFIG,
        post_script=post_script,
    )

    page_html = render_page(
        title=TITLE,
        plot_html=plot_html,
        caption_html=caption_html,
        panel_html=panel_html,
    )

    output_path = output_dir / OUTPUT_FILENAME

    output_path.write_text(
        page_html,
        encoding="utf-8",
    )

    return output_path
