// J(w) = (w - 2)²  — current point is trace 1.
registerHandler("cost", {
    update({graph, value: v}) {
        const cost = (v - 2) ** 2;

        movePoint(graph, 1, v, cost);

        if (Math.abs(v - 2) < 0.001) {
            return "Tham số đã đạt giá trị tối ưu w* = 2. " +
                "Hàm chi phí đạt giá trị nhỏ nhất J(w) = 0.";
        } else if (v < 2) {
            return "Tham số hiện tại w = " + v.toFixed(2) +
                ". Giá trị hàm chi phí J(w) = " +
                cost.toFixed(2) +
                ". Hãy tăng w về gần 2 để giảm chi phí.";
        }

        return "Tham số hiện tại w = " + v.toFixed(2) +
            ". Giá trị hàm chi phí J(w) = " +
            cost.toFixed(2) +
            ". Hãy giảm w về gần 2 để giảm chi phí.";
    }
});
