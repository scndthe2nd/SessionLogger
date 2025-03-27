DEFAULT_CONFIG_FILE = 'config.txt'
DEFAULT_ZIP_FILE = 'config.zip'
DEFAULT_PERMISSIONS = {'read': True, 'write': True}
DEFAULT_ENCRYPTION_FILES = ['certificate.pem', 'private_key.pem']

module_utils_vars = {
    'DEFAULT_CONFIG_FILE': DEFAULT_CONFIG_FILE,
    'DEFAULT_ZIP_FILE': DEFAULT_ZIP_FILE,
    'DEFAULT_PERMISSIONS': DEFAULT_PERMISSIONS,
    'DEFAULT_ENCRYPTION_FILES': DEFAULT_ENCRYPTION_FILES
}

def get_default(var_name):
    return module_utils_vars.get(var_name, None)