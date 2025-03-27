# modules/interactive_cli.py
from setup import configure_via_cli, configure_via_gui
from modules.common_functions import start_server, send_logs, view_logs

def interactive_cli():
    while True:
        print("\nChoose an action:")
        print("1. Setup via CLI")
        print("2. Setup via GUI")
        print("3. Start Server")
        print("4. Send Logs")
        print("5. View Logs")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            configure_via_cli()
        elif choice == '2':
            configure_via_gui()
        elif choice == '3':
            config_file = input("Enter the configuration file path: ")
            start_server(config_file)
        elif choice == '4':
            config_file = input("Enter the configuration file path: ")
            send_logs(config_file)
        elif choice == '5':
            db_file = input("Enter the database file path: ")
            view_logs(db_file)
        elif choice == '6':
            print("Exiting interactive CLI.")
            break
        else:
            print("Invalid choice. Please choose from 1-6.")

if __name__ == "__main__":
    interactive_cli()
# EOF