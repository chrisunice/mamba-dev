"""
TODO next work on getting the background callback working because if the user submits a MPF build and then leaves the
 page nothing will end up being exported
"""

import json
import numpy as np
import pandas as pd
from pathos.pools import ProcessPool
from itertools import product, repeat
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State, ServersideOutput

import mamba_ui as mui
from mamba_dev import logger


def _dbm_query(param_chunks: list) -> pd.DataFrame:
    """ This is a fake function to simulate what the RCS database query would be like with various parameters """

    logger.debug(f"Querying for RCS data with a chunk of {len(param_chunks)} parameters")

    df = pd.DataFrame()
    # Step thru every param set in the param_chunk and perform the query
    for params in param_chunks:
        look, depr, freq, pol = params

        # Generate some fake RCS data
        hits = np.random.randint(10, 100)
        tmp = pd.DataFrame(
            data={'RCS': np.random.random((hits, ))},
        )

        # Add iterable params
        tmp['Look'] = look
        tmp['Depression'] = depr
        tmp['Frequency'] = freq
        tmp['Polarization'] = pol

        # Add constant params
        # for param_name, param_value in const.items():
        #     tmp[param_name] = param_value

        # Append to final data frame
        df = pd.concat((df, tmp))

    logger.debug(f"Finished all queries")

    return df


@mui.app.callback(
    ServersideOutput('mission-planning-output-store', 'data'),
    Output('mission-planning-download-modal', 'is_open'),
    Input('mission-planning-input-store', 'data')
)
def build_mpf(input_store):
    if input_store is None:
        raise PreventUpdate

    logger.debug('Starting to build MPF')

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
        results = pool.map(_dbm_query, chunks)
    except ValueError:
        pool.restart()
        results = pool.map(_dbm_query, chunks)
    pool.close()

    # Return dataframe and pop the download modal
    return pd.concat(results), True
