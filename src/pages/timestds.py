import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import pandas as pd

# Register the page
dash.register_page(__name__, path="/", name="Time Standards")

# Responsive styles
SIDEBAR_STYLE = {
    "padding": "2rem 1rem",
    "backgroundColor": "#f8f9fa",
    "borderRadius": "8px",
    "marginBottom": "1rem",
}

CONTENT_STYLE = {
    "padding": "1rem",
}

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

def layout():
    df = get_data()
    
    filters = html.Div(
        [
            html.H2("Filters", style={"fontSize": "1.5rem", "marginBottom": "1rem"}),
            html.Div(
                [
                    html.Label("Event:", style={"fontWeight": "bold", "display": "block", "marginBottom": "0.5rem"}),
                    dcc.Dropdown(
                        id="event-filter",
                        options=[{"label": x, "value": x} for x in df["Event"].unique()],
                        value=df["Event"].iloc[0],
                        style={"marginBottom": "1rem"},
                    ),
                    html.Label("Gender:", style={"fontWeight": "bold", "display": "block", "marginBottom": "0.5rem"}),
                    dcc.Dropdown(
                        id="gender-filter",
                        options=[{"label": x, "value": x} for x in df["Gender"].unique()],
                        value=df["Gender"].iloc[0],
                        style={"marginBottom": "1rem"},
                    ),
                ],
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    return html.Div(
        [
            filters,
            html.Div(
                [
                    html.H1(
                        "Time Standards Progression",
                        style={
                            "textAlign": "center",
                            "marginBottom": "1.5rem",
                            "fontSize": "calc(1.5rem + 1vw)",
                            "color": "#2c3e50",
                        },
                    ),
                    dcc.Graph(
                        id="time-series-graph",
                        style={"height": "calc(70vh - 100px)"},
                        config={'responsive': True}
                    ),
                ],
                style=CONTENT_STYLE,
            ),
        ]
    )

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
        title=dict(
            text=f"{event} - {gender}",
            font=dict(size=20),
            x=0.5,
            y=0.95
        ),
        xaxis_title="Year",
        yaxis_title="Time (seconds)",
        hovermode="x unified",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(t=100, l=50, r=50, b=50),
    )

    # Make the graph more mobile-friendly
    fig.update_layout(
        autosize=True,
        height=500,  # Fixed height for mobile
        xaxis=dict(tickangle=45),  # Angled labels for better mobile viewing
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#f0f0f0")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#f0f0f0")

    return fig