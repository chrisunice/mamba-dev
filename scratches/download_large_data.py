import base64
import os
import tempfile

from dash import html, dcc
import dash_bootstrap_components as dbc
from flask import send_file
from dash_extensions.enrich import DashProxy, NoOutputTransform

app = DashProxy(
    __name__,
    transforms=[
        NoOutputTransform()
    ]
)

app.layout = html.Div(
    children=[
        # dcc.Download(id='download'),
        # dcc.Store(id='mpf-store', storage_type='memory'),
        # html.Button("Build MPF", id="build-button"),
        # html.Button("Download CSV", id="download-button"),
        dbc.Button(
            children=[html.A("Download CSV", href='/download', style=dict(textDecoration='none', color='black'))],
            color='primary'
        )
    ],
    style=dict(
        display='flex',
        alignItems='center',
        justifyContent='center',
        minHeight='100vh'
    )
)


@app.server.route('/download')
def download_csv():

    # Replace 'your_file.csv' with the actual path to your CSV file
    csv_path = r"C:\Users\ChrisUnice\Downloads\my_big.csv"

    # # Read the contents of the CSV file
    # with open(csv_path, 'rb') as file:
    #     # Base64 encode the file contents
    #     csv_base64 = base64.b64encode(file.read()).decode('utf-8')
    #
    # href = f'data:text/csv;charset=utf-8;base64,{csv_base64}'
    return send_file(csv_path, as_attachment=True)

# @app.callback(
#     Output('mpf-store', 'data'),
#     Input('build-button', 'n_clicks')
# )
# def build_mpf(build_click):
#     if build_click is None:
#         raise PreventUpdate
#
#     # Load your CSV data into a Pandas DataFrame
#     # Replace this with your actual data loading code
#     df = pd.read_csv(r"C:\Users\ChrisUnice\Downloads\large_data.csv")
#
#     # Create a temporary CSV file with the specified root directory
#     temp_fd, temp_file_path = tempfile.mkstemp(dir=r"C:/Mamba", suffix='.csv')
#
#     try:
#         # Write your DataFrame to the temporary file
#         df.to_csv(temp_file_path, index=False)
#
#         # The temporary CSV file will be automatically deleted when it goes out of scope
#     finally:
#         # Ensure the file is closed and removed
#         os.close(temp_fd)
#
#     binary_dict = dcc.send_file(temp_file_path)
#
#     return binary_dict
#
#
# @app.callback(
#     Output('download', 'data'),
#     Input("download-button", "n_clicks"),
#     State('mpf-store', 'data')
# )
# def download_csv(n_clicks, mpf_store):
#     if n_clicks is None:
#         raise PreventUpdate
#
#     # Send the file to the client for download
#     return mpf_store


if __name__ == '__main__':
    app.run_server(debug=True)