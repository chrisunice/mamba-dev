import mamba_ui as mui
from dash_extensions.enrich import Input, Output

from mamba_dev.missionplanning import log_queue


@mui.app.callback(
    Output('mission-planning-placeholder', 'children'),
    Input('mission-planning-page', 'children')
)
def clear_log(_):
    while True:
        if not log_queue.empty():
            msg = log_queue.get()
            print(f'Dumping {msg}')
        else:
            break
    return None
