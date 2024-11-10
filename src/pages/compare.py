import dash
from dash import html

dash.register_page(__name__, name="Compare")

layout = html.Div(
    [
        html.H1(
            "Compare Events",
            style={"textAlign": "center", "marginBottom": "30px", "color": "#2c3e50"},
        ),
        html.P(
            "This page will allow comparison between different events.",
            style={"textAlign": "center"},
        ),
    ],
    style={
        "marginTop": "60px",
        "padding": "2rem",
    },
)
