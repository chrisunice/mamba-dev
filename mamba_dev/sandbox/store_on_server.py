import numpy as np
import pandas as pd
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, ServersideOutput

import mamba_ui as mui


@mui.app.callback(
    ServersideOutput('server-store', 'data'),
    Input('upload-button', 'n_clicks')
)
def store_on_server(button_click: None | int):
    if button_click is None:
        raise PreventUpdate

    df = pd.DataFrame(
        data=np.random.random((4, 4)),
        index=['a', 'b', 'c', 'd'],
        columns=['how', 'now', 'brown', 'cow']
    )

    return df
