# modules/database.py
import sqlite3
from default_variables import get_default

class DatabaseManager:
    def __init__(self, db_file=None):
        self.db_file = db_file or get_default('DEFAULT_CONFIG_FILE')
        self.init_db()

    def init_db(self):
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS logs
                         (session_id TEXT, message TEXT, timestamp TEXT)''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
        finally:
            conn.close()

    def save_log(self, log_data):
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("INSERT INTO logs (session_id, message, timestamp) VALUES (?, ?, ?)",
                      (log_data['session_id'], log_data['message'], log_data['timestamp']))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error saving log: {e}")
        finally:
            conn.close()

    def fetch_logs(self):
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("SELECT * FROM logs")
            logs = c.fetchall()
            return logs
        except sqlite3.Error as e:
            print(f"Error fetching logs: {e}")
            return []
        finally:
            conn.close()

    def set_permissions(self, permissions):
        # Implement permission setting logic here
        pass

    def save_to_database(self, log_data):
        self.save_log(log_data)
        
# EOF
