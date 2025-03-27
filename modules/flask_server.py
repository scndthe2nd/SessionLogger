# modules/flask_server.py

import logging
from flask import Flask, request, jsonify
from modules.utils import read_config
from modules.database import DatabaseManager
from default_variables import get_default

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/logs', methods=['POST'])
def receive_logs():
    log_data = request.get_json()
    db_manager = DatabaseManager(get_default('DEFAULT_CONFIG_FILE'))
    db_manager.save_to_database(log_data)
    logger.info("Log received and saved to database.")
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    config = read_config(get_default('DEFAULT_CONFIG_FILE'))
    port = int(config.get('server_config').get('port', get_default('DEFAULT_PORT')))
    use_encryption = config.get('server_config').get('certificate') and config.get('server_config').get('private_key')
    
    if use_encryption:
        ssl_context = (config['server_config']['certificate'], config['server_config']['private_key'])
        app.run(host='0.0.0.0', port=port, ssl_context=ssl_context)
    else:
        app.run(host='0.0.0.0', port=port)
        
# EOF
