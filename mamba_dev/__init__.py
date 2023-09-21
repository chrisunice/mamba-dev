import os
import json

path_to_config = f"{os.path.dirname(__file__)}\\config.json"
with open(path_to_config, mode='r') as json_file:
    config = json.load(json_file)

from .logger import logger
