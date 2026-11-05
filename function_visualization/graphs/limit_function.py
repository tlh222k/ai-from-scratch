"""Mã dựng graph được chuyển từ notebook gốc; caption và nhãn dùng tiếng Việt."""
import numpy as np
import plotly.graph_objects as go
from function_visualization.core.figure import configure_figure, export_figure

GRAPH_ID = 'limit_function'
OUTPUT_FILENAME = 'limit_function.html'
TITLE = 'Giới hạn và điểm bị loại bỏ'

def build(output_dir):
    def removable_discontinuity_function(x):
        """
        g(x) = (x^2 - 1) / (x - 1)

        Với x != 1 : g(x) = x + 1.
        Tại x = 1  : g(1) = 0/0, không xác định -> trả về NaN.
        """
        x = np.asarray(x, dtype=float)
        y = np.full_like(x, np.nan)

        defined = ~np.isclose(x, 1.0)
        y[defined] = (x[defined] ** 2 - 1) / (x[defined] - 1)

        return y


    # Dữ liệu cho đường thẳng (NaN tại x = 1 tạo ra khoảng hở)
    x_limit = np.linspace(-4, 4, 401)
    y_limit = removable_discontinuity_function(x_limit)

    # Điểm bị loại bỏ và giá trị giới hạn
    HOLE_X = 1
    LIMIT_VALUE = 2

    # Các giá trị x tiến gần 1 từ bên trái và bên phải
    x_left = np.array([0.0, 0.5, 0.9, 0.99])
    x_right = np.array([2.0, 1.5, 1.1, 1.01])

    x_approach = np.concatenate([x_left, x_right])
    y_approach = removable_discontinuity_function(x_approach)

    # Kiểm tra toán học
    assert np.isnan(removable_discontinuity_function([HOLE_X])[0])
    assert np.allclose(y_approach, x_approach + 1)
    assert HOLE_X + 1 == LIMIT_VALUE


    print("g(x) = (x^2 - 1) / (x - 1)")
    print("g(1) = không xác định (0/0)")
    print("Giới hạn khi x -> 1:", LIMIT_VALUE)

    print("\n" + f"{'x':>8} | {'g(x)':>8}")
    print("-" * 19)

    for x_value, y_value in zip(x_approach, y_approach):

        print(f"{x_value:>8.3f} | {y_value:>8.3f}")

    LINE_COLOR = "#2563eb"
    APPROACH_COLOR = "#f97316"

    fig_limit = go.Figure()


    # Đường thẳng y = x + 1 (bị khuyết tại x = 1)
    fig_limit.add_trace(
        go.Scatter(

            x=x_limit,
            y=y_limit,

            mode="lines",

            name="g(x) = (x² − 1)/(x − 1)",

            line=dict(
                width=3,
                color=LINE_COLOR
            ),

            connectgaps=False,

            hovertemplate=(
                "x = %{x:.2f}<br>"
                "g(x) = %{y:.2f}"
                "<extra></extra>"
            )

        )
    )


    # Các điểm x tiến gần 1 từ hai phía
    fig_limit.add_trace(
        go.Scatter(

            x=x_approach,
            y=y_approach,

            mode="markers",

            name="x tiến gần 1",

            marker=dict(
                size=9,
                color=APPROACH_COLOR
            ),

            hovertemplate=(
                "x = %{x}<br>"
                "g(x) = %{y:.3f}"
                "<extra></extra>"
            )

        )
    )


    # Vòng tròn rỗng tại (1, 2): điểm bị loại bỏ
    fig_limit.add_trace(
        go.Scatter(

            x=[HOLE_X],
            y=[LIMIT_VALUE],

            mode="markers",

            name="Điểm bị loại bỏ (1, 2)",

            marker=dict(
                symbol="circle",
                size=15,
                color="white",
                line=dict(
                    width=3,
                    color=LINE_COLOR
                )
            ),

            hovertemplate=(
                "Điểm bị loại bỏ<br>"
                "g(1) không xác định<br>"
                "Giới hạn = 2"
                "<extra></extra>"
            )

        )
    )


    # Đường gióng: giới hạn y = 2 khi x -> 1
    fig_limit.add_shape(
        type="line",
        x0=-4, x1=HOLE_X,
        y0=LIMIT_VALUE, y1=LIMIT_VALUE,
        line=dict(color="#94a3b8", width=2, dash="dot")
    )

    fig_limit.add_shape(
        type="line",
        x0=HOLE_X, x1=HOLE_X,
        y0=-3.5, y1=LIMIT_VALUE,
        line=dict(color="#94a3b8", width=2, dash="dot")
    )


    # Chú thích điểm bị loại bỏ
    fig_limit.add_annotation(
        x=HOLE_X,
        y=LIMIT_VALUE,
        text="Lỗ hổng tại (1, 2)<br>g(1) không xác định<br>Giới hạn = 2",
        showarrow=True,
        arrowhead=2,
        ax=-110,
        ay=-70,
        align="left",
        bgcolor="white",
        bordercolor="#cbd5e1",
        borderwidth=1
    )


    fig_limit = configure_figure(
        fig=fig_limit,

        title="g(x) = (x² − 1) / (x − 1)",

        xaxis_title="Đầu vào (x)",

        yaxis_title="Đầu ra g(x)"
    )

    fig_limit = (
        fig_limit
        .update_xaxes(range=[-4, 4], dtick=1)
        .update_yaxes(range=[-3.5, 5.5], tick0=0, dtick=1)
    )

    limit_caption = r"""
    Xét hàm số \(g(x)=\dfrac{x^2-1}{x-1}\). Hàm số này
    <strong>không xác định tại \(x=1\)</strong> vì mẫu số bằng 0
    (\(g(1)=\dfrac{0}{0}\)).

    <br><br>

    Với mọi \(x\neq 1\), ta có thể rút gọn:

    \[
    g(x)=\frac{(x-1)(x+1)}{x-1}=x+1
    \]

    Vì vậy, đồ thị của \(g(x)\) là
    <strong>đường thẳng \(y=x+1\) bị loại bỏ một điểm duy nhất</strong>
    tại \((1,2)\), được biểu thị bằng một
    <strong>vòng tròn rỗng</strong>.

    <br><br>

    <strong>Giới hạn (limit)</strong> khi \(x\) tiến đến 1 là giá trị
    \(y\) mà hàm số tiến gần đến, tức là 2:

    \[
    \lim_{x\to 1}\frac{x^2-1}{x-1}=2
    \]

    Các điểm màu cam cho thấy: khi \(x\) tiến gần 1 từ bên trái
    (0,9; 0,99) hoặc từ bên phải (1,1; 1,01), giá trị \(g(x)\)
    đều tiến gần 2.

    <br>

    <strong>Ý tưởng chính:</strong>

    Giới hạn chỉ quan tâm hàm số <em>tiến gần</em> đến giá trị nào,
    không yêu cầu hàm số phải xác định tại điểm đó.
    Ở đây \(g(1)\) không tồn tại, nhưng giới hạn vẫn bằng 2.
    """
    return export_figure(fig_limit, output_dir, OUTPUT_FILENAME, limit_caption, 'Tìm hiểu giới hạn và điểm bị loại bỏ', 'Giới hạn của hàm số - AI From Scratch', graph_id=GRAPH_ID)
