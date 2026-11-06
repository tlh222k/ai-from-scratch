// g(x) = a·x²  (trace 0)
registerHandler("quadratic", {
    update({graph, value: v}) {
        restyleCurve(graph, t => v * t * t);

        return "g(x) = " + v.toFixed(2) +
            "x². Dấu của a quyết định chiều mở của parabol.";
    }
});
