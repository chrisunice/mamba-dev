import os
import glob
from dash import dcc
import mamba_ui as mui
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output

from mamba_dev import config


@mui.app.callback(
    Output('platform-database-dropdown', 'children'),
    Input('mission-planning-page', 'children')
)
def populate_platform(_):

    checklist_style = {
        'display': 'flex',
        'flex-direction': 'column',
    }

    checkbox_style = {
        'margin-right': '10px'
    }

    label_style = {
        'color': 'black',
        'font-size': 'larger'
    }

    database_directory = config['test']['test_assets_folder']
    databases = glob.glob(f"{database_directory}\\*mongodb.json")
    platforms = [os.path.basename(db).rstrip('-mongodb.json').upper() for db in databases]
    return dbc.DropdownMenuItem(
        children=[
            dcc.Checklist(
                id='platform-database-checklist',
                options=platforms,
                style=checklist_style,
                inputStyle=checkbox_style,
                labelStyle=label_style
            )
        ],
        style={'background-color': 'transparent'},
        toggle=True
    )


@mui.app.callback(
    Output('platform-database-dropdown', 'label'),
    Input('platform-database-checklist', 'value'),
)
def display_selection(value):
    if value is None:
        raise PreventUpdate

    if not bool(value):
        return 'Select...'
    else:
        return value


@mui.app.callback(
    Output('platform-database-checklist', 'value'),
    Input('platform-database-checklist', 'value'),
)
def force_one(new_value: list):
    if new_value is None:
        raise PreventUpdate

    # Remove
    if len(new_value) > 1:
        new_value = [new_value[-1]]

    return new_value
