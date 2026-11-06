// Secant-to-tangent graph: trace 0 is redrawn as t² (legacy behaviour preserved).
registerHandler("tangent", {
    update({graph, value: v}) {
        restyleCurve(graph, t => t * t);

        return "Khoảng cách h = " + v.toFixed(2) +
            ". Khi h giảm, cát tuyến tiến gần tiếp tuyến.";
    }
});
