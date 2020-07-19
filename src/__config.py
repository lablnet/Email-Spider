"""__config.py: Get config string form config file."""
__author__ = "Muhammad Umer Farooq"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Muhammad Umer Farooq"
__email__ = "contact@muhammadumerfarooq.me"
__status__ = "Production"


import json
import os


# Get config string form config file
def get_config(config):
    if os.path.exists("config.json"):
        file = open("config.json", "r")
        data = file.read()
        configuration = json.loads(data)
        if config in configuration:
            return configuration[config]
        else:
            return None
    return None
