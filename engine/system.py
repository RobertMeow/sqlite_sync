import json


def open_config():
    with open('resources/config/config.json', 'r') as c:
        return json.load(c)
