import os
import zipfile
from configparser import ConfigParser

def read_config(config_file):
    config = ConfigParser()
    config.read(config_file)
    return config

def save_config(config_file, config_data):
    config = ConfigParser()
    config['server config'] = config_data['server_config']
    config['client config'] = config_data['client_config']
    with open(config_file, 'w') as f:
        config.write(f)

def zip_files(zip_filename, files_to_zip):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files_to_zip:
            zipf.write(file, os.path.basename(file))