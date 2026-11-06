
"""Minh họa đạo hàm và hướng di chuyển của Gradient Descent."""

import numpy as np
import plotly.graph_objects as go

from function_visualization.core.figure import (
    configure_figure,
    export_figure,
)


GRAPH_ID = "gradient_descent"
OUTPUT_FILENAME = "gradient_descent.html"
TITLE = "Gradient Descent và đạo hàm"


def function(x):
    """Hàm số f(x) = x²."""
    return x ** 2


def derivative(x):
    """Đạo hàm f'(x) = 2x."""
    return 2 * x


def build(output_dir):
    # ---------------------------------------------------------
    # 1. Dữ liệu hàm số
    # ---------------------------------------------------------

    x_values = np.linspace(-4, 4, 400)
    y_values = function(x_values)

    # Vị trí ban đầu
    current_x = 2.0
    current_y = function(current_x)
    current_gradient = derivative(current_x)

    # Learning rate dùng để minh họa hướng cập nhật
    learning_rate = 0.2
    next_x = current_x - learning_rate * current_gradient

    # Tiếp tuyến tại x = 2:
    # y = f(2) + f'(2)(x - 2)
    tangent_x = np.linspace(
        current_x - 1.2,
        current_x + 1.2,
        100,
    )
    tangent_y = (
        current_y
        + current_gradient * (tangent_x - current_x)
    )

    # ---------------------------------------------------------
    # 2. Khởi tạo biểu đồ
    # ---------------------------------------------------------

    fig = go.Figure()

    # Trace 0: Đường cong f(x) = x²
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines",
            name="Hàm số f(x) = x²",
            line=dict(
                width=3,
                color="#2563eb",
            ),
            hovertemplate=(
                "x = %{x:.2f}<br>"
                "f(x) = %{y:.2f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 1: Điểm hiện tại
    fig.add_trace(
        go.Scatter(
            x=[current_x],
            y=[current_y],
            mode="markers",
            name="Vị trí hiện tại",
            marker=dict(
                size=14,
                color="#f59e0b",
                line=dict(width=2, color="white"),
            ),
            hovertemplate=(
                "x = %{x:.2f}<br>"
                "f(x) = %{y:.2f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 2: Tiếp tuyến tại vị trí hiện tại
    fig.add_trace(
        go.Scatter(
            x=tangent_x,
            y=tangent_y,
            mode="lines",
            name="Tiếp tuyến",
            line=dict(
                width=2.5,
                color="#dc2626",
                dash="dash",
            ),
            hoverinfo="skip",
        )
    )

    # Điểm cực tiểu
    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers",
            name="Điểm cực tiểu",
            marker=dict(
                size=15,
                color="#16a34a",
                symbol="star",
                line=dict(width=1, color="white"),
            ),
            hovertemplate=(
                "Điểm cực tiểu<br>"
                "x* = 0<br>"
                "f(x*) = 0"
                "<extra></extra>"
            ),
        )
    )

    # ---------------------------------------------------------
    # 3. Mũi tên chỉ hướng Gradient Descent
    # ---------------------------------------------------------

    fig.add_annotation(
        x=next_x,
        y=0.55,
        ax=current_x,
        ay=0.55,
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        showarrow=True,
        arrowhead=3,
        arrowsize=1.4,
        arrowwidth=3,
        arrowcolor="#2563eb",
        text="",
    )

    # ---------------------------------------------------------
    # 4. Cấu hình biểu đồ
    # ---------------------------------------------------------

    fig = configure_figure(
        fig=fig,
        title="Gradient Descent: f(x) = x²",
        xaxis_title="Vị trí x",
        yaxis_title="Giá trị hàm số f(x)",
    )

    fig.update_xaxes(range=[-4, 4])
    fig.update_yaxes(range=[-1, 18])

    # ---------------------------------------------------------
    # 5. Caption giải thích
    # ---------------------------------------------------------

    caption = r"""
    <strong>Đạo hàm và hướng di chuyển của Gradient Descent</strong>

    <br><br>

    Giả sử chúng ta đang ở vị trí \(x=2\).
    Giá trị của hàm số tại đó là:

    \[
        f(2)=2^2=4
    \]

    Đạo hàm tại điểm này là:

    \[
        f'(2)=2\times 2=4
    \]

    Vì đạo hàm dương nên hàm số đang tăng tại đây.
    Đường tiếp tuyến màu đỏ nét đứt thể hiện độ dốc dương.

    <br><br>

    <strong>Gradient Descent</strong> sử dụng giá trị đạo hàm
    dương này để xác định rằng cần di chuyển \(x\) sang trái
    (giảm \(x\)), như mũi tên màu xanh chỉ dẫn.

    Bước di chuyển này đưa chúng ta đến gần điểm cực tiểu
    tại \(x=0\).

    <br><br>

    Về mặt toán học, quy tắc cập nhật tham số là:

    \[
        x_{\text{new}} = x - \eta f'(x)
    \]

    Trong đó \(\eta\) là learning rate (tốc độ học).

    <br><br>

    Hãy thay đổi vị trí \(x\) bằng thanh trượt để quan sát
    đạo hàm, tiếp tuyến và hướng di chuyển thay đổi.
    """

    # ---------------------------------------------------------
    # 6. Xuất HTML
    # ---------------------------------------------------------

    return export_figure(
        fig=fig,
        output_dir=output_dir,
        filename=OUTPUT_FILENAME,
        caption=caption,
        caption_title="Từ đạo hàm đến Gradient Descent",
        page_title="Gradient Descent - AI From Scratch",
        graph_id=GRAPH_ID,
    )
