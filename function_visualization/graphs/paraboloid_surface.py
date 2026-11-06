
"""Visualize the 3D paraboloid surface z = x^2 + y^2."""

from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from function_visualization.core.figure import (
    configure_figure,
    export_figure,
)


GRAPH_ID = "paraboloid_surface"
OUTPUT_FILENAME = "paraboloid_surface.html"
TITLE = "Mặt Paraboloid: z = x² + y²"


def function(x, y):
    """Calculate f(x, y) = x^2 + y^2."""
    return x**2 + y**2


def build(output_dir):
    """Build and export the 3D paraboloid visualization."""

    # ---------------------------------------------------------
    # 1. Generate input coordinates
    # ---------------------------------------------------------
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)

    # Create a 2D coordinate grid.
    X, Y = np.meshgrid(x, y)

    # Calculate the output value at every coordinate.
    Z = function(X, Y)

    # ---------------------------------------------------------
    # 2. Create 3D figure
    # ---------------------------------------------------------
    fig = go.Figure()

    # Paraboloid surface
    fig.add_trace(
        go.Surface(
            x=X,
            y=Y,
            z=Z,
            name="f(x, y) = x² + y²",
            colorscale="Viridis",
            opacity=0.95,
            showscale=True,
            colorbar=dict(
                title=dict(
                    text="z = f(x, y)",
                    side="right",
                ),
                thickness=15,
                len=0.7,
            ),
            contours=dict(
                z=dict(
                    show=True,
                    usecolormap=True,
                    highlightcolor="white",
                    project_z=False,
                )
            ),
            hovertemplate=(
                "x = %{x:.2f}<br>"
                "y = %{y:.2f}<br>"
                "z = %{z:.2f}"
                "<extra>Paraboloid</extra>"
            ),
        )
    )

    # ---------------------------------------------------------
    # 3. Mark the global minimum
    # ---------------------------------------------------------
    minimum_x = 0
    minimum_y = 0
    minimum_z = function(minimum_x, minimum_y)

    fig.add_trace(
        go.Scatter3d(
            x=[minimum_x],
            y=[minimum_y],
            z=[minimum_z],
            mode="markers+text",
            name="Điểm cực tiểu",
            marker=dict(
                size=8,
                color="#EF4444",
                symbol="diamond",
                line=dict(
                    color="white",
                    width=2,
                ),
            ),
            text=["Minimum (0, 0, 0)"],
            textposition="top center",
            textfont=dict(
                size=12,
                color="#EF4444",
            ),
            hovertemplate=(
                "x = 0<br>"
                "y = 0<br>"
                "z = 0"
                "<extra>Điểm cực tiểu</extra>"
            ),
        )
    )

    # ---------------------------------------------------------
    # 4. Configure figure style
    # ---------------------------------------------------------
    configure_figure(
        fig,
        title=TITLE,
        height=720,
    )

    fig.update_layout(
        scene=dict(
            xaxis=dict(
                title="x (Input 1)",
                range=[-3, 3],
                backgroundcolor="rgb(245, 247, 250)",
                gridcolor="white",
                zerolinecolor="#64748B",
            ),
            yaxis=dict(
                title="y (Input 2)",
                range=[-3, 3],
                backgroundcolor="rgb(245, 247, 250)",
                gridcolor="white",
                zerolinecolor="#64748B",
            ),
            zaxis=dict(
                title="z = f(x, y)",
                range=[0, 18],
                backgroundcolor="rgb(245, 247, 250)",
                gridcolor="white",
                zerolinecolor="#64748B",
            ),
            aspectmode="manual",
            aspectratio=dict(
                x=1,
                y=1,
                z=0.75,
            ),
            camera=dict(
                eye=dict(
                    x=1.6,
                    y=1.6,
                    z=1.2,
                )
            ),
        ),
        margin=dict(
            l=10,
            r=10,
            t=100,
            b=10,
        ),
        showlegend=True,
    )

    # ---------------------------------------------------------
    # 5. Caption
    # ---------------------------------------------------------
    caption = """
    <p>
        Ví dụ, xét hàm:
        <b>f(x, y) = x² + y²</b>.
    </p>

    <p>
        Hàm này mô tả một bề mặt có hình dạng như chiếc bát,
        được gọi là <b>mặt paraboloid (paraboloid)</b>,
        mở lên trên.
    </p>

    <p>
        Điểm thấp nhất của bề mặt nằm tại
        <b>(x, y) = (0, 0)</b>, nơi
        <b>f(0, 0) = 0</b>.
    </p>

    <p>
        Đồ thị bề mặt của <b>z = x² + y²</b>.
        Hai đầu vào <b>x</b> và <b>y</b> tạo thành mặt phẳng đáy,
        còn độ cao <b>z</b> biểu diễn giá trị đầu ra của hàm.
        Hãy chú ý rằng giá trị nhỏ nhất xuất hiện tại
        gốc tọa độ <b>(0, 0)</b>.
    </p>
    """

    # ---------------------------------------------------------
    # 6. Export HTML
    # ---------------------------------------------------------
    return export_figure(
        fig=fig,
        output_dir=output_dir,
        filename=OUTPUT_FILENAME,
        caption=caption,
        caption_title=TITLE,
        page_title=TITLE,
        graph_id=GRAPH_ID,
    )
