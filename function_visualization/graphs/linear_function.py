"""Mã dựng graph được chuyển từ notebook gốc; caption và nhãn dùng tiếng Việt."""
import numpy as np
import plotly.graph_objects as go
from function_visualization.core.figure import configure_figure, export_figure

GRAPH_ID = 'linear_function'
OUTPUT_FILENAME = 'linear_function.html'
TITLE = 'Hàm số bậc nhất'

def build(output_dir):
    def linear_function(x):
        """
        Linear function: f(x) = 2x + 1
        """
        return 2 * x + 1


    # Generate input values
    x_linear = np.linspace(-10, 10, 200)

    # Calculate output values
    y_linear = linear_function(x_linear)


    print("Hàm số bậc nhất: f(x) = 2x + 1")
    print("Number of data points:", len(x_linear))

    fig_linear = go.Figure()


    # Add linear function
    fig_linear.add_trace(
        go.Scatter(

            x=x_linear,
            y=y_linear,

            mode="lines",

            name="f(x) = 2x + 1",

            line=dict(
                width=3
            ),

            hovertemplate=(
                "x = %{x:.2f}<br>"
                "f(x) = %{y:.2f}"
                "<extra></extra>"
            )

        )
    )


    # Add y-intercept
    fig_linear.add_trace(
        go.Scatter(

            x=[0],
            y=[1],

            mode="markers",

            name="Tung độ gốc (0, 1)",

            marker=dict(
                size=11,
                symbol="circle"
            ),

            hovertemplate=(
                "Tung độ gốc<br>"
                "(%{x}, %{y})"
                "<extra></extra>"
            )

        )
    )


    # Configure figure (displayed together with its caption in the next cell)
    fig_linear = configure_figure(
        fig=fig_linear,

        title="Hàm số bậc nhất: f(x) = 2x + 1",

        xaxis_title="Đầu vào (x)",

        yaxis_title="Đầu ra f(x)"
    )

    linear_caption = r"""
    <strong>Hàm số bậc nhất</strong> có dạng \(f(x)=mx+b\).
    Ở đây, \(f(x)=2x+1\) và đồ thị của nó là một <strong>đường thẳng</strong>.

    <br><br>

    <strong>Hệ số góc (slope)</strong> là \(m=2\).

    Điều này có nghĩa là mỗi khi \(x\) tăng thêm 1 đơn vị,
    giá trị \(f(x)\) tăng thêm 2 đơn vị.

    <br><br>

    <strong>Tung độ gốc (y-intercept)</strong> là \(b=1\).

    Do đó, đường thẳng cắt trục y tại điểm:

    \[
    (0,1)
    \]

    <br>

    <strong>Vì sao đồ thị là một đường thẳng?</strong>

    Vì tốc độ thay đổi luôn không đổi:

    \[
    \frac{f(x+1)-f(x)}{1}=2
    \]

    với mọi giá trị của \(x\). Tốc độ thay đổi không đổi luôn tạo ra một đường thẳng.
    """
    return export_figure(fig_linear, output_dir, OUTPUT_FILENAME, linear_caption, 'Tìm hiểu hàm số bậc nhất', 'Hàm số bậc nhất - AI From Scratch', graph_id=GRAPH_ID)
