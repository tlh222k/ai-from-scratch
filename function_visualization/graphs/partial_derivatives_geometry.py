
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

GRAPH_ID = "partial_derivatives_geometry"
OUTPUT_FILENAME = "partial_derivatives_geometry.html"

TITLE = "Ý nghĩa hình học của đạo hàm riêng"

X_MIN = -2.0
X_MAX = 2.0
Y_MIN = -2.0
Y_MAX = 2.0

INITIAL_X = 1.0
INITIAL_Y = 1.0

# ============================================================
# 2. MATHEMATICAL FUNCTIONS
# ============================================================

def function(x, y):
    """
    f(x, y) = 0.5x² + y²
    """
    return 0.5 * x**2 + y**2


def partial_x(x, y):
    """
    ∂f/∂x = x
    """
    return x


def partial_y(x, y):
    """
    ∂f/∂y = 2y
    """
    return 2 * y


def tangent_x(x, x0, y0):
    """
    Tangent line along x-direction, keeping y = y0.

    z = f(x0, y0) + (∂f/∂x)(x0, y0) * (x - x0)
    """
    z0 = function(x0, y0)
    slope = partial_x(x0, y0)

    return z0 + slope * (x - x0)


def tangent_y(y, x0, y0):
    """
    Tangent line along y-direction, keeping x = x0.

    z = f(x0, y0) + (∂f/∂y)(x0, y0) * (y - y0)
    """
    z0 = function(x0, y0)
    slope = partial_y(x0, y0)

    return z0 + slope * (y - y0)


# ============================================================
# 3. BUILD GRAPH
# ============================================================

