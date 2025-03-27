from flask import Flask, render_template
from database import fetch_logs

app = Flask(__name__)

@app.route('/')
def index():
    logs = fetch_logs()
    return render_template('index.html', logs=logs)

def run_webui():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run_webui()