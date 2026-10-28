# **Chương 2: Các kỹ thuật thao tác Tensor nâng cao (Advanced Tensor Manipulations)**

Dựa trên những phép toán Tensor cơ bản đã được trình bày ở phần trước, chương này giới thiệu các kỹ thuật thao tác Tensor nâng cao hơn. Việc kiểm soát chi tiết cấu trúc Tensor, kiểu dữ liệu và vị trí lưu trữ trên thiết bị là nền tảng quan trọng để chuẩn bị dữ liệu và triển khai hiệu quả các mô hình học sâu (Deep Learning) phức tạp.

Trong chương này, bạn sẽ học cách:

- Lựa chọn và chỉnh sửa chính xác các phần tử của Tensor bằng các phương pháp **đánh chỉ mục (indexing)** và **cắt lát (slicing)**.
- Thay đổi cấu trúc Tensor mà không làm thay đổi dữ liệu bên trong bằng các phương thức **`view()`**, **`reshape()`** và **`permute()`**.
- Kết hợp nhiều Tensor hoặc chia một Tensor thành các phần bằng các hàm **`cat()`**, **`stack()`**, **`split()`** và **`chunk()`**.
- Thực hiện các phép toán giữa những Tensor có hình dạng khác nhau nhưng tương thích với nhau bằng cơ chế **tương thích kích thước (broadcasting)** của PyTorch.
- Làm việc với các kiểu dữ liệu số khác nhau, chẳng hạn như **`float`** và **`int`**, đồng thời chuyển đổi kiểu dữ liệu của Tensor khi cần.
- Chuyển Tensor giữa bộ nhớ CPU và các bộ tăng tốc GPU bằng phương thức **`.to(device)`**.

Nắm vững các kỹ thuật thao tác này là điều cần thiết để xử lý những định dạng dữ liệu đa dạng và đáp ứng các yêu cầu tính toán thường gặp trong quy trình làm việc với mô hình học sâu.

## **Các mục trong chương (Sections)**

- **2.1 Đánh chỉ mục và cắt lát Tensor (Tensor Indexing and Slicing)**
- **2.2 Thay đổi hình dạng và sắp xếp lại Tensor (Reshaping and Rearranging Tensors)**
- **2.3 Ghép nối và chia Tensor (Joining and Splitting Tensors)**
- **2.4 Tìm hiểu về Broadcasting (Understanding Broadcasting)**
- **2.5 Kiểu dữ liệu của Tensor (Tensor Data Types)**
- **2.6 Tensor trên CPU và GPU (CPU vs GPU Tensors)**
- **2.7 Thực hành: Các kỹ thuật thao tác Tensor (Practice: Tensor Manipulation Techniques)**
