# modules/log_viewer.py
import sqlite3
from default_variables import get_default

class LogViewer:
    def __init__(self, db_file=None):
        self.db_file = db_file or get_default('DEFAULT_CONFIG_FILE')

    def fetch_logs(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM logs")
        logs = c.fetchall()
        conn.close()
        return logs

    def display_logs(self):
        logs = self.fetch_logs()
        for log in logs:
            session_id, message, timestamp = log
            print(f"Session ID: {session_id}")
            print(f"Timestamp: {timestamp}")
            print(f"Message: {message}")
            print("-" * 40)

# Example usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='View logs from the database')
    parser.add_argument('--db_file', type=str, help='Database file to use')
    args = parser.parse_args()

    log_viewer = LogViewer(args.db_file)
    log_viewer.display_logs()
        
# EOF
