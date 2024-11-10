# app.py
from dash import Dash, dcc, html, page_container
import dash
import pandas as pd

# Initialize the app with url routing and meta viewport tag for mobile
app = Dash(
    __name__, 
    use_pages=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ]
)

server = app.server

# Read and process data
df = pd.read_csv("2022-03-03 - NCAA Cuts - Sheet1.csv")
df["Year"] = pd.to_numeric(df["Year"])

def convert_to_seconds(time_str):
    try:
        return float(time_str)
    except ValueError:
        minutes, seconds = map(float, time_str.split(":"))
        return minutes * 60 + seconds

df["TimeSeconds"] = df["Time"].apply(convert_to_seconds)

# Responsive styles
NAVBAR_STYLE = {
    "padding": "1rem",
    "background-color": "#333",
    "color": "white",
}

NAVBAR_MOBILE = {
    "flexDirection": "column",
    "alignItems": "center",
    "gap": "1rem",
}

NAVBAR_DESKTOP = {
    "display": "flex",
    "justifyContent": "space-between",
    "alignItems": "center",
}

# Create the responsive navbar
navbar = html.Div(
    [
        html.Div("NCAA Swimming", style={"fontSize": "1.5rem", "fontWeight": "bold"}),
        html.Div(
            [
                dcc.Link(
                    f"{page['name']}",
                    href=page["relative_path"],
                    style={
                        "color": "white",
                        "textDecoration": "none",
                        "padding": "0.5rem",
                        "borderRadius": "4px",
                    },
                    className="nav-link",
                )
                for page in dash.page_registry.values()
            ],
            style={"display": "flex", "gap": "10px", "flexWrap": "wrap", "justifyContent": "center"},
        ),
    ],
    style=NAVBAR_STYLE,
    className="navbar",
)

# Define the app layout
app.layout = html.Div([
    navbar,
    html.Div(page_container, style={"marginTop": "1rem", "padding": "1rem"})
])

# Add responsive CSS
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
            
            /* Mobile styles */
            @media (max-width: 768px) {
                .navbar {
                    flex-direction: column;
                    align-items: center;
                    text-align: center;
                }
                
                .nav-link {
                    width: 100%;
                    text-align: center;
                }
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