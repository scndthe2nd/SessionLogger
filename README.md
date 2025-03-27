
## SessionLogger

SessionLogger is a flexible logging module that outputs JSON logs attached to sessions. The module supports multiple output methods, including file, stdout, and custom handlers like MQTT or Email. You can customize log entries with specific formatting and manage sessions.

## Features

- Log entries with custom fields
- Manage sessions with start and close entries
- Add metadata to sessions
- Output logs to a file, standard output, or custom handlers
- Customizable log entry formatting

## Installation

To use the SessionLogger module, simply include the `session_logger.py` file in your project.

## Usage

For advanced usage, see [SessionLogger Examples](docs/ADVANCED.md)

### Basic Usage

```python
from session_logger import SessionLogger

# Initialize the logger with file output
logger = SessionLogger(method='file')

# Start a session
logger.start_session("001")

# Log entries
logger.log_entry("001", "This is the first log entry.", logging.INFO)
logger.log_entry("001", "This is the second log entry.", logging.WARNING, {"custom_field": "custom_value"})

# Close the session
logger.close_session("001")

# Save logs
logger.save_logs()
```

### Standard Output

```python
from session_logger import SessionLogger

# Initialize the logger with standard output
logger = SessionLogger(method='stdout')

# Start a session
logger.start_session("001")

# Log entries
logger.log_entry("001", "This is a standard output log entry.", logging.INFO)

# Close the session
logger.close_session("001")

# Save logs
logger.save_logs()
```

## Methods

### `__init__(self, method='file', custom_formatter=None, **kwargs)`

Initialize the SessionLogger.

- `method` (str): The output method ('file', 'stdout', 'custom').
- `custom_formatter` (function): A custom formatter function for log entries.
- `kwargs` (dict): Additional arguments for custom handlers.

### `start_session(self, session_id, metadata=None)`

Start a new logging session with optional metadata.

- `session_id` (str): The ID of the session.
- `metadata` (dict): Additional metadata for the session.

### `close_session(self, session_id)`

Close an existing logging session.

- `session_id` (str): The ID of the session.

### `log_entry(self, session_id, message, level=logging.INFO, custom_fields=None)`

Log an entry in the specified session.

- `session_id` (str): The ID of the session.
- `message` (str): The log message.
- `level` (int): The logging level.
- `custom_fields` (dict): Additional custom fields for the log entry.

### `save_logs(self)`

Save the logs based on the specified method.
