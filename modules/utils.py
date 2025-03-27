# modules/utils.py

import json
import os
import zipfile
from default_variables import get_default

def read_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

def save_config(config_file, config_data):
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=4)

def zip_files(zip_file, files):
    with zipfile.ZipFile(zip_file, 'w') as zf:
        for file in files:
            zf.write(file)

def get_config_data(db_file, table, transport_method, port, target_server_url, encryption_enabled):
    return {
        'server config': {
            'database_file': db_file,
            'table': table,
            'transport_method': transport_method,
            'port': port
        },
        'client config': {
            'target_server_url': target_server_url,
            'port': port,
            'encryption_enabled': str(encryption_enabled).lower(),
            'certificate': get_default('DEFAULT_CERT_FILE') if encryption_enabled else '',
            'private_key': get_default('DEFAULT_KEY_FILE') if encryption_enabled else ''
        }
    }