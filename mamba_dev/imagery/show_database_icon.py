from dash.dependencies import Output, Input, State

import mamba_ui as mui


@mui.app.callback(
    Output('database-icon', 'style'),
    Input('url', 'pathname'),
    State('database-icon', 'style')
)
def show_database_icon(pathname: str, style: dict):
    on_data_vis_page = pathname == '/imagery'
    if on_data_vis_page:
        style['display'] = 'inline'
    else:
        style['display'] = 'none'
    return style
