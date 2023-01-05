from dash_extensions.enrich import Output, Input, State

import mamba_ui as mui


@mui.app.callback(
    Output('filter-icon', 'style'),
    Input('url', 'pathname'),
    State('filter-icon', 'style')
)
def show_filter_icon(pathname: str, style: dict):
    on_data_vis_page = pathname == '/data-visualization'
    if on_data_vis_page:
        style['display'] = 'inline'
    else:
        style['display'] = 'none'
    return style
