
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

GRAPH_ID = "derivative_sign_monotonicity"
OUTPUT_FILENAME = "derivative_sign_monotonicity.html"

TITLE = "Dấu đạo hàm và chiều biến thiên của hàm số"

INITIAL_X = -2.0

X_MIN = -2.5
X_MAX = 2.5

Y_MIN = -6.0
Y_MAX = 6.0

CRITICAL_LEFT = -1.0
CRITICAL_RIGHT = 1.0


# ============================================================
# 2. MATHEMATICAL FUNCTIONS
# ============================================================

def function(x):
    """
    f(x) = x³ - 3x
    """
    x = np.asarray(x)
    return x ** 3 - 3 * x


def derivative(x):
    """
    f'(x) = 3x² - 3
    """
    x = np.asarray(x)
    return 3 * x ** 2 - 3


def second_derivative(x):
    """
    f''(x) = 6x
    """
    x = np.asarray(x)
    return 6 * x


def tangent_line(x, a):
    """
    Tangent line at x = a:

        y = f(a) + f'(a)(x-a)
    """
    return function(a) + derivative(a) * (x - a)


def classify_point(x, tolerance=1e-6):
    """
    Determine monotonicity behavior at the current x.
    """

    if abs(x - CRITICAL_LEFT) < tolerance:
        return (
            "Cực đại địa phương",
            "f'(x) = 0. Đạo hàm đổi dấu từ dương sang âm."
        )

    if abs(x - CRITICAL_RIGHT) < tolerance:
        return (
            "Cực tiểu địa phương",
            "f'(x) = 0. Đạo hàm đổi dấu từ âm sang dương."
        )

    slope = float(derivative(x))

    if slope > 0:
        return (
            "Hàm số đồng biến",
            "f'(x) > 0. Hàm số đang tăng."
        )

    if slope < 0:
        return (
            "Hàm số nghịch biến",
            "f'(x) < 0. Hàm số đang giảm."
        )

    return (
        "Điểm tới hạn",
        "Đạo hàm bằng 0."
    )


# ============================================================
# 3. BUILD GRAPH
# ============================================================

