import os
import json

class Settings:
    def __init__(self, filepath='.dl/.settings.json'):
        self.filepath = filepath
        self.data = {}
        self.previous_data = {}
        self.load()

    def load(self):
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath) as file:
                self.data = json.load(file)
        except FileNotFoundError:
            pass
        self.previous_data = self.data.copy()

    def get(self, key, message):
        return self.data.get(key) or input(message)

    def set(self, key, value):
        self.data[key] = value

    def save_if_updated(self):
        if self.data != self.previous_data:
            with open(self.filepath, 'w') as file:
                json.dump(self.data, file)