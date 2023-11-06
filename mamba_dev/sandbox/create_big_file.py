import time
from dash.exceptions import PreventUpdate
from dash import html, dcc
from flask import session
import dash_bootstrap_components as dbc
from dash_extensions.enrich import Output, Input

import mamba_ui as mui


@mui.app.callback(
    Output('sandbox-page', 'children'),
    Input('sandbox-page', 'children'),
)
def build_layout(children):
    new_components = [
        dcc.Store(id='output-store', storage_type='memory'),
        dbc.Button('Build', color='secondary', id='build-btn'),
        dcc.Download(id='mpf-download'),
        dbc.Button(
            children=[
                html.A('Download', href='/download')
                ],
            color='danger',
            id='download-btn')
    ]
    return children + new_components


@mui.app.callback(
    Output('download-btn', 'children'),
    Input('build-btn', 'n_clicks')
)
def simulate_build_mpf(build_click):
    if build_click is None:
        raise PreventUpdate
    time.sleep(2)
    # session['file_path'] = "C:/LODAT/test_assets/imagery_data.csv"

    # return {'mpf_path': ''}



# @mui.app.callback(
#     Output('mpf-download', 'data'),
#     Input('download-btn', 'n_clicks'),
#     State('output-store', 'data')
# )
# def simulate_download_mpf(download_click, mpf_store):
#     if download_click is None:
#         raise PreventUpdate
#
#     mpf_path = mpf_store.get('mpf_path')
#     return dcc.send_file(mpf_path)

# @mui.app.callback(
#     Output('upload-button', 'children'),
#     Trigger('sandbox-page', 'children'),
# )
# def add_anchor_component():
#     """ gets the existing children in the sandbox page and adds a download component """
#     return html.A(
#         id='download-anchor',
#         children='Download',
#         href='/download',
#         style=dict(
#             textDecoration='none',
#             color='white'
#         )
#     )





"""
NOTE Old code
import io
import os
import tempfile
import pandas as pd
from dash.exceptions import PreventUpdate

# @mui.app.callback(
#     Output('upload-button', 'children'),
#     Trigger('sandbox-page', 'children')
# )
# def change_button_name():
#     return 'Download'

# @mui.app.callback(
#     # Output('upload-button', 'n_clicks'),
#     Input('upload-button', 'n_clicks')
# )
# def handle_download(btn_click):
#     if btn_click is None:
#         raise PreventUpdate
#     else:
#         # Load the data to simulate the creation of MPF data frame
#         df = pd.read_csv(r"C:\LODAT\test_assets\large_data.csv")
#
#         # # Create a temporary file to store the CSV data
#         # with tempfile.NamedTemporaryFile(mode='w', delete=True, suffix='.csv') as temp_file:
#         #     # Write your DataFrame to the temporary file
#         #     df.to_csv(temp_file.name, index=False)
#
#         # Create a temporary CSV file with the specified root directory
#         temp_fd, temp_file_path = tempfile.mkstemp(dir=r"C:/Mamba", suffix='.csv')
#
#         try:
#             # Write your DataFrame to the temporary file
#             df.to_csv(temp_file_path, index=False)
#
#             # The temporary CSV file will be automatically deleted when it goes out of scope
#         finally:
#             # Ensure the file is closed and removed
#             os.close(temp_fd)
#
#         # Send the file to the client for download
#         return send_file(temp_file_path, as_attachment=True, download_name="your_data.csv")
"""