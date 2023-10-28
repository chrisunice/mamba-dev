import json
import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State


@mui.app.callback(
    Output('mission-planning-download-modal', 'is_open'),
    Output('mission-planning-input-alert', 'is_open'),
    Output('mission-planning-input-store', 'data'),
    Input('mission-planning-page-submit-button', 'n_clicks'),
    [
        State('platform-database-dropdown-checklist', 'value'),
        State('air-vehicle-configuration-dropdown-checklist', 'value'),
        State('air-vehicle-sub-configuration-dropdown-checklist', 'value'),
        State('missions-dropdown-checklist', 'value'),
        State('vector-groups-dropdown-checklist', 'value'),
        State('look-range-min-input', 'value'),
        State('look-range-max-input', 'value'),
        State('depression-range-min-input', 'value'),
        State('depression-range-max-input', 'value'),
        State('look-bin-width', 'value'),
        State('depression-bin-width', 'value'),
        State('minimum-hits/bin', 'value'),
        State('minimum-missions/bin', 'value'),
        State('compute-metric-dropdown-checklist', 'value'),
        State('percentile', 'value')
    ]
)
def handle_inputs(
        submit_click: int,
        platform: list,
        av_config: list,
        av_sub_config: list,
        missions: list,
        vectors: list,
        look_min: int,
        look_max: int,
        depr_min: int,
        depr_max: int,
        look_width: int,
        depr_width: int,
        hits_per_bin: int,
        msn_per_bin: int,
        metric: list,
        percentile: int
) -> tuple[bool, bool, str | None]:
    # Do nothing until the submit button is clicked
    if submit_click is None:
        raise PreventUpdate

    # Get function arguments as a dictionary and remove the submit_click
    input_args = locals().copy()
    input_args.pop('submit_click')

    # Remove the percentile input if the percentile metric isn't chosen
    if input_args.get('metric')[0].lower() != 'percentile':
        input_args.pop('percentile')

    # Check that all inputs are entered
    for name, value in input_args.items():
        if value is None:
            open_modal = False
            open_alert = True
            user_inputs = None
            return open_modal, open_alert, user_inputs

    # Handle dropdowns with a "Select all" option
    try:
        input_args['missions'].remove('Select all')
    except (ValueError, AttributeError):
        pass

    try:
        input_args['vectors'].remove('Select all')
    except (ValueError, AttributeError):
        pass

    open_modal = True
    open_alert = False
    user_inputs = json.dumps(input_args)
    return open_modal, open_alert, user_inputs
