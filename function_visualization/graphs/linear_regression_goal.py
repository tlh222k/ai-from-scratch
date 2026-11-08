
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

GRAPH_ID = "linear_regression_goal"
OUTPUT_FILENAME = "linear_regression_goal.html"

TITLE = "Visualizing the Goal of Linear Regression"


# ============================================================
# 2. DATASET
# ============================================================

def get_dataset():
    """
    Minh họa mối quan hệ giữa:
        x: Số giờ học
        y: Điểm thi

    Các điểm dữ liệu được ước lượng gần đúng từ hình mẫu.
    """

    x_data = np.array(
        [1, 2, 3, 4, 5, 6],
        dtype=float,
    )

    y_data = np.array(
        [45, 55, 60, 75, 70, 85],
        dtype=float,
    )

    return x_data, y_data


# ============================================================
# 3. CANDIDATE LINE FUNCTIONS
# ============================================================

def line_1(x):
    """
    Đường thẳng màu xanh lá:

        y = 9.3x + 30
    """
    return 9.3 * x + 30


def line_2(x):
    """
    Đường thẳng màu đỏ:

        y = 0x + 60
    """
    return 60 + 0 * x


# ============================================================
# 4. EVALUATION METRIC
# ============================================================

def calculate_mse(y_true, y_pred):
    """
    Mean Squared Error:

        MSE = (1/n) * sum((y_true - y_pred)^2)
    """

    return float(np.mean((y_true - y_pred) ** 2))


# ============================================================
# 5. BUILD GRAPH
# ============================================================

def build(output_dir: Path):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # Dataset
    # --------------------------------------------------------

    x_data, y_data = get_dataset()

    x_line = np.linspace(0, 7, 200)

    y_line_1 = line_1(x_line)
    y_line_2 = line_2(x_line)

    # Predictions at observed data points
    prediction_1 = line_1(x_data)
    prediction_2 = line_2(x_data)

    # Evaluate candidate lines
    mse_1 = calculate_mse(y_data, prediction_1)
    mse_2 = calculate_mse(y_data, prediction_2)

    # --------------------------------------------------------
    # Figure
    # --------------------------------------------------------

    fig = go.Figure()

    # Trace 0: Observed data points
    fig.add_trace(
        go.Scatter(
            x=x_data,
            y=y_data,
            mode="markers",
            name="Các điểm dữ liệu",
            marker=dict(
                size=12,
                color="#2689e8",
                line=dict(
                    color="white",
                    width=1.5,
                ),
            ),
            hovertemplate=(
                "Số giờ học: %{x:.1f} giờ<br>"
                "Điểm thi: %{y:.1f}<br>"
                "<extra></extra>"
            ),
        )
    )

    # Trace 1: Better candidate line
    fig.add_trace(
        go.Scatter(
            x=x_line,
            y=y_line_1,
            mode="lines",
            name="Đường 1: y = 9.3x + 30",
            line=dict(
                color="#10b981",
                width=3,
                dash="dash",
            ),
            hovertemplate=(
                "Đường 1<br>"
                "y = 9.3x + 30<br>"
                "x = %{x:.2f}<br>"
                "y = %{y:.2f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 2: Poor candidate line
    fig.add_trace(
        go.Scatter(
            x=x_line,
            y=y_line_2,
            mode="lines",
            name="Đường 2: y = 0x + 60",
            line=dict(
                color="#ff4d4f",
                width=3,
                dash="dot",
            ),
            hovertemplate=(
                "Đường 2<br>"
                "y = 0x + 60<br>"
                "x = %{x:.2f}<br>"
                "y = %{y:.2f}"
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
        xaxis_title="Số giờ học (x)",
        yaxis_title="Điểm thi (y)",
        height=540,
    )

    fig.update_layout(
        template="plotly_white",
        hovermode="closest",
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(size=12),
        ),
        margin=dict(
            l=70,
            r=230,
            t=80,
            b=75,
        ),
    )

    fig.update_xaxes(
        range=[0, 7],
        dtick=1,
        zeroline=True,
        zerolinewidth=1.5,
        zerolinecolor="#64748b",
        gridcolor="#e5e7eb",
    )

    fig.update_yaxes(
        range=[0, 100],
        dtick=20,
        zeroline=True,
        zerolinewidth=1.5,
        zerolinecolor="#64748b",
        gridcolor="#e5e7eb",
    )

    # --------------------------------------------------------
    # 6. VIETNAMESE CAPTION
    # --------------------------------------------------------

    caption = f"""
    <p>
        Hãy xét một tập dữ liệu nhỏ mô tả mối quan hệ giữa
        <strong>số giờ học (x)</strong> và
        <strong>điểm thi (y)</strong>.
        Mỗi điểm màu xanh dương biểu diễn một quan sát trong tập dữ liệu.
    </p>

    <p>
        <strong>Đường màu xanh lá:</strong>
        Được biểu diễn bởi phương trình
        <strong>y = 9.3x + 30</strong>.
        Đường thẳng này nắm bắt xu hướng chung của các điểm dữ liệu
        tương đối tốt.
    </p>

    <p>
        <strong>Đường màu đỏ:</strong>
        Được biểu diễn bởi phương trình
        <strong>y = 0x + 60</strong>.
        Đây là một đường thẳng nằm ngang, không thể hiện được
        xu hướng điểm thi tăng theo số giờ học.
    </p>

    <p>
        Để đánh giá mức độ phù hợp của mỗi đường thẳng,
        chúng ta có thể sử dụng sai số bình phương trung bình
        (Mean Squared Error – MSE).
        MSE đo lường trung bình bình phương khoảng cách giữa
        giá trị dự đoán và giá trị thực tế.
    </p>

    <p>
        <strong>MSE của đường màu xanh lá:</strong>
        {mse_1:.2f}
    </p>

    <p>
        <strong>MSE của đường màu đỏ:</strong>
        {mse_2:.2f}
    </p>

    <p>
        MSE càng nhỏ thì đường thẳng càng phù hợp với tập dữ liệu
        theo tiêu chí này. Trong ví dụ minh họa,
        đường màu xanh lá có sai số nhỏ hơn đáng kể so với đường màu đỏ.
    </p>

    <p>
        <strong>Mục tiêu của Linear Regression:</strong>
        Tìm các tham số của đường thẳng, bao gồm hệ số góc
        (slope) và tung độ gốc (intercept), sao cho đường thẳng
        tạo ra sai số dự đoán nhỏ nhất trên tập dữ liệu.
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
    )

    page_html = render_page(
        title=TITLE,
        plot_html=plot_html,
        caption_html=caption_html,
        panel_html="",
    )

    output_path = output_dir / OUTPUT_FILENAME

    output_path.write_text(
        page_html,
        encoding="utf-8",
    )

    return output_path
