"""
TODO next work on getting the background callback working because if the user submits a MPF build and then leaves the
 page nothing will end up being exported
"""

import os
import json
import numpy as np
import pandas as pd
from pathos.pools import ProcessPool
from itertools import product, repeat
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State, ServersideOutput

import mamba_ui as mui
from mamba_dev import logger





@mui.app.callback(
    ServersideOutput('mission-planning-output-store', 'data'),
    Output('mission-planning-download-modal', 'is_open'),
    Input('mission-planning-input-store', 'data')
)
def build_mpf(input_store):
    if input_store is None:
        raise PreventUpdate

    logger.debug(f'Parent: ({os.getppid()}) Starting to build MPF')

    user_inputs = json.loads(input_store)

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

    # Assemble parameters that will be iterated over and the constant parameters
    iterable_params = list(product(looks, deprs, freqs, pols))
    constant_params = dict(
        avconfig=user_inputs.get('av_config'),
        avsubconfig=user_inputs.get('av_sub_config')
    )

    # Split the iterable parameters up into chunks based on number of workers
    workers = 8
    chunk_size = np.ceil(len(iterable_params) / workers).astype(int)
    chunks = [iterable_params[i:i + chunk_size] for i in range(0, len(iterable_params), chunk_size)]

    # Perform all the database queries based on the users input
    pool = ProcessPool(workers)
    try:
        results = pool.map(_dbm_query, chunks, repeat(constant_params))
    except ValueError:
        pool.restart()
        results = pool.map(_dbm_query, chunks, repeat(constant_params))
    pool.close()

    # Return dataframe and pop the download modal
    return pd.concat(results), True
