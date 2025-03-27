import requests
from session_logger import SessionLogger

class LogClient:
    def __init__(self, target_server_url):
        self.target_server_url = target_server_url
        self.logger = SessionLogger(method='file')  # Use 'file' method for local logging

    def send_logs_to_server(self):
        log_data = self.logger.save_logs()
        self._send_to_server(log_data)

    def _send_to_server(self, log_data):
        url = self.target_server_url
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=log_data, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to send logs to server: {response.status_code}")

# Example usage:
client = LogClient(target_server_url='http://your-target-server.com/logs')
client.logger.start_session('session_1')
client.logger.log_entry('session_1', 'This is a test log entry.')
client.logger.close_session('session_1')
client.send_logs_to_server()