def build(output_dir: Path):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # Generate surface data
    # --------------------------------------------------------

    x = np.linspace(X_MIN, X_MAX, 70)
    y = np.linspace(Y_MIN, Y_MAX, 70)

    X, Y = np.meshgrid(x, y)
    Z = function(X, Y)

    # Initial observation point
    x0 = INITIAL_X
    y0 = INITIAL_Y
    z0 = float(function(x0, y0))

    # Slice coordinates
    slice_x = np.linspace(X_MIN, X_MAX, 150)
    slice_y = np.linspace(Y_MIN, Y_MAX, 150)

    # Red curve: y = y0, varying x
    red_z = function(slice_x, y0)

    # Blue curve: x = x0, varying y
    blue_z = function(x0, slice_y)

    # Tangent lines at (x0, y0)
    red_tangent_z = tangent_x(slice_x, x0, y0)
    blue_tangent_z = tangent_y(slice_y, x0, y0)

    # --------------------------------------------------------
    # Create figure
    # --------------------------------------------------------

    fig = go.Figure()

    # Trace 0: 3D surface
    fig.add_trace(
        go.Surface(
            x=X,
            y=Y,
            z=Z,
            name="Bề mặt z = 0.5x² + y²",
            colorscale="Blues",
            opacity=0.68,
            showscale=False,
            hovertemplate=(
                "Bề mặt<br>"
                "x = %{x:.2f}<br>"
                "y = %{y:.2f}<br>"
                "z = %{z:.2f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 1: Red slice, y = y0
    fig.add_trace(
        go.Scatter3d(
            x=slice_x,
            y=np.full_like(slice_x, y0),
            z=red_z,
            mode="lines",
            name="Lát cắt theo hướng x (y cố định)",
            line=dict(
                color="#ef4444",
                width=7,
            ),
            hovertemplate=(
                "Lát cắt y = y₀<br>"
                "x = %{x:.3f}<br>"
                "y = %{y:.3f}<br>"
                "z = %{z:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 2: Blue slice, x = x0
    fig.add_trace(
        go.Scatter3d(
            x=np.full_like(slice_y, x0),
            y=slice_y,
            z=blue_z,
            mode="lines",
            name="Lát cắt theo hướng y (x cố định)",
            line=dict(
                color="#2563eb",
                width=7,
            ),
            hovertemplate=(
                "Lát cắt x = x₀<br>"
                "x = %{x:.3f}<br>"
                "y = %{y:.3f}<br>"
                "z = %{z:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 3: Red tangent line along x
    fig.add_trace(
        go.Scatter3d(
            x=slice_x,
            y=np.full_like(slice_x, y0),
            z=red_tangent_z,
            mode="lines",
            name="Tiếp tuyến theo hướng x",
            line=dict(
                color="#f97316",
                width=5,
                dash="dash",
            ),
            hovertemplate=(
                "Tiếp tuyến theo hướng x<br>"
                "x = %{x:.3f}<br>"
                "z = %{z:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 4: Blue tangent line along y
    fig.add_trace(
        go.Scatter3d(
            x=np.full_like(slice_y, x0),
            y=slice_y,
            z=blue_tangent_z,
            mode="lines",
            name="Tiếp tuyến theo hướng y",
            line=dict(
                color="#06b6d4",
                width=5,
                dash="dash",
            ),
            hovertemplate=(
                "Tiếp tuyến theo hướng y<br>"
                "y = %{y:.3f}<br>"
                "z = %{z:.3f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 5: Current point
    fig.add_trace(
        go.Scatter3d(
            x=[x0],
            y=[y0],
            z=[z0],
            mode="markers",
            name="Điểm khảo sát",
            marker=dict(
                size=7,
                color="#f59e0b",
                line=dict(
                    color="white",
                    width=2,
                ),
            ),
            hovertemplate=(
                "Điểm khảo sát<br>"
                "x = %{x:.3f}<br>"
                "y = %{y:.3f}<br>"
                "z = %{z:.3f}"
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
        xaxis_title="Trục x",
        yaxis_title="Trục y",
        height=720,
    )

    fig.update_layout(
        template="plotly_white",
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
            l=0,
            r=0,
            t=105,
            b=0,
        ),
        scene=dict(
            xaxis=dict(
                title="x",
                range=[X_MIN, X_MAX],
                gridcolor="#dbeafe",
                zerolinecolor="#94a3b8",
            ),
            yaxis=dict(
                title="y",
                range=[Y_MIN, Y_MAX],
                gridcolor="#dbeafe",
                zerolinecolor="#94a3b8",
            ),
            zaxis=dict(
                title="z",
                range=[0, 9],
                gridcolor="#dbeafe",
                zerolinecolor="#94a3b8",
            ),
            aspectmode="cube",
            camera=dict(
                eye=dict(x=1.65, y=1.65, z=1.15),
            ),
        ),
    )

    # --------------------------------------------------------
    # 4. INTERACTIVE CONTROL PANEL
    # --------------------------------------------------------

    panel_html = """
    <div class="partial-derivative-panel">

        <div class="panel-heading">
            <h3>Khảo sát đạo hàm riêng trên bề mặt 3D</h3>

            <p>
                Thay đổi vị trí x₀ và y₀ để quan sát hai lát cắt,
                hai đường tiếp tuyến và độ dốc theo từng hướng.
            </p>
        </div>

        <div class="controls-grid">

            <div class="control-group">
                <div class="control-label">
                    <label for="partial-x">Vị trí x₀</label>
                    <strong id="partial-x-value">1.00</strong>
                </div>

                <input
                    id="partial-x"
                    type="range"
                    min="-2"
                    max="2"
                    step="0.05"
                    value="1"
                />
            </div>

            <div class="control-group">
                <div class="control-label">
                    <label for="partial-y">Vị trí y₀</label>
                    <strong id="partial-y-value">1.00</strong>
                </div>

                <input
                    id="partial-y"
                    type="range"
                    min="-2"
                    max="2"
                    step="0.05"
                    value="1"
                />
            </div>

        </div>

        <div class="metrics-grid">

            <div class="metric-card">
                <span>Điểm khảo sát z = f(x₀, y₀)</span>
                <strong id="partial-z">1.5000</strong>
            </div>

            <div class="metric-card red-card">
                <span>Độ dốc theo hướng x</span>
                <strong id="partial-dx">1.0000</strong>
                <small>∂f/∂x = x₀</small>
            </div>

            <div class="metric-card blue-card">
                <span>Độ dốc theo hướng y</span>
                <strong id="partial-dy">2.0000</strong>
                <small>∂f/∂y = 2y₀</small>
            </div>

            <div class="metric-card">
                <span>Gradient tại điểm khảo sát</span>
                <strong id="partial-gradient">(1, 2)</strong>
                <small>∇f = (∂f/∂x, ∂f/∂y)</small>
            </div>

        </div>

        <div class="explanation-box">
            <div class="explanation-item">
                <span class="color-dot red-dot"></span>
                <div>
                    <strong>Hướng x – Đường màu đỏ</strong>
                    <p id="partial-explain-x">
                        Giữ y = 1 cố định và thay đổi x.
                        Độ dốc tại điểm khảo sát bằng 1.
                    </p>
                </div>
            </div>

            <div class="explanation-item">
                <span class="color-dot blue-dot"></span>
                <div>
                    <strong>Hướng y – Đường màu xanh</strong>
                    <p id="partial-explain-y">
                        Giữ x = 1 cố định và thay đổi y.
                        Độ dốc tại điểm khảo sát bằng 2.
                    </p>
                </div>
            </div>
        </div>

        <div class="control-buttons">
            <button id="partial-play" type="button">
                ▶ Play
            </button>

            <button id="partial-pause" type="button">
                ⏸ Pause
            </button>

            <button id="partial-reset" type="button">
                ↺ Reset
            </button>
        </div>

        <div class="formula-box">
            <strong>Các công thức cần quan sát</strong>

            <div class="formula">
                f(x, y) = 0.5x² + y²
            </div>

            <div class="formula">
                ∂f/∂x = x
            </div>

            <div class="formula">
                ∂f/∂y = 2y
            </div>

            <div class="formula">
                ∇f(x, y) = (x, 2y)
            </div>
        </div>

    </div>

    <style>

        .partial-derivative-panel {
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
            font-size: 20px;
            font-variant-numeric: tabular-nums;
            overflow-wrap: anywhere;
        }

        .metric-card small {
            color: #94a3b8;
            font-size: 11px;
        }

        .red-card {
            border-left: 4px solid #ef4444;
        }

        .red-card strong {
            color: #dc2626;
        }

        .blue-card {
            border-left: 4px solid #2563eb;
        }

        .blue-card strong {
            color: #2563eb;
        }

        .explanation-box {
            display: grid;
            gap: 14px;
            padding: 16px;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
        }

        .explanation-item {
            display: flex;
            align-items: flex-start;
            gap: 11px;
        }

        .explanation-item p {
            margin: 5px 0 0;
            color: #64748b;
            font-size: 13px;
            line-height: 1.6;
        }

        .color-dot {
            width: 11px;
            height: 11px;
            flex: 0 0 11px;
            margin-top: 4px;
            border-radius: 50%;
        }

        .red-dot {
            background: #ef4444;
        }

        .blue-dot {
            background: #2563eb;
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

        #partial-pause {
            background: #64748b;
        }

        #partial-reset {
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
            font-size: 19px;
            font-weight: 600;
        }

        @media (max-width: 600px) {
            .controls-grid,
            .metrics-grid {
                grid-template-columns: 1fr;
            }

            .metric-card {
                flex-direction: row;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
            }
        }

    </style>
    """

    # --------------------------------------------------------
    # 5. JAVASCRIPT: INTERACTION AND ANIMATION
    # --------------------------------------------------------

    post_script = r"""
    (function () {

        const INITIAL_X = 1.0;
        const INITIAL_Y = 1.0;

        const MIN_VALUE = -2.0;
        const MAX_VALUE = 2.0;

        const SLICE_POINTS = 150;

        let x0 = INITIAL_X;
        let y0 = INITIAL_Y;

        let timer = null;
        let isRunning = false;
        let animationStep = 0;

        function f(x, y) {
            return 0.5 * x * x + y * y;
        }

        function fx(x, y) {
            return x;
        }

        function fy(x, y) {
            return 2 * y;
        }

        function initialize(attempt = 0) {

            const plot = document.querySelector(".js-plotly-plot");
            const get = (id) => document.getElementById(id);

            const xInput = get("partial-x");
            const yInput = get("partial-y");

            const xValue = get("partial-x-value");
            const yValue = get("partial-y-value");

            const zValue = get("partial-z");
            const dxValue = get("partial-dx");
            const dyValue = get("partial-dy");
            const gradientValue = get("partial-gradient");

            const explainX = get("partial-explain-x");
            const explainY = get("partial-explain-y");

            const playButton = get("partial-play");
            const pauseButton = get("partial-pause");
            const resetButton = get("partial-reset");

            const required = [
                plot,
                xInput,
                yInput,
                xValue,
                yValue,
                zValue,
                dxValue,
                dyValue,
                gradientValue,
                explainX,
                explainY,
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
                        "Partial derivative controls could not be initialized."
                    );
                }

                return;
            }

            // ------------------------------------------------
            // Generate slice coordinates
            // ------------------------------------------------

            const slice = [];

            for (let i = 0; i < SLICE_POINTS; i++) {
                slice.push(
                    MIN_VALUE +
                    (MAX_VALUE - MIN_VALUE) * i / (SLICE_POINTS - 1)
                );
            }

            // ------------------------------------------------
            // Update graph
            // ------------------------------------------------

            function updateGraph() {

                const z0 = f(x0, y0);

                const slopeX = fx(x0, y0);
                const slopeY = fy(x0, y0);

                const redZ = slice.map(
                    x => f(x, y0)
                );

                const blueZ = slice.map(
                    y => f(x0, y)
                );

                const redTangentZ = slice.map(
                    x => z0 + slopeX * (x - x0)
                );

                const blueTangentZ = slice.map(
                    y => z0 + slopeY * (y - y0)
                );

                // Trace 1: Red slice y = y0
                Plotly.restyle(
                    plot,
                    {
                        x: [slice],
                        y: [slice.map(() => y0)],
                        z: [redZ]
                    },
                    [1]
                );

                // Trace 2: Blue slice x = x0
                Plotly.restyle(
                    plot,
                    {
                        x: [slice.map(() => x0)],
                        y: [slice],
                        z: [blueZ]
                    },
                    [2]
                );

                // Trace 3: Tangent along x
                Plotly.restyle(
                    plot,
                    {
                        x: [slice],
                        y: [slice.map(() => y0)],
                        z: [redTangentZ]
                    },
                    [3]
                );

                // Trace 4: Tangent along y
                Plotly.restyle(
                    plot,
                    {
                        x: [slice.map(() => x0)],
                        y: [slice],
                        z: [blueTangentZ]
                    },
                    [4]
                );

                // Trace 5: Current point
                Plotly.restyle(
                    plot,
                    {
                        x: [[x0]],
                        y: [[y0]],
                        z: [[z0]]
                    },
                    [5]
                );

                // Update controls
                xInput.value = x0;
                yInput.value = y0;

                xValue.textContent = x0.toFixed(2);
                yValue.textContent = y0.toFixed(2);

                // Update metrics
                zValue.textContent = z0.toFixed(4);
                dxValue.textContent = slopeX.toFixed(4);
                dyValue.textContent = slopeY.toFixed(4);

                gradientValue.textContent =
                    "(" + slopeX.toFixed(2) +
                    ", " + slopeY.toFixed(2) + ")";

                // Update explanations
                explainX.textContent =
                    "Giữ y = " + y0.toFixed(2) +
                    " cố định và thay đổi x. " +
                    "Độ dốc tại điểm khảo sát là " +
                    slopeX.toFixed(4) + ".";

                explainY.textContent =
                    "Giữ x = " + x0.toFixed(2) +
                    " cố định và thay đổi y. " +
                    "Độ dốc tại điểm khảo sát là " +
                    slopeY.toFixed(4) + ".";
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
            // Play: move along the diagonal x0 = y0
            // ------------------------------------------------

            function play() {

                if (isRunning) {
                    return;
                }

                if (animationStep >= 160) {
                    animationStep = 0;
                }

                isRunning = true;

                timer = setInterval(function () {

                    animationStep++;

                    const value =
                        MIN_VALUE +
                        (MAX_VALUE - MIN_VALUE) *
                        animationStep / 160;

                    x0 = value;
                    y0 = value;

                    updateGraph();

                    if (animationStep >= 160) {
                        stopAnimation();
                    }

                }, 45);
            }

            // ------------------------------------------------
            // Pause
            // ------------------------------------------------

            function pause() {
                stopAnimation();
            }

            // ------------------------------------------------
            // Reset
            // ------------------------------------------------

            function reset() {

                stopAnimation();

                animationStep = 0;

                x0 = INITIAL_X;
                y0 = INITIAL_Y;

                updateGraph();
            }

            // ------------------------------------------------
            // Manual controls
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
        Với hàm hai biến <strong>z = f(x, y) = 0.5x² + y²</strong>,
        đồ thị không còn là một đường cong trên mặt phẳng hai chiều,
        mà là một bề mặt trong không gian ba chiều.
        Tại mỗi điểm trên bề mặt, ta có thể khảo sát độ dốc
        theo từng hướng riêng biệt.
    </p>

    <p>
        Đạo hàm riêng theo x,
        <strong>∂f/∂x = x</strong>,
        mô tả độ dốc khi ta thay đổi x và giữ y cố định.
        Về mặt hình học, điều này tương ứng với việc cắt bề mặt
        bằng một mặt phẳng y = y₀ để tạo thành một đường cong.
        Độ dốc của tiếp tuyến với đường cong đó chính là
        đạo hàm riêng theo x.
    </p>

    <p>
        Tương tự, đạo hàm riêng theo y,
        <strong>∂f/∂y = 2y</strong>,
        mô tả độ dốc khi ta thay đổi y và giữ x cố định.
        Ta có thể hình dung điều này bằng cách cắt bề mặt
        bằng mặt phẳng x = x₀. Tiếp tuyến của đường cong thu được
        cho biết độ dốc theo hướng y.
    </p>

    <p>
        Tại điểm khảo sát <strong>(1, 1)</strong>,
        giá trị hàm số là <strong>f(1, 1) = 1.5</strong>.
        Đạo hàm riêng theo x bằng <strong>1</strong>,
        còn đạo hàm riêng theo y bằng <strong>2</strong>.
        Như vậy, tại điểm này, bề mặt có độ dốc khác nhau
        theo hai hướng đang xét.
    </p>

    <p>
        Hãy thay đổi hai thanh trượt x₀ và y₀ để di chuyển
        điểm khảo sát trên bề mặt. Đường màu đỏ biểu diễn lát cắt
        khi giữ y cố định; đường màu xanh biểu diễn lát cắt
        khi giữ x cố định. Các đường nét đứt là tiếp tuyến
        tương ứng tại điểm khảo sát.
    </p>

    <p>
        Hai đạo hàm riêng có thể được kết hợp thành
        <strong>Gradient</strong>:
        <strong>∇f(x, y) = (x, 2y)</strong>.
        Gradient tập hợp thông tin về tốc độ thay đổi của hàm số
        theo các trục tọa độ. Đây là nền tảng quan trọng để hiểu
        đạo hàm của hàm nhiều biến và Gradient Descent
        trong Machine Learning.
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
