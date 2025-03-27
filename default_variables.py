# default_variables.py

# Define common file names
file_names = {
    'config': 'config.txt',
    'zip': 'config.zip',
    'cert_request': 'certificate_request.csr',
    'cert': 'certificate.pem',
    'key': 'private_key.pem',
    'backup': 'backup_logs.json',
    'logs': 'logs/'
}

# Define common permissions
permissions = {'read': True, 'write': True}

# Define default variables using the common file names
DEFAULT_CONFIG_FILE = file_names['config']
DEFAULT_ZIP_FILE = file_names['zip']
DEFAULT_PERMISSIONS = permissions
DEFAULT_ENCRYPTION_FILES = [file_names['cert'], file_names['key']]
DEFAULT_CERT_REQUEST_FILE = file_names['cert_request']
DEFAULT_CERT_FILE = file_names['cert']
DEFAULT_KEY_FILE = file_names['key']
DEFAULT_BACKUP_FILE = file_names['backup']
DEFAULT_LOGS_PATH = file_names['logs']
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 5
DEFAULT_RESEND_INTERVAL = 60
DEFAULT_PORT = 5000

module_utils_vars = {
    'DEFAULT_CONFIG_FILE': DEFAULT_CONFIG_FILE,
    'DEFAULT_ZIP_FILE': DEFAULT_ZIP_FILE,
    'DEFAULT_PERMISSIONS': DEFAULT_PERMISSIONS,
}

module_configurator_vars = {
    'DEFAULT_ENCRYPTION_FILES': DEFAULT_ENCRYPTION_FILES,
    'DEFAULT_CERT_REQUEST_FILE': DEFAULT_CERT_REQUEST_FILE,
    'DEFAULT_CERT_FILE': DEFAULT_CERT_FILE,
    'DEFAULT_KEY_FILE': DEFAULT_KEY_FILE
}

client_vars = {
    'DEFAULT_BACKUP_FILE': DEFAULT_BACKUP_FILE,
    'DEFAULT_MAX_RETRIES': DEFAULT_MAX_RETRIES,
    'DEFAULT_RETRY_DELAY': DEFAULT_RETRY_DELAY,
    'DEFAULT_RESEND_INTERVAL': DEFAULT_RESEND_INTERVAL,
    'DEFAULT_PORT': DEFAULT_PORT,
    'DEFAULT_LOGS_PATH': DEFAULT_LOGS_PATH,
}

all_vars = {}
all_vars.update(module_utils_vars)
all_vars.update(module_configurator_vars)
all_vars.update(client_vars)

def get_default(var_name):
    return all_vars.get(var_name, None)
        
# EOF
