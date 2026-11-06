"""Slider configuration per graph.

This is the single place that defines slider labels, ranges, defaults and the
JavaScript behaviour (``kind``) used by each graph.  New graphs can either be
added to ``SLIDER_CONFIGS`` or call :func:`register_slider_config` from their
own module, so no shared code needs to change.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union

Number = Union[int, float]


@dataclass(frozen=True)
class SliderConfig:
    label: str          # Text shown next to the slider value.
    minimum: Number
    maximum: Number
    default: Number
    kind: str           # Name of templates/handlers/<kind>.js
    step: Number = 0.05


SLIDER_CONFIGS: dict[str, SliderConfig] = {
    "linear_function": SliderConfig("Hệ số góc m", -5, 5, 2, "linear"),
    "quadratic_function": SliderConfig("Hệ số a", -3, 3, 1, "quadratic"),
    "limit_function": SliderConfig("Vị trí điểm khuyết a", -2, 3, 1, "limit"),
    "limit_approach_function": SliderConfig("Điểm tiến đến a", 0, 5, 3, "approach"),
    "secant_line": SliderConfig("Điểm thứ hai x₂", 1.1, 3.5, 3, "secant"),
    "secant_to_tangent": SliderConfig("Khoảng cách h", 0.05, 2, 1, "tangent"),
    # J(w) = (w - 2)²
    "cost_function": SliderConfig("Tham số mô hình w", -2, 6, 5, "cost"),
    # J(w) = w²
    "quadratic_cost_function": SliderConfig(
        "Tham số mô hình w", -4, 4, 3, "quadratic_cost"
    ),
    # Gradient Descent trên f(x) = x²
    "gradient_descent": SliderConfig(
        "Vị trí hiện tại x", -4, 4, 2, "gradient_descent"
    ),
}


def get_slider_config(graph_id: Optional[str]) -> Optional[SliderConfig]:
    """Return the slider config for ``graph_id`` or ``None`` if it has no slider."""
    if graph_id is None:
        return None
    return SLIDER_CONFIGS.get(graph_id)


def register_slider_config(graph_id: str, config: SliderConfig) -> None:
    """Register (or replace) the slider of a graph from outside this module."""
    SLIDER_CONFIGS[graph_id] = config
