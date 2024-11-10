from dash import Dash, dcc, html, page_container
import dash
import pandas as pd
import styles as styles


# Initialize the app with url routing
app = Dash(__name__, use_pages=True)

server = app.server

# Read and process data - make it available globally
df = pd.read_csv("2022-03-03 - NCAA Cuts - Sheet1.csv")
df["Year"] = pd.to_numeric(df["Year"])


def convert_to_seconds(time_str):
    try:
        return float(time_str)
    except ValueError:
        minutes, seconds = map(float, time_str.split(":"))
        return minutes * 60 + seconds


df["TimeSeconds"] = df["Time"].apply(convert_to_seconds)

df.dtypes

# Create the navbar
navbar = html.Div(
    [
        html.Div("NCAA Swimming", style={"fontSize": "1.5rem", "fontWeight": "bold"}),
        html.Div(
            [
                dcc.Link(
                    f"{page['name']}",
                    href=page["relative_path"],
                    style=styles.NAV_LINK_STYLE,
                    className="nav-link",
                )
                for page in dash.page_registry.values()
            ],
            style={"display": "flex", "gap": "10px"},
        ),
    ],
    style={
        **styles.NAVBAR_STYLE,
        "position": "fixed",
        "top": 0,
        "left": 0,
        "right": 0,
        "zIndex": 1000,
    },
)

# Define the app layout
app.layout = html.Div([navbar, page_container])

# Add some CSS to style the nav links
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>NCAA Swimming Analysis</title>
        {%favicon%}
        {%css%}
        <style>
            .nav-link:hover {
                background-color: #555;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

if __name__ == "__main__":
    app.run_server(debug=True)
