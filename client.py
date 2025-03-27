# client.py
import requests
import time
import json
import threading
from modules.utils import read_config
from modules.logger import SessionLogger
from default_variables import get_default

class LogClient:
    def __init__(self, config_file=None, backup_file=None, max_retries=None, retry_delay=None, resend_interval=None):
        self.config_file = config_file or get_default('DEFAULT_CONFIG_FILE')
        self.backup_file = backup_file or get_default('DEFAULT_BACKUP_FILE')
        self.max_retries = max_retries or get_default('DEFAULT_MAX_RETRIES')
        self.retry_delay = retry_delay or get_default('DEFAULT_RETRY_DELAY')
        self.resend_interval = resend_interval or get_default('DEFAULT_RESEND_INTERVAL')

        self.config = read_config(self.config_file)
        self.target_server_url = self.config['client_config']['target_server_url']
        self.logger = SessionLogger(method='file')  # Use 'file' method for local logging
        self.ssl_context = tuple(get_default('DEFAULT_ENCRYPTION_FILES')) if self.config['client_config']['encryption_enabled'].lower() == 'true' else None
        self._start_resend_thread()

    def send_logs_to_server(self):
        log_data = self.logger.save_logs()
        if not self._send_to_server(log_data):
            self._backup_logs(log_data)

    def _send_to_server(self, log_data):
        url = self.target_server_url
        headers = {'Content-Type': 'application/json'}
        for attempt in range(self.max_retries):
            try:
                response = requests.post(url, data=json.dumps(log_data), headers=headers, verify=self.ssl_context[0] if self.ssl_context else True)
                if response.status_code == 200:
                    print("Logs sent successfully.")
                    return True
                else:
                    raise Exception(f"Failed to send logs to server: {response.status_code}")
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(self.retry_delay)
        return False

    def _backup_logs(self, log_data):
        try:
            with open(self.backup_file, 'a') as f:
                f.write(json.dumps(log_data) + '\n')
            print(f"Logs backed up to {self.backup_file}.")
        except Exception as e:
            print(f"Failed to backup logs: {e}")

    def _resend_logs_from_backup(self):
        while True:
            try:
                with open(self.backup_file, 'r') as f:
                    lines = f.readlines()
                if lines:
                    with open(self.backup_file, 'w') as f:
                        for line in lines:
                            if self._send_to_server(json.loads(line.strip())):
                                print("Resent log from backup.")
                            else:
                                f.write(line)
            except Exception as e:
                print(f"Failed to resend logs from backup: {e}")
            time.sleep(self.resend_interval)

    def _start_resend_thread(self):
        thread = threading.Thread(target=self._resend_logs_from_backup, daemon=True)
        thread.start()

# Example usage
config_file = get_default('DEFAULT_CONFIG_FILE')
log_client = LogClient(config_file)
log_client.send_logs_to_server()