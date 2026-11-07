
"""Sinh trang danh mục visualization bằng tiếng Việt."""

from pathlib import Path
import html


GRAPH_CARDS = [
    (
        "linear_function.html",
        "Hàm số bậc nhất",
        "Khám phá f(x) = 2x + 1: hệ số góc, tung độ gốc và tốc độ thay đổi không đổi.",
    ),
    (
        "quadratic_function.html",
        "Hàm số bậc hai",
        "Khám phá g(x) = x²: đỉnh parabol, tính đối xứng và các điểm nổi bật.",
    ),
    (
        "limit_function.html",
        "Giới hạn và điểm bị loại bỏ",
        "Quan sát g(x) = (x² − 1)/(x − 1), điểm khuyết (1, 2) và giới hạn khi x tiến đến 1.",
    ),
    (
        "limit_approach_function.html",
        "Giới hạn khi x tiến đến 3",
        "Quan sát f(x) = 2x + 1 tiến đến 7 từ cả bên trái và bên phải.",
    ),
    (
        "secant_line_function.html",
        "Đường cát tuyến",
        "Tìm hiểu hệ số góc và tốc độ thay đổi trung bình trên đồ thị f(x) = x².",
    ),
    (
        "secant_to_tangent_function.html",
        "Từ cát tuyến đến tiếp tuyến",
        "Theo dõi điểm Q tiến dần về P và cát tuyến tiến đến tiếp tuyến.",
    ),
    (
        "minimum_point_function.html",
        "Điểm cực tiểu",
        "Quan sát điểm thấp nhất của đồ thị và tiếp tuyến ngang tại điểm cực tiểu.",
    ),
    (
        "cost_function.html",
        "Hàm chi phí và tối ưu hóa tham số",
        "Khám phá mối quan hệ giữa tham số mô hình và giá trị hàm chi phí. Tìm hiểu cách xác định tham số tối ưu.",
    ),
    (
        "quadratic_cost_function.html",
        "Hàm chi phí bậc hai",
        "Khám phá J(w) = w², điểm tối ưu w* = 0 và cách giá trị hàm chi phí thay đổi khi điều chỉnh tham số.",
    ),
    (
        "gradient_descent.html",
        "Gradient Descent và đạo hàm",
        "Quan sát đạo hàm, tiếp tuyến và hướng cập nhật tham số để tìm điểm cực tiểu của hàm số f(x) = x².",
    ),
    (
        "gradient_descent_shifted.html",
        "Gradient Descent trên hàm bậc hai",
        "Quan sát quỹ đạo tối ưu hóa của f(x) = (x − 3)² + 2 từ x = 0 đến điểm cực tiểu x = 3.",
    ),
    (
      "gradient_descent_direction.html",
      "Gradient Descent – Hướng di chuyển",
      "Quan sát cách đạo hàm dương tại x = 2 xác định hướng di chuyển sang trái về điểm cực tiểu x = 0.",
    ),  
    (
        "paraboloid_surface.html",
        "Mặt Paraboloid 3D",
        "Trực quan hóa hàm hai biến f(x, y) = x² + y² và điểm cực tiểu tại gốc tọa độ (0, 0).",
    ),
    (
        "gradient_vector_contour.html",
        "Gradient Vector trên Contour Plot",
        "Quan sát vector gradient vuông góc với đường đồng mức và hướng về phía giá trị hàm số tăng.",
    ),
    (
        "linear_regression.html",
        "Simple Linear Regression",
        "Trực quan hóa mô hình f(x; w, b) = wx + b, vai trò của weight, bias và cách đường thẳng khớp với dữ liệu.",
    ),
]


def generate_index(output_dir):
    output_dir = Path(output_dir)

    cards = []

    for filename, title, description in GRAPH_CARDS:
        exists = (output_dir / filename).is_file()

        status = (
            ""
            if exists
            else '<span class="missing">Chưa có tệp HTML</span>'
        )

        cards.append(
            f"""
            <a class="card" href="./{html.escape(filename)}">
                <h2>{html.escape(title)}</h2>
                <p>{html.escape(description)}</p>
                {status}
            </a>
            """
        )

    page = """<!doctype html>
    <html lang="vi">

    <head>
        <meta charset="utf-8">

        <meta
            name="viewport"
            content="width=device-width,initial-scale=1"
        >

        <title>
            AI From Scratch — Thư viện trực quan hóa
        </title>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                padding: 36px 18px;
                background: #f8fafc;
                color: #1e293b;
                font-family: Arial, sans-serif;
            }

            main {
                max-width: 1000px;
                margin: auto;
            }

            header {
                text-align: center;
                margin-bottom: 32px;
            }

            header h1 {
                font-size: 30px;
                margin: 0 0 10px;
            }

            header p {
                color: #64748b;
                line-height: 1.7;
            }

            .grid {
                display: grid;
                grid-template-columns:
                    repeat(auto-fit, minmax(260px, 1fr));
                gap: 16px;
            }

            .card {
                display: block;
                padding: 22px;
                background: #fff;
                border: 1px solid #e2e8f0;
                border-radius: 14px;
                color: inherit;
                text-decoration: none;
                transition: .18s;
            }

            .card:hover {
                transform: translateY(-3px);
                border-color: #2563eb;
                box-shadow: 0 8px 24px #0f172a12;
            }

            .card h2 {
                margin: 0 0 10px;
                color: #2563eb;
                font-size: 19px;
            }

            .card p {
                margin: 0;
                color: #64748b;
                line-height: 1.65;
            }

            .missing {
                display: inline-block;
                margin-top: 12px;
                color: #b45309;
                font-size: 12px;
            }

            footer {
                text-align: center;
                margin-top: 32px;
                color: #94a3b8;
                font-size: 13px;
            }
        </style>
    </head>

    <body>
        <main>
            <header>
                <h1>AI From Scratch</h1>

                <p>
                    Thư viện biểu đồ tương tác về Toán học,
                    Machine Learning và Deep Learning.
                </p>
            </header>

            <section class="grid">
                CARDS_PLACEHOLDER
            </section>

            <footer>
                Chọn một chủ đề để mở biểu đồ tương tác.
            </footer>
        </main>
    </body>

    </html>
    """

    path = output_dir / "index.html"

    path.write_text(
        page.replace(
            "CARDS_PLACEHOLDER",
            "\n".join(cards),
        ),
        encoding="utf-8",
    )

    return path
