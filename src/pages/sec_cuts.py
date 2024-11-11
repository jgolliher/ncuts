import dash
from dash import html

dash.register_page(__name__, name="SEC Cuts")

layout = html.Div(
    [
        html.H1(
            "SEC Cuts",
            style={"textAlign": "center", "marginBottom": "30px", "color": "#2c3e50"},
        ),
        html.P(
            "This page will contain SEC cuts",
            style={"textAlign": "center"},
        ),
    ],
    style={
        "marginTop": "60px",
        "padding": "2rem",
    },
)
