# main.py
import argparse
from setup import configure_via_cli, configure_via_gui
from modules.interactive_cli import interactive_cli
from modules.common_functions import start_server, send_logs, view_logs

def main():
    parser = argparse.ArgumentParser(description='Main entry point for the logging system')
    parser.add_argument('-c', '--cli', action='store_true', help='Run regular command line interface')
    parser.add_argument('-i', '--interactive', action='store_true', help='Run interactive command line interface')
    parser.add_argument('-g', '--gui', action='store_true', help='Run graphical user interface')
    parser.add_argument('--config_file', type=str, help='Configuration file to use')
    parser.add_argument('--db_file', type=str, help='Database file to use')
    args = parser.parse_args()

    if args.cli:
        action = input("Enter action (setup-cli, setup-gui, start-server, send-logs, view-logs): ").strip()
        if action == 'setup-cli':
            configure_via_cli()
        elif action == 'setup-gui':
            configure_via_gui()
        elif action == 'start-server':
            config_file = args.config_file or input("Enter the configuration file path: ")
            start_server(config_file)
        elif action == 'send-logs':
            config_file = args.config_file or input("Enter the configuration file path: ")
            send_logs(config_file)
        elif action == 'view-logs':
            db_file = args.db_file or input("Enter the database file path: ")
            view_logs(db_file)
        else:
            print("Invalid action. Please choose from 'setup-cli', 'setup-gui', 'start-server', 'send-logs', 'view-logs'.")
    elif args.interactive:
        interactive_cli()
    elif args.gui:
        configure_via_gui()
    else:
        print("Please specify an option: -c for CLI, -i for interactive CLI, or -g for GUI.")

if __name__ == "__main__":
    main()
# EOF