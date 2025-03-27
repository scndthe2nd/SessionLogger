# modules/configurator.py

import os
import sqlite3
import zipfile
from modules.database import DatabaseManager
from modules.utils import read_config, save_config, zip_files
from default_variables import get_default

def generate_keys(cert_file=None, key_file=None, cert_request_file=None):
    cert_file = cert_file or get_default('DEFAULT_CERT_FILE')
    key_file = key_file or get_default('DEFAULT_KEY_FILE')
    cert_request_file = cert_request_file or get_default('DEFAULT_CERT_REQUEST_FILE')
    
    os.system(f"openssl genrsa -out {key_file} 2048")
    os.system(f"openssl req -new -key {key_file} -out {cert_request_file}")
    os.system(f"openssl x509 -req -days 365 -in {cert_request_file} -signkey {key_file} -out {cert_file}")
    if os.path.exists(cert_request_file):
        os.remove(cert_request_file)
    else:
        print(f"Warning: {cert_request_file} not found. Skipping removal.")

def configure_database(config_file, permissions, config_data, use_encryption=False):
    db_manager = DatabaseManager(config_data['server config']['database_file'])
    db_manager.set_permissions(permissions)
    
    if use_encryption:
        cert_file = config_data['server config'].get('certificate', get_default('DEFAULT_CERT_FILE'))
        key_file = config_data['server config'].get('private_key', get_default('DEFAULT_KEY_FILE'))
        generate_keys(cert_file, key_file)
        config_data['server config']['certificate'] = cert_file
        config_data['server config']['private_key'] = key_file
    
    save_config(config_file, config_data)
        
# EOF

    