def build(output_dir: Path):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # Generate function data
    # --------------------------------------------------------

    x = np.linspace(X_MIN, X_MAX, 600)
    y = function(x)

    # Initial observation point
    a = INITIAL_X

    point_y = float(function(a))
    slope = float(derivative(a))

    tangent_x = np.linspace(a - 0.7, a + 0.7, 100)
    tangent_y = tangent_line(tangent_x, a)

    # --------------------------------------------------------
    # Create figure
    # --------------------------------------------------------

    fig = go.Figure()

    # Trace 0: Cubic function
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name="Đồ thị f(x) = x³ − 3x",
            line=dict(
                color="#4169e1",
                width=3,
            ),
            hovertemplate=(
                "x = %{x:.3f}<br>"
                "f(x) = %{y:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 1: Tangent line at current point
    fig.add_trace(
        go.Scatter(
            x=tangent_x,
            y=tangent_y,
            mode="lines",
            name="Tiếp tuyến tại điểm khảo sát",
            line=dict(
                color="#f59e0b",
                width=2.5,
                dash="dash",
            ),
            hovertemplate=(
                "Tiếp tuyến<br>"
                "y = %{y:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 2: Local maximum (-1, 2)
    fig.add_trace(
        go.Scatter(
            x=[CRITICAL_LEFT],
            y=[2],
            mode="markers+text",
            name="Cực đại địa phương (-1, 2)",
            text=["Cực đại"],
            textposition="top center",
            marker=dict(
                size=13,
                color="#ef4444",
                line=dict(
                    color="white",
                    width=2,
                ),
            ),
            hovertemplate=(
                "Cực đại địa phương<br>"
                "x = -1<br>"
                "f(x) = 2<br>"
                "f'(x) = 0"
                "<extra></extra>"
            ),
        )
    )

    # Trace 3: Local minimum (1, -2)
    fig.add_trace(
        go.Scatter(
            x=[CRITICAL_RIGHT],
            y=[-2],
            mode="markers+text",
            name="Cực tiểu địa phương (1, -2)",
            text=["Cực tiểu"],
            textposition="bottom center",
            marker=dict(
                size=13,
                color="#10b981",
                line=dict(
                    color="white",
                    width=2,
                ),
            ),
            hovertemplate=(
                "Cực tiểu địa phương<br>"
                "x = 1<br>"
                "f(x) = -2<br>"
                "f'(x) = 0"
                "<extra></extra>"
            ),
        )
    )

    # Trace 4: Current observation point
    fig.add_trace(
        go.Scatter(
            x=[a],
            y=[point_y],
            mode="markers",
            name="Điểm đang khảo sát",
            marker=dict(
                size=12,
                color="#f59e0b",
                line=dict(
                    color="white",
                    width=2,
                ),
            ),
            hovertemplate=(
                "Điểm khảo sát<br>"
                "x = %{x:.4f}<br>"
                "f(x) = %{y:.4f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 5: Vertical guide
    fig.add_trace(
        go.Scatter(
            x=[a, a],
            y=[0, point_y],
            mode="lines",
            name="Vị trí x đang khảo sát",
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
        xaxis_title="Giá trị x",
        yaxis_title="Giá trị f(x)",
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
            font=dict(size=10),
        ),
        margin=dict(
            l=75,
            r=35,
            t=115,
            b=75,
        ),
        annotations=[
            dict(
                x=-1.9,
                y=4.8,
                text="f'(x) > 0<br>Đồng biến",
                showarrow=False,
                font=dict(
                    size=13,
                    color="#16a34a",
                ),
                bgcolor="rgba(255,255,255,0.8)",
            ),
            dict(
                x=0,
                y=-4.8,
                text="f'(x) < 0<br>Nghịch biến",
                showarrow=False,
                font=dict(
                    size=13,
                    color="#ef4444",
                ),
                bgcolor="rgba(255,255,255,0.8)",
            ),
            dict(
                x=1.9,
                y=4.8,
                text="f'(x) > 0<br>Đồng biến",
                showarrow=False,
                font=dict(
                    size=13,
                    color="#16a34a",
                ),
                bgcolor="rgba(255,255,255,0.8)",
            ),
        ],
    )

    fig.update_xaxes(
        range=[X_MIN, X_MAX],
        dtick=1,
        gridcolor="#e5e7eb",
        zeroline=True,
        zerolinecolor="#64748b",
    )

    fig.update_yaxes(
        range=[Y_MIN, Y_MAX],
        dtick=2,
        gridcolor="#e5e7eb",
        zeroline=True,
        zerolinecolor="#64748b",
    )

    # --------------------------------------------------------
    # 4. INTERACTIVE CONTROL PANEL
    # --------------------------------------------------------

    panel_html = """
    <div class="monotonicity-panel">

        <div class="panel-heading">
            <h3>Khám phá dấu đạo hàm</h3>
            <p>
                Di chuyển điểm khảo sát trên đồ thị để xem
                dấu của đạo hàm cho biết hàm số đang tăng hay giảm.
            </p>
        </div>

        <div class="control-group">

            <div class="control-label">
                <label for="mono-x">
                    Vị trí khảo sát x
                </label>

                <strong id="mono-x-value">-2.000</strong>
            </div>

            <input
                id="mono-x"
                type="range"
                min="-2.5"
                max="2.5"
                step="0.01"
                value="-2"
            />

            <div class="range-hints">
                <span>-2.5</span>
                <span>-1</span>
                <span>0</span>
                <span>1</span>
                <span>2.5</span>
            </div>

        </div>

        <div class="metrics-grid">

            <div class="metric-card">
                <span>Giá trị f(x)</span>
                <strong id="mono-fx">2.000000</strong>
            </div>

            <div class="metric-card">
                <span>Đạo hàm f'(x)</span>
                <strong id="mono-derivative">9.000000</strong>
            </div>

            <div class="metric-card">
                <span>Dấu đạo hàm</span>
                <strong id="mono-sign">Dương (+)</strong>
            </div>

            <div class="metric-card">
                <span>Chiều biến thiên</span>
                <strong id="mono-behavior">Đồng biến</strong>
            </div>

        </div>

        <div id="mono-status" class="mono-status">
            Đạo hàm dương: hàm số đang đồng biến.
        </div>

        <div class="control-buttons">

            <button id="mono-play" type="button">
                ▶ Play
            </button>

            <button id="mono-pause" type="button">
                ⏸ Pause
            </button>

            <button id="mono-reset" type="button">
                ↺ Reset
            </button>

        </div>

        <div class="formula-box">

            <strong>Hàm số và đạo hàm</strong>

            <div class="formula">
                f(x) = x³ − 3x
            </div>

            <div class="formula">
                f'(x) = 3x² − 3
            </div>

            <div class="formula">
                f'(x) = 3(x − 1)(x + 1)
            </div>

        </div>

        <div class="interval-box">

            <strong>Bảng dấu đạo hàm</strong>

            <div class="interval-row">
                <span>x < -1</span>
                <span class="positive">f'(x) > 0</span>
                <span>Đồng biến</span>
            </div>

            <div class="interval-row">
                <span>-1 < x < 1</span>
                <span class="negative">f'(x) < 0</span>
                <span>Nghịch biến</span>
            </div>

            <div class="interval-row">
                <span>x > 1</span>
                <span class="positive">f'(x) > 0</span>
                <span>Đồng biến</span>
            </div>

        </div>

    </div>

    <style>

        .monotonicity-panel {
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

        .control-group {
            margin-bottom: 20px;
        }

        .control-label {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
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
            font-size: 17px;
            overflow-wrap: anywhere;
            font-variant-numeric: tabular-nums;
        }

        .mono-status {
            padding: 13px 14px;
            background: #eff6ff;
            border-radius: 8px;
            color: #1d4ed8;
            font-size: 13px;
            line-height: 1.6;
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

        #mono-pause {
            background: #64748b;
        }

        #mono-reset {
            background: #475569;
        }

        .formula-box,
        .interval-box {
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

        .interval-row {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 8px;
            padding: 11px 0;
            border-bottom: 1px solid #e2e8f0;
            font-size: 13px;
            text-align: center;
        }

        .interval-row:last-child {
            border-bottom: none;
        }

        .positive {
            color: #16a34a;
            font-weight: 700;
        }

        .negative {
            color: #ef4444;
            font-weight: 700;
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

            .interval-row {
                font-size: 11px;
                gap: 4px;
            }

        }

    </style>
    """

    # --------------------------------------------------------
    # 5. JAVASCRIPT: INTERACTION AND ANIMATION
    # --------------------------------------------------------

    post_script = r"""
    (function () {

        const INITIAL_X = -2.0;
        const MIN_X = -2.5;
        const MAX_X = 2.5;

        let currentX = INITIAL_X;
        let timer = null;
        let isRunning = false;

        function initialize(attempt = 0) {

            const plot = document.querySelector(".js-plotly-plot");
            const get = (id) => document.getElementById(id);

            const xInput = get("mono-x");
            const xValue = get("mono-x-value");

            const fxValue = get("mono-fx");
            const derivativeValue = get("mono-derivative");
            const signValue = get("mono-sign");
            const behaviorValue = get("mono-behavior");

            const status = get("mono-status");

            const playButton = get("mono-play");
            const pauseButton = get("mono-pause");
            const resetButton = get("mono-reset");

            const required = [
                plot,
                xInput,
                xValue,
                fxValue,
                derivativeValue,
                signValue,
                behaviorValue,
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
                        "Monotonicity controls could not be initialized."
                    );
                }

                return;
            }

            // ------------------------------------------------
            // Mathematical calculations
            // ------------------------------------------------

            function f(x) {
                return x * x * x - 3 * x;
            }

            function df(x) {
                return 3 * x * x - 3;
            }

            // ------------------------------------------------
            // Update graph and information
            // ------------------------------------------------

            function updateGraph() {

                const y = f(currentX);
                const slope = df(currentX);

                // Tangent line:
                // y = f(a) + f'(a)(x-a)
                const tangentX = Array.from(
                    { length: 100 },
                    (_, i) => currentX - 0.7 + (1.4 * i / 99)
                );

                const tangentY = tangentX.map(
                    x => y + slope * (x - currentX)
                );

                // Trace 1: Tangent line
                Plotly.restyle(
                    plot,
                    {
                        x: [tangentX],
                        y: [tangentY]
                    },
                    [1]
                );

                // Trace 4: Current point
                Plotly.restyle(
                    plot,
                    {
                        x: [[currentX]],
                        y: [[y]]
                    },
                    [4]
                );

                // Trace 5: Vertical guide
                Plotly.restyle(
                    plot,
                    {
                        x: [[currentX, currentX]],
                        y: [[0, y]]
                    },
                    [5]
                );

                // Update numerical values
                xInput.value = currentX;
                xValue.textContent = currentX.toFixed(3);

                fxValue.textContent = y.toFixed(6);
                derivativeValue.textContent = slope.toFixed(6);

                const tolerance = 0.005;

                // ------------------------------------------------
                // Classify derivative sign and behavior
                // ------------------------------------------------

                if (Math.abs(currentX + 1) < tolerance) {

                    signValue.textContent = "Bằng 0";
                    behaviorValue.textContent = "Cực đại";

                    status.textContent =
                        "Tại x = -1, f'(x) = 0. " +
                        "Đạo hàm đổi dấu từ dương sang âm: " +
                        "đây là điểm cực đại địa phương.";

                } else if (Math.abs(currentX - 1) < tolerance) {

                    signValue.textContent = "Bằng 0";
                    behaviorValue.textContent = "Cực tiểu";

                    status.textContent =
                        "Tại x = 1, f'(x) = 0. " +
                        "Đạo hàm đổi dấu từ âm sang dương: " +
                        "đây là điểm cực tiểu địa phương.";

                } else if (slope > 0) {

                    signValue.textContent = "Dương (+)";
                    behaviorValue.textContent = "Đồng biến";

                    status.textContent =
                        "f'(x) > 0: tiếp tuyến có độ dốc dương. " +
                        "Hàm số đang đồng biến.";

                } else {

                    signValue.textContent = "Âm (−)";
                    behaviorValue.textContent = "Nghịch biến";

                    status.textContent =
                        "f'(x) < 0: tiếp tuyến có độ dốc âm. " +
                        "Hàm số đang nghịch biến.";

                }
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
            // Scan from left to right
            // ------------------------------------------------

            function step() {

                currentX += 0.025;

                if (currentX >= MAX_X) {
                    currentX = MAX_X;

                    updateGraph();
                    stopAnimation();

                    status.textContent =
                        "Đã khảo sát toàn bộ đồ thị từ trái sang phải.";

                    return;
                }

                updateGraph();
            }

            // ------------------------------------------------
            // Play
            // ------------------------------------------------

            function play() {

                if (isRunning) {
                    return;
                }

                if (currentX >= MAX_X) {
                    currentX = MIN_X;
                    updateGraph();
                }

                isRunning = true;

                status.textContent =
                    "Đang di chuyển điểm khảo sát từ trái sang phải...";

                timer = setInterval(step, 35);
            }

            // ------------------------------------------------
            // Pause
            // ------------------------------------------------

            function pause() {

                stopAnimation();

                status.textContent =
                    "Đã tạm dừng tại x = " + currentX.toFixed(3) + ".";
            }

            // ------------------------------------------------
            // Reset
            // ------------------------------------------------

            function reset() {

                stopAnimation();

                currentX = INITIAL_X;

                updateGraph();
            }

            // ------------------------------------------------
            // Manual slider
            // ------------------------------------------------

            xInput.addEventListener(
                "input",
                function () {

                    stopAnimation();

                    currentX = parseFloat(xInput.value);

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
        Xét hàm số <strong>f(x) = x³ − 3x</strong>.
        Đạo hàm cấp một của hàm số là
        <strong>f'(x) = 3x² − 3 = 3(x − 1)(x + 1)</strong>.
        Dấu của đạo hàm cho chúng ta biết hàm số đang đồng biến
        hay nghịch biến trên từng khoảng.
    </p>

    <p>
        Khi <strong>x &lt; −1</strong> hoặc <strong>x &gt; 1</strong>,
        đạo hàm dương, tức là <strong>f'(x) &gt; 0</strong>.
        Hàm số đồng biến: khi x tăng, giá trị f(x) cũng tăng.
    </p>

    <p>
        Khi <strong>−1 &lt; x &lt; 1</strong>,
        đạo hàm âm, tức là <strong>f'(x) &lt; 0</strong>.
        Hàm số nghịch biến: khi x tăng, giá trị f(x) giảm.
    </p>

    <p>
        Tại <strong>x = −1</strong>, đạo hàm bằng 0 và đổi dấu
        từ dương sang âm. Hàm số chuyển từ đồng biến sang
        nghịch biến, vì vậy đây là điểm cực đại địa phương
        với tọa độ <strong>(−1, 2)</strong>.
    </p>

    <p>
        Tại <strong>x = 1</strong>, đạo hàm cũng bằng 0 nhưng
        đổi dấu từ âm sang dương. Hàm số chuyển từ nghịch biến
        sang đồng biến, vì vậy đây là điểm cực tiểu địa phương
        với tọa độ <strong>(1, −2)</strong>.
    </p>

    <p>
        Hãy di chuyển thanh trượt hoặc nhấn Play để quan sát
        điểm khảo sát di chuyển trên đồ thị. Tiếp tuyến và giá trị
        đạo hàm sẽ thay đổi theo vị trí của điểm đó.
    </p>

    <p>
        <strong>Điều cần ghi nhớ:</strong>
        Dấu của đạo hàm cho biết chiều biến thiên của hàm số.
        Khi đạo hàm đổi dấu từ dương sang âm, ta có cực đại địa phương.
        Khi đạo hàm đổi dấu từ âm sang dương, ta có cực tiểu địa phương.
        Chỉ riêng điều kiện f'(x) = 0 chưa đủ để kết luận
        một điểm là cực đại hay cực tiểu.
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
