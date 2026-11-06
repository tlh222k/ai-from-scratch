// f(x) = 2x + 1 approaching x = a  (trace 0)
registerHandler("approach", {
    update({graph, value: v}) {
        restyleCurve(graph, t => 2 * t + (v - 3) * 2 + 1);

        return "x tiến đến a = " + v.toFixed(2) +
            "; giới hạn của 2x+1 bằng " +
            (2 * v + 1).toFixed(2) + ".";
    }
});
