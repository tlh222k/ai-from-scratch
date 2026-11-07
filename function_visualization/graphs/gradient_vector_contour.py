
"""Interactive gradient vector visualization on a contour plot.

Function:
    f(x, y) = x^2 + y^2

Features:
    - Contour lines
    - Gradient vectors
    - Adjustable x and y coordinates
    - Adjustable vector scale
    - Adjustable contour levels
    - Play/Pause animation
    - Adjustable animation speed
    - Real-time gradient information
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


# =============================================================
# 1. GRAPH CONFIGURATION
# =============================================================

GRAPH_ID = "gradient_vector_contour"
OUTPUT_FILENAME = "gradient_vector_contour.html"

TITLE = "Gradient Vector trên Contour Plot"


# =============================================================
# 2. MATHEMATICAL FUNCTIONS
# =============================================================

def function(x, y):
    """Calculate f(x, y) = x^2 + y^2."""
    return x**2 + y**2


def gradient(x, y):
    """
    Calculate the gradient vector.

    ∇f(x, y) = (2x, 2y)
    """
    return 2 * x, 2 * y


def gradient_magnitude(x, y):
    """Calculate the magnitude of the gradient vector."""
    gx, gy = gradient(x, y)
    return np.sqrt(gx**2 + gy**2)


# =============================================================
# 3. INITIAL GRAPH CONFIGURATION
# =============================================================

INITIAL_X = 1.5
INITIAL_Y = 1.0

INITIAL_VECTOR_SCALE = 0.20
INITIAL_CONTOUR_LEVELS = 12

INITIAL_ANIMATION_SPEED = 500


# Fixed sample points for gradient vector visualization.
SAMPLE_POINTS = [
    (-1.5, -0.5),
    (-1.0, 1.0),
    (1.0, 1.0),
    (0.5, -1.5),
    (1.5, 0.5),
    (-1.5, 1.0),
    (-0.5, -1.5),
    (1.5, -1.0),
]


# =============================================================
# 4. GRADIENT VECTOR ANNOTATIONS
# =============================================================

def make_gradient_annotations(
    points,
    vector_scale,
    selected_point=None,
):
    """
    Generate Plotly arrow annotations for gradient vectors.

    Each vector starts at (x, y) and points toward:

        (x, y) + vector_scale * ∇f(x, y)
    """

    annotations = []

    for px, py in points:

        gx, gy = gradient(px, py)

        selected = (
            selected_point is not None
            and np.isclose(px, selected_point[0])
            and np.isclose(py, selected_point[1])
        )

        annotations.append(
            dict(
                x=px + gx * vector_scale,
                y=py + gy * vector_scale,

                ax=px,
                ay=py,

                xref="x",
                yref="y",

                axref="x",
                ayref="y",

                text="",
                showarrow=True,

                arrowhead=3,
                arrowsize=1.5 if selected else 1.2,
                arrowwidth=3.5 if selected else 2,

                arrowcolor=(
                    "#F59E0B"
                    if selected
                    else "#EF4444"
                ),
            )
        )

    return annotations


# =============================================================
# 5. HTML CONTROL PANEL
# =============================================================

def build_control_panel():

    return """
    <div
        id="gradient-vector-controls"
        style="
            margin: 20px auto;
            padding: 22px;
            max-width: 1000px;
            border: 1px solid #d1d5db;
            border-radius: 12px;
            background: #f8fafc;
            color: #1e293b;
            font-family: Arial, sans-serif;
        "
    >

        <h3 style="margin-top:0;">
            Gradient Vector Controls
        </h3>

        <p style="color:#64748b; font-size:14px;">
            Adjust the point and observe how the gradient vector changes.
        </p>

        <div
            style="
                display:grid;
                grid-template-columns:repeat(auto-fit,minmax(210px,1fr));
                gap:20px;
            "
        >

            <!-- X POSITION -->
            <div>
                <label for="gv-x">
                    X position:
                    <strong id="gv-x-value">1.50</strong>
                </label>

                <input
                    id="gv-x"
                    type="range"
                    min="-2"
                    max="2"
                    step="0.05"
                    value="1.5"
                    style="width:100%;"
                >
            </div>

            <!-- Y POSITION -->
            <div>
                <label for="gv-y">
                    Y position:
                    <strong id="gv-y-value">1.00</strong>
                </label>

                <input
                    id="gv-y"
                    type="range"
                    min="-2"
                    max="2"
                    step="0.05"
                    value="1"
                    style="width:100%;"
                >
            </div>

            <!-- VECTOR SCALE -->
            <div>
                <label for="gv-scale">
                    Vector scale:
                    <strong id="gv-scale-value">0.20</strong>
                </label>

                <input
                    id="gv-scale"
                    type="range"
                    min="0.05"
                    max="0.35"
                    step="0.01"
                    value="0.2"
                    style="width:100%;"
                >
            </div>

            <!-- CONTOUR LEVELS -->
            <div>
                <label for="gv-levels">
                    Contour levels:
                    <strong id="gv-levels-value">12</strong>
                </label>

                <input
                    id="gv-levels"
                    type="range"
                    min="5"
                    max="20"
                    step="1"
                    value="12"
                    style="width:100%;"
                >
            </div>

            <!-- ANIMATION SPEED -->
            <div>
                <label for="gv-speed">
                    Animation speed:
                    <strong id="gv-speed-value">500 ms</strong>
                </label>

                <input
                    id="gv-speed"
                    type="range"
                    min="100"
                    max="1200"
                    step="50"
                    value="500"
                    style="width:100%;"
                >
            </div>

        </div>

        <!-- ANIMATION BUTTONS -->
        <div
            style="
                display:flex;
                gap:10px;
                margin-top:22px;
                flex-wrap:wrap;
            "
        >

            <button
                id="gv-play"
                type="button"
                style="
                    padding:9px 22px;
                    border:0;
                    border-radius:7px;
                    background:#2563eb;
                    color:white;
                    cursor:pointer;
                "
            >
                ▶ Play
            </button>

            <button
                id="gv-pause"
                type="button"
                style="
                    padding:9px 22px;
                    border:0;
                    border-radius:7px;
                    background:#64748b;
                    color:white;
                    cursor:pointer;
                "
            >
                ⏸ Pause
            </button>

            <button
                id="gv-reset"
                type="button"
                style="
                    padding:9px 22px;
                    border:1px solid #94a3b8;
                    border-radius:7px;
                    background:white;
                    color:#1e293b;
                    cursor:pointer;
                "
            >
                ↺ Reset
            </button>

        </div>

        <!-- MATHEMATICAL INFORMATION -->
        <div
            id="gv-info"
            style="
                margin-top:18px;
                padding:14px;
                border-radius:8px;
                background:white;
                border:1px solid #e2e8f0;
                line-height:1.8;
            "
        >
            <strong>Current point:</strong> (1.50, 1.00)
            <br>

            <strong>Gradient:</strong> ∇f = (3.00, 2.00)
            <br>

            <strong>Function value:</strong> f(x,y) = 3.25
            <br>

            <strong>Gradient magnitude:</strong> 3.61
        </div>

    </div>
    """


# =============================================================
# 6. JAVASCRIPT INTERACTION
# =============================================================

POST_SCRIPT = r"""
(() => {

    let initialized = false;
    let animationTimer = null;
    let animationIndex = 0;

    const MAX_INIT_ATTEMPTS = 120;

    const initial = {
        x: 1.5,
        y: 1.0,
        scale: 0.20,
        levels: 12,
        speed: 500
    };

    const samplePoints = [
        [-1.5, -0.5],
        [-1.0, 1.0],
        [1.0, 1.0],
        [0.5, -1.5],
        [1.5, 0.5],
        [-1.5, 1.0],
        [-0.5, -1.5],
        [1.5, -1.0]
    ];

    function initGradientVectorControls(attempt = 0) {

        if (initialized) return;

        const get = (id) => document.getElementById(id);

        // Find the Plotly chart.
        const plot = document.querySelector(".js-plotly-plot");

        // Find all HTML controls.
        const xInput = get("gv-x");
        const yInput = get("gv-y");
        const scaleInput = get("gv-scale");
        const levelsInput = get("gv-levels");
        const speedInput = get("gv-speed");

        const xValue = get("gv-x-value");
        const yValue = get("gv-y-value");
        const scaleValue = get("gv-scale-value");
        const levelsValue = get("gv-levels-value");
        const speedValue = get("gv-speed-value");

        const info = get("gv-info");

        const playButton = get("gv-play");
        const pauseButton = get("gv-pause");
        const resetButton = get("gv-reset");

        const requiredElements = [
            plot,
            xInput,
            yInput,
            scaleInput,
            levelsInput,
            speedInput,
            xValue,
            yValue,
            scaleValue,
            levelsValue,
            speedValue,
            info,
            playButton,
            pauseButton,
            resetButton
        ];

        // Wait until every element exists.
        if (requiredElements.some(element => element === null)) {

            if (attempt < MAX_INIT_ATTEMPTS) {

                requestAnimationFrame(() => {
                    initGradientVectorControls(attempt + 1);
                });

            } else {

                console.error(
                    "Gradient Vector: Initialization failed. " +
                    "Required HTML elements were not found."
                );

            }

            return;
        }

        // Prevent duplicate event registration.
        initialized = true;

        // -----------------------------------------------------
        // CREATE GRADIENT ANNOTATIONS
        // -----------------------------------------------------

        function makeAnnotations(x, y, scale) {

            const points = [
                ...samplePoints,
                [x, y]
            ];

            return points.map(([px, py], index) => {

                const gx = 2 * px;
                const gy = 2 * py;

                const selected = index === points.length - 1;

                return {

                    x: px + gx * scale,
                    y: py + gy * scale,

                    ax: px,
                    ay: py,

                    xref: "x",
                    yref: "y",

                    axref: "x",
                    ayref: "y",

                    text: "",
                    showarrow: true,

                    arrowhead: 3,
                    arrowsize: selected ? 1.6 : 1.2,
                    arrowwidth: selected ? 3.5 : 2,

                    arrowcolor: selected
                        ? "#F59E0B"
                        : "#EF4444"
                };

            });
        }

        // -----------------------------------------------------
        // UPDATE MATHEMATICAL INFORMATION
        // -----------------------------------------------------

        function updateInfo(x, y) {

            const gx = 2 * x;
            const gy = 2 * y;

            const z = x * x + y * y;

            const magnitude = Math.sqrt(
                gx * gx + gy * gy
            );

            info.innerHTML = `

                <strong>Current point:</strong>
                (${x.toFixed(2)}, ${y.toFixed(2)})

                <br>

                <strong>Gradient:</strong>
                ∇f = (${gx.toFixed(2)}, ${gy.toFixed(2)})

                <br>

                <strong>Function value:</strong>
                f(x,y) = ${z.toFixed(2)}

                <br>

                <strong>Gradient magnitude:</strong>
                ${magnitude.toFixed(2)}

            `;
        }

        // -----------------------------------------------------
        // UPDATE GRAPH
        // -----------------------------------------------------

        function updateGraph() {

            const x = Number(xInput.value);
            const y = Number(yInput.value);

            const scale = Number(scaleInput.value);
            const levels = Number(levelsInput.value);
            const speed = Number(speedInput.value);

            // Update labels.
            xValue.textContent = x.toFixed(2);
            yValue.textContent = y.toFixed(2);

            scaleValue.textContent = scale.toFixed(2);
            levelsValue.textContent = String(levels);
            speedValue.textContent = `${speed} ms`;

            // Update selected point.
            Plotly.restyle(
                plot,
                {
                    x: [[x]],
                    y: [[y]],
                    customdata: [[x * x + y * y]]
                },
                [2]
            );

            // Update contour levels.
            Plotly.restyle(
                plot,
                {
                    ncontours: levels
                },
                [0]
            );

            // Update all gradient arrows.
            Plotly.relayout(
                plot,
                {
                    annotations: makeAnnotations(
                        x,
                        y,
                        scale
                    )
                }
            );

            // Update mathematical information.
            updateInfo(x, y);
        }

        // -----------------------------------------------------
        // SET POSITION
        // -----------------------------------------------------

        function setPosition(x, y) {

            xInput.value = x;
            yInput.value = y;

            updateGraph();
        }

        // -----------------------------------------------------
        // ANIMATION
        // -----------------------------------------------------

        function stopAnimation() {

            if (animationTimer !== null) {

                clearTimeout(animationTimer);
                animationTimer = null;

            }
        }

        function animationStep() {

            const point = samplePoints[
                animationIndex % samplePoints.length
            ];

            setPosition(point[0], point[1]);

            animationIndex += 1;

            animationTimer = setTimeout(
                animationStep,
                Number(speedInput.value)
            );
        }

        function startAnimation() {

            stopAnimation();

            animationStep();
        }

        // -----------------------------------------------------
        // RESET
        // -----------------------------------------------------

        function reset() {

            stopAnimation();

            animationIndex = 0;

            xInput.value = initial.x;
            yInput.value = initial.y;

            scaleInput.value = initial.scale;
            levelsInput.value = initial.levels;
            speedInput.value = initial.speed;

            updateGraph();
        }

        // -----------------------------------------------------
        // EVENT LISTENERS
        // -----------------------------------------------------

        [
            xInput,
            yInput,
            scaleInput,
            levelsInput
        ].forEach(input => {

            input.addEventListener(
                "input",
                updateGraph
            );

        });

        speedInput.addEventListener("input", () => {

            speedValue.textContent =
                `${speedInput.value} ms`;

            // Restart timer with the new speed.
            if (animationTimer !== null) {
                startAnimation();
            }

        });

        playButton.addEventListener(
            "click",
            startAnimation
        );

        pauseButton.addEventListener(
            "click",
            stopAnimation
        );

        resetButton.addEventListener(
            "click",
            reset
        );

        // Initial rendering.
        updateGraph();

        console.log(
            "Gradient Vector controls initialized successfully."
        );
    }

    // Start initialization.
    // Retry while the HTML controls are being inserted.
    initGradientVectorControls();

})();
"""


# =============================================================
# 7. MAIN BUILD FUNCTION
# =============================================================

def build(output_dir):
    """Build and export the interactive gradient contour graph."""

    # ---------------------------------------------------------
    # Generate coordinate grid
    # ---------------------------------------------------------

    axis = np.linspace(-2.5, 2.5, 180)

    X, Y = np.meshgrid(axis, axis)

    Z = function(X, Y)

    # ---------------------------------------------------------
    # Create figure
    # ---------------------------------------------------------

    fig = go.Figure()

    # Trace 0: Contour plot.
    fig.add_trace(
        go.Contour(
            x=axis,
            y=axis,
            z=Z,

            name="Contour lines",

            ncontours=INITIAL_CONTOUR_LEVELS,

            contours=dict(
                coloring="lines",
                showlabels=True,

                labelfont=dict(
                    size=11,
                    color="#334155",
                ),
            ),

            line=dict(
                width=1.2,
            ),

            colorscale=[
                [0.0, "#2563EB"],
                [1.0, "#60A5FA"],
            ],

            showscale=False,

            hovertemplate=(
                "x = %{x:.2f}<br>"
                "y = %{y:.2f}<br>"
                "f(x,y) = %{z:.2f}"
                "<extra>Contour</extra>"
            ),
        )
    )

    # Trace 1: Fixed sample points.
    fig.add_trace(
        go.Scatter(
            x=[point[0] for point in SAMPLE_POINTS],
            y=[point[1] for point in SAMPLE_POINTS],

            mode="markers",

            name="Sample points",

            marker=dict(
                size=8,
                color="#EF4444",

                line=dict(
                    color="white",
                    width=1.5,
                ),
            ),

            hovertemplate=(
                "x = %{x:.2f}<br>"
                "y = %{y:.2f}"
                "<extra>Sample point</extra>"
            ),
        )
    )

    # Trace 2: Selected point.
    fig.add_trace(
        go.Scatter(
            x=[INITIAL_X],
            y=[INITIAL_Y],

            mode="markers+text",

            name="Selected point",

            marker=dict(
                size=13,
                color="#F59E0B",
                symbol="circle",

                line=dict(
                    color="white",
                    width=2,
                ),
            ),

            text=["P"],
            textposition="top right",

            textfont=dict(
                size=13,
                color="#B45309",
            ),

            customdata=[
                [function(INITIAL_X, INITIAL_Y)]
            ],

            hovertemplate=(
                "x = %{x:.2f}<br>"
                "y = %{y:.2f}<br>"
                "f(x,y) = %{customdata[0]:.2f}"
                "<extra>Selected point</extra>"
            ),
        )
    )

    # ---------------------------------------------------------
    # Configure figure appearance
    # ---------------------------------------------------------

    configure_figure(
        fig,
        title=TITLE,
        xaxis_title="x",
        yaxis_title="y",
        height=650,
    )

    fig.update_layout(
        annotations=make_gradient_annotations(
            points=SAMPLE_POINTS,
            vector_scale=INITIAL_VECTOR_SCALE,
            selected_point=(INITIAL_X, INITIAL_Y),
        ),

        xaxis=dict(
            range=[-2.5, 2.5],

            zeroline=True,
            zerolinewidth=1.5,
            zerolinecolor="#475569",

            scaleanchor="y",
            scaleratio=1,
        ),

        yaxis=dict(
            range=[-2.5, 2.5],

            zeroline=True,
            zerolinewidth=1.5,
            zerolinecolor="#475569",
        ),

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
    # Build control panel
    # ---------------------------------------------------------

    panel_html = build_control_panel()

    # ---------------------------------------------------------
    # Build caption
    # ---------------------------------------------------------

    caption = """
    <p>
        Xét hàm hai biến:
        <b>f(x, y) = x² + y²</b>.
        Hàm số có điểm cực tiểu tại gốc tọa độ (0, 0).
    </p>

    <p>
        <b>Contour lines (đường đồng mức)</b> biểu diễn
        những điểm có cùng giá trị hàm số.
        Với hàm này, chúng tạo thành những đường tròn
        đồng tâm quanh gốc tọa độ.
    </p>

    <p>
        <b>Gradient vector (vector gradient)</b> được xác định bởi:
        <b>∇f(x, y) = (2x, 2y)</b>.
        Vector này chỉ về hướng hàm số tăng nhanh nhất.
    </p>

    <p>
        Hãy quan sát hai đặc điểm:
    </p>

    <ol>
        <li>
            Vector gradient tại một điểm khác gốc tọa độ
            vuông góc với đường đồng mức đi qua điểm đó.
        </li>

        <li>
            Vector gradient hướng về phía giá trị hàm số lớn hơn,
            tức là hướng ra xa điểm cực tiểu (0, 0).
        </li>
    </ol>

    <p>
        Thử thay đổi tọa độ (x, y), độ dài vector
        và số đường đồng mức.
        Nhấn Play để quan sát vector gradient tại nhiều vị trí.
    </p>
    """

    caption_html = build_caption_html(
        caption,
        TITLE,
        "16px",
    )

    # ---------------------------------------------------------
    # Export Plotly HTML
    # ---------------------------------------------------------

    plot_html = fig.to_html(
        full_html=False,

        include_plotlyjs=True,

        auto_play=False,

        config=dict(PLOTLY_CONFIG),

        post_script=POST_SCRIPT,
    )

    # ---------------------------------------------------------
    # Render complete HTML page
    # ---------------------------------------------------------

    page_html = render_page(
        title=TITLE,
        plot_html=plot_html,
        caption_html=caption_html,
        panel_html=panel_html,
    )

    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = output_dir / OUTPUT_FILENAME

    output_path.write_text(
        page_html,
        encoding="utf-8",
    )

    return output_path
