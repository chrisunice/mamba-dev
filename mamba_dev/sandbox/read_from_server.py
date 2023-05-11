from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, State

import mamba_ui as mui


@mui.app.callback(
    Input('server-store', 'data'),
    State('server-store', 'data')
)
def read_from_server(data, existing_data):
    if data is None:
        raise PreventUpdate

    print(existing_data)
