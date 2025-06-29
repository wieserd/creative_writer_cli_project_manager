import json
import os

class JsonStore:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def read_json(self, file_path):
        full_path = os.path.join(self.base_dir, file_path)
        if not os.path.exists(full_path):
            return []
        with open(full_path, 'r') as f:
            return json.load(f)

    def write_json(self, file_path, data):
        full_path = os.path.join(self.base_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            json.dump(data, f, indent=4)
