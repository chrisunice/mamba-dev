# import json
# import os
#
# import diskcache
# import numpy as np
# import pandas as pd
# from pathos.pools import ProcessPool
# from itertools import product, repeat
# from dash.exceptions import PreventUpdate
# from dash import DiskcacheManager, callback
# from dash_extensions.enrich import Input, Output, ServersideOutput
#
# import mamba_ui as mui
# from mamba_dev import config
# from mamba_dev import logger
# from .build_mpf import _dbm_query
#
#
# cache = diskcache.Cache(f"{config['default']['root_dir']}\\cache")
# background_callback_manager = DiskcacheManager(cache)
#
#
# @callback(
#     output=ServersideOutput("mission-planning-output-store", "data"),
#     inputs=Input("mission-planning-input-store", "data"),
#     background=True,
#     manager=background_callback_manager,
#     # allow_duplicate=True
# )
# def build_mpf_background(input_store):
#     if input_store is None:
#         raise PreventUpdate
#
#     logger.debug(f'Parent: ({os.getppid()}) Starting to build MPF')
#
#     user_inputs = json.loads(input_store)
#
#     # Get all the iterable parameters
#     # look
#     l0 = user_inputs.get('look_min')
#     l1 = user_inputs.get('look_max')
#     look_width = user_inputs.get('look_width')
#     looks = np.arange(l0, l1, look_width)
#
#     # depression
#     d0 = user_inputs.get('depr_min')
#     d1 = user_inputs.get('depr_max')
#     depr_width = user_inputs.get('depr_width')
#     deprs = np.arange(d0, d1, depr_width)
#
#     # frequency and polarization
#     freqs, pols = [], []
#     for vector in user_inputs.get('vectors'):
#         f, p = vector.split('|')
#         freqs.append(float(f.split(' ')[0]))
#         pols.append(p.rstrip('-pol').strip()*2)
#     freqs = np.unique(freqs).tolist()
#     pols = np.unique(pols).tolist()
#
#     # Assemble parameters that will be iterated over and the constant parameters
#     iterable_params = list(product(looks, deprs, freqs, pols))
#     constant_params = dict(
#         avconfig=user_inputs.get('av_config'),
#         avsubconfig=user_inputs.get('av_sub_config')
#     )
#
#     # Split the iterable parameters up into chunks based on number of workers
#     workers = 8
#     chunk_size = np.ceil(len(iterable_params) / workers).astype(int)
#     chunks = [iterable_params[i:i + chunk_size] for i in range(0, len(iterable_params), chunk_size)]
#
#     # Perform all the database queries based on the users input
#     pool = ProcessPool(workers)
#     try:
#         results = pool.map(_dbm_query, chunks, repeat(constant_params))
#     except ValueError:
#         pool.restart()
#         results = pool.map(_dbm_query, chunks, repeat(constant_params))
#     pool.close()
#
#     # Return dataframe
#     df = pd.concat(results)
#     return df.to_json(orient='split')
#
#
# @mui.app.callback(
#     Output('mission-planning-download-modal', 'is_open'),
#     Input('mission-planning-output-store', 'data')
# )
# def pop_modal(output_store: pd.DataFrame) -> bool:
#     if output_store is None:
#         raise PreventUpdate
#
#     return True
