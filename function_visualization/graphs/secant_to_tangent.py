"""Mã dựng graph được chuyển từ notebook gốc; caption và nhãn dùng tiếng Việt."""
import numpy as np
import plotly.graph_objects as go
from function_visualization.core.figure import configure_figure, export_figure

GRAPH_ID = 'secant_to_tangent'
OUTPUT_FILENAME = 'secant_to_tangent_function.html'
TITLE = 'Từ cát tuyến đến tiếp tuyến'

def quadratic_function(x):
    return x ** 2

def build(output_dir):
    # Điểm cố định P và dãy vị trí của Q trong animation
    X_FIXED = 1.0
    Y_FIXED = float(quadratic_function(X_FIXED))

    # 41 frame: Q di chuyển liên tục từ x=2 đến x=1
    N_FRAMES = 41
    h_values = np.linspace(1.0, 0.0, N_FRAMES)
    x_moving = X_FIXED + h_values
    y_moving = np.asarray(quadratic_function(x_moving), dtype=float)
    secant_slopes = 2.0 + h_values
    tangent_slope = 2.0 * X_FIXED

    # Đường tiếp tuyến tại P: y - 1 = 2(x - 1)
    x_tangent = np.array([-0.5, 3.0])
    y_tangent = Y_FIXED + tangent_slope * (x_tangent - X_FIXED)

    assert np.isclose(secant_slopes[0], 3.0)
    assert np.isclose(secant_slopes[-1], tangent_slope)
    assert np.all(np.diff(secant_slopes) <= 0)

    print(f'P = ({X_FIXED:g}, {Y_FIXED:g})')
    print(f'Q bắt đầu tại ({x_moving[0]:.2f}, {y_moving[0]:.2f})')
    print(f'Q kết thúc tại ({x_moving[-1]:.2f}, {y_moving[-1]:.2f})')
    print('Hệ số góc cát tuyến thay đổi từ 3 đến 2.')


    def vn(number, digits=3):
        """Định dạng số theo kiểu Việt Nam."""
        return f"{number:.{digits}f}".rstrip("0").rstrip(".").replace(".", ",")

    LAST_STEP = N_FRAMES - 1

    def explanation_lines(step):
        """Giải thích thay đổi đồng bộ với vị trí Q ở mỗi frame."""
        h = float(h_values[step])
        xq = float(x_moving[step])
        yq = float(y_moving[step])
        slope = float(secant_slopes[step])

        if step == 0:
            phase = "Bắt đầu · Cát tuyến qua P và Q"
            insight = "Q đang ở xa P; cát tuyến có độ dốc lớn hơn tiếp tuyến."
        elif step < LAST_STEP * 0.35:
            phase = "Quan sát · Q đang tiến về P"
            insight = "Khoảng cách ngang h giảm; cát tuyến bắt đầu xoay về phía tiếp tuyến."
        elif step < LAST_STEP * 0.75:
            phase = "Tiến gần · Độ dốc đang hội tụ"
            insight = "Hệ số góc 2 + h ngày càng gần 2."
        elif step < LAST_STEP:
            phase = "Rất gần · Cát tuyến gần trùng tiếp tuyến"
            insight = "Q gần như chạm P; độ dốc cát tuyến gần bằng 2."
        else:
            phase = "Kết quả · Giới hạn tạo thành tiếp tuyến"
            insight = "Khi h tiến về 0, hệ số góc tiến về 2: đạo hàm tại x = 1."

        return [
            f"<b>Bước {step + 1}/{N_FRAMES} · {phase}</b>",
            f"P = (1; 1) cố định · Q = ({vn(xq)}; {vn(yq)})",
            f"h = x_Q − 1 = {vn(h)}   |   m_PQ = 2 + h = {vn(slope)}",
            insight
        ]

    def step_annotations(step):
        return [
            dict(
                xref="paper", yref="paper", x=0, y=1.12,
                xanchor="left", yanchor="bottom", align="left",
                showarrow=False, text="<br>".join(explanation_lines(step)),
                font=dict(size=13, color="#1e293b"),
                bgcolor="#f8fafc", bordercolor="#cbd5e1",
                borderwidth=1, borderpad=9
            ),
            dict(x=X_FIXED, y=Y_FIXED, text="P (1; 1)",
                 showarrow=True, arrowhead=2, ax=-45, ay=35,
                 font=dict(size=12, color="#dc2626"))
        ]


    # Tạo animation: Q di chuyển liên tục, cát tuyến xoay dần thành tiếp tuyến
    PURPLE = "#a855f7"
    POINT_COLOR = "#ef4444"
    SECANT_COLOR = "#f97316"
    TANGENT_COLOR = "#16a34a"

    x_curve_anim = np.linspace(-0.5, 3.0, 400)
    y_curve_anim = quadratic_function(x_curve_anim)

    def secant_segment(step):
        """Trả về đoạn cát tuyến PQ ở frame hiện tại."""
        xq = float(x_moving[step])
        yq = float(y_moving[step])
        return [X_FIXED, xq], [Y_FIXED, yq]

    fig_tangent = go.Figure()

    # 0: đồ thị hàm số
    fig_tangent.add_trace(go.Scatter(
        x=x_curve_anim, y=y_curve_anim, mode="lines",
        name="f(x) = x²", line=dict(width=3, color="#2563eb"),
        hovertemplate="x = %{x:.2f}<br>f(x) = %{y:.2f}<extra></extra>"
    ))

    # 1: tiếp tuyến là đường đích để so sánh
    fig_tangent.add_trace(go.Scatter(
        x=x_tangent, y=y_tangent, mode="lines",
        name="Tiếp tuyến tại x = 1",
        line=dict(width=3, color=TANGENT_COLOR, dash="dash"),
        hovertemplate="y = 2x − 1<br>Hệ số góc = 2<extra></extra>"
    ))

    # 2: cát tuyến động
    x0, y0 = secant_segment(0)
    fig_tangent.add_trace(go.Scatter(
        x=x0, y=y0, mode="lines", name="Cát tuyến PQ (đang thay đổi)",
        line=dict(width=3, color=SECANT_COLOR, dash="dot"),
        hovertemplate="Cát tuyến PQ<extra></extra>"
    ))

    # 3: điểm P cố định
    fig_tangent.add_trace(go.Scatter(
        x=[X_FIXED], y=[Y_FIXED], mode="markers",
        name="Điểm cố định P", marker=dict(size=12, color=POINT_COLOR),
        hovertemplate="P = (1, 1)<extra></extra>"
    ))

    # 4: điểm Q chuyển động
    fig_tangent.add_trace(go.Scatter(
        x=[x_moving[0]], y=[y_moving[0]], mode="markers",
        name="Điểm Q di chuyển",
        marker=dict(size=12, color=SECANT_COLOR, line=dict(width=1, color="white")),
        hovertemplate="Q = (%{x:.3f}, %{y:.3f})<extra></extra>"
    ))

    # Mỗi frame cập nhật vị trí Q, đường cát tuyến và phần giải thích
    fig_tangent.frames = [
        go.Frame(
            name=str(step),
            data=[
                go.Scatter(x=secant_segment(step)[0], y=secant_segment(step)[1]),
                go.Scatter(x=[x_moving[step]], y=[y_moving[step]])
            ],
            traces=[2, 4],
            layout=go.Layout(annotations=step_annotations(step))
        )
        for step in range(N_FRAMES)
    ]

    play_args = [None, dict(
        frame=dict(duration=110, redraw=True),
        transition=dict(duration=0),
        fromcurrent=True, mode="immediate"
    )]
    pause_args = [[None], dict(
        frame=dict(duration=0, redraw=False),
        transition=dict(duration=0), mode="immediate"
    )]

    def jump_args(step):
        return [[str(step)], dict(
            frame=dict(duration=0, redraw=True),
            transition=dict(duration=0), mode="immediate"
        )]

    fig_tangent = configure_figure(
        fig=fig_tangent,
        title="Từ đường cát tuyến đến đường tiếp tuyến tại x = 1",
        xaxis_title="Đầu vào (x)", yaxis_title="Đầu ra f(x)", height=720
    )

    fig_tangent.update_layout(
        margin=dict(l=65, r=35, t=185, b=165),
        annotations=step_annotations(0),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.24, yanchor="top"),
        updatemenus=[dict(
            type="buttons", direction="left", x=0, xanchor="left",
            y=-0.12, yanchor="top", pad=dict(t=0, r=8),
            buttons=[
                dict(label="▶ Play", method="animate", args=play_args),
                dict(label="⏸ Pause", method="animate", args=pause_args),
                dict(label="↺ Về đầu", method="animate", args=jump_args(0))
            ]
        )],
        sliders=[dict(
            active=0, x=0, xanchor="left", y=-0.34, yanchor="top", len=1,
            currentvalue=dict(prefix="Frame: ", font=dict(size=12)),
            steps=[dict(label=str(step + 1), method="animate", args=jump_args(step))
                   for step in range(N_FRAMES)]
        )]
    )

    fig_tangent.update_xaxes(range=[-0.5, 3.0], dtick=0.5)
    fig_tangent.update_yaxes(range=[-1, 10], dtick=2)


    tangent_caption = r"""
    Đường màu xanh dương là đồ thị \(f(x)=x^2\). Điểm \(P=(1,1)\) được giữ cố định, trong khi điểm \(Q\) di chuyển từ phải sang trái để tiến gần P. Đường nét đứt màu cam nối P và Q là <strong>đường cát tuyến</strong>; đường nét đứt màu xanh lá là <strong>đường tiếp tuyến</strong> tại P.

    Khi \(Q=(1+h,(1+h)^2)\), hệ số góc cát tuyến là:
    \[m_{PQ}=\frac{f(1+h)-f(1)}{h}=\frac{(1+h)^2-1}{h}=2+h.\]

    Trong lúc animation chạy, \(h\), tọa độ Q và hệ số góc được cập nhật liên tục. Bạn sẽ thấy cát tuyến xoay dần về phía tiếp tuyến và hệ số góc tiến gần 2.

    Ở giới hạn \(h\to0\):
    \[f'(1)=\lim_{h\to0}(2+h)=2.\]

    <strong>Ý nghĩa:</strong> đạo hàm tại \(x=1\) là hệ số góc của tiếp tuyến, đồng thời biểu diễn tốc độ thay đổi tức thời của hàm số tại điểm đó.

    <strong>Cách sử dụng:</strong> Bấm <strong>Play</strong> để chạy animation theo thời gian thực; <strong>Pause</strong> để dừng; kéo thanh trượt để xem từng frame hoặc bấm <strong>Về đầu</strong> để phát lại. Khung giải thích phía trên đồ thị thay đổi đồng bộ với chuyển động.
    """

    return export_figure(fig_tangent, output_dir, OUTPUT_FILENAME, tangent_caption, 'Từ đường cát tuyến đến đường tiếp tuyến', 'Cát tuyến và tiếp tuyến - AI From Scratch', graph_id=GRAPH_ID)
