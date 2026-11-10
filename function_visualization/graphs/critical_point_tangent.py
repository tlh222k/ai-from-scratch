
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

GRAPH_ID = "critical_point_tangent"
OUTPUT_FILENAME = "critical_point_tangent.html"

TITLE = "Critical Point: Horizontal Tangent"

INITIAL_A = 2.5
MIN_A = -2.5
MAX_A = 2.5

X_MIN = -3.0
X_MAX = 3.0
Y_MIN = -1.0
Y_MAX = 9.0


# ============================================================
# 2. MATHEMATICAL FUNCTIONS
# ============================================================

def function(x):
    """
    f(x) = x²
    """
    return np.asarray(x) ** 2


def derivative(x):
    """
    f'(x) = 2x
    """
    return 2 * np.asarray(x)


def tangent_line(x, a):
    """
    Tangent line at x = a:

        y = f(a) + f'(a)(x - a)

    For f(x) = x²:

        y = a² + 2a(x - a)
        y = 2ax - a²
    """
    return function(a) + derivative(a) * (x - a)


# ============================================================
# 3. BUILD GRAPH
# ============================================================

def build(output_dir: Path):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # Generate parabola
    # --------------------------------------------------------

    x = np.linspace(X_MIN, X_MAX, 500)
    y = function(x)

    # Initial observation point
    a = INITIAL_A
    point_y = float(function(a))
    slope = float(derivative(a))

    # Tangent segment centered around the observation point
    tangent_x = np.linspace(a - 1.5, a + 1.5, 100)
    tangent_y = tangent_line(tangent_x, a)

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

    # Trace 1: Tangent line
    fig.add_trace(
        go.Scatter(
            x=tangent_x,
            y=tangent_y,
            mode="lines",
            name="Tiếp tuyến tại điểm khảo sát",
            line=dict(
                color="#ef4444",
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

    # Trace 2: Critical point (0, 0)
    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers",
            name="Điểm cực tiểu (0, 0)",
            marker=dict(
                size=14,
                color="#ef4444",
                line=dict(
                    color="white",
                    width=2,
                ),
            ),
            hovertemplate=(
                "Điểm cực tiểu<br>"
                "x = 0<br>"
                "f(x) = 0<br>"
                "f'(x) = 0"
                "<extra></extra>"
            ),
        )
    )

    # Trace 3: Current observation point
    fig.add_trace(
        go.Scatter(
            x=[a],
            y=[point_y],
            mode="markers",
            name="Điểm đang khảo sát",
            marker=dict(
                size=13,
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

    # Trace 4: Vertical guide
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
        height=590,
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
            t=110,
            b=75,
        ),
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
        dtick=1,
        gridcolor="#e5e7eb",
        zeroline=True,
        zerolinecolor="#64748b",
    )

    # --------------------------------------------------------
    # 4. INTERACTIVE CONTROL PANEL
    # --------------------------------------------------------

    panel_html = """
    <div class="critical-panel">

        <div class="panel-heading">
            <h3>Khám phá điểm cực tiểu và tiếp tuyến</h3>
            <p>
                Di chuyển điểm khảo sát trên parabol để quan sát
                sự thay đổi độ dốc của tiếp tuyến.
            </p>
        </div>

        <div class="control-group">

            <div class="control-label">
                <label for="critical-a">
                    Vị trí tiếp xúc a
                </label>

                <strong id="critical-a-value">2.500</strong>
            </div>

            <input
                id="critical-a"
                type="range"
                min="-2.5"
                max="2.5"
                step="0.01"
                value="2.5"
            />

            <div class="range-hints">
                <span>a = -2.5</span>
                <span>a = 0</span>
                <span>a = 2.5</span>
            </div>

        </div>

        <div class="metrics-grid">

            <div class="metric-card">
                <span>Tọa độ điểm khảo sát</span>
                <strong id="critical-point">(2.50, 6.25)</strong>
            </div>

            <div class="metric-card">
                <span>Giá trị hàm số f(a)</span>
                <strong id="critical-function">6.250000</strong>
            </div>

            <div class="metric-card">
                <span>Độ dốc tiếp tuyến f'(a)</span>
                <strong id="critical-slope">5.000000</strong>
            </div>

            <div class="metric-card">
                <span>Khoảng cách đến cực tiểu</span>
                <strong id="critical-distance">2.500000</strong>
            </div>

        </div>

        <div class="control-buttons">

            <button id="critical-play" type="button">
                ▶ Play
            </button>

            <button id="critical-pause" type="button">
                ⏸ Pause
            </button>

            <button id="critical-reset" type="button">
                ↺ Reset
            </button>

            <button id="critical-center" type="button">
                ● Đến cực tiểu
            </button>

        </div>

        <div id="critical-status" class="critical-status">
            Điểm khảo sát đang ở bên phải điểm cực tiểu.
            Độ dốc tiếp tuyến đang dương.
        </div>

        <div class="formula-box">

            <strong>Đạo hàm của hàm số</strong>

            <div class="formula">
                f(x) = x²
            </div>

            <div class="formula">
                f'(x) = 2x
            </div>

            <div class="formula">
                f'(0) = 0
            </div>

            <div class="formula-note">
                Tại điểm cực tiểu x = 0, tiếp tuyến nằm ngang.
            </div>

        </div>

    </div>

    <style>

        .critical-panel {
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

        #critical-pause {
            background: #64748b;
        }

        #critical-reset {
            background: #475569;
        }

        #critical-center {
            background: #16a34a;
        }

        .critical-status {
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

        const INITIAL_A = 2.5;
        const TARGET_A = 0;

        let a = INITIAL_A;
        let timer = null;
        let isRunning = false;

        function initialize(attempt = 0) {

            const plot = document.querySelector(".js-plotly-plot");
            const get = (id) => document.getElementById(id);

            const aInput = get("critical-a");
            const aValue = get("critical-a-value");

            const pointValue = get("critical-point");
            const functionValue = get("critical-function");
            const slopeValue = get("critical-slope");
            const distanceValue = get("critical-distance");

            const status = get("critical-status");

            const playButton = get("critical-play");
            const pauseButton = get("critical-pause");
            const resetButton = get("critical-reset");
            const centerButton = get("critical-center");

            const required = [
                plot,
                aInput,
                aValue,
                pointValue,
                functionValue,
                slopeValue,
                distanceValue,
                status,
                playButton,
                pauseButton,
                resetButton,
                centerButton
            ];

            if (required.some(element => element === null)) {

                if (attempt < 120) {
                    setTimeout(
                        () => initialize(attempt + 1),
                        50
                    );
                } else {
                    console.error(
                        "Critical point controls could not be initialized."
                    );
                }

                return;
            }

            // ------------------------------------------------
            // Update graph and metrics
            // ------------------------------------------------

            function updateGraph() {

                const y = a * a;
                const slope = 2 * a;

                // Tangent:
                // y = a² + 2a(x-a)
                const tangentX = Array.from(
                    { length: 100 },
                    (_, i) => a - 1.5 + (3 * i / 99)
                );

                const tangentY = tangentX.map(
                    x => y + slope * (x - a)
                );

                // Trace 1: tangent line
                Plotly.restyle(
                    plot,
                    {
                        x: [tangentX],
                        y: [tangentY]
                    },
                    [1]
                );

                // Trace 3: current point
                Plotly.restyle(
                    plot,
                    {
                        x: [[a]],
                        y: [[y]]
                    },
                    [3]
                );

                // Trace 4: vertical guide
                Plotly.restyle(
                    plot,
                    {
                        x: [[a, a]],
                        y: [[0, y]]
                    },
                    [4]
                );

                // Update metrics
                aInput.value = a;
                aValue.textContent = a.toFixed(3);

                pointValue.textContent =
                    "(" + a.toFixed(3) + ", " + y.toFixed(3) + ")";

                functionValue.textContent =
                    y.toFixed(6);

                slopeValue.textContent =
                    slope.toFixed(6);

                distanceValue.textContent =
                    Math.abs(a).toFixed(6);

                // Explain current state
                if (Math.abs(a) < 0.000001) {

                    status.textContent =
                        "Đã đến điểm cực tiểu (0, 0). " +
                        "Tiếp tuyến nằm ngang và f'(0) = 0.";

                } else if (a > 0) {

                    status.textContent =
                        "Điểm khảo sát ở bên phải cực tiểu. " +
                        "Đạo hàm dương, tiếp tuyến hướng lên.";

                } else {

                    status.textContent =
                        "Điểm khảo sát ở bên trái cực tiểu. " +
                        "Đạo hàm âm, tiếp tuyến hướng xuống.";

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
            // Move point toward x = 0
            // ------------------------------------------------

            function step() {

                a = a * 0.8;

                if (Math.abs(a) < 0.01) {

                    a = TARGET_A;

                    updateGraph();
                    stopAnimation();

                    status.textContent =
                        "Điểm khảo sát đã đến cực tiểu. " +
                        "Độ dốc tiếp tuyến bằng 0.";

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

                if (Math.abs(a) < 0.000001) {

                    status.textContent =
                        "Điểm đã ở cực tiểu. Nhấn Reset để chạy lại.";

                    return;
                }

                isRunning = true;

                status.textContent =
                    "Đang di chuyển điểm khảo sát về cực tiểu...";

                timer = setInterval(step, 300);
            }

            // ------------------------------------------------
            // Pause
            // ------------------------------------------------

            function pause() {

                stopAnimation();

                status.textContent =
                    "Đã tạm dừng tại x = " + a.toFixed(4) + ".";
            }

            // ------------------------------------------------
            // Reset
            // ------------------------------------------------

            function reset() {

                stopAnimation();

                a = INITIAL_A;

                updateGraph();

                status.textContent =
                    "Đã đặt lại vị trí khảo sát.";
            }

            // ------------------------------------------------
            // Move directly to minimum
            // ------------------------------------------------

            function moveToCenter() {

                stopAnimation();

                a = 0;

                updateGraph();
            }

            // ------------------------------------------------
            // Manual slider
            // ------------------------------------------------

            aInput.addEventListener(
                "input",
                function () {

                    stopAnimation();

                    a = parseFloat(aInput.value);

                    updateGraph();
                }
            );

            // ------------------------------------------------
            // Buttons
            // ------------------------------------------------

            playButton.addEventListener("click", play);
            pauseButton.addEventListener("click", pause);
            resetButton.addEventListener("click", reset);
            centerButton.addEventListener("click", moveToCenter);

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
        Xét hàm số <strong>f(x) = x²</strong>.
        Đồ thị của hàm số là một đường parabol có hình dạng
        giống như một chiếc bát hướng lên trên.
        Điểm thấp nhất của đồ thị nằm tại <strong>(0, 0)</strong>.
    </p>

    <p>
        Đạo hàm của hàm số là
        <strong>f'(x) = 2x</strong>.
        Đạo hàm cho biết độ dốc của đường tiếp tuyến
        tại mỗi điểm trên đồ thị.
    </p>

    <p>
        Khi x &lt; 0, đạo hàm âm: tiếp tuyến có độ dốc âm
        và hàm số đang giảm.
        Khi x &gt; 0, đạo hàm dương: tiếp tuyến có độ dốc dương
        và hàm số đang tăng.
    </p>

    <p>
        Tại x = 0, chúng ta có
        <strong>f'(0) = 0</strong>.
        Đường tiếp tuyến tại điểm (0, 0) nằm ngang,
        nghĩa là độ dốc của nó bằng 0.
        Đây chính là điểm cực tiểu của hàm số trong ví dụ này.
    </p>

    <p>
        Hãy di chuyển thanh trượt để thay đổi vị trí tiếp xúc,
        hoặc nhấn Play để đưa điểm khảo sát dần về x = 0.
        Quan sát cách độ dốc tiếp tuyến thay đổi từ âm,
        tiến về 0, rồi trở thành dương khi đi qua điểm cực tiểu.
    </p>

    <p>
        <strong>Điều cần ghi nhớ:</strong>
        Với hàm số khả vi tại một điểm cực trị nằm bên trong
        miền xác định, đạo hàm tại điểm đó bằng 0.
        Tuy nhiên, đạo hàm bằng 0 chỉ là điều kiện cần,
        không phải lúc nào cũng đảm bảo điểm đó là cực tiểu
        hoặc cực đại.
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
