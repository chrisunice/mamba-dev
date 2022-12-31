from dash.dependencies import Output, Input

import mamba_ui as mui


@mui.app.callback(
    Output('page-container', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/home':
        return mui.pages.home.layout
    elif pathname == '/data-visualization':
        return mui.pages.data_vis.layout
    elif pathname == '/imagery':
        return mui.pages.imagery.layout
    else:
        # todo add an alert here
        return mui.pages.home.layout
