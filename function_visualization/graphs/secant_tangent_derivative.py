
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

GRAPH_ID = "secant_tangent_derivative"
OUTPUT_FILENAME = "secant_tangent_derivative.html"

TITLE = "Derivative as the Slope of a Tangent Line"

A = 1.0
INITIAL_H = 0.8
MIN_H = 0.01
MAX_H = 1.5

X_MIN = -0.5
X_MAX = 2.5


# ============================================================
# 2. MATHEMATICAL FUNCTIONS
# ============================================================

def function(x):
    """
    f(x) = x²
    """
    return x ** 2


def derivative(x):
    """
    f'(x) = 2x
    """
    return 2 * x


def secant_slope(a, h):
    """
    Slope of the secant line through:

        P = (a, f(a))
        Q = (a + h, f(a + h))

    m_secant = [f(a+h) - f(a)] / h

    h must not be zero.
    """

    if np.isclose(h, 0.0):
        raise ValueError(
            "h phải khác 0 khi tính độ dốc đường cát tuyến."
        )

    return (
        function(a + h) - function(a)
    ) / h


def tangent_line(x, a):
    """
    Tangent line at x = a:

        y = f(a) + f'(a)(x-a)
    """

    return function(a) + derivative(a) * (x - a)


def secant_line(x, a, h):
    """
    Secant line through P and Q.
    """

    slope = secant_slope(a, h)

    return function(a) + slope * (x - a)


# ============================================================
# 3. BUILD GRAPH
# ============================================================

