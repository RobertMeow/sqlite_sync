from .system import open_config
from .control_db import Driver

config = open_config()
DB = Driver(warp_file='resources/data.db')
