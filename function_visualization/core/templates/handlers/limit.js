// Line with a removed point at x = a  (trace 0)
registerHandler("limit", {
    update({graph, value: v}) {
        restyleCurve(graph, t => (Math.abs(t - v) < 0.025 ? null : t + v));

        return "Điểm khuyết tại x = " + v.toFixed(2) +
            "; giới hạn tương ứng bằng " +
            (2 * v).toFixed(2) + ".";
    }
});
