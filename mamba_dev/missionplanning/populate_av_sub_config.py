import json
import glob
import numpy as np
import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State

from mamba_dev import config


@mui.app.callback(
    Output('air-vehicle-sub-configuration-dropdown-checklist', 'options'),
    Output('air-vehicle-sub-configuration-dropdown-checklist', 'inputStyle'),
    Input('platform-database-dropdown-checklist', 'value'),
    State('air-vehicle-sub-configuration-dropdown-checklist', 'inputStyle'),
)
def populate_av_sub_config(selected_platform: list, checkbox_style: dict):
    """ The sub configurations available for a given platform """
    # Don't do anything until a platform has been selected
    if not bool(selected_platform):
        raise PreventUpdate

    # Load the database
    path_to_database = glob.glob(f"{config['test']['test_assets_folder']}\\*{selected_platform[0]}*.json")[0]
    with open(path_to_database, mode='r') as f:
        missions = json.load(f)

    # Grab every mission sub config and remove duplicates
    av_sub_configs = [val['sub_config'] for _, val in missions.items()]
    av_sub_configs = list(np.unique(av_sub_configs))

    # Update checkbox style
    if 'display' in checkbox_style.keys():
        checkbox_style['display'] = 'inline'

    return av_sub_configs, checkbox_style


@mui.app.callback(
    Output('air-vehicle-sub-configuration-dropdown-menu', 'label'),
    Input('air-vehicle-sub-configuration-dropdown-checklist', 'value')
)
def display_selection(selected_sub_configs: list):
    if selected_sub_configs is None:
        raise PreventUpdate

    if len(selected_sub_configs) > 2:
        return 'Multiple items selected'
    elif len(selected_sub_configs) == 0:
        return 'Select...'
    else:
        return ', '.join(selected_sub_configs)
