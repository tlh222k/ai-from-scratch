// Secant graph: trace 0 is redrawn as t² (legacy behaviour preserved).
registerHandler("secant", {
    update({graph, value: v}) {
        restyleCurve(graph, t => t * t);

        return "Điều chỉnh x₂ = " + v.toFixed(2) +
            " để khảo sát đường cát tuyến.";
    }
});
