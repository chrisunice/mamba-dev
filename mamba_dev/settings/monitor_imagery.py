import time
from flask import request
import multiprocessing as mp
from dash_extensions.enrich import Input, Trigger

import mamba_ui as mui

# Global variables
# Not good practice to have global variables that could be edited by any client that connects to the server
# However, these variables are used to track the state of the imagery process so that clients don't duplicate work
IMAGERY_PROCESS_RUNNING = False
IMAGERY_PROCESS_NAME = 'imagery'


def worker():
    """ Dummy function """
    while True:
        print(f'\tRunning on process {mp.current_process().pid}')
        time.sleep(0.5)


def _get_imagery_process() -> mp.Process | None:
    """ Get the imaging process if one exists in the parent process """
    global IMAGERY_PROCESS_NAME

    child_processes = mp.active_children()
    if bool(child_processes):
        # Find the imagery process
        for child in child_processes:
            if child.name == IMAGERY_PROCESS_NAME:
                process = child
    else:
        process = None
    return process


@mui.app.callback(
    Trigger('dash-layout', 'children'),
)
def init_monitoring():
    """ Starts an imagery process on application load if one is not already running """
    global IMAGERY_PROCESS_RUNNING

    if not IMAGERY_PROCESS_RUNNING:
        process = mp.Process(name=IMAGERY_PROCESS_NAME, target=worker)
        process.start()
        IMAGERY_PROCESS_RUNNING = True
        print(f'{process} has started by {request.remote_addr}')


@mui.app.callback(
    Input('monitor-imagery-switch', 'on'),
    prevent_initial_call=True
)
def monitor_imagery(switch_on):
    """ Handles starting and stopping imagery process based on switch inputs """

    global IMAGERY_PROCESS_NAME, IMAGERY_PROCESS_RUNNING

    # Scenario 1 - switch is on and image process is already running
    if switch_on and IMAGERY_PROCESS_RUNNING:
        # do nothing
        pass
    # Scenario 2 - switch is off and image process is running
    elif not switch_on and IMAGERY_PROCESS_RUNNING:
        # kill it
        process = _get_imagery_process()
        process.terminate()
        IMAGERY_PROCESS_RUNNING = False
        print(f'{process} has stopped by {request.remote_addr}')
    # Scenario 3 - switch is on and image process has stopped
    elif switch_on and not IMAGERY_PROCESS_RUNNING:
        # start it
        process = mp.Process(name=IMAGERY_PROCESS_NAME, target=worker)
        process.start()
        IMAGERY_PROCESS_RUNNING = True
        print(f'{process} has started by {request.remote_addr}')
    # Scenario 4 - switch is off and image process has stopped
    elif not switch_on and not IMAGERY_PROCESS_RUNNING:
        # do nothing
        pass
    else:
        raise ValueError(
            f'Unhandled scenario with switch state {switch_on} and process state {IMAGERY_PROCESS_RUNNING}'
        )
