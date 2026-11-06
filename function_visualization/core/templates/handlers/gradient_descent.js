// Gradient Descent on f(x) = x².
//   Trace 0: curve.  Trace 1: current point.
//   Trace 2: tangent line.  Trace 3: minimum point.
// The lecture caption below the page is kept (replacesMainCaption: false).
registerHandler("gradient_descent", {
    replacesMainCaption: false,

    update({graph, value: v}) {
        const fx = v ** 2;
        const gradient = 2 * v;
        const learningRate = 0.2;

        // Update rule: x_new = x - eta * f'(x)
        const nextX = v - learningRate * gradient;

        // Current point
        movePoint(graph, 1, v, fx);

        // Tangent: y = f(v) + f'(v)(x - v)
        const tangentX = [];
        const tangentY = [];

        for (let i = 0; i < 100; i++) {
            const t = v - 1.2 + (2.4 * i / 99);

            tangentX.push(t);
            tangentY.push(fx + gradient * (t - v));
        }

        Plotly.restyle(graph, {x: [tangentX], y: [tangentY]}, [2]);

        // Gradient Descent arrow
        Plotly.relayout(graph, {
            annotations: [{
                x: nextX,
                y: 0.55,
                ax: v,
                ay: 0.55,
                xref: "x",
                yref: "y",
                axref: "x",
                ayref: "y",
                showarrow: Math.abs(gradient) > 0.01,
                arrowhead: 3,
                arrowsize: 1.4,
                arrowwidth: 3,
                arrowcolor: "#2563eb",
                text: ""
            }]
        });

        if (Math.abs(v) < 0.01) {
            return "Bạn đang ở gần điểm cực tiểu x = 0. " +
                "Đạo hàm gần bằng 0 nên bước cập nhật rất nhỏ.";
        } else if (gradient > 0) {
            return "f'(x) = " + gradient.toFixed(2) +
                " > 0. Hàm số đang tăng. " +
                "Gradient Descent di chuyển x sang trái, " +
                "từ " + v.toFixed(2) +
                " đến " + nextX.toFixed(2) + ".";
        }

        return "f'(x) = " + gradient.toFixed(2) +
            " < 0. Hàm số đang giảm. " +
            "Gradient Descent di chuyển x sang phải, " +
            "từ " + v.toFixed(2) +
            " đến " + nextX.toFixed(2) + ".";
    }
});
