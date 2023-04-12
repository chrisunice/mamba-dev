import json
import time
import multiprocessing as mp
from dash_extensions.enrich import Input, Output, ServersideOutput, State, Trigger

import mamba_ui as mui

# This is a global variable that is editable by any client
# not good practice
IMAGERY_PROCESS_RUNNING = False
IMAGERY_PROCESS_NAME = 'imagery'


def worker():
    while True:
        print(f'\tRunning on process {mp.current_process().pid}')
        time.sleep(0.5)


@mui.app.callback(
    Trigger('dash-layout', 'children'),
)
def init_monitoring():

    global IMAGERY_PROCESS_RUNNING

    if not IMAGERY_PROCESS_RUNNING:
        process = mp.Process(name=IMAGERY_PROCESS_NAME, target=worker)
        process.start()
        IMAGERY_PROCESS_RUNNING = True
        print(f'{process} has started')


@mui.app.callback(
    Input('monitor-imagery-switch', 'on'),
    prevent_initial_call=True
)
def monitor_imagery(switch_on):

    global IMAGERY_PROCESS_NAME, IMAGERY_PROCESS_RUNNING

    child_processes = mp.active_children()
    for child in child_processes:
        if child.name == IMAGERY_PROCESS_NAME:
            process = child

    if switch_on and not IMAGERY_PROCESS_RUNNING:
        process = mp.Process(name=IMAGERY_PROCESS_NAME, target=worker)
        process.start()
        IMAGERY_PROCESS_RUNNING = True
        print(f'{process} has started')
    else:
        if process.is_alive():
            process.terminate()
            IMAGERY_PROCESS_RUNNING = False
            print(f'{process} has stopped')

# TODO need to update the switch to reflect the state of whether or not the imagery process is running