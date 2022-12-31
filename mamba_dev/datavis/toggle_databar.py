from dash.dependencies import Input, Output, State

import mamba_ui as mui


@mui.app.callback(
    Output('databar', 'is_open'),
    [
        Input('filter-icon', 'n_clicks'),
        # todo this is where the submit button would go
    ],
    State('databar', 'is_open')
)
def toggle_databar(filter_click, is_open):
    if filter_click:
        return not is_open
