import io
import pandas as pd
from dash import dcc
import tempfile
from flask import send_file, Response
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Trigger, Output, State, Input


import mamba_ui as mui


@mui.app.callback(
    Output('upload-button', 'children'),
    Trigger('sandbox-page', 'children')
)
def change_button_name():
    """ change button name to download when the sandbox page loads """
    return 'Download'


@mui.app.callback(
    Output('sandbox-page', 'children'),
    Trigger('sandbox-page', 'children'),
    State('sandbox-page', 'children')
)
def add_download_component(children):
    """ gets the existing children in the sandbox page and adds a download component """
    download_component = dcc.Download(id='sandbox-download')
    children.append(download_component)
    return children

@mui.app.callback(
    Output('sandbox-download', 'data'),
    Input('upload-button', 'n_clicks')
)
def handle_download(btn_click):
    if btn_click is None:
        raise PreventUpdate
    else:
        df = pd.read_csv(r"C:\LODAT\test_assets\large_data.csv")
        writer = df.to_csv
        result = dcc.send_data_frame(writer, filename='my_big.csv')
        return result
