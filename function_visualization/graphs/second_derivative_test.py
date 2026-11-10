
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

GRAPH_ID = "second_derivative_test"
OUTPUT_FILENAME = "second_derivative_test.html"

TITLE = "Second Derivative Test – Đạo hàm cấp hai"

INITIAL_X = -2.0

X_MIN = -2.5
X_MAX = 2.5

Y_MIN = -16.0
Y_MAX = 16.0

LOCAL_MAX_X = -1.0
LOCAL_MIN_X = 1.0
INFLECTION_X = 0.0


# ============================================================
# 2. MATHEMATICAL FUNCTIONS
# ============================================================

def function(x):
    """
    f(x) = x³ - 3x
    """
    x = np.asarray(x)
    return x ** 3 - 3 * x


def first_derivative(x):
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


def classify_concavity(x, tolerance=1e-6):
    """
    Classify the concavity using the second derivative.
    """

    value = float(second_derivative(x))

    if abs(x) < tolerance:
        return (
            "Điểm uốn",
            "f''(0) = 0. Độ cong đổi chiều tại vị trí này."
        )

    if value < 0:
        return (
            "Lõm xuống",
            "f''(x) < 0. Đồ thị có dạng lõm xuống."
        )

    return (
        "Lõm lên",
        "f''(x) > 0. Đồ thị có dạng lõm lên."
    )


