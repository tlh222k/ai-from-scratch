"""Mã dựng graph được chuyển từ notebook gốc; caption và nhãn dùng tiếng Việt."""
import numpy as np
import plotly.graph_objects as go
from function_visualization.core.figure import configure_figure, export_figure

GRAPH_ID = 'quadratic_function'
OUTPUT_FILENAME = 'quadratic_function.html'
TITLE = 'Hàm số bậc hai'

def build(output_dir):
    def quadratic_function(x):
        """
        Quadratic function: g(x) = x²
        """
        return x ** 2


    # Generate input values
    x_quadratic = np.linspace(-5, 5, 300)

    # Calculate output values
    y_quadratic = quadratic_function(x_quadratic)


    # Explicit data points (computed from the function, not hard-coded)
    x_points = np.array([-2, -1, 0, 1, 2])

    y_points = quadratic_function(x_points)

    assert list(y_points) == [4, 1, 0, 1, 4]


    print("Hàm số bậc hai: g(x) = x²")

    print("\nData points:")

    for x, y in zip(x_points, y_points):

        print(f"({x}, {y})")

    fig_quadratic = go.Figure()


    # Add quadratic function
    fig_quadratic.add_trace(
        go.Scatter(

            x=x_quadratic,
            y=y_quadratic,

            mode="lines",

            name="g(x) = x²",

            line=dict(
                width=3
            ),

            hovertemplate=(
                "x = %{x:.2f}<br>"
                "g(x) = %{y:.2f}"
                "<extra></extra>"
            )

        )
    )


    # Add explicit data points
    fig_quadratic.add_trace(
        go.Scatter(

            x=x_points,
            y=y_points,

            mode="markers",

            name="Các điểm nổi bật",

            marker=dict(
                size=11,
                symbol="circle",
                line=dict(
                    width=1
                )
            ),

            hovertemplate=(
                "Điểm: (%{x}, %{y})"
                "<extra></extra>"
            )

        )
    )


    # Configure figure (displayed together with its caption in the next cell)
    fig_quadratic = configure_figure(
        fig=fig_quadratic,

        title="Hàm số bậc hai: g(x) = x²",

        xaxis_title="Đầu vào (x)",

        yaxis_title="Đầu ra g(x)"
    )

    quadratic_caption = r"""
    <strong>Hàm số bậc hai</strong> có dạng
    \(g(x)=ax^2+bx+c\) với \(a\neq 0\).
    Ở đây, \(g(x)=x^2\) và đồ thị của nó là một <strong>parabol</strong> mở lên trên.

    <br><br>

    <strong>Đỉnh (vertex)</strong> của parabol nằm tại:

    \[
    (0,0)
    \]

    Đây là điểm thấp nhất (cực tiểu) của hàm số.

    <br><br>

    Đồ thị <strong>đối xứng qua trục y</strong>,
    vì \(g(-x)=(-x)^2=x^2=g(x)\).

    Ví dụ:

    \[
    g(-2)=(-2)^2=4
    \]

    \[
    g(2)=2^2=4
    \]

    Do đó:

    \[
    g(-2)=g(2)
    \]

    Phép bình phương làm mất dấu của đầu vào, nên hai số đối nhau
    cho cùng một kết quả.

    <br><br>

    <strong>Các điểm được làm nổi bật:</strong>

    \[
    (-2,4),\;(-1,1),\;(0,0),\;(1,1),\;(2,4)
    \]

    <br>

    <strong>Hàm bậc nhất và hàm bậc hai khác nhau thế nào?</strong>

    Hàm bậc nhất như \(f(x)=2x+1\) có tốc độ thay đổi không đổi,
    nên đồ thị là đường thẳng. Hàm bậc hai có tốc độ thay đổi thay đổi
    (độ dốc của \(x^2\) là \(2x\)), nên đồ thị cong thành parabol.
    """
    return export_figure(fig_quadratic, output_dir, OUTPUT_FILENAME, quadratic_caption, 'Tìm hiểu hàm số bậc hai', 'Hàm số bậc hai - AI From Scratch', graph_id=GRAPH_ID)
