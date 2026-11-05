"""Bảo toàn HTML điểm cực tiểu được người dùng cung cấp.

Notebook chứa mã dựng Plotly cho graph này không nằm trong bộ nguồn đã nhận.
Module chỉ xác nhận và giữ nguyên HTML hiện có; không giả lập hoặc ghi đè.
"""
from pathlib import Path
GRAPH_ID = "minimum_point"
OUTPUT_FILENAME = "minimum_point_function.html"
TITLE = "Điểm cực tiểu"

def build(output_dir):
    path = Path(output_dir) / OUTPUT_FILENAME
    if not path.is_file():
        raise FileNotFoundError("Thiếu minimum_point_function.html đã được cung cấp.")
    return path
