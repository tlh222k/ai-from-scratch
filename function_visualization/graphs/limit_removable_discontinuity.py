
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

GRAPH_ID = "limit_removable_discontinuity"
OUTPUT_FILENAME = "limit_removable_discontinuity.html"

TITLE = "Limit: Removable Discontinuity"

LIMIT_X = 1.0
LIMIT_Y = 2.0

INITIAL_EPSILON = 0.5


# ============================================================
# 2. MATHEMATICAL FUNCTIONS
# ============================================================

def original_function(x):
    """
    Original function:

        f(x) = (x² - 1) / (x - 1)

    The function is undefined at x = 1.

    For numerical evaluation where x != 1,
    use the equivalent simplified expression x + 1.
    """

    x = np.asarray(x, dtype=float)

    if np.any(np.isclose(x, LIMIT_X)):
        raise ValueError("Hàm số không xác định tại x = 1.")

    return x + 1


def simplified_function(x):
    """
    Simplified expression for x != 1:

        f(x) = x + 1
    """

    return x + 1


def calculate_limit_value():
    """
    lim(x -> 1) (x² - 1) / (x - 1) = 2
    """
    return LIMIT_X + 1


# ============================================================
# 3. BUILD GRAPH
# ============================================================

def build(output_dir: Path):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # Generate two separate branches.
    #
    # Important: Do not include x = 1.
    # --------------------------------------------------------

    x_left = np.linspace(0, 0.999, 400)
    x_right = np.linspace(1.001, 2, 400)

    y_left = simplified_function(x_left)
    y_right = simplified_function(x_right)

    # Initial observation from the left
    initial_x = LIMIT_X - INITIAL_EPSILON
    initial_y = float(simplified_function(initial_x))

    # --------------------------------------------------------
    # Figure
    # --------------------------------------------------------

    fig = go.Figure()

    # Trace 0: Left branch
    fig.add_trace(
        go.Scatter(
            x=x_left,
            y=y_left,
            mode="lines",
            name="Đồ thị khi x < 1",
            line=dict(
                color="#2689e8",
                width=3,
            ),
            hovertemplate=(
                "x = %{x:.4f}<br>"
                "f(x) = %{y:.4f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 1: Right branch
    fig.add_trace(
        go.Scatter(
            x=x_right,
            y=y_right,
            mode="lines",
            name="Đồ thị khi x > 1",
            line=dict(
                color="#2689e8",
                width=3,
            ),
            hovertemplate=(
                "x = %{x:.4f}<br>"
                "f(x) = %{y:.4f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 2: Open circle at (1, 2)
    fig.add_trace(
        go.Scatter(
            x=[LIMIT_X],
            y=[LIMIT_Y],
            mode="markers",
            name="Điểm khuyết (1, 2)",
            marker=dict(
                size=15,
                color="white",
                line=dict(
                    color="#ef4444",
                    width=3,
                ),
                symbol="circle",
            ),
            hovertemplate=(
                "Điểm khuyết<br>"
                "x = 1<br>"
                "y = 2<br>"
                "Hàm số không xác định tại đây"
                "<extra></extra>"
            ),
        )
    )

    # Trace 3: Current approaching point
    fig.add_trace(
        go.Scatter(
            x=[initial_x],
            y=[initial_y],
            mode="markers",
            name="Vị trí đang khảo sát",
            marker=dict(
                size=13,
                color="#f97316",
                line=dict(
                    color="white",
                    width=2,
                ),
            ),
            hovertemplate=(
                "x = %{x:.6f}<br>"
                "f(x) = %{y:.6f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 4: Vertical dotted guide
    fig.add_trace(
        go.Scatter(
            x=[initial_x, initial_x, None],
            y=[0, initial_y, None],
            mode="lines",
            name="Khoảng cách theo phương đứng",
            line=dict(
                color="#94a3b8",
                width=2,
                dash="dot",
            ),
            hoverinfo="skip",
            connectgaps=False,
        )
    )

    # Trace 5: Horizontal guide toward the limit value
    fig.add_trace(
        go.Scatter(
            x=[0, 2],
            y=[LIMIT_Y, LIMIT_Y],
            mode="lines",
            name="Giá trị giới hạn y = 2",
            line=dict(
                color="#16a34a",
                width=2,
                dash="dash",
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
        range=[0, 2],
        dtick=0.2,
        gridcolor="#e5e7eb",
        zeroline=False,
    )

    fig.update_yaxes(
        range=[0, 3.2],
        dtick=0.4,
        gridcolor="#e5e7eb",
        zeroline=False,
    )

    # --------------------------------------------------------
    # 4. INTERACTIVE CONTROL PANEL
    # --------------------------------------------------------

    panel_html = """
    <div class="limit-panel">

        <div class="panel-heading">
            <h3>Khám phá giới hạn khi x tiến đến 1</h3>
            <p>
                Điều chỉnh khoảng cách giữa x và 1,
                hoặc chạy animation để quan sát giá trị hàm số.
            </p>
        </div>

        <div class="direction-control">

            <label for="limit-direction">
                Hướng tiếp cận
            </label>

            <select id="limit-direction">
                <option value="left">Từ bên trái (x → 1⁻)</option>
                <option value="right">Từ bên phải (x → 1⁺)</option>
            </select>

        </div>

        <div class="control-group">

            <div class="control-label">
                <label for="limit-epsilon">
                    Khoảng cách ε = |x − 1|
                </label>

                <strong id="limit-epsilon-value">0.500</strong>
            </div>

            <input
                id="limit-epsilon"
                type="range"
                min="0.001"
                max="0.9"
                step="0.001"
                value="0.5"
            />

            <div class="range-hints">
                <span>0.001 – Rất gần</span>
                <span>0.9 – Xa hơn</span>
            </div>

        </div>

        <div class="metrics-grid">

            <div class="metric-card">
                <span>Giá trị x</span>
                <strong id="limit-x-value">0.500000</strong>
            </div>

            <div class="metric-card">
                <span>Giá trị f(x)</span>
                <strong id="limit-y-value">1.500000</strong>
            </div>

            <div class="metric-card">
                <span>Khoảng cách đến giới hạn</span>
                <strong id="limit-error-value">0.500000</strong>
            </div>

        </div>

        <div class="control-buttons">

            <button id="limit-play" type="button">
                ▶ Play
            </button>

            <button id="limit-pause" type="button">
                ⏸ Pause
            </button>

            <button id="limit-reset" type="button">
                ↺ Reset
            </button>

        </div>

        <div id="limit-status" class="limit-status">
            Đang tiếp cận từ bên trái. Hãy nhấn Play để bắt đầu.
        </div>

        <div class="limit-result">

            <span>Giá trị giới hạn dự kiến</span>

            <strong>
                lim f(x) = 2
            </strong>

        </div>

    </div>

    <style>

        .limit-panel {
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
            grid-template-columns: repeat(3, 1fr);
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

        #limit-pause {
            background: #64748b;
        }

        #limit-reset {
            background: #475569;
        }

        .limit-status {
            padding: 13px 14px;
            background: #eff6ff;
            border-radius: 8px;
            color: #1d4ed8;
            font-size: 13px;
            line-height: 1.6;
        }

        .limit-result {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            margin-top: 18px;
            padding: 15px;
            background: #ecfdf5;
            border: 1px solid #bbf7d0;
            border-radius: 9px;
        }

        .limit-result span {
            color: #166534;
            font-size: 13px;
        }

        .limit-result strong {
            color: #15803d;
            font-size: 20px;
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

            .limit-result {
                align-items: flex-start;
                flex-direction: column;
            }

        }

    </style>
    """

    # --------------------------------------------------------
    # 5. JAVASCRIPT: INTERACTION AND ANIMATION
    # --------------------------------------------------------

    post_script = r"""
    (function () {

        const LIMIT_X = 1;
        const LIMIT_Y = 2;

        const INITIAL_EPSILON = 0.5;
        const MIN_EPSILON = 0.001;

        let epsilon = INITIAL_EPSILON;
        let direction = "left";

        let timer = null;
        let isRunning = false;

        function initialize(attempt = 0) {

            const plot = document.querySelector(".js-plotly-plot");
            const get = (id) => document.getElementById(id);

            const directionInput = get("limit-direction");
            const epsilonInput = get("limit-epsilon");
            const epsilonValue = get("limit-epsilon-value");

            const xValue = get("limit-x-value");
            const yValue = get("limit-y-value");
            const errorValue = get("limit-error-value");

            const status = get("limit-status");

            const playButton = get("limit-play");
            const pauseButton = get("limit-pause");
            const resetButton = get("limit-reset");

            const required = [
                plot,
                directionInput,
                epsilonInput,
                epsilonValue,
                xValue,
                yValue,
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
                        "Limit controls could not be initialized."
                    );
                }

                return;
            }

            // ------------------------------------------------
            // Calculate current position
            // ------------------------------------------------

            function getCurrentX() {

                return direction === "left"
                    ? LIMIT_X - epsilon
                    : LIMIT_X + epsilon;
            }

            // ------------------------------------------------
            // Update point and vertical guide
            // ------------------------------------------------

            function updateGraph() {

                const x = getCurrentX();

                // For x != 1:
                // (x² - 1) / (x - 1) = x + 1
                const y = x + 1;

                Plotly.restyle(
                    plot,
                    {
                        x: [[x]],
                        y: [[y]]
                    },
                    [3]
                );

                Plotly.restyle(
                    plot,
                    {
                        x: [[x, x, null]],
                        y: [[0, y, null]]
                    },
                    [4]
                );

                epsilonValue.textContent =
                    epsilon.toFixed(3);

                xValue.textContent =
                    x.toFixed(6);

                yValue.textContent =
                    y.toFixed(6);

                errorValue.textContent =
                    Math.abs(y - LIMIT_Y).toFixed(6);

                status.textContent =
                    direction === "left"
                    ? "Đang xét x = " + x.toFixed(6) +
                      ". x đang tiến đến 1 từ bên trái."
                    : "Đang xét x = " + x.toFixed(6) +
                      ". x đang tiến đến 1 từ bên phải.";

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

                epsilon = epsilon * 0.8;

                if (epsilon <= MIN_EPSILON) {

                    epsilon = MIN_EPSILON;

                    updateGraph();

                    stopAnimation();

                    status.textContent =
                        "Đã tiến rất gần đến x = 1. " +
                        "Giá trị f(x) tiến rất gần đến 2, " +
                        "nhưng x vẫn chưa bằng 1.";

                    return;
                }

                epsilonInput.value = epsilon;

                updateGraph();
            }

            // ------------------------------------------------
            // Play
            // ------------------------------------------------

            function play() {

                if (isRunning) {
                    return;
                }

                isRunning = true;

                status.textContent =
                    "Animation đang chạy...";

                timer = setInterval(step, 350);
            }

            // ------------------------------------------------
            // Pause
            // ------------------------------------------------

            function pause() {

                stopAnimation();

                status.textContent =
                    "Đã tạm dừng tại x = " +
                    getCurrentX().toFixed(6) +
                    ".";
            }

            // ------------------------------------------------
            // Reset
            // ------------------------------------------------

            function reset() {

                stopAnimation();

                epsilon = INITIAL_EPSILON;
                epsilonInput.value = epsilon;

                updateGraph();

                status.textContent =
                    "Đã đặt lại mô phỏng.";
            }

            // ------------------------------------------------
            // Direction selection
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
            // Manual epsilon control
            // ------------------------------------------------

            epsilonInput.addEventListener(
                "input",
                function () {

                    stopAnimation();

                    epsilon = parseFloat(
                        epsilonInput.value
                    );

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
        Xét hàm số:
        <strong>f(x) = (x² − 1)/(x − 1)</strong>.
        Khi thay trực tiếp x = 1 vào biểu thức ban đầu,
        chúng ta nhận được dạng 0/0.
        Vì vậy, hàm số không xác định tại x = 1.
    </p>

    <p>
        Tuy nhiên, khi x khác 1, chúng ta có thể phân tích
        tử số thành nhân tử:
        <strong>x² − 1 = (x − 1)(x + 1)</strong>.
        Sau khi rút gọn, biểu thức trở thành
        <strong>f(x) = x + 1, với x ≠ 1</strong>.
    </p>

    <p>
        Trên biểu đồ, đường màu xanh thể hiện hai nhánh
        của đồ thị. Vòng tròn rỗng tại (1, 2) biểu thị
        điểm mà hàm số không xác định.
    </p>

    <p>
        Hãy điều chỉnh khoảng cách ε = |x − 1| hoặc chạy
        animation để quan sát điểm màu cam tiến đến vị trí
        x = 1 từ bên trái hoặc bên phải.
    </p>

    <p>
        Khi x tiến gần đến 1, giá trị f(x) tiến gần đến 2.
        Điều này xảy ra ở cả hai hướng tiếp cận.
        Do đó, giới hạn của hàm số tại x = 1 tồn tại
        và bằng 2.
    </p>

    <p style="text-align:center;">
        <strong>
            lim (x → 1) (x² − 1)/(x − 1) = 2
        </strong>
    </p>

    <p>
        <strong>Điều cần ghi nhớ:</strong>
        Giới hạn mô tả giá trị mà hàm số tiến tới khi
        biến số tiến gần một điểm. Giá trị giới hạn
        không nhất thiết phải bằng giá trị của hàm số
        tại điểm đó; thậm chí hàm số có thể không xác định
        tại điểm đang xét.
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
