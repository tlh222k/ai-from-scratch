
from pathlib import Path
import math

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

GRAPH_ID = "directional_derivative"
OUTPUT_FILENAME = "directional_derivative.html"

TITLE = "Đạo hàm theo hướng – Phép chiếu của Gradient"

INITIAL_X = 1.0
INITIAL_Y = 1.0
INITIAL_THETA = 53.130102

AXIS_LIMIT = 5.0


# ============================================================
# 2. MATHEMATICAL FUNCTIONS
# ============================================================

def function(x, y):
    """
    f(x, y) = 0.5x² + y²
    """
    return 0.5 * x**2 + y**2


def gradient(x, y):
    """
    ∇f(x, y) = (x, 2y)
    """
    return np.array([x, 2.0 * y], dtype=float)


def unit_direction(theta_degrees):
    """
    Unit direction vector:

    u = (cos(theta), sin(theta))
    """
    theta = math.radians(theta_degrees)

    return np.array(
        [math.cos(theta), math.sin(theta)],
        dtype=float,
    )


def directional_derivative(grad, direction):
    """
    D_u f = ∇f · u
    """
    return float(np.dot(grad, direction))


def vector_projection(grad, direction):
    """
    Vector projection of gradient onto u:

    proj_u(∇f) = (∇f · u)u
    """
    return directional_derivative(
        grad,
        direction,
    ) * direction


# ============================================================
# 3. BUILD GRAPH
# ============================================================

