import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
from styles import SIDEBAR_STYLE, CONTENT_STYLE
import pandas as pd

# Register the page
dash.register_page(__name__, path="/", name="Time Standards")


# Get the data from a function to avoid circular imports
def get_data():
    df = pd.read_csv("2022-03-03 - NCAA Cuts - Sheet1.csv")
    df["Year"] = pd.to_numeric(df["Year"])

    def convert_to_seconds(time_str):
        try:
            return float(time_str)
        except ValueError:
            minutes, seconds = map(float, time_str.split(":"))
            return minutes * 60 + seconds

    df["TimeSeconds"] = df["Time"].apply(convert_to_seconds)
    return df


# Create the layout
def layout():
    df = get_data()
    sidebar = html.Div(
        [
            html.H2("Filters", className="display-4", style={"fontSize": "2rem"}),
            html.Hr(),
            html.Div(
                [
                    html.Label(
                        "Event:", style={"fontWeight": "bold", "marginBottom": "5px"}
                    ),
                    dcc.Dropdown(
                        id="event-filter",
                        options=[
                            {"label": x, "value": x} for x in df["Event"].unique()
                        ],
                        value=df["Event"].iloc[0],
                        style={"marginBottom": "15px"},
                    ),
                    html.Label(
                        "Gender:", style={"fontWeight": "bold", "marginBottom": "5px"}
                    ),
                    dcc.Dropdown(
                        id="gender-filter",
                        options=[
                            {"label": x, "value": x} for x in df["Gender"].unique()
                        ],
                        value=df["Gender"].iloc[0],
                        style={"marginBottom": "15px"},
                    ),
                ],
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    content = html.Div(
        [
            html.H1(
                "Time Standards Progression",
                style={
                    "textAlign": "center",
                    "marginBottom": "30px",
                    "color": "#2c3e50",
                },
            ),
            dcc.Graph(id="time-series-graph", style={"height": "80vh"}),
        ],
        style=CONTENT_STYLE,
    )

    return html.Div([sidebar, content])


@callback(
    Output("time-series-graph", "figure"),
    [Input("event-filter", "value"), Input("gender-filter", "value")],
)
def update_graph(event, gender):
    df = get_data()
    filtered_df = df[(df["Event"] == event) & (df["Gender"] == gender)]

    fig = go.Figure()
    colors = {"A": "#2ecc71", "B": "#3498db", "I": "#e74c3c"}

    for cut_type in ["A", "B", "I"]:
        cut_data = filtered_df[filtered_df["CutType"] == cut_type]
        if not cut_data.empty:
            fig.add_trace(
                go.Scatter(
                    x=cut_data["Year"],
                    y=cut_data["TimeSeconds"],
                    name=f"{cut_type}",
                    text=cut_data["Time"],
                    mode="lines+markers",
                    line=dict(color=colors[cut_type]),
                    hovertemplate="%{text}",
                )
            )

    fig.update_layout(
        title=dict(text=f"{event} - {gender}", font=dict(size=24), x=0.5, y=0.95),
        xaxis_title="Year",
        yaxis_title="Time (seconds)",
        hovermode="x unified",
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)",
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(t=100),
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#f0f0f0")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#f0f0f0")

    return fig
