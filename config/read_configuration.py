import json
from collections import namedtuple


class ReadConfiguration:
    file_path = "configuration.json"
    configuration = None

    def __init__(self, config_dir, file_path=None):
        if file_path is not None:
            self.file_path = file_path

        self.file_path = config_dir + self.file_path

        self.read_configuration()

    def read_configuration(self):
        with open(self.file_path) as f:
            data = str(json.load(f)).replace('\'', '"')
            self.configuration = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
