
"""Visualize Gradient Descent on a shifted quadratic function.

Objective:
    f(x) = (x - 3)^2 + 2

Derivative:
    f'(x) = 2(x - 3)

Initial position: x = 0
Learning rate: eta = 0.2
Minimum: (3, 2)
"""

import numpy as np
import plotly.graph_objects as go

from function_visualization.core.figure import (
    configure_figure,
    export_figure,
)


GRAPH_ID = "gradient_descent_shifted"
OUTPUT_FILENAME = "gradient_descent_shifted.html"
TITLE = "Gradient Descent trên hàm bậc hai"


# ---------------------------------------------------------
# 1. Objective function and derivative
# ---------------------------------------------------------

def function(x):
    """Return f(x) = (x - 3)^2 + 2."""
    return (x - 3) ** 2 + 2


def derivative(x):
    """Return f'(x) = 2(x - 3)."""
    return 2 * (x - 3)


# ---------------------------------------------------------
# 2. Gradient Descent algorithm
# ---------------------------------------------------------

def gradient_descent(initial_x=0.0, learning_rate=0.2, n_iterations=12):
    """Calculate the optimization trajectory.

    Returns:
        A list of dictionaries containing iteration, x and f(x).
    """
    x = float(initial_x)
    history = []

    for iteration in range(n_iterations + 1):
        history.append({
            "iteration": iteration,
            "x": x,
            "y": function(x),
        })

        if iteration < n_iterations:
            gradient = derivative(x)
            x = x - learning_rate * gradient

    return history


# ---------------------------------------------------------
# 3. Build visualization
# ---------------------------------------------------------

def build(output_dir):

    # Generate function curve
    x_values = np.linspace(-0.5, 6.5, 400)
    y_values = function(x_values)

    # Calculate optimization trajectory
    learning_rate = 0.2

    history = gradient_descent(
        initial_x=0.0,
        learning_rate=learning_rate,
        n_iterations=12,
    )

    iteration_values = [item["iteration"] for item in history]
    trajectory_x = [item["x"] for item in history]
    trajectory_y = [item["y"] for item in history]

    # -----------------------------------------------------
    # 4. Create Plotly figure
    # -----------------------------------------------------

    fig = go.Figure()

    # Trace 0: Objective function
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines",
            name="Hàm số f(x)",
            line=dict(
                width=3,
                color="#2563eb",
            ),
            hovertemplate=(
                "x = %{x:.4f}<br>"
                "f(x) = %{y:.4f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 1: Gradient Descent trajectory
    fig.add_trace(
        go.Scatter(
            x=trajectory_x,
            y=trajectory_y,
            mode="lines+markers",
            name="Quỹ đạo Gradient Descent",
            line=dict(
                width=2.5,
                color="#f59e0b",
                dash="dot",
            ),
            marker=dict(
                size=10,
                color="#f59e0b",
                line=dict(
                    width=1.5,
                    color="white",
                ),
            ),
            customdata=iteration_values,
            hovertemplate=(
                "Iteration: %{customdata}<br>"
                "x = %{x:.4f}<br>"
                "f(x) = %{y:.4f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 2: Minimum point
    fig.add_trace(
        go.Scatter(
            x=[3],
            y=[2],
            mode="markers",
            name="Điểm cực tiểu",
            marker=dict(
                size=16,
                color="#16a34a",
                symbol="star",
                line=dict(
                    width=1.5,
                    color="white",
                ),
            ),
            hovertemplate=(
                "Điểm cực tiểu<br>"
                "x* = 3<br>"
                "f(x*) = 2"
                "<extra></extra>"
            ),
        )
    )

    # -----------------------------------------------------
    # 5. Configure figure
    # -----------------------------------------------------

    fig = configure_figure(
        fig=fig,
        title="Gradient Descent: f(x) = (x - 3)² + 2",
        xaxis_title="Vị trí x",
        yaxis_title="Giá trị hàm số f(x)",
    )

    fig.update_xaxes(range=[-0.5, 6.5])
    fig.update_yaxes(range=[1, 16])

    # -----------------------------------------------------
    # 6. Vietnamese educational caption
    # -----------------------------------------------------

    caption = r"""
    <strong>Trực quan hóa thuật toán Gradient Descent</strong>

    <br><br>

    Xét hàm số bậc hai:

    \[
        f(x)=(x-3)^2+2
    \]

    Hàm số đạt giá trị cực tiểu tại:

    \[
        x^*=3,\qquad f(3)=2
    \]

    Đạo hàm của hàm số là:

    \[
        f'(x)=2(x-3)
    \]

    <br>

    Giả sử chúng ta bắt đầu tại vị trí \(x_0=0\)
    và chọn learning rate (tốc độ học) \(\eta=0.2\).

    <br><br>

    <strong>Gradient Descent</strong> sử dụng đạo hàm
    để xác định hướng và độ lớn của mỗi bước cập nhật:

    \[
        x_{t+1}=x_t-\eta f'(x_t)
    \]

    <br>

    <strong>Cách đọc biểu đồ:</strong>

    <ul>
        <li>
            Đường màu xanh biểu diễn hàm số
            \(f(x)=(x-3)^2+2\).
        </li>
        <li>
            Các điểm màu cam biểu diễn vị trí của tham số
            qua từng iteration.
        </li>
        <li>
            Đường nét đứt màu cam nối các điểm,
            thể hiện quỹ đạo di chuyển của Gradient Descent.
        </li>
        <li>
            Ngôi sao màu xanh lá đánh dấu điểm cực tiểu
            tại \((3,2)\).
        </li>
    </ul>

    <br>

    Quan sát các điểm màu cam, chúng ta thấy rằng
    mỗi bước cập nhật đưa \(x\) tiến gần hơn đến \(x=3\).

    Khi tiến gần điểm cực tiểu, đạo hàm tiến dần về 0,
    khiến độ lớn của bước cập nhật ngày càng nhỏ.
    """

    # -----------------------------------------------------
    # 7. Export HTML
    # -----------------------------------------------------

    return export_figure(
        fig=fig,
        output_dir=output_dir,
        filename=OUTPUT_FILENAME,
        caption=caption,
        caption_title="Gradient Descent trên hàm bậc hai",
        page_title="Gradient Descent - Shifted Quadratic",
        graph_id=GRAPH_ID,
    )
