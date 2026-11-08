
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

GRAPH_ID = "linear_regression_residuals"
OUTPUT_FILENAME = "linear_regression_residuals.html"

TITLE = "Linear Regression: Residuals and MSE"


# ============================================================
# 2. DATASET
# ============================================================

def get_dataset():
    """
    Dataset minh họa:

        x: Số giờ học
        y: Điểm thực tế

    Các giá trị được ước lượng gần đúng từ hình tham chiếu.
    """

    x_data = np.array(
        [1, 2, 3, 4, 5],
        dtype=float,
    )

    y_data = np.array(
        [2, 3, 5, 4, 6],
        dtype=float,
    )

    return x_data, y_data


# ============================================================
# 3. LINEAR MODEL
# ============================================================

def predict(x, w=1.0, b=0.5):
    """
    Linear Regression model:

        y_hat = wx + b

    Default parameters:
        w = 1
        b = 0.5
    """

    return w * x + b


# ============================================================
# 4. RESIDUALS
# ============================================================

def calculate_residuals(y_true, y_pred):
    """
    Residual:

        e_i = y_i - y_hat_i
    """

    return y_true - y_pred


# ============================================================
# 5. MEAN SQUARED ERROR
# ============================================================

def calculate_mse(y_true, y_pred):
    """
    Mean Squared Error:

        MSE = (1/n) * sum((y_i - y_hat_i)^2)
    """

    residuals = calculate_residuals(y_true, y_pred)

    return float(np.mean(residuals ** 2))


# ============================================================
# 6. BUILD GRAPH
# ============================================================

def build(output_dir: Path):

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # Dataset and predictions
    # --------------------------------------------------------

    x_data, y_data = get_dataset()

    w = 1.0
    b = 0.5

    y_pred = predict(x_data, w, b)

    residuals = calculate_residuals(
        y_data,
        y_pred,
    )

    squared_errors = residuals ** 2

    mse = calculate_mse(
        y_data,
        y_pred,
    )

    # --------------------------------------------------------
    # Regression line
    # --------------------------------------------------------

    x_line = np.linspace(0, 6, 200)
    y_line = predict(x_line, w, b)

    # --------------------------------------------------------
    # Residual segments
    #
    # Each vertical segment connects:
    # predicted value -> actual value
    # --------------------------------------------------------

    residual_x = []
    residual_y = []

    for x, actual, predicted in zip(
        x_data,
        y_data,
        y_pred,
    ):

        residual_x.extend([x, x, None])
        residual_y.extend([predicted, actual, None])

    # --------------------------------------------------------
    # Figure
    # --------------------------------------------------------

    fig = go.Figure()

    # Trace 0: Actual data points
    fig.add_trace(
        go.Scatter(
            x=x_data,
            y=y_data,
            mode="markers",
            name="Giá trị thực tế",
            marker=dict(
                size=12,
                color="#2689e8",
                line=dict(
                    color="white",
                    width=1.5,
                ),
            ),
            hovertemplate=(
                "x = %{x:.1f}<br>"
                "Giá trị thực tế = %{y:.2f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 1: Regression line
    fig.add_trace(
        go.Scatter(
            x=x_line,
            y=y_line,
            mode="lines",
            name="Mô hình: y = x + 0.5",
            line=dict(
                color="#ff3939",
                width=3,
            ),
            hovertemplate=(
                "Mô hình dự đoán<br>"
                "x = %{x:.2f}<br>"
                "ŷ = %{y:.2f}"
                "<extra></extra>"
            ),
        )
    )

    # Trace 2: Residual segments
    fig.add_trace(
        go.Scatter(
            x=residual_x,
            y=residual_y,
            mode="lines",
            name="Phần dư (Residuals)",
            line=dict(
                color="#94a3b8",
                width=2,
                dash="dot",
            ),
            hoverinfo="skip",
            connectgaps=False,
        )
    )

    # --------------------------------------------------------
    # Layout
    # --------------------------------------------------------

    configure_figure(
        fig,
        title=TITLE,
        xaxis_title="Biến đầu vào (x)",
        yaxis_title="Giá trị đầu ra (y)",
        height=560,
    )

    fig.update_layout(
        template="plotly_white",
        hovermode="closest",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=12),
        ),
        margin=dict(
            l=70,
            r=40,
            t=100,
            b=75,
        ),
    )

    fig.update_xaxes(
        range=[0, 6],
        dtick=1,
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor="#64748b",
        gridcolor="#e5e7eb",
    )

    fig.update_yaxes(
        range=[0, 7],
        dtick=1,
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor="#64748b",
        gridcolor="#e5e7eb",
    )

    # --------------------------------------------------------
    # 7. VIETNAMESE CAPTION
    # --------------------------------------------------------

    caption = f"""
    <p>
        Hãy xét một tập dữ liệu gồm các điểm quan sát,
        trong đó mỗi điểm biểu diễn một cặp giá trị
        đầu vào x và đầu ra thực tế y.
    </p>

    <p>
        Đường màu đỏ biểu diễn một mô hình hồi quy tuyến tính:
        <strong>ŷ = x + 0.5</strong>.
        Mô hình sử dụng giá trị x để dự đoán đầu ra ŷ.
    </p>

    <p>
        Tuy nhiên, giá trị dự đoán không nhất thiết trùng với
        giá trị thực tế. Sự chênh lệch giữa hai giá trị này
        được gọi là <strong>phần dư (Residual)</strong>.
    </p>

    <p style="text-align:center;">
        <strong>eᵢ = yᵢ − ŷᵢ</strong>
    </p>

    <p>
        Các đoạn nét đứt màu xám thể hiện phần dư tại từng điểm.
        Nếu điểm dữ liệu nằm phía trên đường hồi quy,
        phần dư mang giá trị dương.
        Nếu điểm nằm phía dưới đường hồi quy,
        phần dư mang giá trị âm.
    </p>

    <p>
        Để đánh giá mức độ sai lệch tổng thể,
        chúng ta sử dụng <strong>Mean Squared Error (MSE)</strong>.
        MSE lấy bình phương từng phần dư rồi tính trung bình.
    </p>

    <p style="text-align:center;">
        <strong>
            MSE = (1/n) Σ (yᵢ − ŷᵢ)²
        </strong>
    </p>

    <p>
        Với mô hình đang xét, MSE bằng
        <strong>{mse:.2f}</strong>.
        Bình phương phần dư giúp các sai lệch âm và dương
        không triệt tiêu lẫn nhau, đồng thời làm cho sai số lớn
        bị phạt mạnh hơn.
    </p>

    <p>
        <strong>Mục tiêu của Linear Regression:</strong>
        Tìm các tham số w và b sao cho MSE đạt giá trị nhỏ nhất.
        Khi đó, đường hồi quy sẽ phù hợp với các điểm dữ liệu
        tốt hơn theo tiêu chí sai số bình phương trung bình.
    </p>
    """

    caption_html = build_caption_html(
        caption,
        TITLE,
        "16px",
    )

    # --------------------------------------------------------
    # 8. EXPORT HTML
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
