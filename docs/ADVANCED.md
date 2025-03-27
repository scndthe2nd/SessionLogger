# SessionLogger Examples

This document provides detailed examples of how to use the SessionLogger module for various use cases.

## Basic Usage

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

## Standard Output

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

## Custom Handler

```python
from session_logger import SessionLogger

def custom_handler(message):
    """
    Custom handler for processing log messages.
    """
    print(f"Custom handler received log message: {message}")

# Initialize the logger with a custom handler
logger = SessionLogger(method='custom', custom_handler=custom_handler)

# Start a session
logger.start_session("001")

# Log entries
logger.log_entry("001", "This is a custom handler log entry.", logging.INFO)

# Close the session
logger.close_session("001")

# Save logs
logger.save_logs()
```

## Custom Formatter

```python
from session_logger import SessionLogger

def custom_formatter(log_entry):
    """
    Custom formatter function to modify log entries with additional fields.
    """
    log_entry['user_id'] = 'user_123'
    log_entry['transaction_id'] = 'txn_456'
    log_entry['location'] = 'New York'
    log_entry['device'] = 'laptop'
    return log_entry

# Initialize the logger with a custom formatter
logger = SessionLogger(method='file', custom_formatter=custom_formatter)

# Start a session
logger.start_session("001")

# Log entries
logger.log_entry("001", "This is the first log entry.", logging.INFO)
logger.log_entry("001", "This is the second log entry.", logging.WARNING)

# Close the session
logger.close_session("001")

# Save logs
logger.save_logs()
```

## Sending Logs via Email

```python
from session_logger import SessionLogger
import smtplib
from email.mime.text import MIMEText

def email_handler(message):
    """
    Custom handler for sending log messages via email.
    """
    from_email = "your_email@example.com"
    password = "your_password"
    to_email = "recipient@example.com"
    subject = "Log Entries"

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.example.com', 465) as server:
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())

# Initialize the logger with the email handler
logger = SessionLogger(method='custom', custom_handler=email_handler)

# Start a session
logger.start_session("001")

# Log entries
logger.log_entry("001", "This is an email log entry.", logging.INFO)

# Close the session
logger.close_session("001")

# Save logs
logger.save_logs()
```

## Publishing Logs to MQTT

```python
from session_logger import SessionLogger
import paho.mqtt.client as mqtt

def mqtt_handler(message):
    """
    Custom handler for publishing log messages to MQTT.
    """
    topic = "logs/session"
    client = mqtt.Client()
    client.connect("mqtt.example.com", 1883, 60)
    client.publish(topic, message)
    client.disconnect()

# Initialize the logger with the MQTT handler
logger = SessionLogger(method='custom', custom_handler=mqtt_handler)

# Start a session
logger.start_session("001")

# Log entries
logger.log_entry("001", "This is an MQTT log entry.", logging.INFO)

# Close the session
logger.close_session("001")

# Save logs
logger.save_logs()
```

## Using Session Metadata

```python
from session_logger import SessionLogger

# Initialize the logger with file output
logger = SessionLogger(method='file')

# Start a session with metadata
session_metadata = {
    "user_id": "user_123",
    "transaction_id": "txn_456",
    "location": "New York"
}
logger.start_session("001", metadata=session_metadata)

# Log entries
logger.log_entry("001", "This is the first log entry.", logging.INFO)
logger.log_entry("001", "This is the second log entry.", logging.WARNING)

# Close the session
logger.close_session("001")

# Save logs
logger.save_logs()
```
