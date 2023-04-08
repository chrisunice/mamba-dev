from dash_extensions.enrich import Input, Output, State

import mamba_ui as mui


@mui.app.callback(
    Output('settings-modal', 'is_open'),
    Input('menu-settings', 'n_clicks'),
    State('upload-modal', 'is_open'),
)
def toggle_settings_window(setting_click, is_open):
    if setting_click:
        return not is_open
    return is_open
