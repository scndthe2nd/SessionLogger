#setup.py
import argparse
import tkinter as tk
from tkinter import simpledialog, messagebox
from modules.configurator import configure_database
from modules.utils import read_config, save_config, zip_files, get_config_data
from default_variables import get_default

def configure_common(db_file, table, transport_method, port, target_server_url, encryption_enabled):
    config_data = get_config_data(db_file, table, transport_method, port, target_server_url, encryption_enabled)
    use_encryption = encryption_enabled
    configure_database(get_default('DEFAULT_CONFIG_FILE'), get_default('DEFAULT_PERMISSIONS'), config_data, use_encryption)
    files_to_zip = [get_default('DEFAULT_CONFIG_FILE')]
    if use_encryption:
        files_to_zip.extend(get_default('DEFAULT_ENCRYPTION_FILES'))
    zip_files(get_default('DEFAULT_ZIP_FILE'), files_to_zip)
    print("Configuration completed and files zipped.")

def configure_via_cli():
    parser = argparse.ArgumentParser(description='Setup Configuration')
    parser.add_argument('--db_file', type=str, required=True, help='Database file name')
    parser.add_argument('--table', type=str, required=True, help='Table name')
    parser.add_argument('--transport_method', type=str, required=True, choices=['flask', 'websocket', 'ftp'], help='Transport method')
    parser.add_argument('--port', type=int, required=True, help='Port number')
    parser.add_argument('--target_server_url', type=str, required=True, help='Target server URL')
    parser.add_argument('--encryption_enabled', type=bool, default=False, help='Enable encryption (true/false)')
    args = parser.parse_args()

    configure_common(args.db_file, args.table, args.transport_method, args.port, args.target_server_url, args.encryption_enabled)

def configure_via_gui():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    db_file = simpledialog.askstring("Input", "Enter database file name:")
    table = simpledialog.askstring("Input", "Enter table name:")
    transport_method = simpledialog.askstring("Input", "Enter transport method (flask/websocket/ftp):")
    port = simpledialog.askinteger("Input", "Enter port number:")
    target_server_url = simpledialog.askstring("Input", "Enter target server URL:")
    encryption_enabled = messagebox.askyesno("Input", "Enable encryption?")

    configure_common(db_file, table, transport_method, port, target_server_url, encryption_enabled)
    messagebox.showinfo("Info", "Configuration completed and files zipped.")

if __name__ == "__main__":
    mode = input("Choose setup mode (cli/gui): ").strip().lower()
    if mode == 'cli':
        configure_via_cli()
    elif mode == 'gui':
        configure_via_gui()
    else:
        print("Invalid mode selected. Please choose 'cli' or 'gui'.")
        
# EOF
