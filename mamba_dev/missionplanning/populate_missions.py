import json
import glob
import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

from mamba_dev import config


@mui.app.callback(
    Output('missions-dropdown', 'children'),
    Input('platform-database-checklist', 'value'),
)
def populate_missions(selected_platform):
    """ The missions available for a given platform """
    # Don't do anything until a platform has been selected
    if not bool(selected_platform):
        raise PreventUpdate

    # Load the database
    path_to_database = glob.glob(f"{config['test']['test_assets_folder']}\\*{selected_platform[0]}*.json")[0]
    with open(path_to_database, mode='r') as f:
        missions = json.load(f)

    # Get UMIs
    umis = [val['umi'] for _, val in missions.items()]
    umis.sort()
    return mui.components.DropdownChecklist(
        id_name='missions',
        items=['Select all', 'Clear all']+umis,
        menu_item_kwargs=dict(toggle=False)
    )


@mui.app.callback(
    Output('missions-dropdown', 'label'),
    Input('missions-checklist', 'value'),
)
def display_selection(selected_missions: list):
    if selected_missions is None:
        raise PreventUpdate

    _ = [selected_missions.remove(item) for item in ['Select all', 'Clear all'] if item in selected_missions]

    num_missions = len(selected_missions)
    if num_missions > 1:
        return f'{num_missions} missions selected'
    elif num_missions == 1:
        return selected_missions
    else:
        return 'Select...'


@mui.app.callback(
    Output('missions-checklist', 'value'),
    Input('missions-checklist', 'value'),
    State('missions-checklist', 'options')
)
def select_all_or_clear_all(selected_mission: list, all_missions: list):
    if selected_mission is None:
        raise PreventUpdate

    # Handle select or clear all missions
    if 'Clear all' in selected_mission:
        return []
    elif 'Select all' in selected_mission:
        all_missions.remove('Clear all')
        return all_missions
    else:
        return selected_mission
