# modules/config_manager.py

import json
from default_variables import get_default

class ConfigManager:
    def __init__(self, config_file=None):
        self.config_file = config_file or get_default('DEFAULT_CONFIG_FILE')
        self.config = self.read_config()

    def read_config(self):
        with open(self.config_file, 'r') as f:
            return json.load(f)

    def save_config(self, config_data):
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent=4)

    def get_config(self):
        return self.config
        
# EOF
