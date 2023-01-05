import os
import glob
import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State

from mamba_dev import config


@mui.app.callback(
    Output('platform-database-dropdown-checklist', 'options'),
    Output('platform-database-dropdown-menu-item', 'toggle'),
    Output('platform-database-dropdown-checklist', 'inputStyle'),
    Input('mission-planning-page', 'children'),
    State('platform-database-dropdown-checklist', 'inputStyle'),
)
def populate_platform(_, checkbox_style: dict):
    # Get platforms
    database_directory = config['test']['test_assets_folder']
    databases = glob.glob(f"{database_directory}\\*mongodb.json")
    platforms = [os.path.basename(db).rstrip('-mongodb.json').upper() for db in databases]

    # Update checkbox style
    if 'display' in checkbox_style.keys():
        checkbox_style['display'] = 'inline'

    return platforms, True, checkbox_style


@mui.app.callback(
    Output('platform-database-dropdown-menu', 'label'),
    Input('platform-database-dropdown-checklist', 'value'),
)
def display_selection(value):
    if value is None:
        raise PreventUpdate

    if not bool(value):
        return 'Select...'
    else:
        return value


@mui.app.callback(
    Output('platform-database-dropdown-checklist', 'value'),
    Input('platform-database-dropdown-checklist', 'value'),
)
def force_one(new_value: list):
    # TODO next this would probably be a good callback to handle reseting all fields on database switch
    if new_value is None:
        raise PreventUpdate

    # Grab only the last checkbox selected
    if len(new_value) > 1:
        new_value = [new_value[-1]]

    return new_value
