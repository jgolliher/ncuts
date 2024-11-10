import dash
from dash import html
import plotly.express as px

dash.register_page(__name__, name="Analysis")

layout = html.Div(
    [
        html.H1(
            "Cut Time Analysis",
            style={"textAlign": "center", "marginBottom": "30px", "color": "#2c3e50"},
        ),
        html.P(
            "This page will contain additional analysis of the cut times.",
            style={"textAlign": "center"},
        ),
    ],
    style={
        "marginTop": "60px",
        "padding": "2rem",
    },
)
