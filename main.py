import numpy as np
import plotly
import plotly.graph_objects as go

print("NumPy:", np.__version__)
print("Plotly:", plotly.__version__)

fig = go.Figure(
    data=go.Scatter(
        x=[1, 2, 3],
        y=[1, 4, 9],
        mode="lines+markers"
    )
)

fig.show()