def classify_critical_point(x, tolerance=1e-6):
    """
    Apply the second derivative test at known critical points.
    """

    if abs(x - LOCAL_MAX_X) < tolerance:
        return (
            "Cực đại địa phương",
            "f'(-1) = 0 và f''(-1) < 0."
        )

    if abs(x - LOCAL_MIN_X) < tolerance:
        return (
            "Cực tiểu địa phương",
            "f'(1) = 0 và f''(1) > 0."
        )

    return None


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
    y_second = second_derivative(x)

    # Initial observation point
    a = INITIAL_X

    point_y = float(function(a))
    second_value = float(second_derivative(a))

    # --------------------------------------------------------
    # Create figure
    # --------------------------------------------------------

    fig = go.Figure()

    # Trace 0: Original function f(x)
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name="Hàm số f(x) = x³ − 3x",
            line=dict(
                color="#4169e1",
                width=3,
            ),
            hovertemplate=(
                "Hàm số f(x)<br>"
                "x = %{x:.3f}<br>"
                "f(x) = %{y:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 1: Second derivative f''(x)
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y_second,
            mode="lines",
            name="Đạo hàm cấp hai f''(x) = 6x",
            line=dict(
                color="#c026d3",
                width=2.5,
                dash="dash",
            ),
            hovertemplate=(
                "Đạo hàm cấp hai<br>"
                "x = %{x:.3f}<br>"
                "f''(x) = %{y:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 2: Local maximum (-1, 2)
    fig.add_trace(
        go.Scatter(
            x=[LOCAL_MAX_X],
            y=[2],
            mode="markers",
            name="Cực đại địa phương",
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
                "f''(-1) = -6"
                "<extra></extra>"
            ),
        )
    )

    # Trace 3: Local minimum (1, -2)
    fig.add_trace(
        go.Scatter(
            x=[LOCAL_MIN_X],
            y=[-2],
            mode="markers",
            name="Cực tiểu địa phương",
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
                "f''(1) = 6"
                "<extra></extra>"
            ),
        )
    )

    # Trace 4: Inflection point (0, 0)
    fig.add_trace(
        go.Scatter(
            x=[INFLECTION_X],
            y=[0],
            mode="markers",
            name="Điểm uốn",
            marker=dict(
                size=12,
                color="#64748b",
                symbol="x",
                line=dict(width=2),
            ),
            hovertemplate=(
                "Điểm uốn<br>"
                "x = 0<br>"
                "f(x) = 0<br>"
                "f''(0) = 0"
                "<extra></extra>"
            ),
        )
    )

    # Trace 5: Current point on f(x)
    fig.add_trace(
        go.Scatter(
            x=[a],
            y=[point_y],
            mode="markers",
            name="Điểm khảo sát trên f(x)",
            marker=dict(
                size=12,
                color="#f59e0b",
                line=dict(
                    color="white",
                    width=2,
                ),
            ),
            hovertemplate=(
                "Điểm trên hàm số<br>"
                "x = %{x:.4f}<br>"
                "f(x) = %{y:.4f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 6: Current point on f''(x)
    fig.add_trace(
        go.Scatter(
            x=[a],
            y=[second_value],
            mode="markers",
            name="Điểm khảo sát trên f''(x)",
            marker=dict(
                size=11,
                color="#c026d3",
                symbol="diamond",
                line=dict(
                    color="white",
                    width=1.5,
                ),
            ),
            hovertemplate=(
                "Điểm trên đạo hàm cấp hai<br>"
                "x = %{x:.4f}<br>"
                "f''(x) = %{y:.4f}"
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
        xaxis_title="Giá trị x",
        yaxis_title="Giá trị hàm số và đạo hàm cấp hai",
        height=640,
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
            l=80,
            r=35,
            t=115,
            b=75,
        ),
        annotations=[
            dict(
                x=-1.8,
                y=12.5,
                text="f''(x) < 0<br>Lõm xuống",
                showarrow=False,
                font=dict(
                    size=13,
                    color="#dc2626",
                ),
                bgcolor="rgba(255,255,255,0.85)",
            ),
            dict(
                x=1.8,
                y=12.5,
                text="f''(x) > 0<br>Lõm lên",
                showarrow=False,
                font=dict(
                    size=13,
                    color="#16a34a",
                ),
                bgcolor="rgba(255,255,255,0.85)",
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
        dtick=4,
        gridcolor="#e5e7eb",
        zeroline=True,
        zerolinecolor="#64748b",
    )

    # --------------------------------------------------------
    # 4. INTERACTIVE CONTROL PANEL
    # --------------------------------------------------------

    panel_html = """
    <div class="second-derivative-panel">

        <div class="panel-heading">
            <h3>Khám phá đạo hàm cấp hai</h3>

            <p>
                Di chuyển điểm khảo sát để quan sát độ cong
                của đồ thị và giá trị đạo hàm cấp hai.
            </p>
        </div>

        <div class="control-group">

            <div class="control-label">
                <label for="second-x">
                    Vị trí khảo sát x
                </label>

                <strong id="second-x-value">-2.000</strong>
            </div>

            <input
                id="second-x"
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
                <span>Giá trị hàm số f(x)</span>
                <strong id="second-fx">2.000000</strong>
            </div>

            <div class="metric-card">
                <span>Đạo hàm cấp một f'(x)</span>
                <strong id="second-first">9.000000</strong>
            </div>

            <div class="metric-card">
                <span>Đạo hàm cấp hai f''(x)</span>
                <strong id="second-value">-12.000000</strong>
            </div>

            <div class="metric-card">
                <span>Trạng thái độ cong</span>
                <strong id="second-concavity">Lõm xuống</strong>
            </div>

        </div>

        <div id="second-status" class="second-status">
            f''(x) < 0: đồ thị lõm xuống.
        </div>

        <div class="control-buttons">

            <button id="second-play" type="button">
                ▶ Play
            </button>

            <button id="second-pause" type="button">
                ⏸ Pause
            </button>

            <button id="second-reset" type="button">
                ↺ Reset
            </button>

        </div>

        <div class="formula-box">

            <strong>Các công thức đạo hàm</strong>

            <div class="formula">
                f(x) = x³ − 3x
            </div>

            <div class="formula">
                f'(x) = 3x² − 3
            </div>

            <div class="formula">
                f''(x) = 6x
            </div>

        </div>

        <div class="test-box">

            <strong>Kiểm tra đạo hàm cấp hai tại điểm tới hạn</strong>

            <div class="test-row">
                <span>x = −1</span>
                <span class="negative">f''(−1) = −6</span>
                <span>Cực đại</span>
            </div>

            <div class="test-row">
                <span>x = 1</span>
                <span class="positive">f''(1) = 6</span>
                <span>Cực tiểu</span>
            </div>

            <div class="test-row">
                <span>x = 0</span>
                <span class="neutral">f''(0) = 0</span>
                <span>Điểm uốn</span>
            </div>

            <p class="test-note">
                Lưu ý: Kiểm tra đạo hàm cấp hai chỉ phân loại
                cực đại hoặc cực tiểu khi f'(x) = 0.
                Nếu f''(x) = 0, phép kiểm tra này chưa đưa ra
                kết luận về cực trị.
            </p>

        </div>

    </div>

    <style>

        .second-derivative-panel {
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

        .second-status {
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

        #second-pause {
            background: #64748b;
        }

        #second-reset {
            background: #475569;
        }

        .formula-box,
        .test-box {
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

        .test-row {
            display: grid;
            grid-template-columns: 1fr 1.3fr 1fr;
            gap: 8px;
            padding: 12px 0;
            border-bottom: 1px solid #e2e8f0;
            font-size: 13px;
            text-align: center;
        }

        .test-row:last-of-type {
            border-bottom: none;
        }

        .positive {
            color: #16a34a;
            font-weight: 700;
        }

        .negative {
            color: #dc2626;
            font-weight: 700;
        }

        .neutral {
            color: #64748b;
            font-weight: 700;
        }

        .test-note {
            margin: 14px 0 0;
            color: #64748b;
            font-size: 12px;
            line-height: 1.6;
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

            .test-row {
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

            const xInput = get("second-x");
            const xValue = get("second-x-value");

            const fxValue = get("second-fx");
            const firstValue = get("second-first");
            const secondValue = get("second-value");
            const concavityValue = get("second-concavity");

            const status = get("second-status");

            const playButton = get("second-play");
            const pauseButton = get("second-pause");
            const resetButton = get("second-reset");

            const required = [
                plot,
                xInput,
                xValue,
                fxValue,
                firstValue,
                secondValue,
                concavityValue,
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
                        "Second derivative controls could not be initialized."
                    );
                }

                return;
            }

            // ------------------------------------------------
            // Mathematical functions
            // ------------------------------------------------

            function f(x) {
                return x * x * x - 3 * x;
            }

            function df(x) {
                return 3 * x * x - 3;
            }

            function ddf(x) {
                return 6 * x;
            }

            // ------------------------------------------------
            // Update graph and metrics
            // ------------------------------------------------

            function updateGraph() {

                const y = f(currentX);
                const first = df(currentX);
                const second = ddf(currentX);

                // Trace 5: Current point on f(x)
                Plotly.restyle(
                    plot,
                    {
                        x: [[currentX]],
                        y: [[y]]
                    },
                    [5]
                );

                // Trace 6: Current point on f''(x)
                Plotly.restyle(
                    plot,
                    {
                        x: [[currentX]],
                        y: [[second]]
                    },
                    [6]
                );

                // Update numerical values
                xInput.value = currentX;
                xValue.textContent = currentX.toFixed(3);

                fxValue.textContent = y.toFixed(6);
                firstValue.textContent = first.toFixed(6);
                secondValue.textContent = second.toFixed(6);

                const tolerance = 0.005;

                // ------------------------------------------------
                // Concavity classification
                // ------------------------------------------------

                if (Math.abs(currentX) < tolerance) {

                    concavityValue.textContent = "Điểm uốn";

                    status.textContent =
                        "Tại x = 0, f''(0) = 0. " +
                        "Độ cong thay đổi từ lõm xuống sang lõm lên. " +
                        "Đây là điểm uốn, không phải cực đại hay cực tiểu.";

                } else if (second < 0) {

                    concavityValue.textContent = "Lõm xuống";

                    status.textContent =
                        "f''(x) < 0: đồ thị lõm xuống. " +
                        "Độ dốc của tiếp tuyến đang giảm khi x tăng.";

                } else {

                    concavityValue.textContent = "Lõm lên";

                    status.textContent =
                        "f''(x) > 0: đồ thị lõm lên. " +
                        "Độ dốc của tiếp tuyến đang tăng khi x tăng.";

                }

                // ------------------------------------------------
                // Second derivative test at critical points
                // ------------------------------------------------

                if (Math.abs(currentX + 1) < tolerance) {

                    status.textContent +=
                        " Tại đây f'(-1) = 0 và f''(-1) = -6 < 0, " +
                        "nên x = -1 là cực đại địa phương.";

                } else if (Math.abs(currentX - 1) < tolerance) {

                    status.textContent +=
                        " Tại đây f'(1) = 0 và f''(1) = 6 > 0, " +
                        "nên x = 1 là cực tiểu địa phương.";

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
                    "Đang quan sát sự thay đổi độ cong của đồ thị...";

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
        Xét lại hàm số <strong>f(x) = x³ − 3x</strong>.
        Ta đã biết đạo hàm cấp một của hàm số là
        <strong>f'(x) = 3x² − 3</strong> và hai điểm tới hạn
        là <strong>x = −1</strong> và <strong>x = 1</strong>.
    </p>

    <p>
        Lấy đạo hàm thêm một lần nữa, ta thu được đạo hàm cấp hai:
        <strong>f''(x) = 6x</strong>.
        Trong khi đạo hàm cấp một cho biết độ dốc của tiếp tuyến,
        đạo hàm cấp hai cho biết độ dốc đó đang tăng hay giảm,
        qua đó giúp chúng ta nhận biết độ cong của đồ thị.
    </p>

    <p>
        Tại <strong>x = −1</strong>, ta có
        <strong>f'(-1) = 0</strong> và
        <strong>f''(-1) = −6 &lt; 0</strong>.
        Đồ thị lõm xuống tại đây. Theo phép kiểm tra đạo hàm cấp hai,
        x = −1 là điểm cực đại địa phương.
    </p>

    <p>
        Tại <strong>x = 1</strong>, ta có
        <strong>f'(1) = 0</strong> và
        <strong>f''(1) = 6 &gt; 0</strong>.
        Đồ thị lõm lên tại đây. Vì vậy, x = 1 là điểm cực tiểu
        địa phương.
    </p>

    <p>
        Tại <strong>x = 0</strong>, ta có
        <strong>f''(0) = 0</strong>.
        Đây là vị trí độ cong thay đổi từ lõm xuống sang lõm lên.
        Điểm tương ứng (0, 0) là một điểm uốn.
        Lưu ý rằng f''(0) = 0 không tự động chứng minh
        đây là điểm uốn; chúng ta còn phải kiểm tra sự thay đổi độ cong
        ở hai phía của điểm đó.
    </p>

    <p>
        Hãy di chuyển thanh trượt hoặc nhấn Play để khảo sát đồ thị.
        Quan sát đường biểu diễn đạo hàm cấp hai f''(x) = 6x:
        khi đường này nằm dưới trục hoành, đồ thị hàm số lõm xuống;
        khi nó nằm trên trục hoành, đồ thị hàm số lõm lên.
    </p>

    <p>
        <strong>Điều cần ghi nhớ:</strong>
        Tại một điểm tới hạn mà f'(x) = 0, nếu f''(x) &lt; 0
        thì điểm đó là cực đại địa phương; nếu f''(x) &gt; 0
        thì điểm đó là cực tiểu địa phương.
        Nếu f''(x) = 0, phép kiểm tra đạo hàm cấp hai
        không đưa ra kết luận về cực trị.
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
