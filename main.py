#main.py

import argparse
from modules.flask_server import app
from modules.log_viewer import LogViewer
from client import LogClient
from setup import configure_via_cli, configure_via_gui
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

def main():
    parser = argparse.ArgumentParser(description='Main entry point for the logging system')
    parser.add_argument('action', choices=['setup-cli', 'setup-gui', 'start-server', 'send-logs', 'view-logs'], help='Action to perform')
    parser.add_argument('--config_file', type=str, help='Configuration file to use')
    parser.add_argument('--db_file', type=str, help='Database file to use')
    args = parser.parse_args()

    if args.action == 'setup-cli':
        configure_via_cli()
    elif args.action == 'setup-gui':
        configure_via_gui()
    elif args.action == 'start-server':
        start_server(args.config_file)
    elif args.action == 'send-logs':
        send_logs(args.config_file)
    elif args.action == 'view-logs':
        view_logs(args.db_file)
    else:
        print("Invalid action. Please choose from 'setup-cli', 'setup-gui', 'start-server', 'send-logs', 'view-logs'.")

if __name__ == "__main__":
    main()
    
        
# EOF
