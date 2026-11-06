# **Chương 4: Xử lý nhiều đầu vào: Đạo hàm riêng (Handling Multiple Inputs: Partial Derivatives)**

Hầu hết các mô hình **Học máy (Machine Learning)** đều hoạt động trên dữ liệu có nhiều đặc trưng hoặc liên quan đến việc điều chỉnh nhiều tham số. Khác với các hàm một biến `f(x)` mà chúng ta đã tìm hiểu cho đến nay, các mô hình thực tế thường có dạng `f(x1,x2,…,xn)`. Khi một hàm số phụ thuộc vào nhiều đầu vào, chúng ta cần một phương pháp để hiểu hàm số thay đổi như thế nào khi chỉ _một_ trong số các đầu vào đó biến thiên.

Chương này giới thiệu kỹ thuật giúp thực hiện điều đó: **đạo hàm riêng (Partial Derivatives)**. Bạn sẽ tìm hiểu:

- Cách hình dung và làm việc với các hàm số nhiều biến.
- Định nghĩa và cách tính đạo hàm riêng, sử dụng các ký hiệu như \(\dfrac{\partial f}{\partial x}\).
- Cách kết hợp các đạo hàm riêng thành **vectơ gradient (Gradient Vector)** (`∇f`).
- Ý nghĩa hình học của gradient và vai trò của nó trong việc xác định hướng thay đổi nhanh nhất của một hàm số.

Những khái niệm này mở rộng hiểu biết của chúng ta về đạo hàm sang các tình huống nhiều chiều thường gặp trong quá trình tối ưu hóa **Học máy**.

## **Các phần (Sections)**

- **4.1 Hàm số nhiều biến (Functions of Multiple Variables)**
- **4.2 Đạo hàm riêng: Khái niệm (Partial Derivatives: The Concept)**
- **4.3 Tính đạo hàm riêng (Calculating Partial Derivatives)**
- **4.4 Ký hiệu đạo hàm riêng (Partial Derivative Notation)**
- **4.5 Vectơ gradient (The Gradient Vector)**
- **4.6 Ý nghĩa hình học của gradient (Geometric Meaning of the Gradient)**
- **4.7 Thực hành: Tính đạo hàm riêng và gradient (Practice: Calculating Partial Derivatives and Gradients)**
