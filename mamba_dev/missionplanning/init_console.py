import json
import mamba_ui as mui
from datetime import datetime
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output


def _formatter(x: list | None):
    if x is None:
        return str(x)
    elif not bool(x):
        return 'None'
    else:
        return '\n\t\t'.join(x)


def _timestamp():
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")


@mui.app.callback(
    Output('output-log', 'value'),
    Input('mission-planning-input-store', 'data')
)
def init_console(data):
    if data is None:
        raise PreventUpdate

    inputs = json.loads(data)

    # Handle metric
    metric = inputs['metric']
    if not bool(metric):
        metric = 'None'
    elif metric == ['Percentile']:
        metric = f"{metric[0]} (P{inputs['percentile']})"
    else:
        metric = metric[0]

    # Build console message
    message = f">> {_timestamp()} - STARTING MPF GENERATION...\n"
    message += f">>\tPlatform: \n\t\t{_formatter(inputs['platform'])}\n"
    message += f">>\tAir Vehicle Configuration(s): \n\t\t{_formatter(inputs['av_config'])}\n"
    message += f">>\tAir Vehicle Sub Configuration(s): \n\t\t{_formatter(inputs['av_sub_config'])}\n"
    message += f">>\tMission(s): \n\t\t{_formatter(inputs['missions'])}\n"
    message += f">>\tVector Group(s): \n\t\t{_formatter(inputs['vectors'])}\n"
    message += f">>\tLook Range: \n\t\t({inputs['look_min']}, {inputs['look_max']})\n"
    message += f">>\tDepression Range: \n\t\t({inputs['depr_min']}, {inputs['depr_max']})\n"
    message += f">>\tBin Size: \n\t\t({inputs['look_width']}, {inputs['depr_width']})\n"
    message += f">>\tMinimum Allowable Hits Per Bin: \n\t\t{inputs['hits_per_bin']}\n"
    message += f">>\tMinimum Allowable Missions Per Bin: \n\t\t{inputs['msn_per_bin']}\n"
    message += f">>\tBin metric: \n\t\t{metric}\n"

    return message
