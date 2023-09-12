import dash
import json
import time
import mamba_ui as mui
import numpy as np
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State

from mamba_dev.missionplanning import log_queue


def _fake_mpf_builder():
    """ This is a placeholder function to imitate the build_mpf method """
    time.sleep(1)
    return None


@mui.app.callback(
    Output('mission-planning-download-modal', 'is_open'),
    Input('mission-planning-page-submit-button', 'n_clicks'),
    State('mission-planning-download-modal', 'is_open')
)
def open_modal(submit_click, modal_open):
    if submit_click is None:
        raise PreventUpdate

    return not modal_open

# @dash.callback(
#     outputs=Output('mission-planning-download-modal', 'is_open'),
#     inputs=[
#         Input('mission-planning-page-submit-button', 'n_clicks'),
#         Input('mission-planning-store', 'data')
#     ],
#     background=True,
#     cancel=[Input('mission-planning-page', 'children')]
# )
# def build_mpf(submit_click, data):
#     if submit_click is None or data is None:
#         raise PreventUpdate
#
#     data = json.loads(data)
#     inputs = data['inputs']
#
#     # Things to iterate over
#     vectors = inputs['vectors']
#     looks = np.arange(inputs['look_min'], inputs['look_max'], inputs['look_width'])
#     deprs = np.arange(inputs['depr_min'], inputs['depr_max'], inputs['depr_width'])
#
#     # Iterate and store in queue
#     for vg in vectors:
#         for lk in looks:
#             for dp in deprs:
#                 message = f"Working on {vg}, Look: {lk}, Depr: {dp}"
#                 log_queue.put(message)
#                 print(f'Just added \n{message}')
#                 _fake_mpf_builder()
#
#     # Pop modal
#     return True
