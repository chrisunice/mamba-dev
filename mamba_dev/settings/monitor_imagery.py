import json
import time
import multiprocessing as mp
from dash_extensions.enrich import Input, Output, ServersideOutput, State, Trigger

import mamba_ui as mui


def worker():
    while True:
        print(f'\tRunning on process {mp.current_process().pid}')
        time.sleep(0.5)


@mui.app.callback(
    Output('settings-store', 'data'),
    Trigger('dash-layout', 'children')
)
def init_monitoring():
    process = mp.Process(name='imagery_process', target=worker)
    process.start()
    print(f'{process} has started')
    data = {'process_name': process.name}
    return json.dumps(data)


@mui.app.callback(
    Input('monitor-imagery-switch', 'on'),
    State('settings-store', 'data'),
    prevent_initial_call=True
)
def monitor_imagery(switch_on, data):

    data = json.loads(data)

    child_processes = mp.active_children()
    for child in child_processes:
        if child.name == data['process_name']:
            process = child

    if switch_on:
        process = mp.Process(name='imagery_process', target=worker)
        process.start()
        print(f'{process} has started')
    else:
        if process.is_alive():
            process.terminate()
            print(f'{process} has stopped')
