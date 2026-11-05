# Function Visualization

Package modular cho 7 visualization của AI From Scratch.

## Cấu trúc
- `graphs/`: một module Python cho mỗi graph.
- `core/`: cấu hình Plotly, caption, export HTML và sinh trang danh mục.
- `build/registry.py`: danh sách graph.
- `build/builder.py`: cache, build và cập nhật manifest.
- `../visualizations/`: HTML và `index.html` ở cấp project.

## Chạy
Từ thư mục gốc `ai-from-scratch`:

```powershell
python -m pip install -r requirements.txt
python -m function_visualization.build.builder
```

Lần chạy đầu sẽ nhận diện và giữ nguyên HTML đã có (`ADOPT`), không ghi đè.
Khi đã kiểm tra mã nguồn module, dùng `build_all(force=True)` để dựng lại 6 graph có mã nguồn trong notebook.

## Lưu ý về graph điểm cực tiểu
Đã nhận HTML `minimum_point_function(1).html` và giữ nguyên dưới tên chuẩn `minimum_point_function.html`.
Bộ file cung cấp không có notebook/mã Python dựng graph điểm cực tiểu, vì vậy `minimum_point.py` chỉ xác nhận và bảo toàn HTML; không tự tạo lại graph này.

Caption, tiêu đề, chú thích, điều khiển và nội dung giao diện do package tạo ra sử dụng tiếng Việt.
