// Core slider runtime. Concatenated (inside an IIFE) with exactly ONE
// handler file from handlers/<kind>.js, then startSlider(kind) is called.
//
// A handler registers itself with:
//   registerHandler("<kind>", {
//       replacesMainCaption: true,          // default true
//       update(ctx) { ...; return caption; }  // ctx = { graph, value }
//   });
// It receives the Plotly graph div and the slider value, updates traces /
// annotations via Plotly, and returns the dynamic caption text.

const handlers = {};

function registerHandler(kind, handler) {
    handlers[kind] = handler;
}

// Shared helper: x runs over [-5, 5] with 300 points; y is computed by yOf(t).
function restyleCurve(graph, yOf) {
    const x = [];
    const y = [];

    for (let i = 0; i < 300; i++) {
        const t = -5 + 10 * i / 299;

        x.push(t);
        y.push(yOf(t));
    }

    Plotly.restyle(graph, {"x": [x], "y": [y]}, [0]);
}

// Shared helper: move the single marker point stored in trace `traceIndex`.
function movePoint(graph, traceIndex, x, y) {
    Plotly.restyle(graph, {x: [[x]], y: [[y]]}, [traceIndex]);
}

function startSlider(kind) {
    const g = document.querySelector(".plotly-graph-div");
    const s = document.getElementById("param-slider");

    if (!g || !s || !window.Plotly) return;

    const handler = handlers[kind];

    if (!handler) return;

    function update() {
        const v = Number(s.value);

        document.getElementById("param-value").textContent = v.toFixed(2);

        const cap = handler.update({graph: g, value: v});

        // Dynamic caption under the slider
        document.getElementById("param-caption").textContent = cap;

        const captionContent = document.querySelector(".caption-content");

        if (captionContent && handler.replacesMainCaption !== false) {
            captionContent.textContent = cap;
        }
    }

    s.addEventListener("input", update);
    update();
}