def build(output_dir: Path):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    x = np.linspace(X_MIN, X_MAX, 500)
    y = function(x)

    tangent_y = tangent_line(x, A)

    initial_h = INITIAL_H
    initial_q_x = A + initial_h
    initial_q_y = function(initial_q_x)

    initial_slope = secant_slope(A, initial_h)
    initial_secant_y = secant_line(x, A, initial_h)

    tangent_slope = derivative(A)

    # --------------------------------------------------------
    # Create figure
    # --------------------------------------------------------

    fig = go.Figure()

    # Trace 0: Parabola
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name="Đồ thị f(x) = x²",
            line=dict(
                color="#2689e8",
                width=3,
            ),
            hovertemplate=(
                "x = %{x:.3f}<br>"
                "f(x) = %{y:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 1: Tangent line at P
    fig.add_trace(
        go.Scatter(
            x=x,
            y=tangent_y,
            mode="lines",
            name="Tangent Line – y = 2x − 1",
            line=dict(
                color="#ef4444",
                width=2.5,
                dash="dash",
            ),
            hovertemplate=(
                "Tiếp tuyến tại P<br>"
                "y = %{y:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 2: Secant line
    fig.add_trace(
        go.Scatter(
            x=x,
            y=initial_secant_y,
            mode="lines",
            name="Secant Line",
            line=dict(
                color="#f97316",
                width=2.5,
            ),
            hovertemplate=(
                "Đường cát tuyến<br>"
                "y = %{y:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 3: Fixed point P
    fig.add_trace(
        go.Scatter(
            x=[A],
            y=[function(A)],
            mode="markers+text",
            name="Điểm cố định P",
            text=["P (1, 1)"],
            textposition="bottom left",
            marker=dict(
                size=13,
                color="#16a34a",
                line=dict(
                    color="white",
                    width=2,
                ),
            ),
            hovertemplate=(
                "Điểm cố định P<br>"
                "x = 1<br>"
                "f(x) = 1"
                "<extra></extra>"
            ),
        )
    )

    # Trace 4: Moving point Q
    fig.add_trace(
        go.Scatter(
            x=[initial_q_x],
            y=[initial_q_y],
            mode="markers+text",
            name="Điểm di chuyển Q",
            text=["Q"],
            textposition="top right",
            marker=dict(
                size=13,
                color="#f59e0b",
                line=dict(
                    color="white",
                    width=2,
                ),
            ),
            hovertemplate=(
                "Điểm Q<br>"
                "x = %{x:.5f}<br>"
                "f(x) = %{y:.5f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 5: Difference between P and Q
    fig.add_trace(
        go.Scatter(
            x=[A, initial_q_x],
            y=[function(A), initial_q_y],
            mode="lines",
            name="Khoảng dịch chuyển từ P đến Q",
            line=dict(
                color="#94a3b8",
                width=1.5,
                dash="dot",
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
        xaxis_title="x",
        yaxis_title="f(x)",
        height=620,
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
            l=75,
            r=35,
            t=115,
            b=75,
        ),
    )

    fig.update_xaxes(
        range=[X_MIN, X_MAX],
        dtick=0.5,
        gridcolor="#e5e7eb",
        zeroline=True,
        zerolinecolor="#94a3b8",
    )

    fig.update_yaxes(
        range=[-1, 7],
        dtick=1,
        gridcolor="#e5e7eb",
        zeroline=True,
        zerolinecolor="#94a3b8",
    )

    # --------------------------------------------------------
    # 4. INTERACTIVE CONTROL PANEL
    # --------------------------------------------------------

    panel_html = """
    <div class="secant-panel">

        <div class="panel-heading">
            <h3>Khám phá sự hình thành đường tiếp tuyến</h3>
            <p>
                Giữ P cố định tại (1, 1), sau đó di chuyển Q
                bằng cách điều chỉnh h.
            </p>
        </div>

        <div class="direction-control">

            <label for="secant-direction">
                Hướng di chuyển của Q
            </label>

            <select id="secant-direction">
                <option value="right">
                    Từ bên phải (h > 0)
                </option>
                <option value="left">
                    Từ bên trái (h < 0)
                </option>
            </select>

        </div>

        <div class="control-group">

            <div class="control-label">
                <label for="secant-h">
                    Khoảng cách h = |xQ − xP|
                </label>

                <strong id="secant-h-value">0.800</strong>
            </div>

            <input
                id="secant-h"
                type="range"
                min="0.01"
                max="1.5"
                step="0.01"
                value="0.8"
            />

            <div class="range-hints">
                <span>0.01 – Gần P</span>
                <span>1.5 – Xa P</span>
            </div>

        </div>

        <div class="metrics-grid">

            <div class="metric-card">
                <span>Hoành độ xQ</span>
                <strong id="secant-qx">1.800000</strong>
            </div>

            <div class="metric-card">
                <span>Độ dốc Secant</span>
                <strong id="secant-slope">2.800000</strong>
            </div>

            <div class="metric-card">
                <span>Độ dốc Tangent</span>
                <strong id="secant-tangent">2.000000</strong>
            </div>

            <div class="metric-card">
                <span>Sai lệch độ dốc</span>
                <strong id="secant-error">0.800000</strong>
            </div>

        </div>

        <div class="control-buttons">

            <button id="secant-play" type="button">
                ▶ Play
            </button>

            <button id="secant-pause" type="button">
                ⏸ Pause
            </button>

            <button id="secant-reset" type="button">
                ↺ Reset
            </button>

        </div>

        <div id="secant-status" class="secant-status">
            Điểm Q đang ở bên phải P. Nhấn Play để đưa Q tiến gần P.
        </div>

        <div class="formula-box">

            <strong>Độ dốc của đường cát tuyến</strong>

            <div class="formula">
                m<sub>secant</sub> =
                [f(1+h) − f(1)] / h
            </div>

            <div class="formula">
                = 2 + h
            </div>

            <div class="formula-note">
                Khi h tiến về 0, độ dốc đường cát tuyến tiến về 2.
            </div>

        </div>

    </div>

    <style>

        .secant-panel {
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
            margin: 0 0 20px;
            color: #64748b;
            font-size: 14px;
            line-height: 1.6;
        }

        .direction-control {
            display: flex;
            flex-direction: column;
            gap: 9px;
            margin-bottom: 20px;
        }

        .direction-control label {
            font-size: 14px;
            font-weight: 600;
        }

        .direction-control select {
            width: 100%;
            max-width: 350px;
            padding: 10px 12px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            background: white;
            color: #1e293b;
            font-size: 14px;
        }

        .control-group {
            margin-bottom: 20px;
        }

        .control-label {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: center;
            margin-bottom: 10px;
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

        .range-hints {
            display: flex;
            justify-content: space-between;
            margin-top: 5px;
            color: #94a3b8;
            font-size: 11px;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin: 20px 0;
        }

        .metric-card {
            display: flex;
            flex-direction: column;
            gap: 8px;
            padding: 13px;
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
            font-size: 18px;
            overflow-wrap: anywhere;
            font-variant-numeric: tabular-nums;
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
            padding: 10px 18px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            color: white;
            background: #2563eb;
        }

        .control-buttons button:hover {
            opacity: 0.85;
        }

        #secant-pause {
            background: #64748b;
        }

        #secant-reset {
            background: #475569;
        }

        .secant-status {
            padding: 13px 14px;
            background: #eff6ff;
            border-radius: 8px;
            color: #1d4ed8;
            font-size: 13px;
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
            font-size: 19px;
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

            .metric-card {
                flex-direction: row;
                justify-content: space-between;
                align-items: center;
            }

        }

    </style>
    """

    # --------------------------------------------------------
    # 5. JAVASCRIPT: INTERACTION AND ANIMATION
    # --------------------------------------------------------

    post_script = r"""
    (function () {

        const A = 1;
        const INITIAL_H = 0.8;
        const MIN_H = 0.01;

        let h = INITIAL_H;
        let direction = "right";

        let timer = null;
        let isRunning = false;

        function initialize(attempt = 0) {

            const plot = document.querySelector(".js-plotly-plot");
            const get = (id) => document.getElementById(id);

            const directionInput = get("secant-direction");
            const hInput = get("secant-h");
            const hValue = get("secant-h-value");

            const qxValue = get("secant-qx");
            const slopeValue = get("secant-slope");
            const tangentValue = get("secant-tangent");
            const errorValue = get("secant-error");

            const status = get("secant-status");

            const playButton = get("secant-play");
            const pauseButton = get("secant-pause");
            const resetButton = get("secant-reset");

            const required = [
                plot,
                directionInput,
                hInput,
                hValue,
                qxValue,
                slopeValue,
                tangentValue,
                errorValue,
                status,
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
                        "Secant-Tangent controls could not be initialized."
                    );
                }

                return;
            }

            // ------------------------------------------------
            // Calculate Q and secant slope
            // ------------------------------------------------

            function getSignedH() {
                return direction === "right" ? h : -h;
            }

            function updateGraph() {

                const signedH = getSignedH();

                const qx = A + signedH;
                const qy = qx * qx;

                // Difference quotient:
                // ((1+h)² - 1) / h = 2 + h
                const secantSlope = 2 + signedH;

                // Tangent at x = 1:
                // f'(1) = 2
                const tangentSlope = 2;

                const error = Math.abs(
                    secantSlope - tangentSlope
                );

                // Secant line:
                // y = 1 + (2+h)(x-1)
                const secantY = [
                    1 + secantSlope * (-0.5 - 1),
                    1 + secantSlope * (2.5 - 1)
                ];

                Plotly.restyle(
                    plot,
                    {
                        y: [[
                            1 + secantSlope * (-0.5 - 1),
                            1 + secantSlope * (2.5 - 1)
                        ]]
                    },
                    [2]
                );

                // Moving point Q
                Plotly.restyle(
                    plot,
                    {
                        x: [[qx]],
                        y: [[qy]]
                    },
                    [4]
                );

                // Segment connecting P and Q
                Plotly.restyle(
                    plot,
                    {
                        x: [[A, qx]],
                        y: [[1, qy]]
                    },
                    [5]
                );

                hValue.textContent = h.toFixed(3);
                qxValue.textContent = qx.toFixed(6);

                slopeValue.textContent =
                    secantSlope.toFixed(6);

                tangentValue.textContent =
                    tangentSlope.toFixed(6);

                errorValue.textContent =
                    error.toFixed(6);

                status.textContent =
                    direction === "right"
                    ? "Q đang tiến đến P từ bên phải. " +
                      "Độ dốc cát tuyến đang tiến về 2."
                    : "Q đang tiến đến P từ bên trái. " +
                      "Độ dốc cát tuyến đang tiến về 2.";
            }

            // ------------------------------------------------
            // Stop animation
            // ------------------------------------------------

            function stopAnimation() {

                if (timer !== null) {
                    clearInterval(timer);
                    timer = null;
                }

                isRunning = false;
            }

            // ------------------------------------------------
            // One animation step
            // ------------------------------------------------

            function step() {

                h = h * 0.8;

                if (h <= MIN_H) {

                    h = MIN_H;

                    hInput.value = h;

                    updateGraph();

                    stopAnimation();

                    status.textContent =
                        "Q đã tiến rất gần P. " +
                        "Độ dốc cát tuyến gần bằng 2, " +
                        "chính là độ dốc tiếp tuyến.";

                    return;
                }

                hInput.value = h;

                updateGraph();
            }

            // ------------------------------------------------
            // Play
            // ------------------------------------------------

            function play() {

                if (isRunning) {
                    return;
                }

                if (h <= MIN_H) {
                    status.textContent =
                        "Đã gần đến giới hạn. Nhấn Reset để chạy lại.";
                    return;
                }

                isRunning = true;

                status.textContent =
                    "Đang đưa Q tiến gần P...";

                timer = setInterval(step, 350);
            }

            // ------------------------------------------------
            // Pause
            // ------------------------------------------------

            function pause() {

                stopAnimation();

                status.textContent =
                    "Đã tạm dừng. Bạn có thể tiếp tục điều chỉnh h.";
            }

            // ------------------------------------------------
            // Reset
            // ------------------------------------------------

            function reset() {

                stopAnimation();

                h = INITIAL_H;
                hInput.value = h;

                updateGraph();

                status.textContent =
                    "Đã đặt lại mô phỏng.";
            }

            // ------------------------------------------------
            // Direction control
            // ------------------------------------------------

            directionInput.addEventListener(
                "change",
                function () {

                    stopAnimation();

                    direction = directionInput.value;

                    updateGraph();
                }
            );

            // ------------------------------------------------
            // Manual h control
            // ------------------------------------------------

            hInput.addEventListener(
                "input",
                function () {

                    stopAnimation();

                    h = parseFloat(hInput.value);

                    updateGraph();
                }
            );

            // ------------------------------------------------
            // Buttons
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
        Xét hàm số <strong>f(x) = x²</strong> và điểm cố định
        <strong>P = (1, 1)</strong> trên đồ thị.
        Chúng ta muốn tìm độ dốc của đồ thị tại điểm P.
    </p>

    <p>
        Để làm điều đó, hãy lấy thêm một điểm Q trên đồ thị,
        với hoành độ x = 1 + h.
        Đường thẳng đi qua P và Q được gọi là
        <strong>đường cát tuyến (Secant Line)</strong>.
    </p>

    <p>
        Độ dốc của đường cát tuyến được tính bằng thương sai phân:
        <strong>[f(1+h) − f(1)] / h = 2 + h</strong>.
        Khi h thay đổi, điểm Q di chuyển và đường cát tuyến
        cũng thay đổi độ nghiêng.
    </p>

    <p>
        Hãy điều chỉnh h hoặc chạy animation để đưa Q tiến gần P.
        Khi h tiến về 0, đường cát tuyến dần tiến đến vị trí
        của <strong>đường tiếp tuyến (Tangent Line)</strong>
        tại P.
    </p>

    <p>
        Đường tiếp tuyến có độ dốc bằng đạo hàm tại x = 1.
        Vì f'(x) = 2x nên f'(1) = 2.
        Đây chính là giá trị mà độ dốc của đường cát tuyến
        tiến đến khi h tiến về 0.
    </p>

    <p>
        <strong>Điều cần ghi nhớ:</strong>
        Đạo hàm tại một điểm không phải là độ dốc của một
        đường cát tuyến bất kỳ. Nó là giới hạn của độ dốc
        các đường cát tuyến khi điểm Q tiến đến P.
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
