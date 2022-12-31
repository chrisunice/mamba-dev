from dash.dependencies import Input, Output, State

import mamba_ui as mui


@mui.app.callback(
    Output('upload-modal', 'is_open'),
    Input('menu-upload', 'n_clicks'),
    Input('upload-modal-close', 'n_clicks'),
    State('upload-modal', 'is_open'),
    prevent_initial_call=True
)
def toggle_upload_window(upload_click, close_click, is_open):
    if upload_click or close_click:
        return not is_open
    return is_open
