# **Chương 3: Giải tích nhiều biến: Gradient và phương hướng (Multivariable Calculus: Gradients and Direction)**

Dựa trên những hiểu biết đã có về các hàm một biến, giờ đây chúng ta chuyển sự chú ý sang các hàm phụ thuộc vào nhiều đầu vào. Đây là nội dung thiết yếu vì hầu hết các mô hình **Học máy (Machine Learning)**, từ hồi quy tuyến tính với nhiều đặc trưng đến các mạng nơ-ron phức tạp, đều liên quan đến việc tối ưu hóa các hàm có nhiều biến hoặc tham số. Để phân tích cách những hàm này thay đổi khi chúng ta điều chỉnh các đầu vào, cần mở rộng các khái niệm của giải tích.

Trong chương này, bạn sẽ tìm hiểu những kiến thức cơ bản về **giải tích nhiều biến (Multivariable Calculus)** có liên quan đến **Học máy**:

- **Đạo hàm riêng (Partial Derivatives):** Chúng ta sẽ định nghĩa đạo hàm riêng, đại lượng đo lường mức độ thay đổi của một hàm khi một biến đầu vào cụ thể thay đổi, trong khi các biến khác được giữ không đổi.
- **Vectơ gradient (Gradient Vector):** Bạn sẽ tìm hiểu về gradient, thường được ký hiệu là `∇f`. Vectơ này tập hợp tất cả các đạo hàm riêng của một hàm và chỉ hướng mà hàm số tăng nhanh nhất.
- **Đạo hàm theo hướng (Directional Derivatives) và Ma trận Hessian (Hessian Matrix):** Chúng ta cũng sẽ tìm hiểu cách đo lường sự thay đổi theo các hướng tùy ý (đạo hàm theo hướng) và giới thiệu ma trận Hessian, ma trận sắp xếp các đạo hàm riêng cấp hai và giúp xác định đặc điểm độ cong.

Những khái niệm này tạo thành nền tảng để hiểu cách di chuyển trên và tối ưu hóa các bề mặt có số chiều cao, chẳng hạn như các hàm chi phí được cực tiểu hóa trong quá trình huấn luyện mô hình. Nắm vững gradient là chìa khóa để hiểu các thuật toán tối ưu hóa được thảo luận ở những phần sau. Chúng ta sẽ kết thúc bằng một bài thực hành sử dụng NumPy để tính gradient bằng phương pháp số.

## **Các phần (Sections)**

- **3.1 Hàm nhiều biến (Functions of Multiple Variables)**
- **3.2 Đạo hàm riêng (Partial Derivatives)**
- **3.3 Vectơ gradient (The Gradient Vector)**
- **3.4 Đạo hàm theo hướng (Directional Derivatives)**
- **3.5 Ma trận Hessian (The Hessian Matrix)**
- **3.6 Các khái niệm tối ưu hóa nhiều biến (Multivariable Optimization Concepts)**
- **3.7 Thực hành: Tính gradient bằng NumPy (Hands-on Practical: Computing Gradients with NumPy)**
