# from dash.exceptions import PreventUpdate
# from dash_extensions.enrich import Input, Output
# import mamba_ui as mui
#
#
# @mui.app.callback(
#     Output('mission-planning-download-modal', 'is_open'),
#     Input('mission-planning-page-submit-button', 'n_clicks'),
# )
# def open_download_window(submit_click: int):
#     if submit_click is None:
#         raise PreventUpdate
#     return True
