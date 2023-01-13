import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output


@mui.app.callback(
    Output('air-vehicle-configuration-dropdown-checklist', 'value'),
    Output('air-vehicle-sub-configuration-dropdown-checklist', 'value'),
    Output('missions-dropdown-checklist', 'value'),
    Output('vector-groups-dropdown-checklist', 'value'),
    Input('platform-database-dropdown-checklist', 'value'),
)
def handle_platform_switch(platform):
    # A database wasn't already loaded, do nothing
    if platform is None:
        raise PreventUpdate
    else:
        # A new database has been selected, reset all the subsequent fields
        return [], [], [], []
