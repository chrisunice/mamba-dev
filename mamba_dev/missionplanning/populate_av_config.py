import json
import glob
import numpy as np
import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output

from mamba_dev import config


@mui.app.callback(
    Output('air-vehicle-configuration', 'options'),
    Input('platform-database', 'value'),
    prevent_initial_call=True
)
def populate_av_config(platform):
    # Don't do anything until a platform has been selected
    if platform is None:
        raise PreventUpdate

    # Load the database
    path_to_database = glob.glob(f"{config['test']['test_assets_folder']}\\*{platform}*.json")[0]
    with open(path_to_database, mode='r') as f:
        missions = json.load(f)

    # Grab every mission config
    av_configs = [val['config'] for _, val in missions.items()]

    # Remove duplicates
    av_configs = np.unique(av_configs)
    return av_configs
