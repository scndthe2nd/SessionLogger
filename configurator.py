import os
import sqlite3
import zipfile
from configparser import ConfigParser
from database import DatabaseManager

def generate_keys(cert_file, key_file):
    os.system(f"openssl genrsa -out {key_file} 2048")
    os.system(f"openssl req -new -key {key_file} -out certificate_request.csr")
    os.system(f"openssl x509 -req -days 365 -in certificate_request.csr -signkey {key_file} -out {cert_file}")
    os.remove("certificate_request.csr")

def save_config(config_file, config_data):
    config = ConfigParser()
    config['server config'] = config_data['server_config']
    config['client config'] = config_data['client_config']
    with open(config_file, 'w') as f:
        config.write(f)

def configure_database(config_file, permissions, config_data, use_encryption=False):
    db_manager = DatabaseManager(config_data['server_config']['database_file'])
    db_manager.set_permissions(permissions)
    
    if use_encryption:
        cert_file = config_data['server_config'].get('certificate', 'certificate.pem')
        key_file = config_data['server_config'].get('private_key', 'private_key.pem')
        generate_keys(cert_file, key_file)
        config_data['server_config']['certificate'] = cert_file
        config_data['server_config']['private_key'] = key_file
    
    save_config(config_file, config_data)

def zip_files(zip_filename, files_to_zip):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files_to_zip:
            zipf.write(file, os.path.basename(file))

# Example usage
config_file = 'config.txt'
permissions = {'read': True, 'write': True}
config_data = {
    'server_config': {
        'database_file': 'server_logs.db',
        'table': 'logs',
        'transport_method': 'flask',
        'port': 5000
    },
    'client_config': {
        'target_server_url': 'https://your_server_address',
        'port': 5000,
        'encryption_enabled': 'true',
        'certificate': 'certificate.pem'
    }
}

use_encryption = config_data['client_config']['encryption_enabled'].lower() == 'true'

configure_database(config_file, permissions, config_data, use_encryption)

# Zip the configuration and client-side certificate files
files_to_zip = [config_file]
if use_encryption:
    files_to_zip.extend([config_data['server_config']['certificate'], config_data['server_config']['private_key']])
zip_filename = 'config_and_keys.zip'

zip_files(zip_filename, files_to_zip)

print(f"Files {files_to_zip} have been zipped into {zip_filename}.")