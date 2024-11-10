# Shared styles for the application
NAVBAR_STYLE = {
    "padding": "1rem",
    "background-color": "#333",
    "display": "flex",
    "flexDirection": "row",
    "alignItems": "center",
    "gap": "20px",
    "color": "white",
}

NAV_LINK_STYLE = {
    "textDecoration": "none",
    "color": "white",
    "padding": "0.5rem 1rem",
    "borderRadius": "4px",
    "transition": "background-color 0.3s",
    "fontSize": "1rem",
}

NAV_LINK_SELECTED = {
    **NAV_LINK_STYLE,
    "backgroundColor": "#555",
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "60px",  # Adjusted to account for navbar height
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "marginLeft": "18rem",
    "marginRight": "2rem",
    "marginTop": "60px",  # Adjusted to account for navbar height
    "padding": "2rem 1rem",
}
