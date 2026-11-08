
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

GRAPH_ID = "learning_rate_comparison"
OUTPUT_FILENAME = "learning_rate_comparison.html"

TITLE = "Gradient Descent: Comparing Learning Rates"

INITIAL_W = 5.0
MAX_ITERATIONS = 15


# ============================================================
# 2. COST FUNCTION AND GRADIENT
# ============================================================

def cost_function(w):
    """
    J(w) = w²
    """
    return w ** 2


def gradient(w):
    """
    J'(w) = 2w
    """
    return 2 * w


def update_parameter(w, learning_rate):
    """
    Gradient Descent update:

        w_next = w - alpha * J'(w)
    """
    return w - learning_rate * gradient(w)


# ============================================================
# 3. LEARNING RATE CONFIGURATION
# ============================================================

LEARNING_RATE_CASES = [
    {
        "name": "Hội tụ ổn định",
        "learning_rate": 0.25,
        "color": "#16a34a",
        "description": "Chi phí giảm đều đặn",
    },
    {
        "name": "Hội tụ chậm",
        "learning_rate": 0.05,
        "color": "#eab308",
        "description": "Chi phí giảm chậm",
    },
    {
        "name": "Dao động",
        "learning_rate": 1.00,
        "color": "#f97316",
        "description": "Đổi chiều nhưng không giảm chi phí",
    },
    {
        "name": "Phân kỳ",
        "learning_rate": 1.10,
        "color": "#ef4444",
        "description": "Chi phí tăng dần",
    },
]


# ============================================================
# 4. GENERATE GRADIENT DESCENT HISTORY
# ============================================================

def generate_history(
    initial_w,
    learning_rate,
    max_iterations,
):
    """
    Generate the parameter and cost at every iteration.
    """

    weights = [float(initial_w)]
    costs = [cost_function(initial_w)]

    w = float(initial_w)

    for _ in range(max_iterations):

        w = update_parameter(
            w,
            learning_rate,
        )

        weights.append(w)
        costs.append(cost_function(w))

    return np.array(weights), np.array(costs)


# ============================================================
# 5. BUILD GRAPH
# ============================================================

