import mamba_ui as mui
from flask import session, send_file


@mui.app.server.route('/download')
def download_mpf():
    mpf_path = session.get('file_path')
    return send_file(mpf_path, as_attachment=True)
