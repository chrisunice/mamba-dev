import json
import glob
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

    # Step through every mission
    av_configs = []
    for _, value in missions.items():
        av_config = value['config']

        # Check for duplicates
        if av_config not in av_configs:
            av_configs.append(av_config)

    av_configs.sort()
    return av_configs
