# **Chương 3: Tối ưu hóa bằng Đạo hàm (Optimization with Derivatives)**

Sau khi tìm hiểu về đạo hàm với vai trò là thước đo mức độ thay đổi tức thời, giờ đây chúng ta sẽ chuyển sang một ứng dụng quan trọng: sử dụng đạo hàm để tìm các điểm tối ưu của hàm số. Quá trình này được gọi là **tối ưu hóa (Optimization)**, đóng vai trò cốt lõi trong cách nhiều mô hình **Học máy (Machine Learning)** học từ dữ liệu.

Trong chương này, bạn sẽ tìm hiểu cách sử dụng đạo hàm để xác định giá trị cực tiểu hoặc cực đại của một hàm số, thường bằng cách tìm những điểm mà tại đó đạo hàm bằng không (`f′(x)=0`). Chúng ta sẽ xem xét khái niệm **hàm chi phí (Cost Function)** (hoặc **hàm mất mát (Loss Function)**) trong **Học máy**, vốn được sử dụng để đo lường mức độ hoạt động hiệu quả của một mô hình, đồng thời tìm hiểu lý do tại sao việc cực tiểu hóa các hàm này lại là mục tiêu cần đạt được. Bạn sẽ được giới thiệu về **Gradient Descent**, một thuật toán nền tảng được sử dụng để cực tiểu hóa các hàm chi phí theo cách lặp. Chúng ta sẽ giải thích cách đạo hàm cung cấp hướng cần thiết cho **Gradient Descent** và trực quan hóa quá trình này để giúp bạn hình thành trực giác.

## **Các phần (Sections)**

- [**3.1 Tìm các điểm cực đại và cực tiểu (Finding Maximum and Minimum Points)**](./01_finding_maximum_and_minimum_points.ipynb)
- [**3.2 Tối ưu hóa: Tại sao cần cực tiểu hóa hoặc cực đại hóa? (Optimization: Why Minimize or Maximize?)**](./02-optimization-why-minimize-or-maximize.ipynb)
- [**3.3 Hàm chi phí trong Học máy (Cost Functions in Machine Learning)**](./03-cost-functions-in-machine-learning.ipynb)
- [**3.4 Mục tiêu: Cực tiểu hóa hàm chi phí (Goal: Minimizing the Cost Function)**](./04-goal-minimizing-the-cost-function.ipynb)
- [**3.5 Giới thiệu về Gradient Descent (Introduction to Gradient Descent)**](./05-introduction-to-gradient-descent.ipynb)
- [**3.6 Cách đạo hàm định hướng Gradient Descent (How Derivatives Guide Gradient Descent)**](./06-how-derivatives-guide-gradient-descent.ipynb)
- [**3.7 Trực quan hóa Gradient Descent (Visualizing Gradient Descent)**](./07-visualizing-gradient-descent.ipynb)
