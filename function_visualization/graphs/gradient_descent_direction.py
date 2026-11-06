
"""Visualize the direction of Gradient Descent on f(x) = x^2.

The graph illustrates:
- The objective function f(x) = x^2.
- The current point P(2, 4).
- The positive tangent slope f'(2) = 4.
- The direction Gradient Descent moves: toward smaller x.
- The minimum point at (0, 0).
"""

from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from function_visualization.core.figure import (
    configure_figure,
    export_figure,
)


GRAPH_ID = "gradient_descent_direction"
OUTPUT_FILENAME = "gradient_descent_direction.html"
TITLE = "Gradient Descent: Hướng di chuyển khi đạo hàm dương"


def function(x):
    """Objective function f(x) = x^2."""
    return x**2


def derivative(x):
    """Derivative f'(x) = 2x."""
    return 2 * x


def build(output_dir):
    """Build and export the Gradient Descent direction graph."""

    # ---------------------------------------------------------
    # 1. Define the function and current point
    # ---------------------------------------------------------
    x = np.linspace(-3, 4, 400)
    y = function(x)

    current_x = 2.0
    current_y = function(current_x)
    current_slope = derivative(current_x)

    # Tangent equation:
    # y - f(2) = f'(2)(x - 2)
    # y - 4 = 4(x - 2)
    # y = 4x - 4
    tangent_x = np.linspace(0.8, 2.8, 100)
    tangent_y = current_y + current_slope * (
        tangent_x - current_x
    )

    # Minimum point
    minimum_x = 0.0
    minimum_y = function(minimum_x)

    # ---------------------------------------------------------
    # 2. Create figure
    # ---------------------------------------------------------
    fig = go.Figure()

    # Objective function
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name="Hàm số f(x) = x²",
            line=dict(
                color="#2563EB",
                width=3,
            ),
            hovertemplate=(
                "x = %{x:.2f}<br>"
                "f(x) = %{y:.2f}"
                "<extra>Hàm số</extra>"
            ),
        )
    )

    # Tangent line at x = 2
    fig.add_trace(
        go.Scatter(
            x=tangent_x,
            y=tangent_y,
            mode="lines",
            name="Tiếp tuyến tại x = 2",
            line=dict(
                color="#EF4444",
                width=2.5,
                dash="dash",
            ),
            hovertemplate=(
                "x = %{x:.2f}<br>"
                "y = %{y:.2f}"
                "<extra>Tiếp tuyến</extra>"
            ),
        )
    )

    # Current point P(2, 4)
    fig.add_trace(
        go.Scatter(
            x=[current_x],
            y=[current_y],
            mode="markers+text",
            name="Vị trí hiện tại P(2, 4)",
            marker=dict(
                color="#F59E0B",
                size=13,
                line=dict(
                    color="white",
                    width=2,
                ),
            ),
            text=["P(2, 4)"],
            textposition="top right",
            textfont=dict(
                size=13,
                color="#B45309",
            ),
            hovertemplate=(
                "x = %{x}<br>"
                "f(x) = %{y}<br>"
                "<extra>Điểm hiện tại</extra>"
            ),
        )
    )

    # Minimum point (0, 0)
    fig.add_trace(
        go.Scatter(
            x=[minimum_x],
            y=[minimum_y],
            mode="markers+text",
            name="Điểm cực tiểu (0, 0)",
            marker=dict(
                color="#16A34A",
                size=13,
                symbol="star",
                line=dict(
                    color="white",
                    width=1.5,
                ),
            ),
            text=["Minimum (0, 0)"],
            textposition="bottom right",
            textfont=dict(
                size=12,
                color="#15803D",
            ),
            hovertemplate=(
                "x = %{x}<br>"
                "f(x) = %{y}"
                "<extra>Điểm cực tiểu</extra>"
            ),
        )
    )

    # ---------------------------------------------------------
    # 3. Annotations
    # ---------------------------------------------------------

    # Positive slope annotation
    fig.add_annotation(
        x=current_x,
        y=current_y,
        text="f′(2) = 4 > 0",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#EF4444",
        ax=65,
        ay=-55,
        font=dict(
            size=13,
            color="#DC2626",
        ),
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#FCA5A5",
        borderwidth=1,
        borderpad=5,
    )

    # Gradient Descent direction: move left
    # This is a directional illustration, not a numerical update step.
    fig.add_annotation(
        x=0.35,
        y=2.7,
        ax=2.4,
        ay=2.7,
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        text="",
        showarrow=True,
        arrowhead=3,
        arrowsize=1.5,
        arrowwidth=3,
        arrowcolor="#16A34A",
    )

    fig.add_annotation(
        x=1.35,
        y=3.05,
        text="Gradient Descent: giảm x",
        showarrow=False,
        font=dict(
            size=13,
            color="#15803D",
        ),
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#86EFAC",
        borderwidth=1,
        borderpad=5,
    )

    # ---------------------------------------------------------
    # 4. Configure layout
    # ---------------------------------------------------------
    configure_figure(
        fig,
        title=TITLE,
        xaxis_title="Vị trí x",
        yaxis_title="Giá trị f(x)",
        height=620,
    )

    fig.update_xaxes(
        range=[-3, 4],
        zeroline=True,
        zerolinewidth=1.5,
        zerolinecolor="#64748B",
    )

    fig.update_yaxes(
        range=[-1, 10],
        zeroline=True,
        zerolinewidth=1.5,
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
    )

    # ---------------------------------------------------------
    # 5. Caption
    # ---------------------------------------------------------
    caption = """
    <p>
        Hãy cùng hình dung quá trình này qua một ví dụ.
        Xét hàm số đơn giản <b>f(x) = x²</b>.
        Rõ ràng, giá trị nhỏ nhất của hàm đạt được tại
        <b>x = 0</b>. Đạo hàm của hàm số là
        <b>f′(x) = 2x</b>.
    </p>

    <p>
        Giả sử chúng ta đang ở vị trí <b>x = 2</b>.
        Giá trị của hàm số tại đó là
        <b>f(2) = 2² = 4</b>.
        Đạo hàm tại điểm này là
        <b>f′(2) = 2 × 2 = 4</b>.
    </p>

    <p>
        Vì đạo hàm dương nên hàm số đang tăng tại đây
        (đường tiếp tuyến màu đỏ nét đứt thể hiện độ dốc dương).
        <b>Gradient Descent</b> sử dụng giá trị đạo hàm dương này
        để xác định rằng cần di chuyển x sang trái (giảm x),
        như mũi tên màu xanh chỉ dẫn.
        Bước di chuyển này đưa chúng ta đến gần điểm cực tiểu
        tại <b>x = 0</b>.
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
