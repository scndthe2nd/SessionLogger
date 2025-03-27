import sqlite3
import json
import os
from flask import Flask, request, jsonify, render_template

class ConfigManager:
    def __init__(self, target_server_url, custom_fields, backup_file='backup_logs.json', max_retries=3, retry_delay=5):
        self.target_server_url = target_server_url
        self.custom_fields = custom_fields
        self.backup_file = backup_file
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def init_db(self):
        conn = sqlite3.connect('server_logs.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS logs
                     (session_id TEXT, message TEXT, timestamp TEXT)''')
        conn.commit()
        conn.close()

    def setup_flask_server(self):
        app = Flask(__name__)

        @app.route('/logs', methods=['POST'])
        def receive_logs():
            log_data = request.get_json()
            self.save_to_database(log_data)
            return jsonify({"status": "success"}), 200

        def save_to_database(log_data):
            conn = sqlite3.connect('server_logs.db')
            c = conn.cursor()
            c.execute("INSERT INTO logs (session_id, message, timestamp) VALUES (?, ?, ?)",
                      (log_data['session_id'], log_data['message'], log_data['timestamp']))
            conn.commit()
            conn.close()

        app.run(host='0.0.0.0', port=5000)

    def setup_webui_server(self):
        app = Flask(__name__)

        @app.route('/')
        def index():
            logs = self.fetch_logs()
            return render_template('index.html', logs=logs)

        def fetch_logs():
            conn = sqlite3.connect('server_logs.db')
            c = conn.cursor()
            c.execute("SELECT * FROM logs")
            logs = c.fetchall()
            conn.close()
            return logs

        app.run(host='0.0.0.0', port=5001)

    def configure_custom_fields(self):
        with open('custom_fields.json', 'w') as f:
            json.dump(self.custom_fields, f)

    def generate_client_config(self):
        config = {
            'target_server_url': self.target_server_url,
            'backup_file': self.backup_file,
            'max_retries': self.max_retries,
            'retry_delay': self.retry_delay
        }
        with open('client_config.json', 'w') as f:
            json.dump(config, f)

    def setup_all(self):
        self.init_db()
        self.configure_custom_fields()
        self.generate_client_config()
        # Start servers in separate threads or processes if needed
        # self.setup_flask_server()
        # self.setup_webui_server()

# Example usage:
if __name__ == '__main__':
    target_server_url = 'http://your-target-server.com/logs'
    custom_fields = {'example_field': 'example_value'}
    config_manager = ConfigManager(target_server_url, custom_fields)
    config_manager.setup_all()