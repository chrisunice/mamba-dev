import json
import glob
import itertools
import numpy as np
import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State, CycleBreakerInput

from mamba_dev import config


@mui.app.callback(
    Output('vector-groups-dropdown-checklist', 'options'),
    Output('vector-groups-dropdown-checklist', 'inputStyle'),
    Input('platform-database-dropdown-checklist', 'value'),
    State('vector-groups-dropdown-checklist', 'inputStyle'),
)
def populate_vectors(selected_platform: list, checkbox_style: dict):
    """ The vector groups available for a given platform """
    # Don't do anything until a platform has been selected
    if not bool(selected_platform):
        raise PreventUpdate

    # Load the database
    path_to_database = glob.glob(f"{config['test']['assets_folder']}\\*{selected_platform[0]}*.json")[0]
    with open(path_to_database, mode='r') as f:
        missions = json.load(f)

    # Get UMIs
    vectors = [val['vectors'] for _, val in missions.items()]
    vectors = np.unique(list(itertools.chain.from_iterable(vectors)))
    vectors = sorted(
        vectors,
        key=lambda x: (
            x.split('|')[-1],
            int(x.split(' ')[0])
        )
    )
    vectors = ['Select all', 'Clear all']+vectors

    # Update checkbox style
    if 'display' in checkbox_style.keys():
        checkbox_style['display'] = 'inline'

    return vectors, checkbox_style


@mui.app.callback(
    Output('vector-groups-dropdown-menu', 'label'),
    Input('vector-groups-dropdown-checklist', 'value'),
)
def display_selection(selected_vectors: list):
    if selected_vectors is None:
        raise PreventUpdate

    _ = [selected_vectors.remove(item) for item in ['Select all', 'Clear all'] if item in selected_vectors]

    num_vectors = len(selected_vectors)
    if num_vectors > 1:
        return f'{num_vectors} vector groups selected'
    elif num_vectors == 1:
        return selected_vectors
    else:
        return 'Select...'


@mui.app.callback(
    Output('vector-groups-dropdown-checklist', 'value'),
    CycleBreakerInput('vector-groups-dropdown-checklist', 'value'),
    State('vector-groups-dropdown-checklist', 'options'),
    prevent_initial_call=True
)
def select_all_or_clear_all(selected_vectors: list, all_vectors: list):
    if selected_vectors is None:
        raise PreventUpdate

    # Handle select or clear all vector groups
    if 'Clear all' in selected_vectors:
        return []
    elif 'Select all' in selected_vectors:
        all_vectors.remove('Clear all')
        return all_vectors
    else:
        return selected_vectors
