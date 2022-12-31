from dash.dependencies import Input, Output, State

import mamba_ui as mui


@mui.app.callback(
    Output("menubar", "is_open"),
    [
        Input("menu-icon", "n_clicks"),
        Input("url", "pathname")
    ],
    State("menubar", "is_open")
)
def toggle_menubar(menu_click, link_click, is_open):
    # If hamburger is clicked open or close the menubar
    if menu_click:
        return not is_open

    # If menubar is already open and link is clicked
    if is_open and link_click:
        return False
