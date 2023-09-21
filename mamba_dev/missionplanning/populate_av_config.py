import json
import glob
import numpy as np
import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State

from mamba_dev import config


@mui.app.callback(
    Output('air-vehicle-configuration-dropdown-checklist', 'options'),
    Output('air-vehicle-configuration-dropdown-checklist', 'inputStyle'),
    Input('platform-database-dropdown-checklist', 'value'),
    State('air-vehicle-configuration-dropdown-checklist', 'inputStyle'),
)
def populate_av_config(selected_platform: list, checkbox_style: dict):
    """ The configurations available for a given platform """
    # Don't do anything until a platform has been selected
    if not bool(selected_platform):
        raise PreventUpdate

    # Load the database
    path_to_database = glob.glob(f"{config['test']['assets_folder']}\\*{selected_platform[0]}*.json")[0]
    with open(path_to_database, mode='r') as f:
        missions = json.load(f)

    # Grab every mission config and remove duplicates
    av_configs = [val['config'] for _, val in missions.items()]
    av_configs = list(np.unique(av_configs))

    # Update checkbox style
    if 'display' in checkbox_style.keys():
        checkbox_style['display'] = 'inline'

    return av_configs, checkbox_style


@mui.app.callback(
    Output('air-vehicle-configuration-dropdown-menu', 'label'),
    Input('air-vehicle-configuration-dropdown-checklist', 'value')
)
def display_selection(selected_configs: list):
    if selected_configs is None:
        raise PreventUpdate

    if len(selected_configs) > 2:
        return 'Multiple items selected'
    elif len(selected_configs) == 0:
        return 'Select...'
    else:
        return ', '.join(selected_configs)
