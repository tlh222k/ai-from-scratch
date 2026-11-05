"""Mã dựng graph được chuyển từ notebook gốc; caption và nhãn dùng tiếng Việt."""
import numpy as np
import plotly.graph_objects as go
from function_visualization.core.figure import configure_figure, export_figure

GRAPH_ID = 'limit_approach_function'
OUTPUT_FILENAME = 'limit_approach_function.html'
TITLE = 'Giới hạn khi x tiến đến 3'

def build(output_dir):
    def approach_function(x):
        """
        Hàm số: f(x) = 2x + 1
        """
        return 2 * np.asarray(x, dtype=float) + 1


    # Điểm mà x tiến đến và giá trị đích (giới hạn)
    APPROACH_X = 3
    TARGET_VALUE = 7

    # Đường thẳng (vùng phóng to quanh x = 3)
    x_line_3 = np.linspace(2.5, 3.5, 200)
    y_line_3 = approach_function(x_line_3)

    # Các giá trị x tiến gần 3 từ bên trái và bên phải
    x_from_left = np.array([2.9, 2.99, 2.999])
    x_from_right = np.array([3.1, 3.01, 3.001])

    y_from_left = approach_function(x_from_left)
    y_from_right = approach_function(x_from_right)

    # Kiểm tra toán học
    assert np.isclose(approach_function(APPROACH_X), TARGET_VALUE)

    # Càng gần 3 thì f(x) càng gần 7
    assert np.all(np.diff(np.abs(y_from_left - TARGET_VALUE)) < 0)
    assert np.all(np.diff(np.abs(y_from_right - TARGET_VALUE)) < 0)


    print("f(x) = 2x + 1")
    print(f"Giới hạn khi x -> {APPROACH_X}: {TARGET_VALUE}")

    print("\n" + f"{'Phía':<8} | {'x':>7} | {'f(x)':>7} | {'|f(x) - 7|':>10}")
    print("-" * 41)

    for side, xs, ys in [
        ("Trái", x_from_left, y_from_left),
        ("Phải", x_from_right, y_from_right),
    ]:

        for x_value, y_value in zip(xs, ys):

            print(
                f"{side:<8} | {x_value:>7.3f} | {y_value:>7.3f} | "
                f"{abs(y_value - TARGET_VALUE):>10.3f}"
            )

    LEFT_COLOR = "#f97316"
    RIGHT_COLOR = "#16a34a"
    TARGET_COLOR = "#dc2626"

    fig_approach = go.Figure()


    # Đường thẳng f(x) = 2x + 1
    fig_approach.add_trace(
        go.Scatter(

            x=x_line_3,
            y=y_line_3,

            mode="lines",

            name="f(x) = 2x + 1",

            line=dict(
                width=3,
                color="#2563eb"
            ),

            hovertemplate=(
                "x = %{x:.3f}<br>"
                "f(x) = %{y:.3f}"
                "<extra></extra>"
            )

        )
    )


    # Các điểm tiến gần từ bên trái
    fig_approach.add_trace(
        go.Scatter(

            x=x_from_left,
            y=y_from_left,

            mode="markers",

            name="x tiến gần 3 từ bên trái",

            marker=dict(
                size=10,
                color=LEFT_COLOR
            ),

            hovertemplate=(
                "Bên trái<br>"
                "x = %{x}<br>"
                "f(x) = %{y:.3f}"
                "<extra></extra>"
            )

        )
    )


    # Các điểm tiến gần từ bên phải
    fig_approach.add_trace(
        go.Scatter(

            x=x_from_right,
            y=y_from_right,

            mode="markers",

            name="x tiến gần 3 từ bên phải",

            marker=dict(
                size=10,
                color=RIGHT_COLOR
            ),

            hovertemplate=(
                "Bên phải<br>"
                "x = %{x}<br>"
                "f(x) = %{y:.3f}"
                "<extra></extra>"
            )

        )
    )


    # Giá trị đích (giới hạn)
    fig_approach.add_trace(
        go.Scatter(

            x=[APPROACH_X],
            y=[TARGET_VALUE],

            mode="markers",

            name="Giá trị đích: 7",

            marker=dict(
                symbol="diamond",
                size=13,
                color=TARGET_COLOR,
                line=dict(
                    width=1,
                    color="white"
                )
            ),

            hovertemplate=(
                "Giới hạn khi x → 3<br>"
                "L = 7"
                "<extra></extra>"
            )

        )
    )


    # Đường gióng: x = 3 và y = 7
    fig_approach.add_shape(
        type="line",
        x0=APPROACH_X, x1=APPROACH_X,
        y0=6, y1=TARGET_VALUE,
        line=dict(color="#94a3b8", width=2, dash="dot")
    )

    fig_approach.add_shape(
        type="line",
        x0=2.5, x1=APPROACH_X,
        y0=TARGET_VALUE, y1=TARGET_VALUE,
        line=dict(color="#94a3b8", width=2, dash="dot")
    )


    # Chú thích hướng tiến gần
    fig_approach.add_annotation(
        x=2.9, y=6.8,
        text="x → 3 từ bên trái",
        showarrow=True, arrowhead=2,
        ax=-60, ay=45,
        font=dict(color=LEFT_COLOR)
    )

    fig_approach.add_annotation(
        x=3.1, y=7.2,
        text="x → 3 từ bên phải",
        showarrow=True, arrowhead=2,
        ax=70, ay=45,
        font=dict(color=RIGHT_COLOR)
    )

    fig_approach.add_annotation(
        x=APPROACH_X, y=TARGET_VALUE,
        text="Giới hạn: f(x) → 7",
        showarrow=True, arrowhead=2,
        ax=-95, ay=-60,
        font=dict(color=TARGET_COLOR),
        bgcolor="white",
        bordercolor="#cbd5e1",
        borderwidth=1
    )


    fig_approach = configure_figure(
        fig=fig_approach,

        title="f(x) = 2x + 1 khi x tiến đến 3",

        xaxis_title="Đầu vào (x)",

        yaxis_title="Đầu ra f(x)"
    )

    fig_approach = (
        fig_approach
        .update_xaxes(range=[2.5, 3.5], dtick=0.1)
        .update_yaxes(range=[6, 8], dtick=0.5)
    )

    approach_caption = r"""
    Xét hàm số \(f(x)=2x+1\) khi \(x\) tiến gần đến 3.

    <br><br>

    Khi các giá trị đầu vào \(x\) tiến gần 3 từ <strong>bên trái</strong>
    (chẳng hạn 2,9; 2,99) và từ <strong>bên phải</strong>
    (chẳng hạn 3,1; 3,01), các giá trị đầu ra \(f(x)\) tiến gần 7:

    \[
    f(2{,}9)=6{,}8,\quad f(2{,}99)=6{,}98,\quad f(2{,}999)=6{,}998
    \]

    \[
    f(3{,}1)=7{,}2,\quad f(3{,}01)=7{,}02,\quad f(3{,}001)=7{,}002
    \]

    <br>

    <strong>Giới hạn (limit)</strong> mô tả giá trị đích này, tức là 7:

    \[
    \lim_{x\to 3^-}f(x)=7,\qquad
    \lim_{x\to 3^+}f(x)=7
    \quad\Rightarrow\quad
    \lim_{x\to 3}(2x+1)=7
    \]

    <br>

    <strong>Ý tưởng chính:</strong>

    Giới hạn tồn tại khi giá trị của \(f(x)\) tiến gần cùng một số
    từ cả hai phía. Càng chọn \(x\) gần 3, khoảng cách
    \(|f(x)-7|\) càng nhỏ.
    """
    return export_figure(fig_approach, output_dir, OUTPUT_FILENAME, approach_caption, 'Tìm hiểu giới hạn khi x tiến đến 3', 'Giới hạn khi x tiến đến 3 - AI From Scratch', graph_id=GRAPH_ID)
