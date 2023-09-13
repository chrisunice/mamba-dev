import os
import json
import time
import psutil
import numpy as np
import mamba_ui as mui
from itertools import product
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State

from mamba_dev.missionplanning import log_queue


def _fake_mpf_builder():
    """ This is a placeholder function to imitate the build_mpf method """
    time.sleep(1)
    return None


# @mui.app.callback(
#     Output('mission-planning-download-modal', 'is_open'),
#     Input('mission-planning-page-submit-button', 'n_clicks'),
#     State('mission-planning-download-modal', 'is_open')
# )
# def open_modal(submit_click, modal_open):
#     if submit_click is None:
#         raise PreventUpdate
#
#     return not modal_open

@mui.app.callback(
    Output('mission-planning-download-modal', 'is_open'),
    Input('mission-planning-store', 'data')
)
def build_mpf(mpf_store):
    if mpf_store is None:
        raise PreventUpdate

    current_pid = os.getpid()
    parent_pid = psutil.Process(current_pid).ppid()
    print(f"The build_mpf callback is running in process: {current_pid} and its parent process is: {parent_pid}")

    user_inputs = json.loads(mpf_store)['inputs']

    # Get all the iterable parameters
    # look
    l0 = user_inputs.get('look_min')
    l1 = user_inputs.get('look_max')
    look_width = user_inputs.get('look_width')
    looks = np.arange(l0, l1, look_width)

    # depression
    d0 = user_inputs.get('depr_min')
    d1 = user_inputs.get('depr_max')
    depr_width = user_inputs.get('depr_width')
    deprs = np.arange(d0, d1, depr_width)

    # frequency and polarization
    freqs, pols = [], []
    for vector in user_inputs.get('vectors'):
        f, p = vector.split('|')
        freqs.append(float(f.split(' ')[0]))
        pols.append(p.rstrip('-pol').strip()*2)
    freqs = np.unique(freqs).tolist()
    pols = np.unique(pols).tolist()


    iterable_params = product(looks, deprs, freqs, pols)

    # I'm going to skip all the constant parameters because I don't actually have a query method to call

    # # Things to iterate over
    # vectors = inputs['vectors']
    # looks = np.arange(inputs['look_min'], inputs['look_max'], inputs['look_width'])
    # deprs = np.arange(inputs['depr_min'], inputs['depr_max'], inputs['depr_width'])
    #
    # # Iterate and store in queue
    # for vg in vectors:
    #     for lk in looks:
    #         for dp in deprs:
    #             message = f"Working on {vg}, Look: {lk}, Depr: {dp}"
    #             log_queue.put(message)
    #             print(f'Just added \n{message}')
    #             _fake_mpf_builder()

    # Pop modal
    return True
