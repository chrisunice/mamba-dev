import pandas as pd
from dash import dcc
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State

import mamba_ui as mui


@mui.app.callback(
    Output('mission-planning-download', 'data'),
    Input('mission-planning-download-button', 'n_clicks'),
    State('mission-planning-output-store', 'data')
)
def handle_download_button(download_click: int, mpf: pd.DataFrame):
    if download_click is None:
        raise PreventUpdate

    return dcc.send_data_frame(mpf.to_csv, 'mpf.csv')


@mui.app.callback(
    Output('mission-planning-download-modal', 'is_open'),
    Input('mission-planning-close-button', 'n_clicks')
)
def handle_close_button(close_click: int):
    if close_click is None:
        raise PreventUpdate

    return False
