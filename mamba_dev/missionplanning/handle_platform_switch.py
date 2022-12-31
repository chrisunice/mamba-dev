import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State


@mui.app.callback(
    Output('air-vehicle-configuration', 'value'),
    Output('air-vehicle-sub-configuration', 'value'),
    Output('missions', 'value'),
    Output('vector-groups', 'value'),
    Input('platform-database', 'value'),
    State('platform-database', 'value')
)
def handle_platform_switch(current_db, prior_db):
    # A database wasn't already loaded, do nothing
    if prior_db is None:
        raise PreventUpdate
    else:
        # A new database has been selected, reset all the subsequent fields
        num_outputs = 4
        return [None]*num_outputs
