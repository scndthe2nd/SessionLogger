# modules/logger.py
import json
import os
import logging
import socket
from datetime import datetime
from default_variables import get_default

class JsonFormatter(logging.Formatter):
    def format(self, record):
        """
        Format the log record as a JSON string.
        """
        log_entry = {
            'timestamp': self.formatTime(record, self.datefmt),
            'session_id': record.session_id,
            'process_id': record.process_id,
            'error_level': record.levelname,
            'message': record.getMessage()
        }
        log_entry.update(record.custom_fields)
        return json.dumps(log_entry)

class SessionLogger:
    def __init__(self, method='file', custom_formatter=None, **kwargs):
        """
        Initialize the SessionLogger.

        Parameters:
        method (str): The output method ('file', 'stdout', 'custom').
        custom_formatter (function): A custom formatter function for log entries.
        kwargs (dict): Additional arguments for custom handlers.
        """
        self.sessions = {}
        self.process_id = os.getpid()
        self.hostname = socket.gethostname()
        self.method = method
        self.custom_formatter = custom_formatter
        self.kwargs = kwargs
        self.logs_path = get_default('DEFAULT_LOGS_PATH')

    def start_session(self, session_id, metadata=None):
        """
        Start a new logging session with optional metadata.

        Parameters:
        session_id (str): The ID of the session.
        metadata (dict): Additional metadata for the session.
        """
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "metadata": metadata or {},
                "logs": []
            }
            self.log_entry(session_id, "Session started", logging.INFO)

    def close_session(self, session_id):
        """
        Close an existing logging session.

        Parameters:
        session_id (str): The ID of the session.
        """
        if session_id in self.sessions:
            self.log_entry(session_id, "Session closed", logging.INFO)

    def log_entry(self, session_id, message, level=logging.INFO, custom_fields=None):
        """
        Log an entry in the specified session.

        Parameters:
        session_id (str): The ID of the session.
        message (str): The log message.
        level (int): The logging level.
        custom_fields (dict): Additional custom fields for the log entry.
        """
        self._add_log_entry(session_id, message, level, custom_fields)

    def _add_log_entry(self, session_id, message, level=logging.INFO, custom_fields=None):
        """
        Add a log entry to the specified session.

        Parameters:
        session_id (str): The ID of the session.
        message (str): The log message.
        level (int): The logging level.
        custom_fields (dict): Additional custom fields for the log entry.
        """
        if session_id in self.sessions:
            if custom_fields is None:
                custom_fields = {}
            log_id = len(self.sessions[session_id]["logs"]) + 1
            log_entry = {
                "log_id": f"{log_id:03}",
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3],
                "process_id": self.process_id,
                "hostname": self.hostname,
                "error_level": logging.getLevelName(level),
                "message": message,
                "custom_fields": custom_fields
            }
            if self.custom_formatter:
                log_entry = self.custom_formatter(log_entry)
            self.sessions[session_id]["logs"].append(log_entry)

    def save_logs(self):
        """
        Save the logs based on the specified method.
        """
        log_data = {"Sessions": []}
        for session_id, session in self.sessions.items():
            session_data = {
                "session_id": session_id,
                "metadata": session["metadata"],
                "Logs": session["logs"]
            }
            log_data["Sessions"].append(session_data)
        
        message = json.dumps(log_data, indent=4)
        
        if self.method == 'file':
            self._write_to_file(message)
        elif self.method == 'stdout':
            self._write_to_stdout(message)
        elif self.method == 'custom':
            self._write_to_custom_handler(message)
        else:
            raise ValueError(f"Unsupported method: {self.method}")

    def _write_to_file(self, message):
        """
        Write the log message to a file.
        """
        file_path = os.path.join(self.logs_path, f"log_{datetime.now().strftime('%Y-%m-%d')}.json")
        with open(file_path, 'w') as f:
            f.write(message)

    def _write_to_stdout(self, message):
        """
        Write the log message to standard output.
        """
        print(message)

    def _write_to_custom_handler(self, message):
        """
        Write the log message using a custom handler.
        """
        custom_handler = self.kwargs.get('custom_handler', lambda x: None)
        custom_handler(message)