from flask import Flask, request, jsonify
import sqlite3
from modules.utils import read_config, save_to_database
from default_variables import get_default

app = Flask(__name__)

@app.route('/logs', methods=['POST'])
def receive_logs():
    log_data = request.get_json()
    save_to_database(get_default('DEFAULT_CONFIG_FILE'), log_data)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    config = read_config(get_default('DEFAULT_CONFIG_FILE'))
    port = int(config.get('server_config').get('port', 5000))
    use_encryption = config.get('server_config').get('certificate') and config.get('server_config').get('private_key')
    
    if use_encryption:
        app.run(host='0.0.0.0', port=port, ssl_context=(config['server_config']['certificate'], config['server_config']['private_key']))
    else:
        app.run(host='0.0.0.0', port=port)