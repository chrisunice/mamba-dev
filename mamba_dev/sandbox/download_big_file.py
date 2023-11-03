from dash import html
from flask import send_file
from dash_extensions.enrich import Trigger, Output

import mamba_ui as mui


@mui.app.callback(
    Output('upload-button', 'children'),
    Trigger('sandbox-page', 'children'),
)
def add_anchor_component():
    """ gets the existing children in the sandbox page and adds a download component """
    return html.A(
        id='download-anchor',
        children='Download',
        href='/download',
        style=dict(
            textDecoration='none',
            color='white'
        )
    )


@mui.app.server.route('/download')
def download_mpf():
    # NOTE this will have to be in a temp folder created by build_mpf background callback
    mpf_path = r"C:\LODAT\test_assets\large_data.csv"
    return send_file(mpf_path, as_attachment=True)


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