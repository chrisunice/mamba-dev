import json
import glob
import numpy as np
import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output

from mamba_dev import config


@mui.app.callback(
    Output('air-vehicle-sub-configuration', 'options'),
    Input('platform-database', 'value'),
    prevent_initial_call=True
)
def populate_av_sub_config(platform):
    """ The sub configurations available for a given platform """
    if platform is None:
        raise PreventUpdate

    # Load the database
    path_to_database = glob.glob(f"{config['test']['test_assets_folder']}\\*{platform}*.json")[0]
    with open(path_to_database, mode='r') as f:
        missions = json.load(f)

    # Grab every mission sub config
    av_sub_configs = [val['sub_config'] for _, val in missions.items()]

    # Remove duplicates
    av_sub_configs = np.unique(av_sub_configs)
    return av_sub_configs
