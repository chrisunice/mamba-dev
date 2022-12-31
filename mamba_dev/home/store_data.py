import os
import json
import dash_uploader
from dash.dependencies import Output


@dash_uploader.callback(
    output=[
        Output('upload-data-output', 'children'),
        Output('session-store', 'data')
    ],
    id='upload-data',
)
def store_uploaded_data(status):
    """
    Stores the data from the dash uploader component and updates
    the session store with a session unique ID and file names
    """
    upload_dir = os.path.dirname(str(status.uploaded_files[0]))
    data = {
        'session-id': status.upload_id,
        'upload_dir': upload_dir,
        'files': os.listdir(upload_dir)
    }
    json_string = json.dumps(data)
    return None, json_string
