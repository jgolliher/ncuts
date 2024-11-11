import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats

# Register the page
dash.register_page(__name__, path="/", name="Time Standards")

# Responsive styles
SIDEBAR_STYLE = {
    "padding": "1rem",
    "backgroundColor": "#f8f9fa",
    "borderRadius": "8px",
    "marginBottom": "1rem",
}

CONTENT_STYLE = {
    "padding": "0.5rem",
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
            html.Div(
                [
                    html.H2(
                        "Filters",
                        style={
                            "fontSize": "1.2rem",
                            "marginBottom": "0.5rem",
                            "marginRight": "1rem",
                            "minWidth": "fit-content",  # Prevents text wrapping
                        },
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label(
                                        "Event:",
                                        style={
                                            "fontWeight": "bold",
                                            "marginBottom": "0.25rem",
                                            "display": "block",
                                        },
                                    ),
                                    dcc.Dropdown(
                                        id="event-filter",
                                        options=[
                                            {"label": x, "value": x}
                                            for x in df["Event"].unique()
                                        ],
                                        value=df["Event"].iloc[0],
                                        style={"width": "100%"},
                                    ),
                                ],
                                style={
                                    "width": "300px",  # Fixed width for event filter
                                    "marginRight": "1rem",
                                },
                            ),
                            html.Div(
                                [
                                    html.Label(
                                        "Gender:",
                                        style={
                                            "fontWeight": "bold",
                                            "marginBottom": "0.25rem",
                                            "display": "block",
                                        },
                                    ),
                                    dcc.Dropdown(
                                        id="gender-filter",
                                        options=[
                                            {"label": x, "value": x}
                                            for x in df["Gender"].unique()
                                        ],
                                        value=df["Gender"].iloc[0],
                                        style={"width": "100%"},
                                    ),
                                ],
                                style={
                                    "width": "200px",  # Fixed width for gender filter
                                },
                            ),
                        ],
                        style={
                            "display": "flex",
                            "gap": "1rem",
                            "alignItems": "flex-start",
                        },
                        className="filters-container",
                    ),
                ],
                style={"display": "flex", "alignItems": "center"},
                className="filters-header",
            ),
        ],
        style=SIDEBAR_STYLE,
        className="sidebar",
    )

    return html.Div(
        [
            filters,
            html.Div(
                [
                    dcc.Graph(
                        id="time-series-graph",
                        style={"height": "calc(85vh - 150px)"},
                        config={"responsive": True},
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

    # Find the overall min and max years across all cut types
    min_year = filtered_df["Year"].min()
    max_year = filtered_df["Year"].max()

    # Create extended year range (2 years before min and 5 years after max)
    extended_years = np.arange(min_year, max_year + 1)

    fig = go.Figure()
    colors = {"A": "#2ecc71", "B": "#3498db", "I": "#e74c3c"}

    for cut_type in ["A", "B", "I"]:
        cut_data = filtered_df[filtered_df["CutType"] == cut_type]
        if not cut_data.empty:
            # Add the actual data points
            fig.add_trace(
                go.Scatter(
                    x=cut_data["Year"],
                    y=cut_data["TimeSeconds"],
                    name=f"{cut_type} Cut",
                    text=cut_data["Time"],
                    mode="lines+markers",
                    line=dict(color=colors[cut_type]),
                    hovertemplate="%{text}<br>Year: %{x}<extra></extra>",
                )
            )

            # Calculate and add extended trendline
            x = cut_data["Year"].values
            y = cut_data["TimeSeconds"].values

            # Calculate trend line using linear regression
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

            # Calculate extended trendline
            extended_line = slope * extended_years + intercept

            # Calculate R² value
            r_squared = r_value**2

            # Create hover text for extended trendline
            hover_text = [
                (
                    f"Year: {year}<br>Projected: {time:.2f}s"
                    if year > max_year or year < min_year
                    else f"Trend<br>R²={r_squared:.3f}"
                )
                for year, time in zip(extended_years, extended_line)
            ]

            fig.add_trace(
                go.Scatter(
                    x=extended_years,
                    y=extended_line,
                    name=f"{cut_type} Trend (R²={r_squared:.3f})",
                    mode="lines",
                    line=dict(color=colors[cut_type], dash="dot", width=1),
                    hovertemplate="%{text}<extra></extra>",
                    text=hover_text,
                    showlegend=True,
                    opacity=0.7,
                )
            )

    fig.update_layout(
        title=dict(text=f"{event} - {gender}", font=dict(size=18), x=0.5, y=0.95),
        xaxis_title="Year",
        yaxis_title="Time (seconds)",
        hovermode="x unified",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255, 255, 255, 0.8)",
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(t=80, l=50, r=50, b=50),
    )

    # Update x-axis to show all years
    fig.update_xaxes(
        tickangle=45,
        showgrid=True,
        gridwidth=1,
        gridcolor="#f0f0f0",
        dtick=1,  # Show every year
        range=[min_year, max_year + 1],  # Set visible range
    )

    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#f0f0f0")

    return fig
