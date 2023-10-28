from dash_extensions.enrich import Trigger, Output

import mamba_ui as mui


@mui.app.callback(
    Output('upload-button', 'children'),
    Trigger('sandbox-page', 'children')
)
def change_button_name():
    """ change button name to download when the sandbox page loads """
    return 'Download'
