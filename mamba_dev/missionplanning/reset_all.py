import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State


@mui.app.callback(
    [
        Output('platform-database-dropdown-checklist', 'value'),
        Output('air-vehicle-configuration-dropdown-checklist', 'value'),
        Output('air-vehicle-sub-configuration-dropdown-checklist', 'value'),
        Output('missions-dropdown-checklist', 'value'),
        Output('vector-groups-dropdown-checklist', 'value'),
        Output('look-range-min-input', 'value'),
        Output('look-range-max-input', 'value'),
        Output('depression-range-min-input', 'value'),
        Output('depression-range-max-input', 'value'),
        Output('look-bin-width', 'value'),
        Output('depression-bin-width', 'value'),
        Output('minimum-hits/bin', 'value'),
        Output('minimum-missions/bin', 'value'),
        Output('compute-metric-dropdown-checklist', 'value'),
        Output('percentile', 'value'),
        Output('look-range-slider', 'value'),
        Output('depression-range-slider', 'value'),
        Output('output-log', 'value')
    ],
    Input('mission-planning-page-reset-button', 'n_clicks'),
    [
        State('look-range-slider', 'min'),
        State('look-range-slider', 'max'),
        State('depression-range-slider', 'min'),
        State('depression-range-slider', 'max')
    ]
)
def reset_all(reset_click: int, look_min: int, look_max: int, depr_min: int, depr_max: int) -> list:
    # Do nothing until the submit button is clicked
    if reset_click is None:
        raise PreventUpdate

    outputs = {
        'platform-database-dropdown-checklist-value': [],
        'air-vehicle-configuration-dropdown-checklist-value': [],
        'air-vehicle-sub-configuration-dropdown-checklist-value': [],
        'missions-dropdown-checklist-value': [],
        'vector-groups-dropdown-checklist-value': [],
        'look-range-min-input-value': None,
        'look-range-max-input-value': None,
        'depression-range-min-input-value': None,
        'depression-range-max-input-value': None,
        'look-bin-width-value': None,
        'depression-bin-width-value': None,
        'minimum-hits/bin-value': None,
        'minimum-missions/bin-value': None,
        'compute-metric-dropdown-checklist-value': [],
        'percentile-value': None,
        'look-range-slider-value': [look_min, look_max],
        'depression-range-slider-value': [depr_min, depr_max],
        'output-log-value': ''
    }

    return list(outputs.values())
