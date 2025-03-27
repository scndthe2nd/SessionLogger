# modules/common_functions.py
from modules.flask_server import app
from modules.log_viewer import LogViewer
from client import LogClient
from default_variables import get_default

def start_server(config_file=None):
    config_file = config_file or get_default('DEFAULT_CONFIG_FILE')
    app.run(host='0.0.0.0', port=5000)

def send_logs(config_file=None):
    config_file = config_file or get_default('DEFAULT_CONFIG_FILE')
    log_client = LogClient(config_file)
    log_client.send_logs_to_server()

def view_logs(db_file=None):
    db_file = db_file or get_default('DEFAULT_CONFIG_FILE')
    log_viewer = LogViewer(db_file)
    log_viewer.display_logs()
# EOF