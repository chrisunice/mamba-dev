from dash.dependencies import Input, Output

import mamba_ui as mui


@mui.app.callback(
    Output('row-2', 'children'),
    Input('data-vis-tabs', 'active_tab')
)
def switch_tabs(active_tab):
    if active_tab == 'polar':
        return mui.components.plots.PolarPlot
    elif active_tab == 'linear':
        return mui.components.plots.LinearPlot
    else:
        return None
