
from dataclasses import dataclass
from importlib import import_module


@dataclass(frozen=True)
class GraphSpec:
    graph_id: str
    module: str
    output_filename: str
    title: str


_MODULES = [
    "linear_function",
    "quadratic_function",
    "limit_function",
    "limit_approach_function",
    "secant_line",
    "secant_to_tangent",
    "minimum_point",
    "cost_function",
]


GRAPH_REGISTRY = []

for name in _MODULES:
    module = import_module(
        f"function_visualization.graphs.{name}"
    )

    GRAPH_REGISTRY.append(
        GraphSpec(
            module.GRAPH_ID,
            module.__name__,
            module.OUTPUT_FILENAME,
            module.TITLE,
        )
    )
