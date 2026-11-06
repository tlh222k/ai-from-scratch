
"""Minh họa hàm chi phí và quá trình tối ưu hóa tham số."""

import numpy as np
import plotly.graph_objects as go

from function_visualization.core.figure import (
    configure_figure,
    export_figure,
)


GRAPH_ID = "cost_function"
OUTPUT_FILENAME = "cost_function.html"
TITLE = "Hàm chi phí và tối ưu hóa tham số"


def cost_function(w):
    """Hàm chi phí minh họa: J(w) = (w - 2)^2."""
    return (w - 2) ** 2


def build(output_dir):
    # ---------------------------------------------------------
    # 1. Dữ liệu hàm chi phí
    # ---------------------------------------------------------
    w_values = np.linspace(-2, 6, 400)
    cost_values = cost_function(w_values)

    # Tham số hiện tại
    current_w = 5.0
    current_cost = cost_function(current_w)

    # Tham số tối ưu
    optimal_w = 2.0
    optimal_cost = cost_function(optimal_w)

    # ---------------------------------------------------------
    # 2. Khởi tạo biểu đồ
    # ---------------------------------------------------------
    fig = go.Figure()

    # Trace 0: Đường cong hàm chi phí
    fig.add_trace(
        go.Scatter(
            x=w_values,
            y=cost_values,
            mode="lines",
            name="Hàm chi phí J(w)",
            line=dict(
                width=3,
                color="#2563eb",
            ),
            hovertemplate=(
                "Tham số w = %{x:.2f}<br>"
                "Chi phí J(w) = %{y:.2f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 1: Điểm tham số hiện tại
    # Đây là trace sẽ được cập nhật bởi slider.
    fig.add_trace(
        go.Scatter(
            x=[current_w],
            y=[current_cost],
            mode="markers",
            name="Tham số hiện tại",
            marker=dict(
                size=14,
                color="#f59e0b",
                line=dict(
                    width=2,
                    color="white",
                ),
            ),
            hovertemplate=(
                "Tham số hiện tại w = %{x:.2f}<br>"
                "Chi phí J(w) = %{y:.2f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 2: Điểm tối ưu
    fig.add_trace(
        go.Scatter(
            x=[optimal_w],
            y=[optimal_cost],
            mode="markers",
            name="Điểm tối ưu",
            marker=dict(
                size=15,
                color="#16a34a",
                symbol="star",
                line=dict(
                    width=1,
                    color="white",
                ),
            ),
            hovertemplate=(
                "Tham số tối ưu w* = %{x:.2f}<br>"
                "Chi phí tối thiểu = %{y:.2f}"
                "<extra></extra>"
            ),
        )
    )

    # Đường thẳng đánh dấu vị trí tối ưu
    fig.add_vline(
        x=optimal_w,
        line_dash="dash",
        line_color="#16a34a",
        annotation_text="Tham số tối ưu w* = 2",
        annotation_position="top",
    )

    # ---------------------------------------------------------
    # 3. Cấu hình biểu đồ
    # ---------------------------------------------------------
    fig = configure_figure(
        fig=fig,
        title="Hàm chi phí: J(w) = (w - 2)²",
        xaxis_title="Tham số mô hình (w)",
        yaxis_title="Giá trị hàm chi phí J(w)",
    )

    fig.update_xaxes(range=[-2, 6])
    fig.update_yaxes(range=[-1, 18])

    # ---------------------------------------------------------
    # 4. Caption giải thích
    # ---------------------------------------------------------
    caption = r"""
    <strong>Hàm chi phí (Cost Function)</strong> biểu diễn
    mức độ sai số của mô hình ứng với từng giá trị tham số.

    <br><br>

    Trong ví dụ này, ta sử dụng hàm chi phí:

    \[
        J(w) = (w-2)^2
    \]

    Trong đó:

    <ul>
        <li><strong>w</strong>: tham số của mô hình.</li>
        <li><strong>J(w)</strong>: giá trị hàm chi phí.</li>
    </ul>

    <br>

    <strong>Điểm tối ưu (Optimal Parameter)</strong> nằm tại:

    \[
        w^* = 2,\qquad J(w^*) = 0
    \]

    Đây là điểm mà hàm chi phí đạt giá trị nhỏ nhất.

    <br><br>

    Hãy sử dụng thanh trượt để thay đổi tham số w.
    Quan sát cách điểm hiện tại di chuyển trên đường cong
    và cách giá trị hàm chi phí thay đổi.

    <br><br>

    <strong>Lưu ý:</strong> Đây là hàm chi phí minh họa
    có dạng parabol, được sử dụng để giải thích ý tưởng
    tối ưu hóa tham số.
    """

    # ---------------------------------------------------------
    # 5. Xuất HTML
    # ---------------------------------------------------------
    return export_figure(
        fig=fig,
        output_dir=output_dir,
        filename=OUTPUT_FILENAME,
        caption=caption,
        caption_title="Tìm hiểu hàm chi phí",
        page_title="Hàm chi phí - AI From Scratch",
        graph_id=GRAPH_ID,
    )
