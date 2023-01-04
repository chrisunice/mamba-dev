import json
import glob
import numpy as np
import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output

from mamba_dev import config


@mui.app.callback(
    Output('air-vehicle-configuration-dropdown', 'children'),
    Input('platform-database-checklist', 'value'),
)
def populate_av_config(selected_platform: list):
    """ The configurations available for a given platform """
    # Don't do anything until a platform has been selected
    if not bool(selected_platform):
        raise PreventUpdate

    # Load the database
    path_to_database = glob.glob(f"{config['test']['test_assets_folder']}\\*{selected_platform[0]}*.json")[0]
    with open(path_to_database, mode='r') as f:
        missions = json.load(f)

    # Grab every mission config and remove duplicates
    av_configs = [val['config'] for _, val in missions.items()]
    av_configs = list(np.unique(av_configs))

    return mui.components.DropdownChecklist(
        id_name='air-vehicle-configuration',
        items=av_configs,
        menu_item_kwargs=dict(toggle=False)
    )


@mui.app.callback(
    Output('air-vehicle-configuration-dropdown', 'label'),
    Input('air-vehicle-configuration-checklist', 'value')
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