def build(output_dir: Path):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # Initial mathematical values
    # --------------------------------------------------------

    x0 = INITIAL_X
    y0 = INITIAL_Y
    theta = INITIAL_THETA

    grad = gradient(x0, y0)
    u = unit_direction(theta)

    derivative = directional_derivative(grad, u)
    projection = vector_projection(grad, u)

    residual = grad - projection

    # --------------------------------------------------------
    # Create figure
    # --------------------------------------------------------

    fig = go.Figure()

    # Trace 0: Gradient vector
    fig.add_trace(
        go.Scatter(
            x=[0, grad[0]],
            y=[0, grad[1]],
            mode="lines+markers+text",
            name="Gradient (∇f)",
            line=dict(
                color="#ef4444",
                width=5,
            ),
            marker=dict(
                size=[0, 10],
                color="#ef4444",
            ),
            text=["", "∇f"],
            textposition="top right",
            textfont=dict(size=14),
            hovertemplate=(
                "Gradient ∇f<br>"
                "x = %{x:.3f}<br>"
                "y = %{y:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 1: Unit direction vector
    fig.add_trace(
        go.Scatter(
            x=[0, u[0]],
            y=[0, u[1]],
            mode="lines+markers+text",
            name="Vector hướng đơn vị (u)",
            line=dict(
                color="#3b82f6",
                width=4,
                dash="dot",
            ),
            marker=dict(
                size=[0, 10],
                color="#3b82f6",
            ),
            text=["", "u"],
            textposition="bottom right",
            textfont=dict(size=14),
            hovertemplate=(
                "Vector hướng u<br>"
                "x = %{x:.3f}<br>"
                "y = %{y:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 2: Vector projection
    fig.add_trace(
        go.Scatter(
            x=[0, projection[0]],
            y=[0, projection[1]],
            mode="lines+markers+text",
            name="Vector hình chiếu",
            line=dict(
                color="#10b981",
                width=5,
            ),
            marker=dict(
                size=[0, 11],
                color="#10b981",
                symbol="x",
            ),
            text=["", "projᵤ(∇f)"],
            textposition="top left",
            textfont=dict(size=12),
            hovertemplate=(
                "Vector hình chiếu<br>"
                "x = %{x:.3f}<br>"
                "y = %{y:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 3: Perpendicular residual
    fig.add_trace(
        go.Scatter(
            x=[projection[0], grad[0]],
            y=[projection[1], grad[1]],
            mode="lines",
            name="Thành phần vuông góc với u",
            line=dict(
                color="#94a3b8",
                width=2,
                dash="dash",
            ),
            hovertemplate=(
                "Thành phần vuông góc<br>"
                "x = %{x:.3f}<br>"
                "y = %{y:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 4: Origin
    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers",
            name="Gốc tọa độ",
            marker=dict(
                size=7,
                color="#334155",
            ),
            hoverinfo="skip",
        )
    )

    # --------------------------------------------------------
    # Layout
    # --------------------------------------------------------

    configure_figure(
        fig,
        title=TITLE,
        xaxis_title="Thành phần theo trục x",
        yaxis_title="Thành phần theo trục y",
        height=620,
    )

    fig.update_layout(
        template="plotly_white",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.16,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
        ),
        margin=dict(
            l=55,
            r=35,
            t=85,
            b=105,
        ),
        xaxis=dict(
            title="Thành phần theo trục x",
            range=[-AXIS_LIMIT, AXIS_LIMIT],
            zeroline=True,
            zerolinewidth=1.5,
            zerolinecolor="#64748b",
            gridcolor="#e2e8f0",
            scaleanchor="y",
            scaleratio=1,
        ),
        yaxis=dict(
            title="Thành phần theo trục y",
            range=[-AXIS_LIMIT, AXIS_LIMIT],
            zeroline=True,
            zerolinewidth=1.5,
            zerolinecolor="#64748b",
            gridcolor="#e2e8f0",
        ),
        annotations=[
            dict(
                x=grad[0],
                y=grad[1],
                ax=0,
                ay=0,
                xref="x",
                yref="y",
                axref="x",
                ayref="y",
                showarrow=True,
                arrowhead=3,
                arrowsize=1.4,
                arrowwidth=2,
                arrowcolor="#ef4444",
            ),
            dict(
                x=u[0],
                y=u[1],
                ax=0,
                ay=0,
                xref="x",
                yref="y",
                axref="x",
                ayref="y",
                showarrow=True,
                arrowhead=3,
                arrowsize=1.4,
                arrowwidth=2,
                arrowcolor="#3b82f6",
            ),
            dict(
                x=projection[0],
                y=projection[1],
                ax=0,
                ay=0,
                xref="x",
                yref="y",
                axref="x",
                ayref="y",
                showarrow=True,
                arrowhead=3,
                arrowsize=1.4,
                arrowwidth=2,
                arrowcolor="#10b981",
            ),
        ],
    )

    # --------------------------------------------------------
    # 4. INTERACTIVE CONTROL PANEL
    # --------------------------------------------------------

    panel_html = """
    <div class="directional-panel">

        <div class="panel-heading">
            <h3>Khảo sát đạo hàm theo hướng</h3>

            <p>
                Di chuyển điểm khảo sát và xoay vector hướng
                để quan sát phép chiếu của Gradient.
            </p>
        </div>

        <div class="controls-grid">

            <div class="control-group">
                <div class="control-label">
                    <label for="directional-x">Tọa độ x₀</label>
                    <strong id="directional-x-value">1.00</strong>
                </div>

                <input
                    id="directional-x"
                    type="range"
                    min="-2"
                    max="2"
                    step="0.05"
                    value="1"
                />
            </div>

            <div class="control-group">
                <div class="control-label">
                    <label for="directional-y">Tọa độ y₀</label>
                    <strong id="directional-y-value">1.00</strong>
                </div>

                <input
                    id="directional-y"
                    type="range"
                    min="-2"
                    max="2"
                    step="0.05"
                    value="1"
                />
            </div>

        </div>

        <div class="control-group angle-control">
            <div class="control-label">
                <label for="directional-angle">
                    Góc của vector hướng θ
                </label>

                <strong id="directional-angle-value">
                    53.13°
                </strong>
            </div>

            <input
                id="directional-angle"
                type="range"
                min="0"
                max="360"
                step="1"
                value="53"
            />

            <div class="angle-hints">
                <span>0°</span>
                <span>90°</span>
                <span>180°</span>
                <span>270°</span>
                <span>360°</span>
            </div>
        </div>

        <div class="metrics-grid">

            <div class="metric-card">
                <span>Gradient ∇f</span>
                <strong id="directional-gradient">
                    (1.00, 2.00)
                </strong>
            </div>

            <div class="metric-card blue-card">
                <span>Vector hướng đơn vị u</span>
                <strong id="directional-unit">
                    (0.60, 0.80)
                </strong>
            </div>

            <div class="metric-card green-card">
                <span>Đạo hàm theo hướng Dᵤf</span>
                <strong id="directional-value">
                    2.2000
                </strong>
                <small>Giá trị vô hướng (scalar)</small>
            </div>

            <div class="metric-card">
                <span>Vector hình chiếu</span>
                <strong id="directional-projection">
                    (1.32, 1.76)
                </strong>
                <small>(∇f · u)u</small>
            </div>

        </div>

        <div class="interpretation-box">
            <strong>Ý nghĩa của kết quả</strong>
            <p id="directional-explanation">
                Gradient có thành phần theo hướng u bằng 2.2.
                Hàm số đang tăng theo hướng này.
            </p>
        </div>

        <div class="control-buttons">
            <button id="directional-play" type="button">
                ▶ Xoay hướng
            </button>

            <button id="directional-pause" type="button">
                ⏸ Tạm dừng
            </button>

            <button id="directional-reset" type="button">
                ↺ Đặt lại
            </button>
        </div>

        <div class="formula-box">
            <strong>Các công thức cần quan sát</strong>

            <div class="formula">
                f(x, y) = 0.5x² + y²
            </div>

            <div class="formula">
                ∇f(x, y) = (x, 2y)
            </div>

            <div class="formula">
                u = (cos θ, sin θ)
            </div>

            <div class="formula">
                Dᵤf = ∇f · u
            </div>

            <div class="formula">
                projᵤ(∇f) = (∇f · u)u
            </div>
        </div>

    </div>

    <style>

        .directional-panel {
            width: 100%;
            max-width: 950px;
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
            margin: 0 0 20px;
            color: #64748b;
            font-size: 14px;
            line-height: 1.6;
        }

        .controls-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 22px;
        }

        .control-group {
            margin-bottom: 18px;
        }

        .control-label {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            margin-bottom: 9px;
            font-size: 14px;
            font-weight: 600;
        }

        .control-label strong {
            color: #2563eb;
            font-variant-numeric: tabular-nums;
        }

        .control-group input[type="range"] {
            width: 100%;
            accent-color: #2563eb;
            cursor: pointer;
        }

        .angle-hints {
            display: flex;
            justify-content: space-between;
            color: #94a3b8;
            font-size: 11px;
            margin-top: 5px;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin: 15px 0 20px;
        }

        .metric-card {
            display: flex;
            flex-direction: column;
            gap: 7px;
            padding: 14px;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 9px;
            min-width: 0;
        }

        .metric-card span {
            color: #64748b;
            font-size: 12px;
        }

        .metric-card strong {
            font-size: 19px;
            font-variant-numeric: tabular-nums;
            overflow-wrap: anywhere;
        }

        .metric-card small {
            color: #94a3b8;
            font-size: 11px;
        }

        .blue-card {
            border-left: 4px solid #3b82f6;
        }

        .blue-card strong {
            color: #2563eb;
        }

        .green-card {
            border-left: 4px solid #10b981;
        }

        .green-card strong {
            color: #059669;
        }

        .interpretation-box {
            padding: 15px;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            margin-bottom: 18px;
        }

        .interpretation-box p {
            margin: 7px 0 0;
            color: #64748b;
            font-size: 13px;
            line-height: 1.7;
        }

        .control-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
        }

        .control-buttons button {
            border: none;
            border-radius: 8px;
            padding: 10px 16px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            color: white;
            background: #2563eb;
        }

        .control-buttons button:hover {
            opacity: 0.85;
        }

        #directional-pause {
            background: #64748b;
        }

        #directional-reset {
            background: #475569;
        }

        .formula-box {
            padding: 16px;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
        }

        .formula {
            margin: 12px 0;
            text-align: center;
            font-size: 17px;
            font-weight: 600;
        }

        @media (max-width: 600px) {
            .controls-grid,
            .metrics-grid {
                grid-template-columns: 1fr;
            }
        }

    </style>
    """

    # --------------------------------------------------------
    # 5. JAVASCRIPT
    # --------------------------------------------------------

    post_script = r"""
    (function () {

        const INITIAL_X = 1.0;
        const INITIAL_Y = 1.0;
        const INITIAL_THETA = 53.130102;

        let x0 = INITIAL_X;
        let y0 = INITIAL_Y;
        let theta = INITIAL_THETA;

        let timer = null;
        let isRunning = false;

        function gradient(x, y) {
            return [x, 2 * y];
        }

        function direction(angle) {
            const rad = angle * Math.PI / 180;

            return [
                Math.cos(rad),
                Math.sin(rad)
            ];
        }

        function dot(a, b) {
            return a[0] * b[0] + a[1] * b[1];
        }

        function initialize(attempt = 0) {

            const plot = document.querySelector(".js-plotly-plot");
            const get = id => document.getElementById(id);

            const xInput = get("directional-x");
            const yInput = get("directional-y");
            const angleInput = get("directional-angle");

            const xValue = get("directional-x-value");
            const yValue = get("directional-y-value");
            const angleValue = get("directional-angle-value");

            const gradientValue = get("directional-gradient");
            const unitValue = get("directional-unit");
            const derivativeValue = get("directional-value");
            const projectionValue = get("directional-projection");
            const explanation = get("directional-explanation");

            const playButton = get("directional-play");
            const pauseButton = get("directional-pause");
            const resetButton = get("directional-reset");

            const required = [
                plot,
                xInput,
                yInput,
                angleInput,
                xValue,
                yValue,
                angleValue,
                gradientValue,
                unitValue,
                derivativeValue,
                projectionValue,
                explanation,
                playButton,
                pauseButton,
                resetButton
            ];

            if (required.some(element => element === null)) {

                if (attempt < 120) {
                    setTimeout(
                        () => initialize(attempt + 1),
                        50
                    );
                } else {
                    console.error(
                        "Directional derivative controls could not be initialized."
                    );
                }

                return;
            }

            // ------------------------------------------------
            // Update all vectors and values
            // ------------------------------------------------

            function updateGraph() {

                const grad = gradient(x0, y0);
                const u = direction(theta);

                const derivative = dot(grad, u);

                const projection = [
                    derivative * u[0],
                    derivative * u[1]
                ];

                // Gradient vector: trace 0
                Plotly.restyle(
                    plot,
                    {
                        x: [[0, grad[0]]],
                        y: [[0, grad[1]]],
                        text: [["", "∇f"]]
                    },
                    [0]
                );

                // Unit direction vector: trace 1
                Plotly.restyle(
                    plot,
                    {
                        x: [[0, u[0]]],
                        y: [[0, u[1]]],
                        text: [["", "u"]]
                    },
                    [1]
                );

                // Vector projection: trace 2
                Plotly.restyle(
                    plot,
                    {
                        x: [[0, projection[0]]],
                        y: [[0, projection[1]]],
                        text: [["", "projᵤ(∇f)"]]
                    },
                    [2]
                );

                // Perpendicular residual: trace 3
                Plotly.restyle(
                    plot,
                    {
                        x: [[projection[0], grad[0]]],
                        y: [[projection[1], grad[1]]]
                    },
                    [3]
                );

                // Update vector arrowheads
                Plotly.relayout(
                    plot,
                    {
                        annotations: [
                            {
                                x: grad[0],
                                y: grad[1],
                                ax: 0,
                                ay: 0,
                                xref: "x",
                                yref: "y",
                                axref: "x",
                                ayref: "y",
                                showarrow: true,
                                arrowhead: 3,
                                arrowsize: 1.4,
                                arrowwidth: 2,
                                arrowcolor: "#ef4444"
                            },
                            {
                                x: u[0],
                                y: u[1],
                                ax: 0,
                                ay: 0,
                                xref: "x",
                                yref: "y",
                                axref: "x",
                                ayref: "y",
                                showarrow: true,
                                arrowhead: 3,
                                arrowsize: 1.4,
                                arrowwidth: 2,
                                arrowcolor: "#3b82f6"
                            },
                            {
                                x: projection[0],
                                y: projection[1],
                                ax: 0,
                                ay: 0,
                                xref: "x",
                                yref: "y",
                                axref: "x",
                                ayref: "y",
                                showarrow: true,
                                arrowhead: 3,
                                arrowsize: 1.4,
                                arrowwidth: 2,
                                arrowcolor: "#10b981"
                            }
                        ]
                    }
                );

                // Update sliders
                xInput.value = x0;
                yInput.value = y0;
                angleInput.value = theta;

                xValue.textContent = x0.toFixed(2);
                yValue.textContent = y0.toFixed(2);
                angleValue.textContent = theta.toFixed(1) + "°";

                // Update mathematical values
                gradientValue.textContent =
                    "(" + grad[0].toFixed(2) +
                    ", " + grad[1].toFixed(2) + ")";

                unitValue.textContent =
                    "(" + u[0].toFixed(2) +
                    ", " + u[1].toFixed(2) + ")";

                derivativeValue.textContent =
                    derivative.toFixed(4);

                projectionValue.textContent =
                    "(" + projection[0].toFixed(2) +
                    ", " + projection[1].toFixed(2) + ")";

                // Interpret the directional derivative
                let message;

                if (derivative > 0.000001) {
                    message =
                        "Dᵤf = " + derivative.toFixed(4) +
                        ". Hàm số đang tăng theo hướng u. " +
                        "Thành phần của Gradient theo hướng này là dương.";
                } else if (derivative < -0.000001) {
                    message =
                        "Dᵤf = " + derivative.toFixed(4) +
                        ". Hàm số đang giảm theo hướng u. " +
                        "Thành phần của Gradient theo hướng này là âm.";
                } else {
                    message =
                        "Dᵤf = 0.0000. Tại điểm đang xét, " +
                        "tốc độ thay đổi tức thời theo hướng u bằng 0.";
                }

                explanation.textContent = message;
            }

            // ------------------------------------------------
            // Animation controls
            // ------------------------------------------------

            function stopAnimation() {

                if (timer !== null) {
                    clearInterval(timer);
                    timer = null;
                }

                isRunning = false;
            }

            function play() {

                if (isRunning) {
                    return;
                }

                isRunning = true;

                timer = setInterval(function () {

                    theta += 2;

                    if (theta >= 360) {
                        theta = 0;
                    }

                    updateGraph();

                }, 45);
            }

            function pause() {
                stopAnimation();
            }

            function reset() {

                stopAnimation();

                x0 = INITIAL_X;
                y0 = INITIAL_Y;
                theta = INITIAL_THETA;

                updateGraph();
            }

            // ------------------------------------------------
            // Slider events
            // ------------------------------------------------

            xInput.addEventListener("input", function () {
                stopAnimation();
                x0 = parseFloat(xInput.value);
                updateGraph();
            });

            yInput.addEventListener("input", function () {
                stopAnimation();
                y0 = parseFloat(yInput.value);
                updateGraph();
            });

            angleInput.addEventListener("input", function () {
                stopAnimation();
                theta = parseFloat(angleInput.value);
                updateGraph();
            });

            // ------------------------------------------------
            // Button events
            // ------------------------------------------------

            playButton.addEventListener("click", play);
            pauseButton.addEventListener("click", pause);
            resetButton.addEventListener("click", reset);

            updateGraph();
        }

        initialize();

    })();
    """

    # --------------------------------------------------------
    # 6. VIETNAMESE CAPTION
    # --------------------------------------------------------

    caption = """
    <p>
        Với một hàm nhiều biến, <strong>Gradient</strong> (vector gradient)
        tập hợp các đạo hàm riêng và chỉ hướng mà hàm số tăng nhanh nhất.
        Tuy nhiên, trong nhiều tình huống, ta không chỉ muốn biết
        hướng tăng nhanh nhất mà còn muốn biết hàm số thay đổi như thế nào
        theo một hướng cụ thể.
    </p>

    <p>
        Đó là ý nghĩa của <strong>Directional Derivative</strong>
        (đạo hàm theo hướng). Với vector hướng đơn vị
        <strong>u = (cos θ, sin θ)</strong>, đạo hàm theo hướng
        được tính bằng tích vô hướng giữa Gradient và vector hướng:
        <strong>Dᵤf = ∇f · u</strong>.
    </p>

    <p>
        Trong hình minh họa, vector màu đỏ biểu diễn Gradient ∇f;
        vector màu xanh dương biểu diễn hướng đơn vị u.
        Vector màu xanh lá là <strong>vector hình chiếu</strong>
        của Gradient lên hướng u, được tính bằng
        <strong>(∇f · u)u</strong>. Đoạn nét đứt màu xám thể hiện
        thành phần còn lại, vuông góc với hướng u.
    </p>

    <p>
        Cần phân biệt hai khái niệm: <strong>Dᵤf</strong> là một
        giá trị vô hướng, cho biết tốc độ thay đổi của hàm số theo hướng u;
        còn <strong>(∇f · u)u</strong> là một vector, biểu diễn phần
        Gradient nằm dọc theo hướng đó. Hai đại lượng có liên hệ trực tiếp,
        nhưng không phải cùng một thứ.
    </p>

    <p>
        Ta sử dụng hàm số <strong>f(x, y) = 0.5x² + y²</strong>.
        Tại điểm khảo sát <strong>(1, 1)</strong>, Gradient bằng
        <strong>∇f = (1, 2)</strong>. Với hướng đơn vị
        <strong>u = (0.6, 0.8)</strong>, ta thu được:
        <strong>Dᵤf = 1(0.6) + 2(0.8) = 2.2</strong>.
    </p>

    <p>
        Hãy thay đổi tọa độ x₀, y₀ và góc θ để quan sát kết quả.
        Khi Dᵤf dương, hàm số đang tăng theo hướng u; khi Dᵤf âm,
        hàm số đang giảm theo hướng đó; khi Dᵤf bằng 0,
        tốc độ thay đổi tức thời theo hướng đang xét bằng 0.
        Nút <strong>Xoay hướng</strong> giúp bạn quan sát sự thay đổi
        của đạo hàm theo hướng khi vector u quay quanh gốc tọa độ.
    </p>
    """

    caption_html = build_caption_html(
        caption,
        TITLE,
        "16px",
    )

    # --------------------------------------------------------
    # 7. EXPORT HTML
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
