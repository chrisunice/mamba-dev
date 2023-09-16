import time
from flask import request
import multiprocessing as mp
import threading
from dash_extensions.enrich import Input, Trigger

import mamba_ui as mui

# Global variables
# Not good practice to have global variables that could be edited by any client that connects to the server
# However, these variables are used to track the state of the imagery process so that clients don't duplicate work
IMAGERY_THREAD_RUNNING = False
SHUTDOWN_EVENT = threading.Event()


def worker():
    """ Dummy function """
    global IMAGERY_THREAD_RUNNING

    while not SHUTDOWN_EVENT.is_set():
        # do work
        print(f'\tImagery thread is doing work son')
        time.sleep(0.5)
        pass
    # Set the thread flag to False
    IMAGERY_THREAD_RUNNING = False
    return None


# def _get_imagery_process() -> mp.Process | None:
#     """ Get the imaging process if one exists in the parent process """
#     global IMAGERY_THREAD_NAME
#
#     child_processes = mp.active_children()
#     if bool(child_processes):
#         # Find the imagery process
#         for child in child_processes:
#             if child.name == IMAGERY_THREAD_NAME:
#                 process = child
#     else:
#         process = None
#     return process


def start_thread():
    global IMAGERY_THREAD_RUNNING, SHUTDOWN_EVENT

    # Make sure there isn't any prior shut down events
    SHUTDOWN_EVENT.clear()

    # Spawn and start a new thread
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

    # Flip the thread bit
    IMAGERY_THREAD_RUNNING = True
    return None


# @mui.app.callback(
#     Trigger('dash-layout', 'children'),
# )
# def init_monitoring():
#     """ Start an imagery thread on application load if one is not already running """
#     global IMAGERY_THREAD_RUNNING
#     if not IMAGERY_THREAD_RUNNING:
#         start_thread()
#         print(f'Imagery thread has been started by {request.remote_addr}')


@mui.app.callback(
    Input('monitor-imagery-switch', 'on'),
    prevent_initial_call=True
)
def monitor_imagery(switch_on):
    """ Handles starting and stopping imagery process based on switch inputs """

    global IMAGERY_THREAD_RUNNING

    # Scenario 1 - switch is on and image process is already running
    if switch_on and IMAGERY_THREAD_RUNNING:
        pass        # do nothing
    # Scenario 2 - switch is off and image process is running
    elif not switch_on and IMAGERY_THREAD_RUNNING:
        # trigger shutdown event
        SHUTDOWN_EVENT.set()
        print(f'Imagery thread has been stopped by {request.remote_addr}')
    # Scenario 3 - switch is on and image process has stopped
    elif switch_on and not IMAGERY_THREAD_RUNNING:
        # start it
        start_thread()
        print(f'Imagery thread has been started by {request.remote_addr}')
    # Scenario 4 - switch is off and image process has stopped
    elif not switch_on and not IMAGERY_THREAD_RUNNING:
        # do nothing
        pass
    else:
        raise ValueError(
            f'Unhandled scenario with switch state {switch_on} and process state {IMAGERY_THREAD_RUNNING}'
        )
