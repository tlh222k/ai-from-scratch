
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

GRAPH_ID = "quadratic_cost_optimization"
OUTPUT_FILENAME = "quadratic_cost_optimization.html"

TITLE = "Optimization: Finding the Minimum of J(w)"


# ============================================================
# 2. MATHEMATICAL FUNCTION
# ============================================================

def cost_function(w):
    """
    Quadratic cost function:

        J(w) = w^2

    Global minimum:
        w* = 0
        J(w*) = 0
    """
    return w ** 2


def gradient(w):
    """
    Derivative of the cost function:

        J'(w) = 2w
    """
    return 2 * w


def gradient_descent_step(w, learning_rate):
    """
    One Gradient Descent update:

        w_next = w - learning_rate * J'(w)
    """
    return w - learning_rate * gradient(w)


# ============================================================
# 3. BUILD INTERACTIVE GRAPH
# ============================================================

def build(output_dir: Path):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # Dataset for the cost curve
    # --------------------------------------------------------

    w_values = np.linspace(-4, 4, 400)
    j_values = cost_function(w_values)

    initial_w = 3.0
    initial_cost = cost_function(initial_w)

    minimum_w = 0.0
    minimum_cost = 0.0

    # --------------------------------------------------------
    # Create Plotly figure
    # --------------------------------------------------------

    fig = go.Figure()

    # Trace 0: Cost Function
    fig.add_trace(
        go.Scatter(
            x=w_values,
            y=j_values,
            mode="lines",
            name="Cost Function",
            line=dict(
                color="#2563eb",
                width=3,
            ),
            hovertemplate=(
                "w = %{x:.3f}<br>"
                "J(w) = %{y:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 1: Global minimum
    fig.add_trace(
        go.Scatter(
            x=[minimum_w],
            y=[minimum_cost],
            mode="markers",
            name="Global Minimum",
            marker=dict(
                size=13,
                color="#16a34a",
                line=dict(
                    color="white",
                    width=2,
                ),
            ),
            hovertemplate=(
                "Minimum<br>"
                "w = 0<br>"
                "J(w) = 0"
                "<extra></extra>"
            ),
        )
    )

    # Trace 2: Current parameter position
    fig.add_trace(
        go.Scatter(
            x=[initial_w],
            y=[initial_cost],
            mode="markers",
            name="Current Parameter",
            marker=dict(
                size=13,
                color="#f97316",
                line=dict(
                    color="white",
                    width=2,
                ),
            ),
            hovertemplate=(
                "Current Parameter<br>"
                "w = %{x:.3f}<br>"
                "J(w) = %{y:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 3: Projection from current point to x-axis
    fig.add_trace(
        go.Scatter(
            x=[initial_w, initial_w],
            y=[0, initial_cost],
            mode="lines",
            name="Current Cost",
            line=dict(
                color="#f97316",
                width=2,
                dash="dash",
            ),
            hoverinfo="skip",
        )
    )

    # --------------------------------------------------------
    # Figure layout
    # --------------------------------------------------------

    configure_figure(
        fig,
        title=TITLE,
        xaxis_title="Parameter (w)",
        yaxis_title="Cost Function J(w)",
        height=560,
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
        ),
        margin=dict(
            l=65,
            r=35,
            t=100,
            b=65,
        ),
    )

    fig.update_xaxes(
        range=[-4.3, 4.3],
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor="#64748b",
        gridcolor="#e2e8f0",
    )

    fig.update_yaxes(
        range=[-1, 18],
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor="#64748b",
        gridcolor="#e2e8f0",
    )

    # --------------------------------------------------------
    # Interactive control panel
    # --------------------------------------------------------

    panel_html = """
    <div class="optimization-panel">

        <div class="panel-heading">
            <h3>Optimization Controls</h3>
            <p>
                Explore how the parameter w moves toward
                the minimum of the cost function.
            </p>
        </div>

        <div class="control-group">

            <div class="control-label">
                <label for="opt-w">
                    Current Parameter (w)
                </label>

                <span id="opt-w-value">3.00</span>
            </div>

            <input
                id="opt-w"
                type="range"
                min="-4"
                max="4"
                step="0.05"
                value="3"
            />

        </div>

        <div class="control-group">

            <div class="control-label">
                <label for="opt-lr">
                    Learning Rate (η)
                </label>

                <span id="opt-lr-value">0.15</span>
            </div>

            <input
                id="opt-lr"
                type="range"
                min="0.01"
                max="0.45"
                step="0.01"
                value="0.15"
            />

        </div>

        <div class="metrics-grid">

            <div class="metric-card">
                <span class="metric-label">Current Cost</span>
                <strong id="opt-cost">9.000</strong>
            </div>

            <div class="metric-card">
                <span class="metric-label">Gradient J'(w)</span>
                <strong id="opt-gradient">6.000</strong>
            </div>

            <div class="metric-card">
                <span class="metric-label">Iterations</span>
                <strong id="opt-iterations">0</strong>
            </div>

        </div>

        <div class="optimization-buttons">

            <button id="opt-play" type="button">
                ▶ Play
            </button>

            <button id="opt-pause" type="button">
                ⏸ Pause
            </button>

            <button id="opt-reset" type="button">
                ↺ Reset
            </button>

        </div>

        <div id="opt-status" class="optimization-status">
            Ready to optimize.
        </div>

        <div class="formula-box">

            <strong>Gradient Descent Update Rule</strong>

            <div class="formula">
                w<sub>t+1</sub> = w<sub>t</sub> − η · 2w<sub>t</sub>
            </div>

            <div class="formula-note">
                The parameter is updated in the opposite
                direction of the gradient.
            </div>

        </div>

    </div>

    <style>

        .optimization-panel {
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
            margin-bottom: 22px;
        }

        .control-label {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            font-size: 14px;
            font-weight: 600;
        }

        .control-label span {
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
            gap: 12px;
            margin: 20px 0;
        }

        .metric-card {
            padding: 14px;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .metric-label {
            color: #64748b;
            font-size: 12px;
        }

        .metric-card strong {
            font-size: 20px;
            font-variant-numeric: tabular-nums;
        }

        .optimization-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
        }

        .optimization-buttons button {
            border: none;
            border-radius: 8px;
            padding: 10px 18px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            background: #2563eb;
            color: white;
            transition: opacity 0.2s;
        }

        .optimization-buttons button:hover {
            opacity: 0.85;
        }

        #opt-pause {
            background: #64748b;
        }

        #opt-reset {
            background: #475569;
        }

        .optimization-status {
            padding: 12px 14px;
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
    # JavaScript: Interactive Gradient Descent
    # --------------------------------------------------------

    post_script = r"""
    (function () {

        let currentW = 3.0;
        let learningRate = 0.15;
        let iteration = 0;

        let animationTimer = null;
        let isRunning = false;

        const minimumW = 0;
        const epsilon = 0.005;
        const maxIterations = 500;

        function initialize(attempt = 0) {

            const plot = document.querySelector(".js-plotly-plot");

            const get = (id) => document.getElementById(id);

            const wInput = get("opt-w");
            const lrInput = get("opt-lr");

            const wValue = get("opt-w-value");
            const lrValue = get("opt-lr-value");

            const costValue = get("opt-cost");
            const gradientValue = get("opt-gradient");
            const iterationValue = get("opt-iterations");

            const status = get("opt-status");

            const playButton = get("opt-play");
            const pauseButton = get("opt-pause");
            const resetButton = get("opt-reset");

            const required = [
                plot,
                wInput,
                lrInput,
                wValue,
                lrValue,
                costValue,
                gradientValue,
                iterationValue,
                status,
                playButton,
                pauseButton,
                resetButton
            ];

            if (required.some(element => element === null)) {

                if (attempt < 120) {
                    setTimeout(() => initialize(attempt + 1), 50);
                } else {
                    console.error(
                        "Optimization controls could not be initialized."
                    );
                }

                return;
            }

            // ------------------------------------------------
            // Update graph and metrics
            // ------------------------------------------------

            function updateGraph() {

                const currentCost = currentW * currentW;
                const currentGradient = 2 * currentW;

                // Trace 2: Current parameter marker
                Plotly.restyle(
                    plot,
                    {
                        x: [[currentW]],
                        y: [[currentCost]]
                    },
                    [2]
                );

                // Trace 3: Vertical projection
                Plotly.restyle(
                    plot,
                    {
                        x: [[currentW, currentW]],
                        y: [[0, currentCost]]
                    },
                    [3]
                );

                wInput.value = currentW;
                lrInput.value = learningRate;

                wValue.textContent = currentW.toFixed(3);
                lrValue.textContent = learningRate.toFixed(2);

                costValue.textContent = currentCost.toFixed(4);
                gradientValue.textContent = currentGradient.toFixed(4);

                iterationValue.textContent = iteration;
            }

            // ------------------------------------------------
            // Stop animation
            // ------------------------------------------------

            function stopAnimation() {

                if (animationTimer !== null) {
                    clearInterval(animationTimer);
                    animationTimer = null;
                }

                isRunning = false;
            }

            // ------------------------------------------------
            // Manual parameter adjustment
            // ------------------------------------------------

            wInput.addEventListener("input", function () {

                stopAnimation();

                currentW = parseFloat(wInput.value);
                iteration = 0;

                updateGraph();

                status.textContent =
                    "Manual adjustment: w = " +
                    currentW.toFixed(3);
            });

            // ------------------------------------------------
            // Learning rate adjustment
            // ------------------------------------------------

            lrInput.addEventListener("input", function () {

                learningRate = parseFloat(lrInput.value);

                updateGraph();

                status.textContent =
                    "Learning Rate η = " +
                    learningRate.toFixed(2);
            });

            // ------------------------------------------------
            // One Gradient Descent step
            // ------------------------------------------------

            function optimizeStep() {

                const currentGradient = 2 * currentW;

                currentW =
                    currentW - learningRate * currentGradient;

                iteration += 1;

                updateGraph();

                return Math.abs(currentW) < epsilon ||
                       iteration >= maxIterations;
            }

            // ------------------------------------------------
            // Play Gradient Descent
            // ------------------------------------------------

            function play() {

                if (isRunning) {
                    return;
                }

                if (
                    Math.abs(currentW) < epsilon ||
                    iteration >= maxIterations
                ) {
                    status.textContent =
                        "Optimization has converged. Press Reset to restart.";
                    return;
                }

                isRunning = true;

                status.textContent =
                    "Gradient Descent is optimizing the parameter...";

                animationTimer = setInterval(function () {

                    const converged = optimizeStep();

                    if (converged) {

                        stopAnimation();

                        status.textContent =
                            "Converged! The parameter is approaching w = 0.";

                    } else {

                        status.textContent =
                            "Iteration " + iteration +
                            ": moving toward the minimum.";
                    }

                }, 300);
            }

            // ------------------------------------------------
            // Pause
            // ------------------------------------------------

            function pause() {

                stopAnimation();

                status.textContent =
                    "Optimization paused at iteration " + iteration + ".";
            }

            // ------------------------------------------------
            // Reset
            // ------------------------------------------------

            function reset() {

                stopAnimation();

                currentW = 3.0;
                learningRate = 0.15;
                iteration = 0;

                updateGraph();

                status.textContent =
                    "Reset completed. Ready to optimize.";
            }

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
    # 4. EXPORT HTML
    # --------------------------------------------------------

    plot_html = fig.to_html(
        full_html=False,
        include_plotlyjs=True,
        config=PLOTLY_CONFIG,
        post_script=post_script,
    )

    
    caption = """
    <p>
        Hãy tưởng tượng một bài toán tối ưu hóa đơn giản chỉ có một tham số,
        được ký hiệu là <strong>w</strong>.
    </p>

    <p>
        Hàm chi phí (Cost Function) được biểu diễn bởi:
        <strong>J(w) = w²</strong>.
        Đồ thị của hàm số có dạng một đường cong hình chữ U.
        Giá trị chi phí nhỏ nhất đạt được tại
        <strong>w = 0</strong>, khi đó <strong>J(w) = 0</strong>.
    </p>

    <p>
        <strong>Tối ưu hóa (Optimization)</strong> là quá trình tìm giá trị
        tham số <strong>w</strong> sao cho hàm chi phí đạt giá trị nhỏ nhất.
    </p>

    <p>
        Sử dụng thanh trượt <strong>w</strong> để thay đổi giá trị tham số
        và quan sát sự thay đổi của chi phí tương ứng trên đồ thị.
    </p>

    <p>
        Nhấn <strong>Play</strong> để mô phỏng thuật toán Gradient Descent.
        Ở mỗi bước lặp, tham số được cập nhật theo công thức:
    </p>

    <p style="text-align:center;">
        <strong>wₜ₊₁ = wₜ − η · 2wₜ</strong>
    </p>

    <p>
        Tốc độ học (Learning Rate) η quyết định độ lớn của mỗi lần cập nhật.
        Thuật toán sử dụng đạo hàm để điều chỉnh tham số theo hướng làm giảm
        hàm chi phí, tiến dần đến điểm cực tiểu tại <strong>w = 0</strong>.
    </p>
    """


    caption_html = build_caption_html(
        caption,
        TITLE,
        "16px",
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
