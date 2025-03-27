import requests
from logger import SessionLogger

class LogClient:
    def __init__(self, target_server_url, backup_file='backup_logs.json', max_retries=3, retry_delay=5):
        self.target_server_url = target_server_url
        self.logger = SessionLogger(method='file')  # Use 'file' method for local logging
        self.backup_file = backup_file
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def send_logs_to_server(self):
        log_data = self.logger.save_logs()
        if not self._send_to_server(log_data):
            self._backup_logs(log_data)

    def _send_to_server(self, log_data):
        url = self.target_server_url
        headers = {'Content-Type': 'application/json'}
        for attempt in range(self.max_retries):
            try:
                response = requests.post(url, data=log_data, headers=headers)
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
                f.write(log_data + '\n')
            print(f"Logs backed up to {self.backup_file}.")
        except Exception as e:
            print(f"Failed to backup logs: {e}")

# Example usage:
client = LogClient(target_server_url='http://your-target-server.com/logs')
client.logger.start_session('session_1')
client.logger.log_entry('session_1', 'This is a test log entry.')
client.logger.close_session('session_1')
client.send_logs_to_server()