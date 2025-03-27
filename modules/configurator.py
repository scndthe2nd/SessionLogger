import os
import sqlite3
import zipfile
from modules.database import DatabaseManager
from modules.utils import read_config, save_config, zip_files
from default_variables import get_default

def generate_keys(cert_file, key_file):
    os.system(f"openssl genrsa -out {key_file} 2048")
    os.system(f"openssl req -new -key {key_file} -out certificate_request.csr")
    os.system(f"openssl x509 -req -days 365 -in certificate_request.csr -signkey {key_file} -out {cert_file}")
    if os.path.exists("certificate_request.csr"):
        os.remove("certificate_request.csr")
    else:
        print("Warning: certificate_request.csr not found. Skipping removal.")

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

def configurator_demo():
    config_file = get_default('DEFAULT_CONFIG_FILE')
    permissions = get_default('DEFAULT_PERMISSIONS')
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
        files_to_zip.extend(get_default('DEFAULT_ENCRYPTION_FILES'))
    zip_filename = get_default('DEFAULT_ZIP_FILE')

    zip_files(zip_filename, files_to_zip)

    print(f"Files {files_to_zip} have been zipped into {zip_filename}.")

# Call the demo function
configurator_demo()