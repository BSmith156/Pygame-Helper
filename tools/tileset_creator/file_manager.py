import json

class FileManager():
    def __init__(self):
        self.data = {"colorkey": False, "tiles": []}
        self.unsaved = False

    def load_data(self, path):
        try:
            with open(path, "r", encoding="utf-8") as config_file:
                self.data = json.loads(config_file.read())
            self.unsaved = False
        except FileNotFoundError:
            self.data = {"colorkey": False, "tiles": []}
            self.unsaved = True

    def save_data(self, path):
        with open(path, 'w', encoding = "utf-8") as config_file:
            json.dump(self.data, config_file)
        self.unsaved = False
