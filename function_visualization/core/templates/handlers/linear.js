// f(x) = m·x + 1  (trace 0)
registerHandler("linear", {
    update({graph, value: v}) {
        restyleCurve(graph, t => v * t + 1);

        return "f(x) = " + v.toFixed(2) +
            "x + 1. Hệ số góc m quyết định độ dốc của đường thẳng.";
    }
});
