"""Mã dựng graph được chuyển từ notebook gốc; caption và nhãn dùng tiếng Việt."""
import numpy as np
import plotly.graph_objects as go
from function_visualization.core.figure import configure_figure, export_figure

GRAPH_ID = 'secant_line'
OUTPUT_FILENAME = 'secant_line_function.html'
TITLE = 'Đường cát tuyến'

def quadratic_function(x):
    return x ** 2

def build(output_dir):
    def average_rate_of_change(func, x_start, x_end):
        """
        Tốc độ thay đổi trung bình của func trên [x_start, x_end]
        = hệ số góc của đường cát tuyến nối hai điểm.
        """
        return (func(x_end) - func(x_start)) / (x_end - x_start)


    # Hai điểm tạo nên đường cát tuyến
    x_secant = np.array([1.0, 3.0])
    y_secant = quadratic_function(x_secant)

    # Tốc độ thay đổi trung bình giữa x = 1 và x = 3
    secant_slope = average_rate_of_change(quadratic_function, 1, 3)

    # Đồ thị f(x) = x^2 trong vùng quan sát
    x_curve_secant = np.linspace(-0.5, 3.5, 300)
    y_curve_secant = quadratic_function(x_curve_secant)

    # Kiểm tra toán học
    assert list(y_secant) == [1.0, 9.0]
    assert secant_slope == 4

    # Hàm bậc hai: tốc độ thay đổi trung bình phụ thuộc vào khoảng chọn
    assert average_rate_of_change(quadratic_function, 0, 1) == 1


    print("f(x) = x²")
    print(f"Điểm 1: ({x_secant[0]:.0f}, {y_secant[0]:.0f})")
    print(f"Điểm 2: ({x_secant[1]:.0f}, {y_secant[1]:.0f})")

    print(f"\nΔx = {x_secant[1] - x_secant[0]:.0f}")
    print(f"Δy = {y_secant[1] - y_secant[0]:.0f}")
    print(f"Tốc độ thay đổi trung bình = Δy/Δx = {secant_slope:.0f}")

    SECANT_COLOR = "#ef4444"

    fig_secant = go.Figure()


    # Đồ thị f(x) = x²
    fig_secant.add_trace(
        go.Scatter(

            x=x_curve_secant,
            y=y_curve_secant,

            mode="lines",

            name="f(x) = x²",

            line=dict(
                width=3,
                color="#2563eb"
            ),

            hovertemplate=(
                "x = %{x:.2f}<br>"
                "f(x) = %{y:.2f}"
                "<extra></extra>"
            )

        )
    )


    # Đường cát tuyến nối (1, 1) và (3, 9)
    fig_secant.add_trace(
        go.Scatter(

            x=x_secant,
            y=y_secant,

            mode="lines+markers",

            name="Đường cát tuyến (tốc độ thay đổi trung bình)",

            line=dict(
                width=3,
                color=SECANT_COLOR
            ),

            marker=dict(
                size=11,
                color=SECANT_COLOR
            ),

            hovertemplate=(
                "Điểm (%{x:.0f}, %{y:.0f})"
                "<extra></extra>"
            )

        )
    )


    # Tam giác thể hiện Δx và Δy (đường nét đứt)
    fig_secant.add_shape(
        type="line",
        x0=1, x1=3, y0=1, y1=1,
        line=dict(color="#94a3b8", width=2, dash="dot")
    )

    fig_secant.add_shape(
        type="line",
        x0=3, x1=3, y0=1, y1=9,
        line=dict(color="#94a3b8", width=2, dash="dot")
    )

    fig_secant.add_annotation(
        x=2, y=1,
        text="Δx = 2",
        showarrow=False,
        yshift=-16,
        font=dict(color="#475569")
    )

    fig_secant.add_annotation(
        x=3, y=5,
        text="Δy = 8",
        showarrow=False,
        xshift=34,
        font=dict(color="#475569")
    )

    fig_secant.add_annotation(
        x=1.1, y=8.2,
        text="Hệ số góc = Δy / Δx = 8 / 2 = 4",
        showarrow=False,
        xanchor="left",
        font=dict(color=SECANT_COLOR),
        bgcolor="white",
        bordercolor="#fecaca",
        borderwidth=1
    )


    fig_secant = configure_figure(
        fig=fig_secant,

        title="Đường cát tuyến của f(x) = x²",

        xaxis_title="Đầu vào (x)",

        yaxis_title="Đầu ra f(x)"
    )

    fig_secant = (
        fig_secant
        .update_xaxes(range=[-0.5, 3.8], dtick=1)
        .update_yaxes(range=[-0.5, 11], dtick=2)
    )

    secant_caption = r"""
    Đường màu đỏ nối hai điểm \((1,1)\) và \((3,9)\) trên đồ thị của
    \(f(x)=x^2\). Đường thẳng đi qua hai điểm của một đồ thị được gọi là
    <strong>đường cát tuyến (secant line)</strong>.

    <br><br>

    <strong>Hệ số góc</strong> của nó biểu diễn
    <strong>tốc độ thay đổi trung bình</strong> giữa \(x=1\) và \(x=3\):

    \[
    \frac{f(3)-f(1)}{3-1}=\frac{9-1}{2}=4
    \]

    Nghĩa là: trung bình, trong khoảng từ \(x=1\) đến \(x=3\), mỗi khi
    \(x\) tăng 1 đơn vị thì \(f(x)\) tăng 4 đơn vị.

    <br>

    <strong>Ý tưởng chính:</strong>

    Với hàm bậc hai, tốc độ thay đổi trung bình <em>phụ thuộc vào khoảng
    được chọn</em>. Chẳng hạn, giữa \(x=0\) và \(x=1\) nó chỉ bằng 1,
    còn giữa \(x=1\) và \(x=3\) nó bằng 4. Đường cát tuyến chỉ cho biết
    mức thay đổi <em>trung bình</em>, không phải tốc độ thay đổi tại một điểm.
    """
    return export_figure(fig_secant, output_dir, OUTPUT_FILENAME, secant_caption, 'Tìm hiểu đường cát tuyến và tốc độ thay đổi trung bình', 'Đường cát tuyến - AI From Scratch', graph_id=GRAPH_ID)
