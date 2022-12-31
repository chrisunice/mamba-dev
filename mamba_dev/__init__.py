import os
from configparser import ConfigParser

config = ConfigParser()
config.read(f"{os.path.dirname(__file__)}\\config.ini")