def build(output_dir: Path):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    iterations = np.arange(MAX_ITERATIONS + 1)

    # --------------------------------------------------------
    # Generate histories for all learning rates
    # --------------------------------------------------------

    histories = []

    for case in LEARNING_RATE_CASES:

        weights, costs = generate_history(
            initial_w=INITIAL_W,
            learning_rate=case["learning_rate"],
            max_iterations=MAX_ITERATIONS,
        )

        histories.append({
            **case,
            "weights": weights,
            "costs": costs,
        })

    # --------------------------------------------------------
    # Create figure
    # --------------------------------------------------------

    fig = go.Figure()

    # Trace 0-3: Cost trajectories
    for history in histories:

        fig.add_trace(
            go.Scatter(
                x=iterations,
                y=history["costs"],
                mode="lines",
                name=(
                    f"{history['name']} "
                    f"(α = {history['learning_rate']:.2f})"
                ),
                line=dict(
                    color=history["color"],
                    width=3,
                ),
                hovertemplate=(
                    "Vòng lặp: %{x}<br>"
                    "Chi phí J(w): %{y:.6g}"
                    "<extra></extra>"
                ),
            )
        )

    # Trace 4-7: Animated current positions
    for history in histories:

        fig.add_trace(
            go.Scatter(
                x=[0],
                y=[history["costs"][0]],
                mode="markers",
                name=f"Vị trí hiện tại – {history['name']}",
                marker=dict(
                    size=11,
                    color=history["color"],
                    line=dict(
                        color="white",
                        width=1.5,
                    ),
                ),
                showlegend=False,
                hovertemplate=(
                    "Vòng lặp: %{x}<br>"
                    "Chi phí: %{y:.6g}"
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
        xaxis_title="Số vòng lặp (Iteration)",
        yaxis_title="Cost Function J(w) – thang logarithmic",
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
            l=85,
            r=35,
            t=115,
            b=75,
        ),
    )

    fig.update_xaxes(
        range=[0, MAX_ITERATIONS],
        dtick=1,
        gridcolor="#e5e7eb",
        zeroline=False,
    )

    fig.update_yaxes(
        type="log",
        range=[-8, 4],
        gridcolor="#e5e7eb",
        zeroline=False,
        exponentformat="power",
    )

    # --------------------------------------------------------
    # 6. INTERACTIVE CONTROL PANEL
    # --------------------------------------------------------

    panel_html = """
    <div class="learning-rate-panel">

        <div class="panel-heading">
            <h3>Mô phỏng ảnh hưởng của Learning Rate</h3>
            <p>
                Quan sát bốn chiến lược cập nhật tham số
                bắt đầu từ cùng một vị trí w = 5.
            </p>
        </div>

        <div class="scenario-grid">

            <div class="scenario-card">
                <span class="scenario-dot green"></span>
                <div>
                    <strong>α = 0.25</strong>
                    <small>Hội tụ ổn định</small>
                </div>
            </div>

            <div class="scenario-card">
                <span class="scenario-dot yellow"></span>
                <div>
                    <strong>α = 0.05</strong>
                    <small>Hội tụ chậm</small>
                </div>
            </div>

            <div class="scenario-card">
                <span class="scenario-dot orange"></span>
                <div>
                    <strong>α = 1.00</strong>
                    <small>Dao động</small>
                </div>
            </div>

            <div class="scenario-card">
                <span class="scenario-dot red"></span>
                <div>
                    <strong>α = 1.10</strong>
                    <small>Phân kỳ</small>
                </div>
            </div>

        </div>

        <div class="control-group">

            <div class="control-label">
                <label for="lr-speed">
                    Tốc độ mô phỏng
                </label>

                <strong id="lr-speed-value">400 ms</strong>
            </div>

            <input
                id="lr-speed"
                type="range"
                min="100"
                max="1000"
                step="50"
                value="400"
            />

        </div>

        <div class="metrics-grid">

            <div class="metric-card">
                <span>Iteration hiện tại</span>
                <strong id="lr-iteration">0</strong>
            </div>

            <div class="metric-card">
                <span>Learning Rate tốt</span>
                <strong id="lr-good-cost">25.000</strong>
            </div>

            <div class="metric-card">
                <span>Learning Rate quá lớn</span>
                <strong id="lr-diverge-cost">25.000</strong>
            </div>

        </div>

        <div class="control-buttons">

            <button id="lr-play" type="button">
                ▶ Play
            </button>

            <button id="lr-pause" type="button">
                ⏸ Pause
            </button>

            <button id="lr-reset" type="button">
                ↺ Reset
            </button>

        </div>

        <div id="lr-status" class="lr-status">
            Sẵn sàng mô phỏng. Nhấn Play để bắt đầu.
        </div>

        <div class="formula-box">

            <strong>Quy tắc cập nhật Gradient Descent</strong>

            <div class="formula">
                w<sub>t+1</sub> = w<sub>t</sub> − α(2w<sub>t</sub>)
            </div>

            <div class="formula-note">
                Learning Rate α quyết định độ lớn của mỗi bước cập nhật.
            </div>

        </div>

    </div>

    <style>

        .learning-rate-panel {
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

        .scenario-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-bottom: 22px;
        }

        .scenario-card {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 9px;
        }

        .scenario-card div {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .scenario-card strong {
            font-size: 14px;
        }

        .scenario-card small {
            color: #64748b;
            font-size: 12px;
        }

        .scenario-dot {
            width: 11px;
            height: 11px;
            border-radius: 50%;
            flex-shrink: 0;
        }

        .scenario-dot.green {
            background: #16a34a;
        }

        .scenario-dot.yellow {
            background: #eab308;
        }

        .scenario-dot.orange {
            background: #f97316;
        }

        .scenario-dot.red {
            background: #ef4444;
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
            color: #2563eb;
            font-variant-numeric: tabular-nums;
        }

        .control-group input[type="range"] {
            width: 100%;
            accent-color: #2563eb;
            cursor: pointer;
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
        }

        .metric-card span {
            color: #64748b;
            font-size: 12px;
        }

        .metric-card strong {
            font-size: 19px;
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

        #lr-pause {
            background: #64748b;
        }

        #lr-reset {
            background: #475569;
        }

        .lr-status {
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
            font-size: 20px;
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

            .scenario-grid {
                grid-template-columns: 1fr;
            }

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
    # 7. JAVASCRIPT: ANIMATION
    # --------------------------------------------------------

    post_script = r"""
    (function () {

        const MAX_ITERATIONS = 15;

        let currentIteration = 0;
        let speed = 400;

        let timer = null;
        let isRunning = false;

        function initialize(attempt = 0) {

            const plot = document.querySelector(".js-plotly-plot");
            const get = (id) => document.getElementById(id);

            const speedInput = get("lr-speed");
            const speedValue = get("lr-speed-value");

            const iterationValue = get("lr-iteration");
            const goodCostValue = get("lr-good-cost");
            const divergeCostValue = get("lr-diverge-cost");

            const status = get("lr-status");

            const playButton = get("lr-play");
            const pauseButton = get("lr-pause");
            const resetButton = get("lr-reset");

            const required = [
                plot,
                speedInput,
                speedValue,
                iterationValue,
                goodCostValue,
                divergeCostValue,
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
                        "Learning Rate controls could not be initialized."
                    );
                }

                return;
            }

            // ------------------------------------------------
            // Learning rate cases
            // ------------------------------------------------

            const cases = [
                { alpha: 0.25, trace: 4 },
                { alpha: 0.05, trace: 5 },
                { alpha: 1.00, trace: 6 },
                { alpha: 1.10, trace: 7 }
            ];

            // ------------------------------------------------
            // Calculate cost at a specific iteration
            // ------------------------------------------------

            function getCost(alpha, iteration) {

                let w = 5;

                for (let i = 0; i < iteration; i++) {
                    w = w - alpha * (2 * w);
                }

                return w * w;
            }

            // ------------------------------------------------
            // Update animated markers and metrics
            // ------------------------------------------------

            function updateGraph() {

                cases.forEach(function (item) {

                    const cost = getCost(
                        item.alpha,
                        currentIteration
                    );

                    Plotly.restyle(
                        plot,
                        {
                            x: [[currentIteration]],
                            y: [[cost]]
                        },
                        [item.trace]
                    );
                });

                const goodCost = getCost(
                    0.25,
                    currentIteration
                );

                const divergeCost = getCost(
                    1.10,
                    currentIteration
                );

                iterationValue.textContent = currentIteration;

                goodCostValue.textContent =
                    goodCost.toExponential(3);

                divergeCostValue.textContent =
                    divergeCost.toFixed(3);
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

                if (currentIteration >= MAX_ITERATIONS) {

                    stopAnimation();

                    status.textContent =
                        "Đã hoàn thành mô phỏng. " +
                        "Hãy quan sát sự khác biệt giữa bốn Learning Rate.";

                    return;
                }

                currentIteration += 1;

                updateGraph();

                status.textContent =
                    "Đang mô phỏng vòng lặp " +
                    currentIteration +
                    "/" +
                    MAX_ITERATIONS +
                    ".";
            }

            // ------------------------------------------------
            // Play
            // ------------------------------------------------

            function play() {

                if (isRunning) {
                    return;
                }

                if (currentIteration >= MAX_ITERATIONS) {
                    status.textContent =
                        "Mô phỏng đã kết thúc. Nhấn Reset để chạy lại.";
                    return;
                }

                isRunning = true;

                status.textContent =
                    "Gradient Descent đang chạy...";

                timer = setInterval(step, speed);
            }

            // ------------------------------------------------
            // Pause
            // ------------------------------------------------

            function pause() {

                stopAnimation();

                status.textContent =
                    "Đã tạm dừng tại vòng lặp " +
                    currentIteration +
                    ".";
            }

            // ------------------------------------------------
            // Reset
            // ------------------------------------------------

            function reset() {

                stopAnimation();

                currentIteration = 0;

                updateGraph();

                status.textContent =
                    "Đã đặt lại mô phỏng. Sẵn sàng bắt đầu.";
            }

            // ------------------------------------------------
            // Speed control
            // ------------------------------------------------

            speedInput.addEventListener("input", function () {

                speed = parseInt(speedInput.value, 10);

                speedValue.textContent = speed + " ms";

                if (isRunning) {

                    stopAnimation();

                    play();
                }
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
    # 8. VIETNAMESE CAPTION
    # --------------------------------------------------------

    caption = """
    <p>
        Hãy xét một hàm chi phí đơn giản chỉ phụ thuộc vào
        một tham số w:
        <strong>J(w) = w²</strong>.
        Mục tiêu của chúng ta là tìm giá trị w khiến hàm chi phí
        đạt cực tiểu tại w = 0.
    </p>

    <p>
        Mô phỏng bắt đầu từ cùng một vị trí
        <strong>w₀ = 5</strong>.
        Ở mỗi vòng lặp, Gradient Descent cập nhật tham số theo quy tắc:
    </p>

    <p style="text-align:center;">
        <strong>wₜ₊₁ = wₜ − α(2wₜ)</strong>
    </p>

    <p>
        <strong>Đường màu xanh lá (α = 0.25):</strong>
        Learning Rate phù hợp giúp tham số tiến dần về 0
        và chi phí giảm nhanh, ổn định.
    </p>

    <p>
        <strong>Đường màu vàng (α = 0.05):</strong>
        Learning Rate nhỏ khiến mỗi bước cập nhật ngắn.
        Chi phí vẫn giảm nhưng cần nhiều vòng lặp hơn để tiến gần
        điểm cực tiểu.
    </p>

    <p>
        <strong>Đường màu cam (α = 1.00):</strong>
        Tham số liên tục đổi dấu giữa hai phía của điểm cực tiểu.
        Tuy nhiên, độ lớn của tham số không thay đổi,
        vì vậy chi phí không giảm.
    </p>

    <p>
        <strong>Đường màu đỏ (α = 1.10):</strong>
        Learning Rate quá lớn khiến mỗi lần cập nhật vượt quá
        điểm cực tiểu. Độ lớn của tham số tăng dần,
        làm chi phí tăng và thuật toán phân kỳ.
    </p>

    <p>
        <strong>Kết luận:</strong>
        Learning Rate quá nhỏ khiến quá trình tối ưu hóa chậm;
        Learning Rate phù hợp giúp hội tụ hiệu quả;
        Learning Rate quá lớn có thể khiến thuật toán dao động
        hoặc phân kỳ.
    </p>
    """

    caption_html = build_caption_html(
        caption,
        TITLE,
        "16px",
    )

    # --------------------------------------------------------
    # 9. EXPORT HTML
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
