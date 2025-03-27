from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def save_to_database(log_data):
    conn = sqlite3.connect('server_logs.db')
    c = conn.cursor()
    c.execute("INSERT INTO logs (session_id, message, timestamp) VALUES (?, ?, ?)",
              (log_data['session_id'], log_data['message'], log_data['timestamp']))
    conn.commit()
    conn.close()

@app.route('/logs', methods=['POST'])
def receive_logs():
    log_data = request.get_json()
    save_to_database(log_data)
    return jsonify({"status": "success"}), 200

def read_config(config_file):
    config = {}
    with open(config_file, 'r') as f:
        for line in f:
            key, value = line.strip().split('=')
            config[key] = value
    return config

if __name__ == '__main__':
    config = read_config('db_config.txt')
    port = int(config.get('port', 5000))
    use_encryption = config.get('certificate') and config.get('private_key')
    
    if use_encryption:
        app.run(host='0.0.0.0', port=port, ssl_context=(config['certificate'], config['private_key']))
    else:
        app.run(host='0.0.0.0', port=port)