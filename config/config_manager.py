import os
import json


class ConfigManager:
    def __init__(self):
        self.app_dir = os.path.expanduser('~/.OcrRecall')
        self.config_path = os.path.join(self.app_dir, 'config.json')
        self.ensure_app_directory()
        self.config = self.load_config()

    def ensure_app_directory(self):
        os.makedirs(self.app_dir, exist_ok=True)

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}  # Default empty config

    def save_config(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

    def get_app_dir(self):
        return self.app_dir
