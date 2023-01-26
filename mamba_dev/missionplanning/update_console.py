import mamba_ui as mui
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State

from mamba_dev.missionplanning import log_queue


@mui.app.callback(
    Output('output-log', 'value'),
    Input('output-interval', 'n_intervals'),
    State('output-log', 'value')
)
def update_console(_, current_log):
    # Page is loading
    if _ is None or current_log is None:
        raise PreventUpdate

    # Do nothing unless there are messages in the queue
    if log_queue.empty():
        raise PreventUpdate

    # Add most recent message from the queue to the existing log
    message = f'\n>> {log_queue.get()}'
    new_log = current_log + message

    return new_log
