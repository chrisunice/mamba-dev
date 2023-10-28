import json
import os

import diskcache
import numpy as np
import pandas as pd
from pathos.pools import ProcessPool
from itertools import product, repeat
from dash.exceptions import PreventUpdate
from dash import DiskcacheManager, callback
from dash_extensions.enrich import Input, Output, ServersideOutput

from mamba_dev import config
from mamba_dev import logger


cache = diskcache.Cache(f"{config['default']['root_dir']}\\cache")
background_callback_manager = DiskcacheManager(cache)


@callback(
    output=ServersideOutput("mission-planning-output-store", "data"),
    inputs=Input("mission-planning-input-store", "data"),
    background=True,
    manager=background_callback_manager,
    running=[
        (Output('mission-planning-download-button', 'disabled'), True, False)
    ],
    cancel=[Input('mission-planning-close-button', 'n_clicks')]
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
    num_workers = max(1, int(config['missionplanning']['cpu_allocation']*os.cpu_count()))
    chunk_size = np.ceil(len(iterable_params) / num_workers).astype(int)
    chunks = [iterable_params[i:i + chunk_size] for i in range(0, len(iterable_params), chunk_size)]

    # Perform all the database queries based on the users input
    if num_workers > 1:
        # Parallel processing
        pool = ProcessPool(num_workers)
        try:
            results = pool.map(_dbm_query, chunks, repeat(constant_params))
        except ValueError:
            pool.restart()
            results = pool.map(_dbm_query, chunks, repeat(constant_params))
        pool.close()
    else:
        results = list(map(_dbm_query, chunks, repeat(constant_params)))

    # Return dataframe
    df = pd.concat(results)
    return df.to_json(orient='split')


def _dbm_query(param_chunks: list, const: dict) -> pd.DataFrame:
    """ This is a fake function to simulate what the RCS database query would be like with various parameters """

    logger.debug(f"Parent: ({os.getppid()}) - Querying for RCS data with a chunk of {len(param_chunks)}")

    df = pd.DataFrame()
    # Step through every param set in the param_chunk and perform the query
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
        for param_name, param_value in const.items():
            tmp[param_name] = param_value[0]

        # Append to final data frame
        df = pd.concat((df, tmp))

    logger.debug(f"Parent: ({os.getppid()}) - Finished all queries")

    return df
