import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State, CycleBreakerInput

from mamba_dev import config


@mui.app.callback(
    Output('compute-metric-dropdown-checklist', 'options'),
    Output('compute-metric-dropdown-menu-item', 'toggle'),
    Output('compute-metric-dropdown-checklist', 'inputStyle'),
    Input('mission-planning-page', 'children'),
    State('compute-metric-dropdown-checklist', 'inputStyle')
)
def populate_metrics(_, checkbox_style: dict):
    # Get metrics
    metrics = [val.capitalize() for val in config['missionplanning']['metrics']]

    # Update checkbox style
    if 'display' in checkbox_style.keys():
        checkbox_style['display'] = 'inline'

    return metrics, True, checkbox_style


@mui.app.callback(
    Output('compute-metric-dropdown-menu', 'label'),
    Input('compute-metric-dropdown-checklist', 'value'),
)
def display_selection(value):
    if value is None:
        raise PreventUpdate

    if not bool(value):
        return 'Select...'
    else:
        return value


@mui.app.callback(
    Output('compute-metric-dropdown-checklist', 'value'),
    CycleBreakerInput('compute-metric-dropdown-checklist', 'value'),
)
def force_one(new_value: list):
    if new_value is None:
        raise PreventUpdate

    # Grab only the last checkbox selected
    if len(new_value) > 1:
        new_value = [new_value[-1]]

    return new_value
