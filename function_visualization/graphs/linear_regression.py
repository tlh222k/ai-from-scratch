
"""Interactive visualization of a simple Linear Regression model.

Model:
    f(x; w, b) = wx + b

Features:
- Illustrative scatter dataset
- Adjustable weight (w) and bias (b)
- Animated transition toward the least-squares solution
- Play, Pause, and Reset controls
- Live parameter and prediction updates
"""

from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from function_visualization.core.figure import configure_figure
from function_visualization.core.captions import build_caption_html
from function_visualization.core.exporter import (
    PLOTLY_CONFIG,
    render_page,
)


GRAPH_ID = "linear_regression"
OUTPUT_FILENAME = "linear_regression.html"
TITLE = "Linear Regression: f(x; w, b) = wx + b"


def function(x, w, b):
    """Linear regression model: f(x; w, b) = wx + b."""
    return w * x + b


def build(output_dir):
    """Build and export the interactive Linear Regression graph."""

    # ---------------------------------------------------------
    # 1. Illustrative dataset
    # ---------------------------------------------------------
    # These are example observations, not real-world measurements.
    x_data = np.array(
        [0, 1, 2, 3, 4, 5, 6],
        dtype=float,
    )

    y_data = np.array(
        [1.2, 2.8, 4.1, 7.2, 8.8, 11.1, 12.7],
        dtype=float,
    )

    # Least-squares solution for the illustrative dataset.
    target_w, target_b = np.polyfit(x_data, y_data, 1)

    # ---------------------------------------------------------
    # 2. Initial model parameters
    # ---------------------------------------------------------
    initial_w = 0.3
    initial_b = 2.0

    x_line = np.linspace(-0.5, 6.5, 200)

    initial_y = function(
        x_line,
        initial_w,
        initial_b,
    )

    target_y = function(
        x_line,
        target_w,
        target_b,
    )

    # ---------------------------------------------------------
    # 3. Create Plotly figure
    # ---------------------------------------------------------
    fig = go.Figure()

    # Trace 0: observed data points
    fig.add_trace(
        go.Scatter(
            x=x_data,
            y=y_data,
            mode="markers",
            name="Observed data",
            marker=dict(
                size=11,
                color="#2563EB",
                line=dict(
                    color="white",
                    width=1.5,
                ),
            ),
            hovertemplate=(
                "x = %{x:.2f}<br>"
                "y = %{y:.2f}"
                "<extra>Data point</extra>"
            ),
        )
    )

    # Trace 1: current model prediction
    fig.add_trace(
        go.Scatter(
            x=x_line,
            y=initial_y,
            mode="lines",
            name="Current model",
            line=dict(
                color="#F59E0B",
                width=3,
            ),
            hovertemplate=(
                "x = %{x:.2f}<br>"
                "f(x) = %{y:.2f}"
                "<extra>Current model</extra>"
            ),
        )
    )

    # Trace 2: least-squares reference line
    fig.add_trace(
        go.Scatter(
            x=x_line,
            y=target_y,
            mode="lines",
            name="Least-squares reference",
            line=dict(
                color="#16A34A",
                width=2,
                dash="dash",
            ),
            hovertemplate=(
                "x = %{x:.2f}<br>"
                "f(x) = %{y:.2f}"
                "<extra>Least-squares reference</extra>"
            ),
        )
    )

    # ---------------------------------------------------------
    # 4. Configure layout
    # ---------------------------------------------------------
    configure_figure(
        fig,
        title=TITLE,
        xaxis_title="Input x",
        yaxis_title="Output y",
        height=620,
    )

    fig.update_xaxes(
        range=[-0.5, 6.5],
        zeroline=True,
        zerolinewidth=1.2,
        zerolinecolor="#64748B",
    )

    fig.update_yaxes(
        range=[-2, 16],
        zeroline=True,
        zerolinewidth=1.2,
        zerolinecolor="#64748B",
    )

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(
            l=65,
            r=30,
            t=100,
            b=65,
        ),
        hovermode="closest",
    )

    # ---------------------------------------------------------
    # 5. Interactive control panel
    # ---------------------------------------------------------
    panel_html = """
    <div id="lr-controls"
         style="
            max-width:1000px;
            margin:20px auto;
            padding:22px;
            border:1px solid #d1d5db;
            border-radius:12px;
            background:#f8fafc;
            color:#1e293b;
            font-family:Arial,sans-serif;
         ">

        <h3 style="margin-top:0;">
            Linear Regression Controls
        </h3>

        <div style="
            display:grid;
            grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
            gap:22px;
        ">

            <div>
                <label for="lr-w">
                    Weight (w):
                    <strong id="lr-w-value">0.30</strong>
                </label>
                <input id="lr-w"
                       type="range"
                       min="-1"
                       max="4"
                       step="0.05"
                       value="0.3"
                       style="width:100%;">
                <small>
                    Controls the slope of the line.
                </small>
            </div>

            <div>
                <label for="lr-b">
                    Bias (b):
                    <strong id="lr-b-value">2.00</strong>
                </label>
                <input id="lr-b"
                       type="range"
                       min="-5"
                       max="5"
                       step="0.05"
                       value="2"
                       style="width:100%;">
                <small>
                    Controls the vertical intercept.
                </small>
            </div>

            <div>
                <label for="lr-speed">
                    Animation duration:
                    <strong id="lr-speed-value">2000 ms</strong>
                </label>
                <input id="lr-speed"
                       type="range"
                       min="500"
                       max="5000"
                       step="250"
                       value="2000"
                       style="width:100%;">
                <small>
                    Controls how long the fitting animation takes.
                </small>
            </div>

        </div>

        <div style="
            display:flex;
            gap:10px;
            flex-wrap:wrap;
            margin-top:22px;
        ">
            <button id="lr-play"
                    style="
                        padding:10px 22px;
                        border:0;
                        border-radius:7px;
                        background:#2563eb;
                        color:white;
                        cursor:pointer;
                    ">
                ▶ Play fitting
            </button>

            <button id="lr-pause"
                    style="
                        padding:10px 22px;
                        border:0;
                        border-radius:7px;
                        background:#64748b;
                        color:white;
                        cursor:pointer;
                    ">
                ⏸ Pause
            </button>

            <button id="lr-reset"
                    style="
                        padding:10px 22px;
                        border:1px solid #94a3b8;
                        border-radius:7px;
                        background:white;
                        color:#1e293b;
                        cursor:pointer;
                    ">
                ↺ Reset
            </button>
        </div>

        <div id="lr-info"
             style="
                margin-top:18px;
                padding:14px;
                border:1px solid #e2e8f0;
                border-radius:8px;
                background:white;
                line-height:1.8;
             ">
            <strong>Current model:</strong>
            f(x) = 0.30x + 2.00
            <br>
            <strong>Weight:</strong> 0.30
            <br>
            <strong>Bias:</strong> 2.00
        </div>
    </div>
    """

    # ---------------------------------------------------------
    # 6. JavaScript: interactive controls and animation
    # ---------------------------------------------------------
    post_script = r"""
    (() => {
        const targetW = __TARGET_W__;
        const targetB = __TARGET_B__;

        const initialW = 0.3;
        const initialB = 2.0;

        const xMin = -0.5;
        const xMax = 6.5;
        const linePoints = 200;

        const xLine = Array.from(
            { length: linePoints },
            (_, i) => xMin + (xMax - xMin) * i / (linePoints - 1)
        );

        let animationTimer = null;
        let animationStart = null;
        let startW = initialW;
        let startB = initialB;

        function initialize(attempt = 0) {
            const plot = document.querySelector(".js-plotly-plot");

            const get = (id) => document.getElementById(id);

            const wInput = get("lr-w");
            const bInput = get("lr-b");
            const speedInput = get("lr-speed");

            const wValue = get("lr-w-value");
            const bValue = get("lr-b-value");
            const speedValue = get("lr-speed-value");

            const info = get("lr-info");

            const playButton = get("lr-play");
            const pauseButton = get("lr-pause");
            const resetButton = get("lr-reset");

            const required = [
                plot,
                wInput,
                bInput,
                speedInput,
                wValue,
                bValue,
                speedValue,
                info,
                playButton,
                pauseButton,
                resetButton
            ];

            if (required.some(element => element === null)) {
                if (attempt < 120) {
                    setTimeout(() => initialize(attempt + 1), 50);
                } else {
                    console.error(
                        "Linear Regression: controls could not be initialized."
                    );
                }
                return;
            }

            function stopAnimation() {
                if (animationTimer !== null) {
                    clearInterval(animationTimer);
                    animationTimer = null;
                }
            }

            function updateGraph(w, b) {
                const yLine = xLine.map(x => w * x + b);

                Plotly.restyle(
                    plot,
                    {
                        x: [xLine],
                        y: [yLine]
                    },
                    [1]
                );

                wInput.value = w;
                bInput.value = b;

                wValue.textContent = w.toFixed(2);
                bValue.textContent = b.toFixed(2);

                const equation =
                    `f(x) = ${w.toFixed(2)}x ` +
                    `${b >= 0 ? "+" : "-"} ${Math.abs(b).toFixed(2)}`;

                info.innerHTML = `
                    <strong>Current model:</strong> ${equation}
                    <br>
                    <strong>Weight (w):</strong> ${w.toFixed(2)}
                    — controls the slope
                    <br>
                    <strong>Bias (b):</strong> ${b.toFixed(2)}
                    — controls the vertical intercept
                    <br>
                    <strong>Reference solution:</strong>
                    w = ${targetW.toFixed(3)},
                    b = ${targetB.toFixed(3)}
                `;
            }

            function animate() {
                stopAnimation();

                startW = Number(wInput.value);
                startB = Number(bInput.value);

                animationStart = performance.now();

                const duration = Number(speedInput.value);

                animationTimer = setInterval(() => {
                    const elapsed = performance.now() - animationStart;
                    const progress = Math.min(elapsed / duration, 1);

                    // Smooth ease-in-out interpolation.
                    const eased = progress * progress * (3 - 2 * progress);

                    const w = startW + (targetW - startW) * eased;
                    const b = startB + (targetB - startB) * eased;

                    updateGraph(w, b);

                    if (progress >= 1) {
                        stopAnimation();
                        updateGraph(targetW, targetB);
                    }
                }, 30);
            }

            function reset() {
                stopAnimation();
                updateGraph(initialW, initialB);
            }

            wInput.addEventListener("input", () => {
                stopAnimation();
                updateGraph(
                    Number(wInput.value),
                    Number(bInput.value)
                );
            });

            bInput.addEventListener("input", () => {
                stopAnimation();
                updateGraph(
                    Number(wInput.value),
                    Number(bInput.value)
                );
            });

            speedInput.addEventListener("input", () => {
                speedValue.textContent = `${speedInput.value} ms`;
            });

            playButton.addEventListener("click", animate);
            pauseButton.addEventListener("click", stopAnimation);
            resetButton.addEventListener("click", reset);

            updateGraph(initialW, initialB);
        }

        initialize();
    })();
    """

    # Inject the least-squares parameters into the JavaScript.
    post_script = (
        post_script
        .replace("__TARGET_W__", repr(float(target_w)))
        .replace("__TARGET_B__", repr(float(target_b)))
    )

    # ---------------------------------------------------------
    # 7. Caption
    # ---------------------------------------------------------
    caption = """
    <p>
        Một mô hình <b>hồi quy tuyến tính đơn giản
        (Simple Linear Regression)</b> được biểu diễn bằng
        một đường thẳng khớp với các điểm dữ liệu.
    </p>

    <p>
        Mô hình có dạng:
        <b>f(x; w, b) = wx + b</b>.
        Trong đó, hai tham số <b>w</b> và <b>b</b>
        quyết định hình dạng và vị trí của đường thẳng.
    </p>

    <p>
        <b>Weight (w)</b> quyết định độ dốc (slope).
        Khi w thay đổi, đường thẳng sẽ nghiêng nhiều hơn,
        ít hơn hoặc đổi hướng.
    </p>

    <p>
        <b>Bias (b)</b> quyết định tung độ gốc
        (y-intercept). Khi b thay đổi mà w giữ nguyên,
        đường thẳng sẽ dịch chuyển lên hoặc xuống.
    </p>

    <p>
        Hãy thử thay đổi w và b bằng các thanh trượt.
        Nhấn <b>Play fitting</b> để quan sát đường thẳng
        chuyển dần đến nghiệm bình phương tối thiểu
        (Least Squares) của bộ dữ liệu minh họa.
    </p>

    <p>
        Các điểm màu xanh là dữ liệu quan sát.
        Đường màu cam là mô hình hiện tại.
        Đường nét đứt màu xanh lá biểu diễn nghiệm
        Least Squares tham chiếu.
    </p>
    """

    # ---------------------------------------------------------
    # 8. Export HTML
    # ---------------------------------------------------------
    plot_html = fig.to_html(
        full_html=False,
        include_plotlyjs=True,
        auto_play=False,
        config=dict(PLOTLY_CONFIG),
        post_script=post_script,
    )

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

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / OUTPUT_FILENAME
    output_path.write_text(
        page_html,
        encoding="utf-8",
    )

    return output_path
