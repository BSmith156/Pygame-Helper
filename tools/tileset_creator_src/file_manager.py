import json

class FileManager():
    def __init__(self):
        self._data = {"colorkey": False, "tiles": []}
        self._unsaved = False

    @property
    def data(self):
        return self._data

    @property
    def unsaved(self):
        return self._unsaved

    @unsaved.setter
    def unsaved(self, new_unsaved):
        self._unsaved = new_unsaved

    def save_data(self, path):
        with open(path, 'w', encoding = "utf-8") as config_file:
            json.dump(self._data, config_file)
        self._unsaved = False

    def load_data(self, path):
        try:
            with open(path, "r", encoding="utf-8") as config_file:
                self._data = json.loads(config_file.read())
            self._unsaved = False
        except FileNotFoundError:
            self._data = {"colorkey": False, "tiles": []}
            self._unsaved = True
