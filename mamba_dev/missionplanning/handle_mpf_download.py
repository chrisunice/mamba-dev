from flask import session, send_file, request
import pandas as pd
from dash import dcc, html
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State

import mamba_ui as mui


# @mui.app.callback(
#     Input('mission-planning-output-store', 'data')
# )
# def store_mpf_path(mpf_store: dict):
#     if mpf_store is None:
#         raise PreventUpdate
#
#     session['mpf_path'] = mpf_store['mpf_path']


@mui.app.server.route('/download-mpf')
def handle_download_button():
    path_to_mpf = request.args.get('mpf_path')
    return send_file(path_to_mpf, as_attachment=True)


@mui.app.callback(
    Output('mission-planning-download-modal', 'is_open'),
    Input('mission-planning-close-button', 'n_clicks')
)
def handle_close_button(close_click: int):
    if close_click is None:
        raise PreventUpdate

    return False
