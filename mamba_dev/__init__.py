# from .display_page import display_page
# from .toggle_sidebar import toggle_sidebar
# from .change_menu_icon import change_menu_icon
# from .store_data import store_uploaded_data
# from .toggle_upload import toggle_upload_window
#
# from . import imagery
# from . import data_visualization

import os
from configparser import ConfigParser

config = ConfigParser()
config.read(f"{os.path.dirname(__file__)}\\config.ini")
