import numpy as np
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State

import lodat as lo
import mamba_ui as mui


@mui.app.callback(
    Output('polar-plot', 'figure'),
    Input('submit-button', 'n_clicks'),
    State('polar-plot', 'figure'),
    State('file-checklist', 'value'),
    State('freq-checklist', 'value'),
    State('pol-checklist', 'value'),
    State('depr-slider', 'value')
)
def render_plot(submit_click: int, figure: dict, files: list, freqs: list, pols: list, depr: list):
    if submit_click is None:
        raise PreventUpdate

    fig = go.Figure(figure)
    for file, freq, pol in zip(files, freqs, pols):
        obj = lo.DataObject(file)
        bin_data = obj.get_bin_data(freq, pol, np.mean(depr), bin_size=(1, np.abs(np.subtract(*depr))))
        fig.add_trace(
            go.Scatterpolargl(
                theta=bin_data.index,
                r=bin_data.RCS,
                name=file
            )
        )
    return fig
